#!/usr/bin/env python3
"""
Create Generic Field Mapping - Simplified

Creates a generic, reusable field mapping that removes specific data values
and focuses on field relationships and transformations.

Author: AI Assistant
Date: October 2025
"""

import pandas as pd
import csv
from pathlib import Path


def categorize_field_type(field_name: str) -> str:
    """Categorize field into generic types."""
    if not field_name:
        return 'Unknown'
    
    field_lower = field_name.lower()
    
    if any(word in field_lower for word in ['revenue', 'sales']):
        return 'Revenue'
    elif any(word in field_lower for word in ['north america', 'united states', 'germany', 'china', 'japan', 'asia', 'europe']):
        return 'Geographic'
    elif any(word in field_lower for word in ['laser', 'systems', 'materials processing', 'applications']):
        return 'Product_Segment'
    elif any(word in field_lower for word in ['cost', 'expenses', 'income', 'profit']):
        return 'Income_Statement'
    elif any(word in field_lower for word in ['assets', 'liabilities', 'equity']):
        return 'Balance_Sheet'
    elif any(word in field_lower for word in ['cash flow', 'operating', 'investing', 'financing']):
        return 'Cash_Flow'
    elif 'total' in field_lower or '%' in field_lower:
        return 'Total_Percentage'
    else:
        return 'Other'


def determine_transformation_type(row) -> str:
    """Determine what transformation is needed."""
    
    transformations = []
    
    # Check for composite fields
    if '+' in str(row['Source_Row_Number']):
        transformations.append('SUM_MULTIPLE_FIELDS')
    
    # Check for data type
    try:
        q2_value = float(row['Source_Q2_Value'])
        if 0 < q2_value < 1:
            transformations.append('DECIMAL_VALUE')
        elif q2_value == 0:
            transformations.append('ZERO_VALUE')
        else:
            transformations.append('ABSOLUTE_VALUE')
    except:
        transformations.append('DIRECT_COPY')
    
    return ';'.join(transformations) if transformations else 'DIRECT_COPY'


def determine_mapping_relationship(dest_name: str, source_name: str) -> str:
    """Determine the relationship between fields."""
    
    if not dest_name or not source_name:
        return 'Unknown'
    
    dest_lower = dest_name.lower()
    source_lower = source_name.lower()
    
    # Exact match
    if dest_lower == source_lower:
        return 'Exact_Match'
    
    # Geographic translations
    geographic_mappings = {
        'united states and other north america': 'north america',
        'other including eastern europe/cis': 'other europe',
        'other asian countries': 'other asia'
    }
    
    for dest_geo, source_geo in geographic_mappings.items():
        if dest_geo in dest_lower and source_geo in source_lower:
            return 'Geographic_Translation'
    
    # Terminology translations
    if ('end market' in dest_lower and 'application' in source_lower) or \
       ('segment breakdown' in dest_lower and 'product' in source_lower):
        return 'Terminology_Translation'
    
    # Semantic match
    common_words = set(dest_lower.split()) & set(source_lower.split())
    if len(common_words) >= 2:
        return 'Semantic_Match'
    
    return 'Manual_Match'


def create_generic_mapping():
    """Create generic mapping from consolidated mapping."""
    
    print("=== CREATING GENERIC FIELD MAPPING ===")
    
    # Load consolidated mapping
    df = pd.read_csv('/Users/michaelkim/code/Bernstein/CONSOLIDATED_FIELD_MAPPINGS.csv')
    print(f"Loaded {len(df)} consolidated mappings")
    
    generic_mappings = []
    
    for _, row in df.iterrows():
        generic_mapping = {
            # CORE FIELD IDENTIFICATION
            'Dest_Row_Number': row['Dest_Row_Number'],
            'Dest_Field_Name': row['Dest_Field_Name'],
            'Dest_Field_Type': categorize_field_type(row['Dest_Field_Name']),
            'Dest_Section': row['Dest_Major_Section_Context'] if pd.notna(row['Dest_Major_Section_Context']) else '',
            
            # SOURCE FIELD IDENTIFICATION
            'Source_Sheet_Name': row['Source_Sheet_Name'],
            'Source_Row_Number': row['Source_Row_Number'],
            'Source_Field_Name': row['Source_Field_Name'],
            'Source_Field_Type': categorize_field_type(row['Source_Field_Name']),
            'Source_Data_Column': 'CO',  # Generic column reference
            
            # MAPPING RELATIONSHIP
            'Mapping_Relationship': determine_mapping_relationship(row['Dest_Field_Name'], row['Source_Field_Name']),
            'Transformation_Type': determine_transformation_type(row),
            'Confidence_Level': 'HIGH' if float(row.get('Match_Confidence', 0)) >= 0.9 else 'MEDIUM',
            
            # MAPPING RULES
            'Validation_Method': 'Historical_Verification' if 'Q1' in row['Match_Method'] else 'Field_Name_Matching',
            'Composite_Field': 'YES' if '+' in str(row['Source_Row_Number']) else 'NO',
            'Manual_Override': 'YES' if 'Manual' in row['Match_Method'] else 'NO',
            
            # DOCUMENTATION
            'Field_Mapping_Notes': create_mapping_notes(row),
            'Original_Method': row['Match_Method']
        }
        
        generic_mappings.append(generic_mapping)
    
    return generic_mappings


def create_mapping_notes(row) -> str:
    """Create concise mapping notes."""
    
    notes = []
    
    # Field relationship
    dest_name = row['Dest_Field_Name'].lower()
    source_name = row['Source_Field_Name'].lower()
    
    if dest_name == source_name:
        notes.append("Exact field name match")
    elif 'north america' in dest_name and 'north america' in source_name:
        notes.append("Geographic field - direct match")
    elif 'other europe' in source_name and 'eastern europe' in dest_name:
        notes.append("Geographic translation: Other Europe → Eastern Europe/CIS")
    elif 'application' in source_name and 'end market' in dest_name:
        notes.append("Terminology: Revenue by application → End market breakdown")
    elif 'product' in source_name and 'segment' in dest_name:
        notes.append("Terminology: Revenue by product → Segment breakdown")
    else:
        notes.append("Semantic match based on field meaning")
    
    # Special handling
    if '+' in str(row['Source_Row_Number']):
        notes.append("Composite field - sum multiple source rows")
    
    return '; '.join(notes)


def save_generic_mapping(mappings):
    """Save generic mapping to CSV."""
    
    output_file = "/Users/michaelkim/code/Bernstein/GENERIC_FIELD_MAPPINGS.csv"
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'Dest_Row_Number', 'Dest_Field_Name', 'Dest_Field_Type', 'Dest_Section',
            'Source_Sheet_Name', 'Source_Row_Number', 'Source_Field_Name', 'Source_Field_Type', 'Source_Data_Column',
            'Mapping_Relationship', 'Transformation_Type', 'Confidence_Level',
            'Validation_Method', 'Composite_Field', 'Manual_Override',
            'Field_Mapping_Notes', 'Original_Method'
        ]
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(mappings)
    
    print(f"Generic mapping saved to: {output_file}")
    return output_file


def main():
    """Main entry point."""
    
    print("="*80)
    print("CREATING GENERIC REUSABLE FIELD MAPPING")
    print("="*80)
    
    try:
        # Create generic mappings
        generic_mappings = create_generic_mapping()
        
        # Save to file
        output_file = save_generic_mapping(generic_mappings)
        
        # Show summary
        print(f"\n=== GENERIC MAPPING SUMMARY ===")
        df = pd.DataFrame(generic_mappings)
        
        print(f"Total mappings: {len(df)}")
        print(f"\nField types:")
        print(df['Dest_Field_Type'].value_counts())
        
        print(f"\nMapping relationships:")
        print(df['Mapping_Relationship'].value_counts())
        
        print(f"\nTransformation types:")
        print(df['Transformation_Type'].value_counts())
        
        print(f"\n✅ Generic mapping created successfully!")
        print(f"📁 File: {output_file}")
        print(f"🎯 Ready for reuse with different datasets!")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
