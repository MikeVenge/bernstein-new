#!/usr/bin/env python3
"""
Consolidate All Mappings

Consolidates all individual mapping CSV files into one comprehensive mapping file
and cleans up the individual files that have been consolidated.

Author: AI Assistant
Date: October 2025
"""

import csv
import pandas as pd
from pathlib import Path
import os
from typing import Dict, List, Set


def identify_mapping_files_to_consolidate() -> Dict[str, List[str]]:
    """Identify which mapping files should be consolidated vs kept."""
    
    # Files that contain actual field mappings (to be consolidated)
    mapping_files = [
        'complete_q1_verified_mapping.csv',              # Main Q1 verification mappings
        'precision_adjusted_q1_mapping.csv',             # Precision-adjusted percentage fields
        'manual_balance_sheet_mappings.csv',             # Manual Balance Sheet fields
        'manual_equity_mappings.csv',                    # Manual equity section fields
        'manual_cash_flow_mappings.csv',                 # Manual Cash Flow fields
        'complete_missing_fields_mappings.csv',          # Complete missing fields batch
        'q1_2023_cash_flow_mappings.csv',                # Q1 2023 verified Cash Flow fields
        'row_135_other_assets_mapping.csv',              # Row 135 Other assets
        'row_205_principal_payments_mapping.csv',        # Row 205 Principal payments
        'composite_accrued_expenses_mappings.csv'        # Composite accrued expenses
    ]
    
    # Files that are source data or intermediate results (to be kept)
    files_to_keep = [
        'final_improved_key_metrics_mapping.csv',        # Source enhanced mapping
        'income_statement_enhanced_mapping.csv',         # Source enhanced mapping
        'balance_sheet_enhanced_mapping.csv',            # Source enhanced mapping
        'cash_flows_enhanced_mapping.csv',               # Source enhanced mapping
        'reported_tab_comprehensive_mapping.csv'         # Destination enhanced mapping
    ]
    
    # Files that are old/superseded (to be archived)
    files_to_archive = [
        'config_based_mapping_results.csv',
        'destination_driven_mapping_results.csv',
        'hybrid_mapping_results.csv',
        'improved_key_metrics_mapping.csv',
        'key_metrics_comprehensive_mapping.csv',
        'fixed_q1_verified_mapping.csv',
        'q1_verified_field_mapping.csv',
        'smart_scope_mapping_results.csv',
        'comprehensive_q1_verified_mapping.csv',
        'manual_accrued_expenses_mappings.csv'
    ]
    
    return {
        'consolidate': mapping_files,
        'keep': files_to_keep,
        'archive': files_to_archive
    }


def load_and_standardize_mapping_file(file_path: str) -> List[Dict]:
    """Load a mapping file and standardize its format."""
    
    if not Path(file_path).exists():
        print(f"  ⚠️  File not found: {file_path}")
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
        
        print(f"  ✅ Loaded {len(rows)} rows from {Path(file_path).name}")
        
        # Standardize field names across different mapping files
        standardized_rows = []
        for row in rows:
            standardized_row = {
                'Dest_Row_Number': row.get('Dest_Row_Number', ''),
                'Dest_Field_Name': row.get('Dest_Field_Name', ''),
                'Dest_Enhanced_Scope': row.get('Dest_Enhanced_Scope', ''),
                'Dest_Section_Context': row.get('Dest_Section_Context', ''),
                'Dest_Major_Section_Context': row.get('Dest_Major_Section_Context', ''),
                'Source_Sheet_Name': row.get('Source_Sheet_Name', ''),
                'Source_Row_Number': row.get('Source_Row_Number', ''),
                'Source_Field_Name': row.get('Source_Field_Name', ''),
                'Source_Enhanced_Scope': row.get('Source_Enhanced_Scope', ''),
                'Source_Section_Context': row.get('Source_Section_Context', ''),
                'Q1_Verification_Value': row.get('Q1_Verification_Value', row.get('Q1_Verification_Value_Original', '')),
                'Source_Q1_Value': row.get('Source_Q1_Value', ''),
                'Source_Q2_Value': row.get('Source_Q2_Value', row.get('Source_Q2_2024_Value', '')),
                'Match_Method': row.get('Match_Method', ''),
                'Match_Confidence': row.get('Match_Confidence', ''),
                'Match_Reason': row.get('Match_Reason', ''),
                'Source_File': Path(file_path).name
            }
            standardized_rows.append(standardized_row)
        
        return standardized_rows
        
    except Exception as e:
        print(f"  ❌ Error loading {file_path}: {e}")
        return []


def consolidate_all_mappings(file_categories: Dict[str, List[str]]) -> str:
    """Consolidate all mapping files into one comprehensive file."""
    
    print("="*80)
    print("CONSOLIDATING ALL MAPPING FILES")
    print("="*80)
    
    all_mappings = []
    processed_files = []
    
    # Load and consolidate mapping files
    for file_name in file_categories['consolidate']:
        file_path = f"/Users/michaelkim/code/Bernstein/{file_name}"
        standardized_mappings = load_and_standardize_mapping_file(file_path)
        
        if standardized_mappings:
            all_mappings.extend(standardized_mappings)
            processed_files.append(file_name)
    
    print(f"\nLoaded mappings from {len(processed_files)} files")
    print(f"Total mappings before deduplication: {len(all_mappings)}")
    
    # Remove duplicates based on destination row number (keep the latest/best mapping)
    deduplicated_mappings = {}
    
    for mapping in all_mappings:
        dest_row = mapping['Dest_Row_Number']
        if dest_row and dest_row.strip():
            # If we already have this destination row, keep the one with higher confidence
            if dest_row in deduplicated_mappings:
                existing_confidence = float(deduplicated_mappings[dest_row].get('Match_Confidence', '0') or '0')
                new_confidence = float(mapping.get('Match_Confidence', '0') or '0')
                
                if new_confidence >= existing_confidence:
                    deduplicated_mappings[dest_row] = mapping
                    print(f"  Updated Row {dest_row}: {mapping['Dest_Field_Name']} (confidence: {new_confidence})")
            else:
                deduplicated_mappings[dest_row] = mapping
    
    # Convert back to list and sort by destination row number
    final_mappings = list(deduplicated_mappings.values())
    final_mappings.sort(key=lambda x: int(x['Dest_Row_Number']) if x['Dest_Row_Number'].isdigit() else 999999)
    
    print(f"Total mappings after deduplication: {len(final_mappings)}")
    
    # Save consolidated mapping file
    output_file = "/Users/michaelkim/code/Bernstein/CONSOLIDATED_FIELD_MAPPINGS.csv"
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'Dest_Row_Number', 'Dest_Field_Name', 'Dest_Enhanced_Scope',
            'Dest_Section_Context', 'Dest_Major_Section_Context',
            'Source_Sheet_Name', 'Source_Row_Number', 'Source_Field_Name',
            'Source_Enhanced_Scope', 'Source_Section_Context',
            'Q1_Verification_Value', 'Source_Q1_Value', 'Source_Q2_Value',
            'Match_Method', 'Match_Confidence', 'Match_Reason', 'Source_File'
        ]
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(final_mappings)
    
    print(f"\n✅ Consolidated mapping saved to: {output_file}")
    print(f"Contains {len(final_mappings)} unique field mappings")
    
    return output_file, processed_files


def archive_old_files(file_categories: Dict[str, List[str]], processed_files: List[str]):
    """Archive old mapping files that have been consolidated."""
    
    print(f"\n" + "="*80)
    print("ARCHIVING CONSOLIDATED FILES")
    print("="*80)
    
    # Create archive directory
    archive_dir = Path("/Users/michaelkim/code/Bernstein/archived_mappings")
    archive_dir.mkdir(exist_ok=True)
    
    archived_count = 0
    
    # Archive the files that were successfully consolidated
    for file_name in processed_files:
        source_path = Path(f"/Users/michaelkim/code/Bernstein/{file_name}")
        archive_path = archive_dir / file_name
        
        if source_path.exists():
            # Move file to archive
            source_path.rename(archive_path)
            archived_count += 1
            print(f"  ✅ Archived: {file_name}")
    
    # Also archive old/superseded files
    for file_name in file_categories['archive']:
        source_path = Path(f"/Users/michaelkim/code/Bernstein/{file_name}")
        archive_path = archive_dir / file_name
        
        if source_path.exists():
            source_path.rename(archive_path)
            archived_count += 1
            print(f"  📁 Archived (old): {file_name}")
    
    print(f"\nArchived {archived_count} files to: {archive_dir}")
    return archived_count


def generate_consolidation_summary(consolidated_file: str):
    """Generate a summary of the consolidated mappings."""
    
    print(f"\n" + "="*80)
    print("CONSOLIDATION SUMMARY")
    print("="*80)
    
    df = pd.read_csv(consolidated_file)
    
    # Summary statistics
    print(f"CONSOLIDATED MAPPING STATISTICS:")
    print(f"  Total unique field mappings: {len(df)}")
    print(f"  Destination rows covered: {df['Dest_Row_Number'].nunique()}")
    
    # Breakdown by source sheet
    print(f"\nMAPPINGS BY SOURCE SHEET:")
    source_breakdown = df['Source_Sheet_Name'].value_counts()
    for sheet, count in source_breakdown.items():
        print(f"  {sheet}: {count} mappings")
    
    # Breakdown by match method
    print(f"\nMAPPINGS BY METHOD:")
    method_breakdown = df['Match_Method'].value_counts()
    for method, count in method_breakdown.items():
        print(f"  {method}: {count} mappings")
    
    # Breakdown by major section
    print(f"\nMAPPINGS BY DESTINATION SECTION:")
    section_breakdown = df['Dest_Major_Section_Context'].value_counts()
    for section, count in section_breakdown.items():
        print(f"  {section}: {count} mappings")
    
    # Show sample mappings
    print(f"\nSAMPLE CONSOLIDATED MAPPINGS:")
    for i, row in df.head(5).iterrows():
        print(f"  Row {row['Dest_Row_Number']}: {row['Dest_Field_Name']}")
        print(f"    → {row['Source_Sheet_Name']} Row {row['Source_Row_Number']}: {row['Source_Field_Name']}")
        print(f"    Method: {row['Match_Method']} (Confidence: {row['Match_Confidence']})")
        print()


def main():
    """Main entry point for mapping consolidation."""
    
    print("="*80)
    print("COMPREHENSIVE MAPPING CONSOLIDATION")
    print("="*80)
    print("Consolidating all individual mapping files into one master file")
    print("and archiving the consolidated files")
    
    try:
        # Identify files to consolidate, keep, and archive
        file_categories = identify_mapping_files_to_consolidate()
        
        print(f"\nFile categorization:")
        print(f"  Files to consolidate: {len(file_categories['consolidate'])}")
        print(f"  Files to keep: {len(file_categories['keep'])}")
        print(f"  Files to archive: {len(file_categories['archive'])}")
        
        # Consolidate mapping files
        consolidated_file, processed_files = consolidate_all_mappings(file_categories)
        
        # Generate summary
        generate_consolidation_summary(consolidated_file)
        
        # Archive old files
        archived_count = archive_old_files(file_categories, processed_files)
        
        print(f"\n" + "="*80)
        print("CONSOLIDATION COMPLETE")
        print("="*80)
        print(f"✅ Consolidated file: CONSOLIDATED_FIELD_MAPPINGS.csv")
        print(f"✅ Processed {len(processed_files)} mapping files")
        print(f"✅ Archived {archived_count} old files")
        print(f"✅ Kept {len(file_categories['keep'])} source/reference files")
        
        print(f"\nFINAL STATE:")
        print(f"  📁 Master mapping: CONSOLIDATED_FIELD_MAPPINGS.csv")
        print(f"  📁 Source mappings: {', '.join(file_categories['keep'])}")
        print(f"  📁 Archived files: archived_mappings/ directory")
        print(f"  🧹 Workspace cleaned and organized!")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
