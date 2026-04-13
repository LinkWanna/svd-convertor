import argparse
import sys
from pathlib import Path

from src import (
    build_payload,
    dump_split_files,
    generate_split_peripheral_headers,
)

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="svd-convert", description="Convert CMSIS-SVD (.svd/.xml) files to split JSON and split header outputs.")
    parser.add_argument("input", help="Path to source .svd/.xml file")
    parser.add_argument("--indent", type=int, default=4, help="JSON indentation spaces (default: 2)")
    parser.add_argument("--compact", action="store_true", help="Write compact JSON without indentation")
    parser.add_argument("--keep-empty", action="store_true", help="Keep null/empty fields in JSON output")
    parser.add_argument("--no-sort", action="store_true", help="Do not sort peripherals by name")
    parser.add_argument("--split-dir", help="Dump grouped peripheral files into this directory")
    parser.add_argument("--header-common-include", default="types.h", help='Header include used in generated file (default: "common.h")')
    parser.add_argument("--split-header-dir", help="Generate split peripheral header files into this directory")
    parser.add_argument("--split-header-index", default="peripherals.h", help="Index header file name in split-header mode (default: peripherals.h)")
    return parser


def main():
    args = build_parser().parse_args()

    input_path = Path(args.input)
    if not args.split_dir and not args.split_header_dir:
        raise SystemExit("Please provide at least one output target: --split-dir and/or --split-header-dir")

    # parse SVD and build payload
    payload = build_payload(
        input_path=input_path,
        keep_empty=args.keep_empty,
        sort_peripherals=not args.no_sort,
    )

    # dump split JSON files if requested
    split_result = None
    if args.split_dir:
        split_result = dump_split_files(
            payload=payload,
            output_dir=Path(args.split_dir),
            indent=args.indent,
            compact=args.compact,
            summary_file_name="chip_summary.json",
        )

    # generate split header files if requested
    split_header_info = None
    if args.split_header_dir:
        split_header_info = generate_split_peripheral_headers(
            payload=payload,
            output_dir=Path(args.split_header_dir),
            include_header=args.header_common_include,
            summary_header_name=args.split_header_index,
        )

    summary = payload.get("summary", {})
    message = "Dumped split outputs"
    if split_result:
        message += f" | jsonDir={split_result['outputDir']}, jsonFiles={split_result['groupFileCount']}, summary={split_result['summaryFile']}"
    if split_header_info:
        message += (
            " | "
            f"splitHeaders={split_header_info['outputDir']}, "
            f"files={split_header_info['headerFileCount']}, "
            f"index={split_header_info['summaryHeader']}"
        )
    message += (
        f" | peripherals={summary.get('peripheralCount', 0)}, registers={summary.get('registerCount', 0)}, fields={summary.get('fieldCount', 0)}"
    )
    print(message)


if __name__ == "__main__":
    main()
