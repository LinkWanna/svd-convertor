import re
from typing import Any

_WHITESPACE_RE = re.compile(r"\s+")


def clean_text(value: str | None) -> str | None:
    if value is None:
        return None
    compact = _WHITESPACE_RE.sub(" ", value).strip()
    return compact or None


def parse_int(value: str | None) -> int | None:
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None
    try:
        return int(text, 0)
    except ValueError:
        # Some SVD files contain values like "00000010" without 0x prefix.
        if text.isdigit() and text.startswith("0") and len(text) > 1:
            return int(text, 16)
        if all(ch in "0123456789abcdefABCDEF" for ch in text):
            return int(text, 16)
        raise


def parse_bool(value: str | None) -> bool | None:
    if value is None:
        return None
    text = value.strip().lower()
    if text == "true":
        return True
    if text == "false":
        return False
    return None


def to_hex(value: int | None, width: int = 0) -> str | None:
    if value is None:
        return None
    if width > 0:
        return f"0x{value:0{width}X}"
    return f"0x{value:X}"


def prune_empty(value: Any) -> Any:
    if isinstance(value, dict):
        filtered = {k: prune_empty(v) for k, v in value.items()}
        return {k: v for k, v in filtered.items() if v not in (None, [], {})}
    if isinstance(value, list):
        filtered_list = [prune_empty(v) for v in value]
        return [v for v in filtered_list if v not in (None, [], {})]
    return value
