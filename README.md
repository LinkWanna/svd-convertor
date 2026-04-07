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

Dump into many grouped files (recommended for readability):

```bash
python main.py cmsis-svd-stm32/stm32f1/STM32F103.svd --split-dir output
```

This creates files like:

- `output/adc.json` (includes `ADC1`, `ADC2`, `ADC3`)
- `output/gpio.json`
- `output/tim.json`
- `output/usart.json`
- `output/chip_summary.json`

You can also keep single full JSON at the same time:

```bash
python main.py cmsis-svd-stm32/stm32f1/STM32F103.svd --split-dir output -o output/full.json
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
- `--split-dir DIR`: dump peripheral-group JSON files to directory `DIR`
- `--summary-file NAME`: summary file name in split mode (default `chip_summary.json`)

## Output Design

The converter keeps both numeric and readable forms for key values.

Example register fields include:

- `addressOffset` and `addressOffsetHex`
- `absoluteAddress` and `absoluteAddressHex`
- `resetValue` and `resetValueHex`
- `bitOffset`, `bitWidth`, and derived `bitRange`

This makes output easier to inspect in tools while preserving numeric utility.
