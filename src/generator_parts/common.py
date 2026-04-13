from __future__ import annotations

import re
from typing import Any

ACCESS_MAP = {
    "read-write": "rw",
    "read-only": "ro",
    "write-only": "wo",
}


def normalize_key(value: str) -> str:
    key = re.sub(r"[^0-9A-Za-z]+", "_", value.strip().lower())
    key = key.strip("_")
    return key or "misc"


def sanitize_identifier(value: str, *, upper: bool = False) -> str:
    """
    Convert a string to a valid C identifier by replacing invalid characters with
    underscores and ensuring it doesn't start with a digit.
    """
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


def hex_to_int(value: Any, default: int = 0) -> int:
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
