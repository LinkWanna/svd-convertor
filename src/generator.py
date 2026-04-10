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
    *,
    struct_name: str | None = None,
) -> list[str]:
    resolved_struct_name = struct_name or f"{_sanitize_identifier(str(peripheral.get('name') or 'peripheral'))}_t"
    lines = ["typedef struct {"]

    used_names: dict[str, int] = {}
    cursor = 0
    reserved_index = 0

    offset_groups: dict[int, list[dict[str, Any]]] = {}
    for register in registers:
        offset = _hex_to_int(register.get("addressOffset"), 0)
        offset_groups.setdefault(offset, []).append(register)

    register_entries: list[dict[str, Any]] = []
    for offset in sorted(offset_groups.keys()):
        regs_at_offset = offset_groups[offset]
        size_bytes = max(max(_hex_to_int(item.get("size"), 32) // 8, 1) for item in regs_at_offset)

        primary = regs_at_offset[0]
        reg_name = _sanitize_identifier(str(primary.get("name") or "reg"))
        count = used_names.get(reg_name, 0)
        used_names[reg_name] = count + 1
        if count > 0:
            reg_name = f"{reg_name}_{count}"

        ctype = _ctype_for_register(primary)

        alias_text = ""
        if len(regs_at_offset) > 1:
            alias_names = [str(item.get("name") or "") for item in regs_at_offset[1:]]
            alias_text = ", ".join(name for name in alias_names if name)

        register_entries.append(
            {
                "offset": offset,
                "sizeBytes": size_bytes,
                "ctype": ctype,
                "name": reg_name,
                "aliasText": alias_text,
            }
        )

    def split_indexed_name(name: str) -> tuple[str, int] | None:
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*?)(\d+)$", name)
        if not match:
            return None
        return match.group(1), int(match.group(2))

    idx = 0
    while idx < len(register_entries):
        entry = register_entries[idx]
        offset = int(entry["offset"])

        if offset > cursor:
            gap = offset - cursor
            lines.append(f"    uint8_t _reserved_{reserved_index}[0x{gap:X}];")
            reserved_index += 1
            cursor = offset

        indexed = split_indexed_name(str(entry["name"]))
        if indexed is not None and not entry["aliasText"]:
            base_name, number = indexed
            run_end = idx
            expected_number = number
            expected_offset = int(entry["offset"])
            element_size = int(entry["sizeBytes"])
            ctype = str(entry["ctype"])

            while run_end < len(register_entries):
                current = register_entries[run_end]
                current_indexed = split_indexed_name(str(current["name"]))
                if current_indexed is None or current["aliasText"]:
                    break

                current_base, current_number = current_indexed
                if current_base != base_name:
                    break
                if current_number != expected_number:
                    break
                if str(current["ctype"]) != ctype:
                    break
                if int(current["sizeBytes"]) != element_size:
                    break
                if int(current["offset"]) != expected_offset:
                    break

                run_end += 1
                expected_number += 1
                expected_offset += element_size

            run_length = run_end - idx
            if run_length >= 2 and number == 0:
                lines.append(f"    {ctype} {base_name}[{run_length}];")
                cursor = max(cursor, expected_offset)
                idx = run_end
                continue

        lines.append(f"    {entry['ctype']} {entry['name']};")
        if entry["aliasText"]:
            lines.append(f"    /* Alias registers at same offset: {entry['aliasText']} */")

        cursor = max(cursor, offset + int(entry["sizeBytes"]))
        idx += 1

    lines.append(f"}} {resolved_struct_name};")
    return lines


def _layout_signature(registers: list[dict[str, Any]]) -> tuple[tuple[str, str, str, str], ...]:
    items: list[tuple[str, str, str, str]] = []
    for register in sorted(registers, key=lambda r: _hex_to_int(r.get("addressOffset"), 0)):
        items.append(
            (
                str(register.get("addressOffset") or ""),
                str(register.get("size") or ""),
                str(register.get("access") or ""),
                str(register.get("name") or ""),
            )
        )
    return tuple(items)


def _render_header_content(
    device_name: str,
    peripherals: list[dict[str, Any]],
    include_header: str,
    force_struct_type: str | None = None,
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

    if force_struct_type:
        template_peripheral = peripherals_sorted[0] if peripherals_sorted else {"name": "peripheral"}
        template_registers = _resolve_registers(template_peripheral, name_map)
        content.extend(
            _struct_for_peripheral(
                template_peripheral,
                template_registers,
                struct_name=force_struct_type,
            )
        )
        content.append("")
        struct_count = 1

        for peripheral in peripherals_sorted:
            name = str(peripheral.get("name") or "PERIPHERAL")
            macro_name = f"{_sanitize_identifier(name, upper=True)}"
            base_addr = str(peripheral.get("baseAddress") or "0x0")
            macro_lines.append(f"#define {macro_name} (({force_struct_type} *){base_addr})")

        content.extend(macro_lines)
        return "\n".join(content).rstrip() + "\n", struct_count, len(peripherals_sorted)

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

        name_map = {str(item.get("name")): item for item in group_peripherals if item.get("name")}
        signatures: set[tuple[tuple[str, str, str, str], ...]] = set()
        for peripheral in group_peripherals:
            registers = _resolve_registers(peripheral, name_map)
            if registers:
                signatures.add(_layout_signature(registers))

        force_struct_type = None
        if len(signatures) == 1 and signatures:
            force_struct_type = f"{_sanitize_identifier(group_key, upper=True)}_t"

        rendered, struct_count, _ = _render_header_content(
            device_name=device_name,
            peripherals=group_peripherals,
            include_header=include_header,
            force_struct_type=force_struct_type,
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
