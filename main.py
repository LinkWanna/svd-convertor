import argparse
import sys
from pathlib import Path

from src import convert_svd_file

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="svd-convert",
        description="Convert CMSIS-SVD (.svd/.xml) files to readable JSON.",
    )
    parser.add_argument("input", help="Path to source .svd/.xml file")
    parser.add_argument(
        "-o",
        "--output",
        help="Output JSON path (default: same file name with .json)",
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="JSON indentation spaces (default: 2)",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Write compact JSON without indentation",
    )
    parser.add_argument(
        "--keep-empty",
        action="store_true",
        help="Keep null/empty fields in JSON output",
    )
    parser.add_argument(
        "--no-sort",
        action="store_true",
        help="Do not sort peripherals by name",
    )
    return parser


def main():
    args = build_parser().parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else input_path.with_suffix(".json")

    payload = convert_svd_file(
        input_path=input_path,
        output_path=output_path,
        indent=args.indent,
        compact=args.compact,
        keep_empty=args.keep_empty,
        sort_peripherals=not args.no_sort,
    )

    summary = payload.get("summary", {})
    print(
        "Converted "
        f"{input_path} -> {output_path} | "
        f"peripherals={summary.get('peripheralCount', 0)}, "
        f"registers={summary.get('registerCount', 0)}, "
        f"fields={summary.get('fieldCount', 0)}"
    )


if __name__ == "__main__":
    main()
