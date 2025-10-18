# Parameter Clarification Examples

## Parameter Definitions

### `--column` (DESTINATION)
- **Purpose**: Specifies which column in the **destination file** to populate
- **Format**: Column number (1-based)
- **Example**: `--column 75` means populate Column 75 in destination file

### `--data-column` (SOURCE)  
- **Purpose**: Specifies which column in the **source file** to read data from
- **Format**: Column reference (like "BR", "CO", "BS")
- **Example**: `--data-column "BR"` means read data from Column BR in source file

## Data Flow Direction

```
SOURCE FILE                    DESTINATION FILE
Column BR (--data-column)  →   Column 75 (--column)
```

## Practical Examples

### Example 1: Read from Source Column CO, Write to Destination Column 71
```bash
python generic_parameterized_mapper.py \
  --source "Q3_2024_Source.xlsx" \
  --destination "Q3_2024_Destination.xlsx" \
  --mapping "GENERIC_FIELD_MAPPINGS.csv" \
  --column 71 \
  --data-column "CO"
```
**Result**: Reads Q3 data from Source Column CO → Writes to Destination Column 71

### Example 2: Read from Source Column BR, Write to Destination Column 75
```bash
python generic_parameterized_mapper.py \
  --source "Q1_2025_Source.xlsx" \
  --destination "Q1_2025_Destination.xlsx" \
  --mapping "GENERIC_FIELD_MAPPINGS.csv" \
  --column 75 \
  --data-column "BR"
```
**Result**: Reads Q1 data from Source Column BR → Writes to Destination Column 75

### Example 3: Different Company, Different Columns
```bash
python generic_parameterized_mapper.py \
  --source "CompanyB_Financial_Data.xlsx" \
  --destination "CompanyB_Template.xlsx" \
  --mapping "GENERIC_FIELD_MAPPINGS.csv" \
  --column 50 \
  --data-column "BZ"
```
**Result**: Reads data from Source Column BZ → Writes to Destination Column 50

## Column Reference Guide

### Common Source Columns (--data-column):
- **"BR"**: Typically Q1 data
- **"CO"**: Typically Q2 data (our current default)
- **"BS"**: Typically another period
- **"BT"**: Typically another period

### Common Destination Columns (--column):
- **71**: Column BS (our current target)
- **72**: Column BT (auto-used for source tracking)
- **73**: Column BU
- **75**: Column BW
- **80**: Column CB

## Automatic Source Tracking

The mapper automatically adds source tracking to the **next column** after your target:
- If `--column 75`, source tracking goes to Column 76
- If `--column 71`, source tracking goes to Column 72

## Summary

**`--column`** = **WHERE** to put data (destination)
**`--data-column`** = **WHERE** to get data (source)

This design allows maximum flexibility for different time periods, companies, and data layouts while maintaining the same field relationship logic.
