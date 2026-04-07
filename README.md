# SVD Convertor

Convert CMSIS-SVD (`.svd` / XML) files into readable JSON with a clear hierarchical structure:

- Device metadata
- Peripheral list
- Register list under each peripheral
- Field list under each register
- Summary counts (peripherals/registers/fields)

## Quick Start

Dump into many grouped JSON files:

```bash
python main.py cmsis-svd-stm32/stm32f1/STM32F103.svd --split-dir output/json
```

Generate grouped JSON and split headers together:

```bash
python main.py cmsis-svd-stm32/stm32f1/STM32F103.svd --split-dir output --split-header-dir output/headers
```

Generate split peripheral headers (multiple files):

```bash
python main.py cmsis-svd-stm32/stm32f1/STM32F103.svd --split-header-dir output/headers
```

This creates files like:

- `output/headers/adc.h`
- `output/headers/gpio.h`
- `output/headers/tim.h`
- `output/headers/peripherals.h` (index header)

This creates files like:

- `output/adc.json` (includes `ADC1`, `ADC2`, `ADC3`)
- `output/gpio.json`
- `output/tim.json`
- `output/usart.json`
- `output/chip_summary.json`

## CLI Options

- `input`: input `.svd` or `.xml` file
- `--indent N`: pretty indent size (default `2`)
- `--compact`: compact one-line JSON output
- `--keep-empty`: keep empty/null fields
- `--no-sort`: keep original peripheral order (default is sorted by peripheral name)
- `--split-dir DIR`: dump peripheral-group JSON files to directory `DIR`
- `--header-common-include NAME`: include used by generated header (default `common.h`)
- `--split-header-dir DIR`: generate split header files into `DIR`
- `--split-header-index NAME`: index header file name in split-header mode (default `peripherals.h`)

## Output Design

The converter keeps both numeric and readable forms for key values.

Example register fields include:

- `addressOffset` and `addressOffsetHex`
- `absoluteAddress` and `absoluteAddressHex`
- `resetValue` and `resetValueHex`
- `bitOffset`, `bitWidth`, and derived `bitRange`

This makes output easier to inspect in tools while preserving numeric utility.
