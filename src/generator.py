from __future__ import annotations

import re
from pathlib import Path
from typing import Any

_ACCESS_MAP = {
    "read-write": "rw",
    "read-only": "ro",
    "write-only": "wo",
}


def _normalize_key(value: str) -> str:
    key = re.sub(r"[^0-9A-Za-z]+", "_", value.strip().lower())
    key = key.strip("_")
    return key or "misc"


def _sanitize_identifier(value: str, *, upper: bool = False) -> str:
    chars: list[str] = []
    for i, ch in enumerate(value):
        if ch.isalnum() or ch == "_":
            chars.append(ch)
        else:
            chars.append("_")
        if i == 0 and chars[-1].isdigit():
            chars.insert(0, "_")
    result = "".join(chars).strip("_") or "_"
    if upper:
        return result.upper()
    return result


def _hex_to_int(value: Any, default: int = 0) -> int:
    if value is None:
        return default
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return default
        return int(text, 0)
    return default


def _resolve_registers(
    peripheral: dict[str, Any],
    name_map: dict[str, dict[str, Any]],
    visiting: set[str] | None = None,
) -> list[dict[str, Any]]:
    registers = peripheral.get("registers") or []
    if registers:
        return registers

    name = str(peripheral.get("name") or "")
    if visiting is None:
        visiting = set()
    if name and name in visiting:
        return []
    if name:
        visiting.add(name)

    parent_name = peripheral.get("derivedFrom")
    if isinstance(parent_name, str) and parent_name:
        parent = name_map.get(parent_name)
        if parent is not None:
            return _resolve_registers(parent, name_map, visiting)

    return []


def _peripheral_group_key(peripheral: dict[str, Any]) -> str:
    group_name = peripheral.get("groupName")
    if isinstance(group_name, str) and group_name.strip():
        return _normalize_key(group_name)

    name = str(peripheral.get("name") or "")
    if not name:
        return "misc"

    prefix = re.match(r"[A-Za-z]+", name)
    if prefix:
        return _normalize_key(prefix.group(0))

    return _normalize_key(name)


def _group_peripherals(peripherals: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    name_to_peripheral: dict[str, dict[str, Any]] = {str(item.get("name")): item for item in peripherals if item.get("name")}
    group_cache: dict[str, str] = {}

    def resolve_group_key(peripheral: dict[str, Any], visiting: set[str] | None = None) -> str:
        name = str(peripheral.get("name") or "")
        if name and name in group_cache:
            return group_cache[name]

        if visiting is None:
            visiting = set()
        if name in visiting:
            return _peripheral_group_key(peripheral)

        visiting.add(name)
        parent_name = peripheral.get("derivedFrom")
        if isinstance(parent_name, str) and parent_name:
            parent = name_to_peripheral.get(parent_name)
            if parent is not None:
                group = resolve_group_key(parent, visiting)
                if name:
                    group_cache[name] = group
                return group

        group = _peripheral_group_key(peripheral)
        if name:
            group_cache[name] = group
        return group

    groups: dict[str, list[dict[str, Any]]] = {}
    for peripheral in peripherals:
        key = resolve_group_key(peripheral)
        groups.setdefault(key, []).append(peripheral)
    return groups


def _ctype_for_register(register: dict[str, Any]) -> str:
    size = _hex_to_int(register.get("size"), 32)
    if size not in (8, 16, 32, 64):
        size = 32

    access = str(register.get("access") or "read-write").strip().lower()
    access_key = _ACCESS_MAP.get(access, "rw")
    return f"io_{access_key}_{size}"


def _struct_for_peripheral(
    peripheral: dict[str, Any],
    registers: list[dict[str, Any]],
) -> list[str]:
    struct_name = f"{_sanitize_identifier(str(peripheral.get('name') or 'peripheral'))}_t"
    lines = ["typedef struct {"]

    used_names: dict[str, int] = {}
    cursor = 0
    reserved_index = 0

    offset_groups: dict[int, list[dict[str, Any]]] = {}
    for register in registers:
        offset = _hex_to_int(register.get("addressOffset"), 0)
        offset_groups.setdefault(offset, []).append(register)

    for offset in sorted(offset_groups.keys()):
        regs_at_offset = offset_groups[offset]
        size_bytes = max(max(_hex_to_int(item.get("size"), 32) // 8, 1) for item in regs_at_offset)

        if offset > cursor:
            gap = offset - cursor
            lines.append(f"    uint8_t _reserved_{reserved_index}[0x{gap:X}];")
            reserved_index += 1
            cursor = offset

        primary = regs_at_offset[0]
        reg_name = _sanitize_identifier(str(primary.get("name") or "reg"))
        count = used_names.get(reg_name, 0)
        used_names[reg_name] = count + 1
        if count > 0:
            reg_name = f"{reg_name}_{count}"

        ctype = _ctype_for_register(primary)
        lines.append(f"    {ctype} {reg_name};")

        if len(regs_at_offset) > 1:
            alias_names = [str(item.get("name") or "") for item in regs_at_offset[1:]]
            alias_text = ", ".join(name for name in alias_names if name)
            if alias_text:
                lines.append(f"    /* Alias registers at same offset: {alias_text} */")

        cursor = max(cursor, offset + size_bytes)

    lines.append(f"}} {struct_name};")
    return lines


def _render_header_content(
    *,
    device_name: str,
    peripherals: list[dict[str, Any]],
    include_header: str,
) -> tuple[str, int, int]:
    peripherals_sorted = sorted(peripherals, key=lambda p: _hex_to_int(p.get("baseAddress"), 0))
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

    for peripheral in peripherals_sorted:
        name = str(peripheral.get("name") or "PERIPHERAL")
        registers = _resolve_registers(peripheral, name_map)

        struct_type = f"{_sanitize_identifier(name)}_t"
        if not (peripheral.get("registers") or []):
            derived_from = peripheral.get("derivedFrom")
            if isinstance(derived_from, str) and derived_from in peripheral_struct_types:
                struct_type = peripheral_struct_types[derived_from]

        if struct_type not in defined_structs:
            content.extend(_struct_for_peripheral(peripheral, registers))
            content.append("")
            defined_structs.add(struct_type)
            struct_count += 1

        if name:
            peripheral_struct_types[name] = struct_type

        macro_name = f"{_sanitize_identifier(name, upper=True)}"
        base_addr = str(peripheral.get("baseAddress") or "0x0")
        macro_lines.append(f"#define {macro_name} (({struct_type} *){base_addr})")

    content.extend(macro_lines)

    return "\n".join(content).rstrip() + "\n", struct_count, len(peripherals_sorted)


def generate_split_peripheral_headers(
    payload: dict[str, Any],
    output_dir: str | Path,
    *,
    include_header: str = "common.h",
    summary_header_name: str = "peripherals.h",
) -> dict[str, Any]:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    device_name = str(payload.get("device", {}).get("name") or "device")
    peripherals = payload.get("peripherals") or []
    groups = _group_peripherals(peripherals)

    generated_files: list[str] = []
    total_structs = 0
    for group_key, group_peripherals in sorted(groups.items()):
        file_name = f"{group_key}.h"
        header_path = out_dir / file_name
        rendered, struct_count, _ = _render_header_content(
            device_name=device_name,
            peripherals=group_peripherals,
            include_header=include_header,
        )
        header_path.write_text(rendered, encoding="utf-8")
        generated_files.append(file_name)
        total_structs += struct_count

    summary_guard = _sanitize_identifier(f"{device_name}_{summary_header_name}", upper=True)
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
