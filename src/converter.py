import json
import re
from pathlib import Path
from typing import Any

from .parser import parse_svd
from .utils import prune_empty


def _build_summary(payload: dict[str, Any]) -> dict[str, int]:
    peripheral_count = len(payload.get("peripherals", []))

    register_count = 0
    field_count = 0
    for peripheral in payload.get("peripherals", []):
        registers = peripheral.get("registers", [])
        register_count += len(registers)
        for register in registers:
            field_count += len(register.get("fields", []))

    return {
        "peripheralCount": peripheral_count,
        "registerCount": register_count,
        "fieldCount": field_count,
    }


def _normalize_key(value: str) -> str:
    key = re.sub(r"[^0-9A-Za-z]+", "_", value.strip().lower())
    key = key.strip("_")
    return key or "misc"


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


def _serialize_json(payload: dict[str, Any], *, indent: int, compact: bool) -> str:
    if compact:
        return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return json.dumps(payload, ensure_ascii=False, indent=indent)


def build_payload(
    input_path: str | Path,
    *,
    keep_empty: bool = False,
    sort_peripherals: bool = True,
) -> dict[str, Any]:
    payload = parse_svd(str(input_path))

    if sort_peripherals:
        payload["peripherals"].sort(key=lambda item: item.get("name") or "")

    payload["summary"] = _build_summary(payload)

    if not keep_empty:
        payload = prune_empty(payload)

    return payload


def dump_split_files(
    payload: dict[str, Any],
    output_dir: str | Path,
    *,
    indent: int = 2,
    compact: bool = False,
    summary_file_name: str = "chip_summary.json",
) -> dict[str, Any]:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    peripherals = payload.get("peripherals", [])
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

        derived_from = peripheral.get("derivedFrom")
        if isinstance(derived_from, str) and derived_from:
            parent = name_to_peripheral.get(derived_from)
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

    file_summaries: list[dict[str, Any]] = []
    for group_key, peripherals in sorted(groups.items()):
        peripheral_count = len(peripherals)
        register_count = sum(len(item.get("registers", [])) for item in peripherals)
        field_count = sum(len(register.get("fields", [])) for item in peripherals for register in item.get("registers", []))

        group_payload = {
            "chip": payload.get("device", {}).get("name"),
            "group": group_key,
            "summary": {
                "peripheralCount": peripheral_count,
                "registerCount": register_count,
                "fieldCount": field_count,
            },
            "peripherals": peripherals,
        }

        file_name = f"{group_key}.json"
        group_file = out_dir / file_name
        group_file.write_text(
            _serialize_json(group_payload, indent=indent, compact=compact) + "\n",
            encoding="utf-8",
        )

        file_summaries.append(
            {
                "file": file_name,
                "group": group_key,
                "peripherals": [item.get("name") for item in peripherals],
                "summary": group_payload["summary"],
            }
        )

    summary_payload = {
        "chip": payload.get("device", {}),
        "summary": payload.get("summary", {}),
        "groupFileCount": len(file_summaries),
        "groupFiles": file_summaries,
    }

    summary_file = out_dir / summary_file_name
    summary_file.write_text(
        _serialize_json(summary_payload, indent=indent, compact=compact) + "\n",
        encoding="utf-8",
    )

    return {
        "outputDir": str(out_dir),
        "groupFileCount": len(file_summaries),
        "summaryFile": summary_file_name,
    }
