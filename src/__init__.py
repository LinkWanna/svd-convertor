"""SVD to JSON converter package."""

from .converter import build_payload, dump_split_files
from .generator import generate_split_peripheral_headers

__all__ = [
    "build_payload",
    "dump_split_files",
    "generate_split_peripheral_headers",
]
