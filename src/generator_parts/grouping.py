from __future__ import annotations

import re
from typing import Any

from .common import normalize_key


def resolve_registers(
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
            return resolve_registers(parent, name_map, visiting)

    return []


def peripheral_group_key(peripheral: dict[str, Any]) -> str:
    group_name = peripheral.get("groupName")
    if isinstance(group_name, str) and group_name.strip():
        return normalize_key(group_name)

    name = str(peripheral.get("name") or "")
    if not name:
        return "misc"

    prefix = re.match(r"[A-Za-z]+", name)
    if prefix:
        return normalize_key(prefix.group(0))

    return normalize_key(name)


def group_peripherals(peripherals: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    name_to_peripheral: dict[str, dict[str, Any]] = {str(item.get("name")): item for item in peripherals if item.get("name")}
    group_cache: dict[str, str] = {}

    def resolve_group_key(peripheral: dict[str, Any], visiting: set[str] | None = None) -> str:
        name = str(peripheral.get("name") or "")
        if name and name in group_cache:
            return group_cache[name]

        if visiting is None:
            visiting = set()
        if name in visiting:
            return peripheral_group_key(peripheral)

        visiting.add(name)
        parent_name = peripheral.get("derivedFrom")
        if isinstance(parent_name, str) and parent_name:
            parent = name_to_peripheral.get(parent_name)
            if parent is not None:
                group = resolve_group_key(parent, visiting)
                if name:
                    group_cache[name] = group
                return group

        group = peripheral_group_key(peripheral)
        if name:
            group_cache[name] = group
        return group

    groups: dict[str, list[dict[str, Any]]] = {}
    for peripheral in peripherals:
        key = resolve_group_key(peripheral)
        groups.setdefault(key, []).append(peripheral)
    return groups
