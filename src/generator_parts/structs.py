from __future__ import annotations

import re
from typing import Any

from .common import ACCESS_MAP, hex_to_int, sanitize_identifier


def ctype_for_register(register: dict[str, Any]) -> str:
    size = hex_to_int(register.get("size"), 32)
    if size not in (8, 16, 32, 64):
        size = 32

    access = str(register.get("access") or "read-write").strip().lower()
    access_key = ACCESS_MAP.get(access, "rw")
    return f"io_{access_key}_{size}"


def layout_signature(registers: list[dict[str, Any]]) -> tuple[tuple[str, str, str, str], ...]:
    items: list[tuple[str, str, str, str]] = []
    for register in sorted(registers, key=lambda r: hex_to_int(r.get("addressOffset"), 0)):
        items.append(
            (
                str(register.get("addressOffset") or ""),
                str(register.get("size") or ""),
                str(register.get("access") or ""),
                str(register.get("name") or ""),
            )
        )
    return tuple(items)


def struct_for_peripheral(
    peripheral: dict[str, Any],
    registers: list[dict[str, Any]],
    *,
    struct_name: str | None = None,
) -> list[str]:
    resolved_struct_name = struct_name or f"{sanitize_identifier(str(peripheral.get('name') or 'peripheral'))}_t"
    lines = ["typedef struct {"]

    used_names: dict[str, int] = {}
    cursor = 0
    reserved_index = 0

    offset_groups: dict[int, list[dict[str, Any]]] = {}
    for register in registers:
        offset = hex_to_int(register.get("addressOffset"), 0)
        offset_groups.setdefault(offset, []).append(register)

    register_entries: list[dict[str, Any]] = []
    for offset in sorted(offset_groups.keys()):
        regs_at_offset = offset_groups[offset]
        size_bytes = max(max(hex_to_int(item.get("size"), 32) // 8, 1) for item in regs_at_offset)

        primary = regs_at_offset[0]
        reg_name = sanitize_identifier(str(primary.get("name") or "reg"))
        count = used_names.get(reg_name, 0)
        used_names[reg_name] = count + 1
        if count > 0:
            reg_name = f"{reg_name}_{count}"

        ctype = ctype_for_register(primary)

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
            # Fold contiguous suffix-numbered registers into arrays for common
            # 0-based and 1-based naming schemes (e.g. REG0..REG3, REG1..REG4).
            if run_length >= 2 and number in (0, 1):
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
