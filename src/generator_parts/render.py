from __future__ import annotations

from typing import Any

from .common import hex_to_int, sanitize_identifier
from .grouping import resolve_registers
from .structs import struct_for_peripheral


def render_header_content(
    peripherals: list[dict[str, Any]],
    include_header: str,
    force_struct_type: str | None = None,
) -> tuple[str, int, int]:
    peripherals_sorted = sorted(peripherals, key=lambda p: hex_to_int(p.get("baseAddress"), 0))
    name_map = {str(item.get("name")): item for item in peripherals if item.get("name")}

    content: list[str] = [
        "#pragma once",
        "",
        f'#include "{include_header}"',
        "",
    ]

    defined_structs: set[str] = set()
    peripheral_struct_types: dict[str, str] = {}
    macro_lines: list[str] = []
    struct_count = 0

    if force_struct_type:
        template_peripheral = peripherals_sorted[0] if peripherals_sorted else {"name": "peripheral"}
        template_registers = resolve_registers(template_peripheral, name_map)
        content.extend(
            struct_for_peripheral(
                template_peripheral,
                template_registers,
                struct_name=force_struct_type,
            )
        )
        content.append("")
        struct_count = 1

        for peripheral in peripherals_sorted:
            name = str(peripheral.get("name") or "PERIPHERAL")
            macro_name = f"{sanitize_identifier(name, upper=True)}"
            base_addr = str(peripheral.get("baseAddress") or "0x0")
            macro_lines.append(f"#define {macro_name} (({force_struct_type} *){base_addr})")

        content.extend(macro_lines)
        return "\n".join(content).rstrip() + "\n", struct_count, len(peripherals_sorted)

    for peripheral in peripherals_sorted:
        name = str(peripheral.get("name") or "PERIPHERAL")
        registers = resolve_registers(peripheral, name_map)

        struct_type = f"{sanitize_identifier(name)}_t"
        if not (peripheral.get("registers") or []):
            derived_from = peripheral.get("derivedFrom")
            if isinstance(derived_from, str) and derived_from in peripheral_struct_types:
                struct_type = peripheral_struct_types[derived_from]

        if struct_type not in defined_structs:
            content.extend(struct_for_peripheral(peripheral, registers))
            content.append("")
            defined_structs.add(struct_type)
            struct_count += 1

        if name:
            peripheral_struct_types[name] = struct_type

        macro_name = f"{sanitize_identifier(name, upper=True)}"
        base_addr = str(peripheral.get("baseAddress") or "0x0")
        macro_lines.append(f"#define {macro_name} (({struct_type} *){base_addr})")

    content.extend(macro_lines)

    return "\n".join(content).rstrip() + "\n", struct_count, len(peripherals_sorted)
