from __future__ import annotations

from pathlib import Path
from typing import Any

from .generator_parts import (
    group_peripherals,
    layout_signature,
    render_header_content,
    resolve_registers,
    sanitize_identifier,
)


def generate_split_peripheral_headers(
    payload: dict[str, Any],
    output_dir: str | Path,
    include_header: str = "types.h",
    summary_header_name: str = "peripherals.h",
) -> dict[str, Any]:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    peripherals = payload.get("peripherals") or []
    groups = group_peripherals(peripherals)

    # Generate header files for each peripheral group
    generated_files: list[str] = []
    total_structs = 0
    for group_key, peripheral_group in sorted(groups.items()):
        file_name = f"{group_key}.h"
        header_path = out_dir / file_name

        name_map = {str(item.get("name")): item for item in peripheral_group if item.get("name")}
        signatures: set[tuple[tuple[str, str, str, str], ...]] = set()
        for peripheral in peripheral_group:
            registers = resolve_registers(peripheral, name_map)
            if registers:
                signatures.add(layout_signature(registers))

        force_struct_type = None
        if len(signatures) == 1 and signatures:
            force_struct_type = f"{sanitize_identifier(group_key, upper=True)}_t"

        rendered, struct_count, _ = render_header_content(
            peripherals=peripheral_group,
            include_header=include_header,
            force_struct_type=force_struct_type,
        )
        header_path.write_text(rendered, encoding="utf-8")
        generated_files.append(file_name)
        total_structs += struct_count

    # Generate summary header that includes all group headers
    device_name = str(payload.get("device", {}).get("name") or "device")
    summary_guard = sanitize_identifier(f"{device_name}_{summary_header_name}", upper=True)
    summary_lines = [
        "#pragma once",
        "",
    ]
    for file_name in generated_files:
        summary_lines.append(f'#include "{file_name}"')
    summary_lines.append("")

    summary_path = out_dir / summary_header_name
    summary_path.write_text("\n".join(summary_lines), encoding="utf-8")

    return {
        "outputDir": str(out_dir),
        "headerFileCount": len(generated_files),
        "summaryHeader": summary_header_name,
        "structCount": total_structs,
        "headerFiles": generated_files,
        "includeGuardHint": summary_guard,
    }
