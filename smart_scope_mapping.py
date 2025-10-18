#!/usr/bin/env python3
"""
Smart Scope-Based Field Mapping

This script creates intelligent mapping between source and destination fields
by understanding the semantic equivalence between different scoping systems.

For example:
- Source: Revenue_Statement.Geographic_Breakdown.Germany
- Destination: Destination.Segment_Information_In_000_Usd_Ytd.Germany
- These should match because both refer to "Germany revenue data"

Author: AI Assistant
Date: October 2025
"""

import pandas as pd
import openpyxl
import csv
from pathlib import Path
import re
from typing import Dict, List, Tuple, Optional
from difflib import SequenceMatcher


def load_enhanced_mappings() -> Tuple[List[Dict], List[Dict]]:
    """Load the enhanced mappings for both source and destination."""
    print("Loading enhanced field mappings...")
    
    # Load source mapping (Key Metrics with enhanced scoping)
    source_file = "/Users/michaelkim/code/Bernstein/final_improved_key_metrics_mapping.csv"
    if Path(source_file).exists():
        source_df = pd.read_csv(source_file)
        source_fields = []
        for _, row in source_df.iterrows():
            source_fields.append({
                'row_number': row['Row_Number'],
                'original_field_name': row['Original_Field_Name'],
                'cleaned_field_name': row['Cleaned_Field_Name'],
                'section_context': row['Section_Context'],
                'enhanced_scoped_name': row['Enhanced_Scoped_Name'],
                'q1_2024_value': row['Q1_2024_Value'] if pd.notna(row['Q1_2024_Value']) else None,
                'q2_2024_value': row['Q2_2024_Value'] if pd.notna(row['Q2_2024_Value']) else None,
                'file_type': 'source'
            })
        print(f"Loaded {len(source_fields)} source fields")
    else:
        print(f"Source mapping file not found: {source_file}")
        source_fields = []
    
    # Load destination mapping (Reported with enhanced scoping)
    dest_file = "/Users/michaelkim/code/Bernstein/reported_tab_comprehensive_mapping.csv"
    if Path(dest_file).exists():
        dest_df = pd.read_csv(dest_file)
        dest_fields = []
        for _, row in dest_df.iterrows():
            dest_fields.append({
                'row_number': row['Row_Number'],
                'original_field_name': row['Original_Field_Name'],
                'cleaned_field_name': row['Cleaned_Field_Name'],
                'major_section_context': row['Major_Section_Context'],
                'section_context': row['Section_Context'],
                'enhanced_scoped_name': row['Enhanced_Scoped_Name'],
                'file_type': 'destination'
            })
        print(f"Loaded {len(dest_fields)} destination fields")
    else:
        print(f"Destination mapping file not found: {dest_file}")
        dest_fields = []
    
    return source_fields, dest_fields


def extract_semantic_components(scoped_name: str, field_name: str) -> Dict:
    """
    Extract semantic components from a scoped name.
    """
    components = {
        'statement_type': None,
        'data_category': None,
        'value_type': None,
        'geographic_region': None,
        'field_name': field_name.lower()
    }
    
    scope_lower = scoped_name.lower()
    field_lower = field_name.lower()
    
    # Determine statement type
    if any(term in scope_lower for term in ['revenue', 'sales']):
        components['statement_type'] = 'revenue'
    elif any(term in scope_lower for term in ['income', 'profit', 'expense']):
        components['statement_type'] = 'income'
    elif any(term in scope_lower for term in ['balance', 'asset', 'liability', 'equity']):
        components['statement_type'] = 'balance_sheet'
    elif any(term in scope_lower for term in ['cash', 'flow']):
        components['statement_type'] = 'cash_flow'
    elif any(term in scope_lower for term in ['operation', 'employee']):
        components['statement_type'] = 'operations'
    
    # Determine data category
    if any(term in scope_lower for term in ['geographic', 'region']):
        components['data_category'] = 'geographic'
    elif any(term in scope_lower for term in ['product', 'application']):
        components['data_category'] = 'product'
    elif any(term in scope_lower for term in ['total']):
        components['data_category'] = 'total'
    
    # Determine value type
    if any(term in scope_lower for term in ['percent', '%', 'ratio']):
        components['value_type'] = 'percentage'
    else:
        components['value_type'] = 'absolute'
    
    # Determine geographic region
    geo_regions = {
        'north_america': 'north_america',
        'united_states': 'north_america', 
        'germany': 'germany',
        'china': 'china',
        'japan': 'japan',
        'europe': 'europe',
        'asia': 'asia',
        'korea': 'korea',
        'world': 'world'
    }
    
    for geo_key, geo_value in geo_regions.items():
        if geo_key in field_lower or geo_key in scope_lower:
            components['geographic_region'] = geo_value
            break
    
    return components


def calculate_semantic_similarity(source_field: Dict, dest_field: Dict) -> float:
    """
    Calculate semantic similarity between source and destination fields.
    """
    # Extract semantic components
    source_components = extract_semantic_components(
        source_field['enhanced_scoped_name'], 
        source_field['original_field_name']
    )
    dest_components = extract_semantic_components(
        dest_field['enhanced_scoped_name'], 
        dest_field['original_field_name']
    )
    
    score = 0.0
    
    # Field name similarity (highest weight)
    field_similarity = SequenceMatcher(
        None, 
        source_components['field_name'], 
        dest_components['field_name']
    ).ratio()
    score += field_similarity * 0.4
    
    # Statement type match
    if (source_components['statement_type'] == dest_components['statement_type'] and 
        source_components['statement_type'] is not None):
        score += 0.2
    
    # Data category match
    if (source_components['data_category'] == dest_components['data_category'] and 
        source_components['data_category'] is not None):
        score += 0.2
    
    # Geographic region match (very important for regional data)
    if (source_components['geographic_region'] == dest_components['geographic_region'] and 
        source_components['geographic_region'] is not None):
        score += 0.15
    
    # Value type match (absolute vs percentage)
    if source_components['value_type'] == dest_components['value_type']:
        score += 0.05
    
    return min(score, 1.0)


def find_smart_matches(source_fields: List[Dict], dest_fields: List[Dict]) -> List[Dict]:
    """
    Find smart matches using semantic similarity.
    """
    print("Finding smart matches using semantic similarity...")
    
    matches = []
    used_source_indices = set()  # Track which source fields have been used
    
    for dest_field in dest_fields:
        dest_name = dest_field['original_field_name']
        print(f"\nFinding source for: {dest_name}")
        
        best_match = None
        best_score = 0.0
        best_source_idx = None
        
        for i, source_field in enumerate(source_fields):
            # Skip if this source field is already used
            if i in used_source_indices:
                continue
                
            score = calculate_semantic_similarity(source_field, dest_field)
            
            if score > best_score:
                best_score = score
                best_match = source_field
                best_source_idx = i
        
        # Only accept matches above threshold
        if best_match and best_score > 0.6:
            used_source_indices.add(best_source_idx)  # Mark this source as used
            
            match = {
                'dest_field': dest_field,
                'source_field': best_match,
                'similarity_score': best_score,
                'match_quality': get_match_quality(best_score)
            }
            matches.append(match)
            
            print(f"  → MATCHED: {best_match['original_field_name']} (Score: {best_score:.3f})")
            print(f"    Source scope: {best_match['enhanced_scoped_name']}")
            print(f"    Dest scope: {dest_field['enhanced_scoped_name']}")
        else:
            match = {
                'dest_field': dest_field,
                'source_field': None,
                'similarity_score': 0.0,
                'match_quality': 'No Match'
            }
            matches.append(match)
            print(f"  → No suitable match found")
    
    print(f"\nTotal matches found: {len([m for m in matches if m['source_field'] is not None])}")
    print(f"Unique source fields used: {len(used_source_indices)}")
    
    return matches


def get_destination_q1_values(dest_fields: List[Dict]) -> Dict:
    """Get Q1 2024 values from destination file."""
    print("Loading destination Q1 2024 values...")
    
    target_file = "/Users/michaelkim/code/Bernstein/20240725_IPGP.US-IPG Photonics.xlsx"
    wb = openpyxl.load_workbook(target_file, data_only=True)
    sheet = wb['Reported']
    
    dest_values = {}
    for dest_field in dest_fields:
        row_num = dest_field['row_number']
        q1_value = sheet.cell(row_num, 70).value  # Column BR (Q1 2024)
        dest_values[row_num] = q1_value
    
    wb.close()
    return dest_values


def save_smart_mapping_results(matches: List[Dict], dest_q1_values: Dict, output_file: str):
    """Save smart mapping results."""
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'Dest_Row_Number',
            'Dest_Field_Name',
            'Dest_Enhanced_Scope',
            'Source_Row_Number',
            'Source_Field_Name',
            'Source_Enhanced_Scope',
            'Source_Q1_2024_Value',
            'Dest_Q1_2024_Value',
            'Source_Q2_2024_Value',
            'Similarity_Score',
            'Match_Quality',
            'Values_Match'
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
                if dest_q1 == source_q1:
                    values_match = 'Exact Match'
                elif abs(float(dest_q1) - float(source_q1)) / float(source_q1) < 0.05:
                    values_match = 'Close Match'
                else:
                    values_match = 'Different'
            elif dest_q1 is None and source_q1 is None:
                values_match = 'Both Empty'
            else:
                values_match = 'One Empty'
            
            writer.writerow({
                'Dest_Row_Number': dest['row_number'],
                'Dest_Field_Name': dest['original_field_name'],
                'Dest_Enhanced_Scope': dest['enhanced_scoped_name'],
                'Source_Row_Number': source['row_number'] if source else '',
                'Source_Field_Name': source['original_field_name'] if source else '',
                'Source_Enhanced_Scope': source['enhanced_scoped_name'] if source else '',
                'Source_Q1_2024_Value': source_q1 if source_q1 is not None else '',
                'Dest_Q1_2024_Value': dest_q1 if dest_q1 is not None else '',
                'Source_Q2_2024_Value': source_q2 if source_q2 is not None else '',
                'Similarity_Score': f"{match['similarity_score']:.3f}",
                'Match_Quality': match['match_quality'],
                'Values_Match': values_match
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
    output_file = "/Users/michaelkim/code/Bernstein/smart_scope_mapping_results.csv"
    
    print("="*80)
    print("SMART SCOPE-BASED FIELD MAPPING")
    print("="*80)
    print("Using semantic similarity to match fields across different scoping systems")
    print(f"Output file: {output_file}")
    
    try:
        # Load enhanced mappings
        source_fields, dest_fields = load_enhanced_mappings()
        
        if not source_fields or not dest_fields:
            print("ERROR: Could not load mapping files")
            return
        
        # Find smart matches
        matches = find_smart_matches(source_fields, dest_fields)
        
        # Get destination Q1 values
        dest_q1_values = get_destination_q1_values(dest_fields)
        
        # Save results
        save_smart_mapping_results(matches, dest_q1_values, output_file)
        
        # Summary
        successful_matches = [m for m in matches if m['source_field'] is not None]
        exact_matches = [m for m in matches if m['source_field'] and 
                        dest_q1_values.get(m['dest_field']['row_number']) == m['source_field']['q1_2024_value']]
        
        print(f"\n" + "="*80)
        print("SMART MAPPING RESULTS")
        print("="*80)
        print(f"Total destination fields: {len(dest_fields)}")
        print(f"Successful matches: {len(successful_matches)}")
        print(f"Exact value matches: {len(exact_matches)}")
        print(f"Match rate: {len(successful_matches)/len(dest_fields)*100:.1f}%")
        print(f"Value accuracy: {len(exact_matches)/len(successful_matches)*100:.1f}%" if successful_matches else "N/A")
        
        print(f"\nResults saved to: {output_file}")
        print("This mapping prevents one-to-many matches by using semantic similarity.")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
