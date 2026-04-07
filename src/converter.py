import json
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


def convert_svd_file(
    input_path: str | Path,
    output_path: str | Path,
    *,
    indent: int = 2,
    compact: bool = False,
    keep_empty: bool = False,
    sort_peripherals: bool = True,
) -> dict[str, Any]:
    payload = parse_svd(str(input_path))

    if sort_peripherals:
        payload["peripherals"].sort(key=lambda item: item.get("name") or "")

    payload["summary"] = _build_summary(payload)

    if not keep_empty:
        payload = prune_empty(payload)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    if compact:
        serialized = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    else:
        serialized = json.dumps(payload, ensure_ascii=False, indent=indent)

    output.write_text(serialized + "\n", encoding="utf-8")
    return payload
