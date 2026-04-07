# SVD Convertor

Convert CMSIS-SVD (`.svd` / XML) files into readable JSON with a clear hierarchical structure:

- Device metadata
- Peripheral list
- Register list under each peripheral
- Field list under each register
- Summary counts (peripherals/registers/fields)

## Quick Start

Run using `main.py`:

```bash
python main.py cmsis-svd-stm32/stm32f1/STM32F103.svd -o out/STM32F103.json
```

Or use module mode:

```bash
python -m svd_convertor.cli cmsis-svd-stm32/stm32f1/STM32F103.svd -o out/STM32F103.json
```

If installed as a package, use script:

```bash
svd-convert cmsis-svd-stm32/stm32f1/STM32F103.svd -o out/STM32F103.json
```

## CLI Options

- `input`: input `.svd` or `.xml` file
- `-o, --output`: output `.json` path (default: same file name, `.json` suffix)
- `--indent N`: pretty indent size (default `2`)
- `--compact`: compact one-line JSON output
- `--keep-empty`: keep empty/null fields
- `--no-sort`: keep original peripheral order (default is sorted by peripheral name)

## Output Design

The converter keeps both numeric and readable forms for key values.

Example register fields include:

- `addressOffset` and `addressOffsetHex`
- `absoluteAddress` and `absoluteAddressHex`
- `resetValue` and `resetValueHex`
- `bitOffset`, `bitWidth`, and derived `bitRange`

This makes output easier to inspect in tools while preserving numeric utility.
