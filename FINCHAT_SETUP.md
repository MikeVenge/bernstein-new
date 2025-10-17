# Finchat PDF Query Setup Guide

## Overview

The `finchat_pdf_query.py` script automates the process of:
1. **Uploading** the `2024Q2.pdf` file to Consomme (document storage)
2. **Creating** a Finchat session with the PDF attached
3. **Querying** each financial field from `verification_report.csv` via AI
4. **Extracting** values directly from the PDF using natural language queries
5. **Generating** an enhanced verification report comparing:
   - Excel-extracted values (from structured workbook)
   - PDF-extracted values (from unstructured document)

## Why Use Finchat for PDF?

The PDF (`2024Q2.pdf`) is **unstructured** - it contains:
- Tables with varying formats
- Text narratives
- Multiple sections and pages
- No standardized field names

Finchat solves this by:
- Using AI to understand document structure
- Finding values based on semantic meaning
- Handling different formats and variations
- Providing confidence in extracted data

## Prerequisites

### 1. API Credentials

You need access to **two services**:

#### Consomme (Document Storage)
- Purpose: Stores and indexes documents
- Required:
  - `CONSOMME_API_URL` - API endpoint URL
  - `CONSOMME_API_TOKEN` - Authentication token

#### Finchat (Q&A Service)
- Purpose: Queries documents using AI
- Required:
  - `FINCHAT_URL` - API endpoint (default: https://finchat-api.adgo.dev)
  - `FINCHAT_API_TOKEN` - Authentication token

### 2. How to Get Credentials

**Option A: Contact Finchat/Adgorithmics**
- Email: support@adgorithmics.com
- Request API access for document Q&A
- Mention you need Consomme + Finchat access

**Option B: Use Existing Account**
- If you already have access, find your tokens in:
  - Finchat Dashboard → API Keys
  - Consomme Dashboard → Settings → API Tokens

## Setup Instructions

### Step 1: Set Environment Variables

Create a `.env` file or export variables:

```bash
# Option 1: Export in terminal (temporary)
export CONSOMME_API_URL='https://consomme-api.adgo.dev'
export CONSOMME_API_TOKEN='your_consomme_token_here'
export FINCHAT_URL='https://finchat-api.adgo.dev'
export FINCHAT_API_TOKEN='your_finchat_token_here'

# Option 2: Add to ~/.bashrc or ~/.zshrc (permanent)
echo "export CONSOMME_API_URL='https://consomme-api.adgo.dev'" >> ~/.zshrc
echo "export CONSOMME_API_TOKEN='your_token_here'" >> ~/.zshrc
echo "export FINCHAT_URL='https://finchat-api.adgo.dev'" >> ~/.zshrc
echo "export FINCHAT_API_TOKEN='your_token_here'" >> ~/.zshrc
source ~/.zshrc

# Option 3: Create .env file (for use with python-dotenv)
cat > .env << EOF
CONSOMME_API_URL=https://consomme-api.adgo.dev
CONSOMME_API_TOKEN=your_consomme_token_here
FINCHAT_URL=https://finchat-api.adgo.dev
FINCHAT_API_TOKEN=your_finchat_token_here
EOF
```

### Step 2: Install Dependencies

```bash
pip3 install requests
```

### Step 3: Run the Script

```bash
cd /Users/michaelkim/code/Bernstein
python3 finchat_pdf_query.py
```

## What the Script Does

### Workflow

```
┌─────────────────┐
│   2024Q2.pdf    │
└────────┬────────┘
         │ Upload
         ▼
┌─────────────────┐
│    Consomme     │ ← Document Storage & Indexing
│  (Document DB)  │
└────────┬────────┘
         │ Document ID
         ▼
┌─────────────────┐
│     Finchat     │ ← AI-Powered Q&A
│   (Q&A Engine)  │
└────────┬────────┘
         │
         │ For each field in verification_report.csv:
         │   "What is the value for 'Net Sales' in Q2 2024?"
         │
         ▼
┌─────────────────┐
│  Enhanced CSV   │ ← Excel Values + PDF Values
│  Verification   │
└─────────────────┘
```

### Output

Creates `verification_report_with_pdf.csv` with columns:

| Column | Description |
|--------|-------------|
| Row | Row number in target Excel file |
| Target Field Name | Name of the financial metric |
| Source Sheet | Excel sheet where data was found |
| Source Field Name | Matching field in Excel source |
| Q1 Target | Q1 2024 value from target file |
| Q1 Source | Q1 2024 value from source file |
| Q2 Target (Populated) | Q2 2024 value from Excel |
| Match Status | MATCHED / NOT FOUND |
| **Q2 PDF (Finchat)** | **Q2 2024 value from PDF** ← NEW! |

## Example Usage

### Sample Query Flow

For the field "Net Sales":

1. **Script sends:**
   ```
   What is the exact value for 'Net sales' in Q2 2024 
   (quarter ended June 30, 2024)? 
   Return only the numerical value in thousands of dollars.
   ```

2. **Finchat responds:**
   ```
   257,645
   ```

3. **Script parses:**
   - Cleans formatting
   - Validates it's a number
   - Stores in CSV

### Comparison

You can then compare:
- **Excel value**: 257645 (from structured workbook)
- **PDF value**: 257,645 (from AI extraction)
- **Verification**: Values match! ✓

## Benefits

### 1. Cross-Validation
- Compare structured (Excel) vs unstructured (PDF) sources
- Catch discrepancies automatically
- Verify data accuracy

### 2. Missing Field Detection
- Find values that weren't in the Excel workbook
- Extract from PDF when Excel source incomplete
- Fill gaps in data

### 3. Audit Trail
- Complete record of all sources
- Transparency in data origin
- Easy to review and verify

## Limitations & Considerations

### Rate Limiting
- Queries ~88 fields sequentially
- Takes approximately 5-10 minutes
- Script includes 0.5s delay between queries

### Accuracy
- AI extraction may have errors
- Always verify critical values manually
- Use Q1 matching strategy for validation

### Cost
- API calls may incur usage fees
- Check your Finchat pricing plan
- Consider batch processing for efficiency

## Troubleshooting

### "ERROR: Missing required environment variables"
- Ensure all 4 environment variables are set
- Check spelling and format
- Try `echo $FINCHAT_API_TOKEN` to verify

### "ERROR uploading to Consomme"
- Check API token is valid
- Verify URL is correct
- Ensure PDF file exists in current directory

### "ERROR creating Finchat session"
- Check Finchat API token
- Verify API endpoint URL
- Check network connectivity

### Timeout Issues
- Increase timeout in script if needed
- Check API service status
- Try again later if service is busy

### Incorrect Values
- Review Finchat's response in console output
- Adjust query phrasing in script
- Consider adding field-specific query templates

## Advanced Usage

### Custom Queries

You can modify the query template in `finchat_pdf_query.py`:

```python
# Current query:
query = f"What is the exact value for '{field_name}' in Q2 2024?"

# Add more context:
query = f"In the Q2 2024 financial statements, what is the value for '{field_name}'? Look in the income statement, balance sheet, or cash flow statement. Return only the number."

# For specific sections:
query = f"In the Q2 2024 consolidated income statement, what is '{field_name}'?"
```

### Batch Processing

To process in batches (faster, but less accurate):

```python
# Group multiple fields in one query
fields = ["Net Sales", "Cost of sales", "Gross profit"]
query = f"For Q2 2024, what are the values for: {', '.join(fields)}? Return as comma-separated numbers in the same order."
```

### Validation Strategy

Compare extracted values with Q1 verification:

```python
# In process_verification_report()
pdf_q2 = query_finchat(finchat, session_id, field_name, q1_value)
excel_q2 = row['Q2 Target (Populated)']

if pdf_q2 == excel_q2:
    row['Validation'] = 'MATCH'
elif abs(float(pdf_q2) - float(excel_q2)) < 1:
    row['Validation'] = 'CLOSE_MATCH'
else:
    row['Validation'] = 'MISMATCH'
```

## Next Steps

After running the script:

1. **Review the output CSV**
   - Open `verification_report_with_pdf.csv`
   - Compare Excel vs PDF values
   - Flag any mismatches

2. **Investigate discrepancies**
   - Large differences may indicate errors
   - Check source documents manually
   - Verify field name mapping

3. **Automate future quarters**
   - Reuse this script for Q3, Q4, etc.
   - Just update the PDF file and quarter references
   - Build historical comparison database

## Support

For issues or questions:
- Check script output for detailed error messages
- Review Finchat API documentation
- Contact Adgorithmics support for API help

---

**Created:** October 2025
**Version:** 1.0
**Author:** Automated via AI Assistant

