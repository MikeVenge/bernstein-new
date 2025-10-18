#!/usr/bin/env python3
"""
Hybrid Field Mapping Strategy

Combines both strategies:
1. Enhanced scope matching for precise hierarchical context
2. Semantic configuration mappings for terminology differences

This provides the best of both worlds:
- Precise scope-based matching when scopes align
- Semantic translation when terminology differs
- One-to-one mapping guarantee
- Complete coverage of field mappings

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

# Import the configuration mappings
from field_mapping_config import (
    SECTION_MAPPINGS,
    FIELD_NAME_MAPPINGS,
    get_semantic_equivalence_score,
    normalize_section_name,
    normalize_field_name
)


def load_both_enhanced_mappings() -> Tuple[List[Dict], List[Dict]]:
    """Load enhanced mappings for both source and destination with full context."""
    print("Loading enhanced field mappings for hybrid strategy...")
    
    # Load source mapping (Key Metrics)
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
                'is_percentage': row['Is_Percentage_Section'] if 'Is_Percentage_Section' in row else False
            })
        print(f"Loaded {len(source_fields)} source fields with enhanced scoping")
    
    # Load destination mapping (Reported)
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
                'file_type': 'destination'
            })
        print(f"Loaded {len(dest_fields)} destination fields with enhanced scoping")
    
    return source_fields, dest_fields


def calculate_hybrid_similarity(source_field: Dict, dest_field: Dict) -> Tuple[float, str]:
    """
    Calculate similarity using both enhanced scope and semantic configuration.
    Returns (score, method_used)
    """
    source_scope = source_field['enhanced_scoped_name'].lower()
    dest_scope = dest_field['enhanced_scoped_name'].lower()
    
    # Strategy 1: Direct enhanced scope matching
    if source_scope == dest_scope:
        return 1.0, 'exact_scope_match'
    
    # Strategy 2: Scope similarity (hierarchical components)
    scope_similarity = calculate_scope_similarity(source_scope, dest_scope)
    if scope_similarity > 0.8:
        return scope_similarity, 'scope_similarity'
    
    # Strategy 3: Semantic configuration-based matching
    semantic_score = get_semantic_equivalence_score(source_field, dest_field)
    if semantic_score > 0.6:
        return semantic_score, 'semantic_config'
    
    # Strategy 4: Field name similarity with context awareness
    field_similarity = calculate_contextual_field_similarity(source_field, dest_field)
    if field_similarity > 0.7:
        return field_similarity, 'contextual_field'
    
    # Strategy 5: Geographic/product specific matching
    specialized_score = calculate_specialized_matching(source_field, dest_field)
    if specialized_score > 0.6:
        return specialized_score, 'specialized_match'
    
    return 0.0, 'no_match'


def calculate_scope_similarity(source_scope: str, dest_scope: str) -> float:
    """Calculate similarity between enhanced scoped names."""
    if not source_scope or not dest_scope:
        return 0.0
    
    # Split scopes into components
    source_parts = source_scope.split('.')
    dest_parts = dest_scope.split('.')
    
    # Calculate component-wise similarity
    max_parts = max(len(source_parts), len(dest_parts))
    matching_parts = 0
    
    for i in range(min(len(source_parts), len(dest_parts))):
        if source_parts[i] == dest_parts[i]:
            matching_parts += 1
        elif SequenceMatcher(None, source_parts[i], dest_parts[i]).ratio() > 0.8:
            matching_parts += 0.5
    
    return matching_parts / max_parts if max_parts > 0 else 0.0


def calculate_contextual_field_similarity(source_field: Dict, dest_field: Dict) -> float:
    """Calculate field similarity with context awareness."""
    source_name = source_field['original_field_name'].lower()
    dest_name = dest_field['original_field_name'].lower()
    
    # Apply field name normalization
    normalized_source = normalize_field_name(source_name)
    normalized_dest = normalize_field_name(dest_name)
    
    if normalized_source == normalized_dest:
        return 0.9
    
    # String similarity on normalized names
    return SequenceMatcher(None, normalized_source, normalized_dest).ratio()


def calculate_specialized_matching(source_field: Dict, dest_field: Dict) -> float:
    """Calculate specialized matching for geographic/product/financial terms."""
    source_name = source_field['original_field_name'].lower()
    dest_name = dest_field['original_field_name'].lower()
    
    # Geographic terms matching
    geo_terms = ['north america', 'germany', 'china', 'japan', 'europe', 'asia', 'korea', 'world']
    source_geo = [term for term in geo_terms if term in source_name]
    dest_geo = [term for term in geo_terms if term in dest_name]
    
    if source_geo and dest_geo:
        if source_geo[0] == dest_geo[0]:
            return 0.8
        # Handle special cases
        if source_geo[0] == 'north america' and 'united states' in dest_name:
            return 0.7
        if source_geo[0] == 'other asia' and 'asian countries' in dest_name:
            return 0.7
    
    # Product/application terms
    product_terms = ['materials processing', 'communications', 'medical', 'advanced', 'high-power', 'pulsed', 'qcw', 'systems']
    source_prod = [term for term in product_terms if term in source_name]
    dest_prod = [term for term in product_terms if term in dest_name]
    
    if source_prod and dest_prod and source_prod[0] == dest_prod[0]:
        return 0.8
    
    # Financial terms
    financial_terms = ['revenue', 'total', 'income', 'sales', 'assets', 'cash', 'expense']
    source_fin = [term for term in financial_terms if term in source_name]
    dest_fin = [term for term in financial_terms if term in dest_name]
    
    if source_fin and dest_fin and source_fin[0] == dest_fin[0]:
        return 0.6
    
    return 0.0


def find_hybrid_matches(source_fields: List[Dict], dest_fields: List[Dict]) -> List[Dict]:
    """
    Find matches using hybrid strategy combining scope and semantic approaches.
    """
    print("Finding matches using hybrid strategy (scope + semantic)...")
    
    matches = []
    used_source_indices = set()
    
    # Sort destination fields by priority (geographic and key metrics first)
    def get_priority(dest_field):
        name = dest_field['original_field_name'].lower()
        if any(geo in name for geo in ['north america', 'germany', 'china', 'japan']):
            return 1  # Highest priority
        elif any(term in name for term in ['total', 'revenue', 'materials processing']):
            return 2  # High priority
        else:
            return 3  # Normal priority
    
    sorted_dest_fields = sorted(dest_fields, key=get_priority)
    
    for dest_field in sorted_dest_fields:
        dest_name = dest_field['original_field_name']
        
        print(f"\nFinding source for: {dest_name}")
        
        best_match = None
        best_score = 0.0
        best_source_idx = None
        best_method = None
        
        for i, source_field in enumerate(source_fields):
            if i in used_source_indices:
                continue
            
            score, method = calculate_hybrid_similarity(source_field, dest_field)
            
            if score > best_score:
                best_score = score
                best_match = source_field
                best_source_idx = i
                best_method = method
        
        # Accept matches above threshold
        if best_match and best_score > 0.6:
            used_source_indices.add(best_source_idx)
            
            match = {
                'dest_field': dest_field,
                'source_field': best_match,
                'similarity_score': best_score,
                'match_quality': get_match_quality(best_score),
                'matching_method': best_method
            }
            matches.append(match)
            
            print(f"  → MATCHED: {best_match['original_field_name']} (Score: {best_score:.3f}, Method: {best_method})")
            if best_method == 'semantic_config':
                source_section = str(best_match.get('section_context', '')).lower()
                dest_section = str(dest_field.get('section_context', '')).lower()
                if source_section in SECTION_MAPPINGS:
                    print(f"    Applied section mapping: '{source_section}' → '{SECTION_MAPPINGS[source_section]}'")
        else:
            match = {
                'dest_field': dest_field,
                'source_field': None,
                'similarity_score': 0.0,
                'match_quality': 'No Match',
                'matching_method': 'none'
            }
            matches.append(match)
            print(f"  → No suitable match found")
    
    successful_matches = [m for m in matches if m['source_field'] is not None]
    print(f"\nHybrid matching complete:")
    print(f"  Total matches: {len(successful_matches)}")
    print(f"  Unique source fields used: {len(used_source_indices)}")
    
    # Show method breakdown
    method_counts = {}
    for match in successful_matches:
        method = match['matching_method']
        method_counts[method] = method_counts.get(method, 0) + 1
    
    print("  Matching methods used:")
    for method, count in sorted(method_counts.items()):
        print(f"    {method}: {count} matches")
    
    return matches


def get_destination_q1_values_hybrid(dest_fields: List[Dict]) -> Dict:
    """Get Q1 2024 values from destination file (Column BR)."""
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
    return dest_values


def save_hybrid_results(matches: List[Dict], dest_q1_values: Dict, output_file: str):
    """Save hybrid mapping results."""
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
            'Matching_Method',
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
            
            # Handle NaN values safely
            def safe_str(val):
                return str(val) if val and not pd.isna(val) else ''
            
            writer.writerow({
                'Dest_Row_Number': dest['row_number'],
                'Dest_Field_Name': dest['original_field_name'],
                'Dest_Section_Context': safe_str(dest.get('section_context', '')),
                'Dest_Enhanced_Scope': dest['enhanced_scoped_name'],
                'Source_Row_Number': source['row_number'] if source else '',
                'Source_Field_Name': source['original_field_name'] if source else '',
                'Source_Section_Context': safe_str(source.get('section_context', '')) if source else '',
                'Source_Enhanced_Scope': source['enhanced_scoped_name'] if source else '',
                'Source_Q1_2024_Value': source_q1 if source_q1 is not None else '',
                'Dest_Q1_2024_Value': dest_q1 if dest_q1 is not None else '',
                'Source_Q2_2024_Value': source_q2 if source_q2 is not None else '',
                'Similarity_Score': f"{match['similarity_score']:.3f}",
                'Match_Quality': match['match_quality'],
                'Matching_Method': match['matching_method'],
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
    output_file = "/Users/michaelkim/code/Bernstein/hybrid_mapping_results.csv"
    
    print("="*80)
    print("HYBRID FIELD MAPPING STRATEGY")
    print("="*80)
    print("Combining enhanced scope matching + semantic configuration")
    print("Strategy 1: Enhanced scope matching for precise context")
    print("Strategy 2: Semantic configuration for terminology differences")
    print("Strategy 3: Contextual field similarity")
    print("Strategy 4: Specialized geographic/product matching")
    print(f"Output file: {output_file}")
    
    try:
        # Load enhanced mappings
        source_fields, dest_fields = load_both_enhanced_mappings()
        
        if not source_fields or not dest_fields:
            print("ERROR: Could not load mapping files")
            return
        
        # Find hybrid matches
        matches = find_hybrid_matches(source_fields, dest_fields)
        
        # Get destination Q1 values
        dest_q1_values = get_destination_q1_values_hybrid(dest_fields)
        
        # Save results
        save_hybrid_results(matches, dest_q1_values, output_file)
        
        # Comprehensive summary
        successful_matches = [m for m in matches if m['source_field'] is not None]
        exact_value_matches = []
        
        for match in successful_matches:
            dest_row = match['dest_field']['row_number']
            dest_q1 = dest_q1_values.get(dest_row)
            source_q1 = match['source_field']['q1_2024_value']
            
            if dest_q1 is not None and source_q1 is not None and dest_q1 == source_q1:
                exact_value_matches.append(match)
        
        print(f"\n" + "="*80)
        print("HYBRID MAPPING RESULTS")
        print("="*80)
        print(f"Total destination fields: {len(dest_fields)}")
        print(f"Successful matches: {len(successful_matches)}")
        print(f"Exact value matches: {len(exact_value_matches)}")
        print(f"Match rate: {len(successful_matches)/len(dest_fields)*100:.1f}%")
        print(f"Value accuracy: {len(exact_value_matches)/len(successful_matches)*100:.1f}%" if successful_matches else "N/A")
        
        # Show examples of exact value matches
        print(f"\nExact value matches (Source CN = Dest BR):")
        for match in exact_value_matches[:10]:  # Show first 10
            dest_field = match['dest_field']
            source_field = match['source_field']
            dest_q1 = dest_q1_values.get(dest_field['row_number'])
            print(f"  {source_field['original_field_name']} → {dest_field['original_field_name']}: {dest_q1:,}")
        
        print(f"\nResults saved to: {output_file}")
        print("Hybrid strategy provides maximum coverage with one-to-one mapping!")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
