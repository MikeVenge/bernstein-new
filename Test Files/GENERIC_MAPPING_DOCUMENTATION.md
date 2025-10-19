# Generic Field Mapping Documentation

## Overview
The `GENERIC_FIELD_MAPPINGS.csv` file provides a **reusable, data-agnostic** mapping template that focuses on **field relationships and transformations** rather than specific data values.

## Key Improvements Over Specific Mapping

### ❌ Removed (Data-Specific Elements):
- Specific Q1/Q2 values (e.g., 63964, 76905)
- Specific company names in enhanced scopes
- Date-specific references (2024, Q1, Q2)
- Exact numerical match confidence scores

### ✅ Added (Generic Elements):
- **Field Categories**: Revenue, Geographic, Product_Segment, etc.
- **Mapping Relationships**: Exact_Match, Semantic_Match, Geographic_Translation
- **Transformation Types**: DIRECT_COPY, SUM_FIELDS, PERCENTAGE_VALUE
- **Validation Methods**: Historical_Data, Field_Names
- **Reusable Notes**: Generic explanations of mapping logic

## Generic Mapping Structure

### Core Fields:
- **Dest_Row**: Destination row number
- **Dest_Field**: Destination field name  
- **Dest_Section**: Generic section (Segment Information, Income Statement, etc.)
- **Source_Sheet**: Source sheet name
- **Source_Row**: Source row number (supports composite like "30+31+32+33")
- **Source_Field**: Source field name
- **Source_Column**: Generic column reference ("CO" for data column)

### Mapping Logic:
- **Mapping_Type**: How fields relate (Exact_Match, Semantic_Match, etc.)
- **Transformation**: What to do with data (DIRECT_COPY, SUM_FIELDS, etc.)
- **Confidence**: Quality level (HIGH, MEDIUM, LOW)
- **Validation**: How mapping was verified (Historical_Data, Field_Names)
- **Notes**: Human-readable explanation

## Mapping Types

### 1. **Exact_Match**
- Field names are identical
- Example: "Germany" → "Germany"

### 2. **Geographic_Translation**  
- Standard geographic name variations
- Example: "United States and other North America" → "North America"

### 3. **Semantic_Match**
- Same meaning, different wording
- Example: "Net Sales" → "Total revenue"

### 4. **Composite_Match**
- Destination field is sum of multiple source fields
- Example: "Accrued expenses and other liabilities" → Sum of rows 30+31+32+33

## Transformation Types

### 1. **DIRECT_COPY**
- Copy value as-is from source to destination
- Most common transformation

### 2. **SUM_FIELDS**  
- Sum values from multiple source rows
- Used for composite fields

### 3. **PERCENTAGE_VALUE**
- Handle decimal percentage values (0.0 to 1.0)
- Preserve decimal precision

### 4. **ZERO_VALUE**
- Handle zero/null values appropriately

## Validation Methods

### 1. **Historical_Data**
- Mapping verified using historical period data
- High confidence level

### 2. **Field_Names**
- Mapping based on field name similarity
- Medium to high confidence

### 3. **Manual_Validation**
- Manually verified mapping
- Variable confidence

## Usage with Parameterized Mapper

```bash
# Use with any time period data
python parameterized_field_mapper.py \
  --source "Q3_2024_Source.xlsx" \
  --destination "Q3_2024_Destination.xlsx" \
  --mapping "GENERIC_FIELD_MAPPINGS.csv" \
  --column 75

# Use with different company data  
python parameterized_field_mapper.py \
  --source "Company_B_Financial_Data.xlsx" \
  --destination "Company_B_Template.xlsx" \
  --mapping "GENERIC_FIELD_MAPPINGS.csv" \
  --column 50
```

## Benefits of Generic Format

1. **🔄 Reusable**: Works across different time periods
2. **🏢 Portable**: Can be adapted for different companies
3. **📋 Template**: Serves as template for similar mappings
4. **🎯 Focused**: Emphasizes relationships over specific values
5. **📚 Documented**: Clear explanation of mapping logic
6. **🔧 Maintainable**: Easy to update and modify

## File Structure Summary

| Column | Purpose | Example |
|--------|---------|---------|
| Dest_Row | Destination row number | 12 |
| Dest_Field | Destination field name | "United States and other North America" |
| Source_Sheet | Source sheet name | "Key Metrics" |
| Source_Row | Source row(s) | "6" or "30+31+32+33" |
| Source_Field | Source field name | "North America" |
| Mapping_Type | Relationship type | "Geographic_Translation" |
| Transformation | Data transformation | "DIRECT_COPY" |
| Notes | Mapping explanation | "Geographic translation: US → North America" |

This generic format enables the field mapping solution to be reused across different datasets while maintaining the intelligence and relationships discovered during the original mapping process.
