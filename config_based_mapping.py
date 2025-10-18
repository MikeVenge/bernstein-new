#!/usr/bin/env python3
"""
Configuration-Based Field Mapping

Uses the field_mapping_config.py to handle semantic mappings between
source and destination terminology.

Examples:
- Source "Revenue by application:" → Destination "End market breakdown"
- Source "Revenue by product:" → Destination "Segment breakdown"
- Source "North America" → Destination "United States and other North America"

Author: AI Assistant
Date: October 2025
"""

import pandas as pd
import openpyxl
import csv
from pathlib import Path
import re
from typing import Dict, List, Tuple, Optional

# Import the configuration mappings
from field_mapping_config import (
    SECTION_MAPPINGS,
    FIELD_NAME_MAPPINGS,
    get_semantic_equivalence_score,
    normalize_section_name,
    normalize_field_name
)


def load_enhanced_mappings_with_config() -> Tuple[List[Dict], List[Dict]]:
    """Load enhanced mappings and apply configuration normalization."""
    print("Loading enhanced field mappings with configuration...")
    
    # Load source mapping
    source_file = "/Users/michaelkim/code/Bernstein/final_improved_key_metrics_mapping.csv"
    source_fields = []
    if Path(source_file).exists():
        source_df = pd.read_csv(source_file)
        for _, row in source_df.iterrows():
            source_fields.append({
                'row_number': row['Row_Number'],
                'original_field_name': row['Original_Field_Name'],
                'cleaned_field_name': row['Cleaned_Field_Name'],
                'section_context': row['Section_Context'],
                'enhanced_scoped_name': row['Enhanced_Scoped_Name'],
                'q1_2024_value': row['Q1_2024_Value'] if pd.notna(row['Q1_2024_Value']) else None,
                'q2_2024_value': row['Q2_2024_Value'] if pd.notna(row['Q2_2024_Value']) else None,
                'file_type': 'source',
                # Add normalized versions
                'normalized_field_name': normalize_field_name(row['Original_Field_Name']),
                'normalized_section': normalize_section_name(row['Section_Context'])
            })
        print(f"Loaded {len(source_fields)} source fields")
    
    # Load destination mapping
    dest_file = "/Users/michaelkim/code/Bernstein/reported_tab_comprehensive_mapping.csv"
    dest_fields = []
    if Path(dest_file).exists():
        dest_df = pd.read_csv(dest_file)
        for _, row in dest_df.iterrows():
            dest_fields.append({
                'row_number': row['Row_Number'],
                'original_field_name': row['Original_Field_Name'],
                'cleaned_field_name': row['Cleaned_Field_Name'],
                'major_section_context': row['Major_Section_Context'],
                'section_context': row['Section_Context'],
                'enhanced_scoped_name': row['Enhanced_Scoped_Name'],
                'file_type': 'destination',
                # Add normalized versions
                'normalized_field_name': normalize_field_name(row['Original_Field_Name']),
                'normalized_section': normalize_section_name(row['Section_Context'])
            })
        print(f"Loaded {len(dest_fields)} destination fields")
    
    return source_fields, dest_fields


def find_config_based_matches(source_fields: List[Dict], dest_fields: List[Dict]) -> List[Dict]:
    """
    Find matches using configuration-based semantic equivalence.
    """
    print("Finding matches using configuration-based semantic equivalence...")
    
    matches = []
    used_source_indices = set()
    
    for dest_field in dest_fields:
        dest_name = dest_field['original_field_name']
        dest_section = dest_field.get('section_context', '')
        
        print(f"\nFinding source for: {dest_name}")
        print(f"  Dest section: {dest_section}")
        print(f"  Dest scope: {dest_field['enhanced_scoped_name']}")
        
        best_match = None
        best_score = 0.0
        best_source_idx = None
        
        for i, source_field in enumerate(source_fields):
            if i in used_source_indices:
                continue
            
            # Use configuration-based semantic equivalence
            score = get_semantic_equivalence_score(source_field, dest_field)
            
            if score > best_score:
                best_score = score
                best_match = source_field
                best_source_idx = i
        
        # Accept matches above threshold
        if best_match and best_score > 0.6:
            used_source_indices.add(best_source_idx)
            
            match = {
                'dest_field': dest_field,
                'source_field': best_match,
                'similarity_score': best_score,
                'match_quality': get_match_quality(best_score)
            }
            matches.append(match)
            
            print(f"  → MATCHED: {best_match['original_field_name']} (Score: {best_score:.3f})")
            print(f"    Source section: {best_match.get('section_context', '')}")
            print(f"    Normalized mapping: {best_match['normalized_section']} → {dest_field['normalized_section']}")
        else:
            match = {
                'dest_field': dest_field,
                'source_field': None,
                'similarity_score': 0.0,
                'match_quality': 'No Match'
            }
            matches.append(match)
            print(f"  → No suitable match found")
    
    successful_matches = [m for m in matches if m['source_field'] is not None]
    print(f"\nConfiguration-based matching complete:")
    print(f"  Total matches: {len(successful_matches)}")
    print(f"  Unique source fields used: {len(used_source_indices)}")
    
    return matches


def get_destination_q1_values(dest_fields: List[Dict]) -> Dict:
    """Get Q1 2024 values from destination file."""
    print("Loading destination Q1 2024 values from Column BR...")
    
    target_file = "/Users/michaelkim/code/Bernstein/20240725_IPGP.US-IPG Photonics.xlsx"
    wb = openpyxl.load_workbook(target_file, data_only=True)
    sheet = wb['Reported']
    
    dest_values = {}
    for dest_field in dest_fields:
        row_num = dest_field['row_number']
        q1_value = sheet.cell(row_num, 70).value  # Column BR (Q1 2024)
        dest_values[row_num] = q1_value
    
    wb.close()
    print(f"Loaded Q1 values for {len(dest_values)} destination rows")
    return dest_values


def save_config_based_results(matches: List[Dict], dest_q1_values: Dict, output_file: str):
    """Save configuration-based mapping results."""
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'Dest_Row_Number',
            'Dest_Field_Name',
            'Dest_Section_Context',
            'Dest_Enhanced_Scope',
            'Source_Row_Number',
            'Source_Field_Name',
            'Source_Section_Context', 
            'Source_Enhanced_Scope',
            'Source_Q1_2024_Value',
            'Dest_Q1_2024_Value',
            'Source_Q2_2024_Value',
            'Similarity_Score',
            'Match_Quality',
            'Values_Match',
            'Section_Mapping_Applied'
        ]
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for match in matches:
            dest = match['dest_field']
            source = match['source_field']
            
            dest_q1 = dest_q1_values.get(dest['row_number'])
            source_q1 = source['q1_2024_value'] if source else None
            source_q2 = source['q2_2024_value'] if source else None
            
            # Check if values match
            values_match = 'N/A'
            if dest_q1 is not None and source_q1 is not None:
                try:
                    if dest_q1 == source_q1:
                        values_match = 'Exact Match'
                    elif abs(float(dest_q1) - float(source_q1)) / float(source_q1) < 0.05:
                        values_match = 'Close Match'
                    else:
                        values_match = 'Different'
                except:
                    values_match = 'Different'
            elif dest_q1 is None and source_q1 is None:
                values_match = 'Both Empty'
            else:
                values_match = 'One Empty'
            
            # Check if section mapping was applied
            source_section = source.get('section_context', '').lower() if source else ''
            dest_section = dest.get('section_context', '').lower()
            section_mapping_applied = source_section in SECTION_MAPPINGS and SECTION_MAPPINGS[source_section] == dest_section
            
            writer.writerow({
                'Dest_Row_Number': dest['row_number'],
                'Dest_Field_Name': dest['original_field_name'],
                'Dest_Section_Context': dest.get('section_context', ''),
                'Dest_Enhanced_Scope': dest['enhanced_scoped_name'],
                'Source_Row_Number': source['row_number'] if source else '',
                'Source_Field_Name': source['original_field_name'] if source else '',
                'Source_Section_Context': source.get('section_context', '') if source else '',
                'Source_Enhanced_Scope': source['enhanced_scoped_name'] if source else '',
                'Source_Q1_2024_Value': source_q1 if source_q1 is not None else '',
                'Dest_Q1_2024_Value': dest_q1 if dest_q1 is not None else '',
                'Source_Q2_2024_Value': source_q2 if source_q2 is not None else '',
                'Similarity_Score': f"{match['similarity_score']:.3f}",
                'Match_Quality': match['match_quality'],
                'Values_Match': values_match,
                'Section_Mapping_Applied': 'Yes' if section_mapping_applied else 'No'
            })


def get_match_quality(score: float) -> str:
    """Get match quality description."""
    if score >= 0.9:
        return 'Excellent'
    elif score >= 0.7:
        return 'Good'
    elif score >= 0.6:
        return 'Fair'
    else:
        return 'Poor'


def main():
    """Main entry point."""
    output_file = "/Users/michaelkim/code/Bernstein/config_based_mapping_results.csv"
    
    print("="*80)
    print("CONFIGURATION-BASED FIELD MAPPING")
    print("="*80)
    print("Using semantic configuration to handle terminology differences")
    print("Examples:")
    print("  'Revenue by application:' → 'End market breakdown'")
    print("  'Revenue by product:' → 'Segment breakdown'")
    print("  'North America' → 'United States and other North America'")
    print(f"Output file: {output_file}")
    
    try:
        # Load enhanced mappings
        source_fields, dest_fields = load_enhanced_mappings_with_config()
        
        if not source_fields or not dest_fields:
            print("ERROR: Could not load mapping files")
            return
        
        # Find config-based matches
        matches = find_config_based_matches(source_fields, dest_fields)
        
        # Get destination Q1 values
        dest_q1_values = get_destination_q1_values(dest_fields)
        
        # Save results
        save_config_based_results(matches, dest_q1_values, output_file)
        
        # Summary statistics
        successful_matches = [m for m in matches if m['source_field'] is not None]
        exact_matches = [m for m in matches if m['source_field'] and 
                        dest_q1_values.get(m['dest_field']['row_number']) == m['source_field']['q1_2024_value']]
        
        # Count section mappings applied
        section_mappings_used = set()
        for match in successful_matches:
            source_section = match['source_field'].get('section_context', '').lower()
            if source_section in SECTION_MAPPINGS:
                section_mappings_used.add(f"{source_section} → {SECTION_MAPPINGS[source_section]}")
        
        print(f"\n" + "="*80)
        print("CONFIGURATION-BASED MAPPING RESULTS")
        print("="*80)
        print(f"Total destination fields: {len(dest_fields)}")
        print(f"Successful matches: {len(successful_matches)}")
        print(f"Exact value matches: {len(exact_matches)}")
        print(f"Match rate: {len(successful_matches)/len(dest_fields)*100:.1f}%")
        print(f"Value accuracy: {len(exact_matches)/len(successful_matches)*100:.1f}%" if successful_matches else "N/A")
        
        print(f"\nSection mappings applied:")
        for mapping in sorted(section_mappings_used):
            print(f"  {mapping}")
        
        print(f"\nResults saved to: {output_file}")
        print("One-to-one mapping with semantic configuration applied!")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
