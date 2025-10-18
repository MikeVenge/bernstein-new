#!/usr/bin/env python3
"""
Create Generic Field Mapping

Transforms the current specific mapping into a generic, reusable mapping format
that focuses on field relationships and transformations rather than specific data values.

Author: AI Assistant
Date: October 2025
"""

import pandas as pd
import csv
from pathlib import Path
from typing import Dict, List, Optional


def transform_to_generic_mapping(specific_mapping_file: str) -> List[Dict]:
    """Transform specific mapping to generic reusable format."""
    
    print("=== TRANSFORMING TO GENERIC MAPPING FORMAT ===")
    
    # Load current specific mapping
    df = pd.read_csv(specific_mapping_file)
    print(f"Loaded {len(df)} specific mappings")
    
    generic_mappings = []
    
    for _, row in df.iterrows():
        # Create generic mapping focused on relationships, not specific values
        generic_mapping = {
            # DESTINATION FIELD DEFINITION
            'Dest_Row_Number': row['Dest_Row_Number'],
            'Dest_Field_Name': row['Dest_Field_Name'],
            'Dest_Field_Category': categorize_field(row['Dest_Field_Name']),
            'Dest_Section': extract_section(row['Dest_Major_Section_Context']),
            'Dest_Subsection': extract_subsection(row['Dest_Section_Context']),
            
            # SOURCE FIELD DEFINITION  
            'Source_Sheet_Name': row['Source_Sheet_Name'],
            'Source_Row_Number': row['Source_Row_Number'],
            'Source_Field_Name': row['Source_Field_Name'],
            'Source_Field_Category': categorize_field(row['Source_Field_Name']),
            'Source_Section': extract_section(row['Source_Section_Context']),
            
            # MAPPING RELATIONSHIP
            'Mapping_Type': determine_mapping_type(row),
            'Field_Relationship': determine_field_relationship(row['Dest_Field_Name'], row['Source_Field_Name']),
            'Transformation_Required': determine_transformation(row),
            'Data_Source_Column': 'CO',  # Generic reference to Q2 column
            'Confidence_Level': normalize_confidence(row.get('Match_Confidence', '1.0')),
            
            # VALIDATION RULES
            'Validation_Method': generalize_validation_method(row['Match_Method']),
            'Historical_Verification': 'YES' if 'Historical' in row['Match_Method'] else 'NO',
            'Composite_Field': 'YES' if '+' in str(row['Source_Row_Number']) else 'NO',
            
            # NOTES
            'Mapping_Notes': create_generic_notes(row),
            'Original_Match_Method': row['Match_Method']  # Keep for reference
        }
        
        generic_mappings.append(generic_mapping)
    
    print(f"Created {len(generic_mappings)} generic mappings")
    return generic_mappings


def categorize_field(field_name: str) -> str:
    """Categorize field into generic types."""
    if not field_name:
        return 'Unknown'
    
    field_lower = field_name.lower()
    
    # Revenue/Sales categories
    if any(word in field_lower for word in ['revenue', 'sales', 'net sales']):
        return 'Revenue'
    
    # Geographic categories
    if any(word in field_lower for word in ['north america', 'united states', 'germany', 'china', 'japan', 'asia', 'europe']):
        return 'Geographic'
    
    # Product/Segment categories
    if any(word in field_lower for word in ['laser', 'systems', 'materials processing', 'applications']):
        return 'Product_Segment'
    
    # Financial statement categories
    if any(word in field_lower for word in ['cost', 'expenses', 'income', 'profit', 'assets', 'liabilities', 'equity']):
        return 'Financial_Statement_Item'
    
    # Cash flow categories
    if any(word in field_lower for word in ['cash flow', 'operating activities', 'investing', 'financing']):
        return 'Cash_Flow'
    
    # Percentage/Ratio categories
    if '%' in field_lower or 'total' in field_lower:
        return 'Percentage_Total'
    
    return 'Other'


def extract_section(section_context: str) -> str:
    """Extract generic section from specific context."""
    if not section_context or pd.isna(section_context):
        return 'Unknown'
    
    section_lower = str(section_context).lower()
    
    # Standardize section names
    if 'segment' in section_lower or 'breakdown' in section_lower:
        return 'Segment_Information'
    elif 'income' in section_lower and 'statement' in section_lower:
        return 'Income_Statement'
    elif 'balance' in section_lower and 'sheet' in section_lower:
        return 'Balance_Sheet'
    elif 'cash' in section_lower and 'flow' in section_lower:
        return 'Cash_Flow_Statement'
    elif 'operating' in section_lower:
        return 'Operating_Activities'
    elif 'investing' in section_lower:
        return 'Investing_Activities'
    elif 'financing' in section_lower:
        return 'Financing_Activities'
    else:
        return str(section_context)


def extract_subsection(subsection_context: str) -> str:
    """Extract generic subsection from specific context."""
    if not subsection_context or pd.isna(subsection_context):
        return ''
    
    return str(subsection_context).replace('_', ' ').title()


def determine_mapping_type(row: Dict) -> str:
    """Determine the type of mapping relationship."""
    
    dest_name = str(row['Dest_Field_Name']).lower()
    source_name = str(row['Source_Field_Name']).lower()
    
    # Exact match
    if dest_name == source_name:
        return 'Exact_Match'
    
    # Semantic equivalent
    if any(word in source_name for word in dest_name.split() if len(word) > 3):
        return 'Semantic_Match'
    
    # Composite field
    if '+' in str(row['Source_Row_Number']):
        return 'Composite_Match'
    
    # Geographic mapping
    geographic_mappings = {
        'north america': 'united states',
        'other europe': 'eastern europe',
        'other asia': 'asian countries'
    }
    
    for source_geo, dest_geo in geographic_mappings.items():
        if source_geo in source_name and dest_geo in dest_name:
            return 'Geographic_Translation'
    
    # Broader category match
    if len(source_name.split()) < len(dest_name.split()):
        return 'Broader_Category_Match'
    
    return 'Manual_Match'


def determine_field_relationship(dest_field: str, source_field: str) -> str:
    """Determine the relationship between destination and source fields."""
    
    if not dest_field or not source_field:
        return 'Unknown'
    
    dest_lower = dest_field.lower()
    source_lower = source_field.lower()
    
    # Direct equivalents
    if dest_lower == source_lower:
        return 'Direct_Equivalent'
    
    # Geographic translations
    geo_translations = [
        ('united states and other north america', 'north america'),
        ('other including eastern europe/cis', 'other europe'),
        ('other asian countries', 'other asia')
    ]
    
    for dest_geo, source_geo in geo_translations:
        if dest_geo in dest_lower and source_geo in source_lower:
            return 'Geographic_Translation'
    
    # Terminology differences
    terminology_mappings = [
        ('end market breakdown', 'revenue by application'),
        ('segment breakdown', 'revenue by product'),
        ('region breakdown', 'revenue by region')
    ]
    
    for dest_term, source_term in terminology_mappings:
        if dest_term in dest_lower and source_term in source_lower:
            return 'Terminology_Translation'
    
    # Broader to specific
    if any(word in source_lower for word in dest_lower.split() if len(word) > 3):
        return 'Semantic_Equivalent'
    
    return 'Manual_Mapping'


def determine_transformation(row: Dict) -> str:
    """Determine what transformation is required during mapping."""
    
    transformations = []
    
    # Composite field transformation
    if '+' in str(row['Source_Row_Number']):
        transformations.append('SUM_MULTIPLE_FIELDS')
    
    # Data type transformations
    source_q2 = row.get('Source_Q2_Value', '')
    if source_q2:
        try:
            value = float(source_q2)
            if 0 < value < 1:
                transformations.append('PERCENTAGE_TO_DECIMAL')
            elif value == 0:
                transformations.append('ZERO_VALUE')
        except:
            pass
    
    # Sign transformations (if needed)
    match_reason = row.get('Match_Reason', '')
    if 'different sign' in match_reason.lower():
        transformations.append('SIGN_ADJUSTMENT')
    
    # Default
    if not transformations:
        transformations.append('DIRECT_COPY')
    
    return ';'.join(transformations)


def normalize_confidence(confidence: str) -> str:
    """Normalize confidence to standard levels."""
    try:
        conf_value = float(confidence)
        if conf_value >= 0.95:
            return 'HIGH'
        elif conf_value >= 0.80:
            return 'MEDIUM'
        else:
            return 'LOW'
    except:
        return 'UNKNOWN'


def generalize_validation_method(match_method: str) -> str:
    """Generalize validation method to reusable categories."""
    
    if 'Q1_Value_Verification' in match_method:
        return 'Historical_Value_Verification'
    elif 'Q1_2023_Verification' in match_method:
        return 'Multi_Period_Historical_Verification'
    elif 'Manual_Field_Name_Match' in match_method:
        return 'Field_Name_Matching'
    elif 'Manual_Semantic_Match' in match_method:
        return 'Semantic_Matching'
    elif 'Manual_Composite_Match' in match_method:
        return 'Composite_Field_Matching'
    elif 'Historical_Verification' in match_method:
        return 'Historical_Data_Verification'
    else:
        return 'Manual_Validation'


def create_generic_notes(row: Dict) -> str:
    """Create generic notes explaining the mapping."""
    
    notes = []
    
    # Field relationship notes
    dest_name = row['Dest_Field_Name']
    source_name = row['Source_Field_Name']
    
    if dest_name.lower() == source_name.lower():
        notes.append("Exact field name match")
    elif any(word in source_name.lower() for word in dest_name.lower().split() if len(word) > 3):
        notes.append("Semantic field name match")
    else:
        notes.append("Manual field mapping required")
    
    # Transformation notes
    if '+' in str(row['Source_Row_Number']):
        notes.append("Composite field - sum multiple source fields")
    
    # Validation notes
    if row.get('Match_Confidence'):
        conf = float(row['Match_Confidence'])
        if conf < 0.9:
            notes.append("Lower confidence mapping - review recommended")
    
    return '; '.join(notes)


def save_generic_mapping(generic_mappings: List[Dict], output_file: str):
    """Save the generic mapping to CSV file."""
    
    print(f"\nSaving generic mapping to: {output_file}")
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            # DESTINATION FIELD DEFINITION
            'Dest_Row_Number', 'Dest_Field_Name', 'Dest_Field_Category',
            'Dest_Section', 'Dest_Subsection',
            
            # SOURCE FIELD DEFINITION
            'Source_Sheet_Name', 'Source_Row_Number', 'Source_Field_Name',
            'Source_Field_Category', 'Source_Section',
            
            # MAPPING RELATIONSHIP
            'Mapping_Type', 'Field_Relationship', 'Transformation_Required',
            'Data_Source_Column', 'Confidence_Level',
            
            # VALIDATION RULES
            'Validation_Method', 'Historical_Verification', 'Composite_Field',
            
            # NOTES
            'Mapping_Notes', 'Original_Match_Method'
        ]
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(generic_mappings)
    
    print(f"Generic mapping saved with {len(generic_mappings)} entries")


def generate_mapping_summary(generic_mappings: List[Dict]):
    """Generate summary of the generic mapping."""
    
    print(f"\n=== GENERIC MAPPING SUMMARY ===")
    
    # Count by categories
    categories = {}
    mapping_types = {}
    transformations = {}
    
    for mapping in generic_mappings:
        # Field categories
        dest_cat = mapping['Dest_Field_Category']
        categories[dest_cat] = categories.get(dest_cat, 0) + 1
        
        # Mapping types
        map_type = mapping['Mapping_Type']
        mapping_types[map_type] = mapping_types.get(map_type, 0) + 1
        
        # Transformations
        transform = mapping['Transformation_Required']
        transformations[transform] = transformations.get(transform, 0) + 1
    
    print(f"Field categories:")
    for category, count in sorted(categories.items()):
        print(f"  {category}: {count}")
    
    print(f"\nMapping types:")
    for map_type, count in sorted(mapping_types.items()):
        print(f"  {map_type}: {count}")
    
    print(f"\nTransformations required:")
    for transform, count in sorted(transformations.items()):
        print(f"  {transform}: {count}")


def create_generic_mapper_template():
    """Create a template for using generic mappings."""
    
    template_content = '''# Generic Field Mapping Template

## Usage
This generic mapping file can be used with any similar financial data mapping project.

## Field Categories
- Revenue: Sales, revenue, and income fields
- Geographic: Country/region-specific fields  
- Product_Segment: Product lines, segments, applications
- Financial_Statement_Item: Standard financial statement line items
- Cash_Flow: Cash flow statement items
- Percentage_Total: Percentage breakdowns and totals

## Mapping Types
- Exact_Match: Field names are identical
- Semantic_Match: Field names have same meaning but different wording
- Geographic_Translation: Country/region name differences
- Composite_Match: Destination field is sum of multiple source fields
- Broader_Category_Match: Source field is broader category than destination

## Transformations
- DIRECT_COPY: Copy value as-is
- SUM_MULTIPLE_FIELDS: Sum values from multiple source fields
- PERCENTAGE_TO_DECIMAL: Convert percentage to decimal format
- ZERO_VALUE: Handle zero/null values appropriately
- SIGN_ADJUSTMENT: Adjust positive/negative sign if needed

## Validation Methods
- Historical_Value_Verification: Use historical data to verify matches
- Field_Name_Matching: Match based on field name similarity
- Semantic_Matching: Match based on field meaning
- Composite_Field_Matching: Handle multi-field aggregations
'''
    
    template_file = "/Users/michaelkim/code/Bernstein/GENERIC_MAPPING_TEMPLATE.md"
    with open(template_file, 'w') as f:
        f.write(template_content)
    
    print(f"Generic mapping template saved to: {template_file}")
    return template_file


def main():
    """Main entry point for creating generic field mapping."""
    
    print("="*80)
    print("CREATE GENERIC FIELD MAPPING")
    print("="*80)
    print("Transforming specific data mapping to generic reusable format")
    
    try:
        # Input and output files
        specific_mapping_file = "/Users/michaelkim/code/Bernstein/CONSOLIDATED_FIELD_MAPPINGS.csv"
        generic_mapping_file = "/Users/michaelkim/code/Bernstein/GENERIC_FIELD_MAPPINGS.csv"
        
        # Transform to generic format
        generic_mappings = transform_to_generic_mapping(specific_mapping_file)
        
        # Save generic mapping
        save_generic_mapping(generic_mappings, generic_mapping_file)
        
        # Generate summary
        generate_mapping_summary(generic_mappings)
        
        # Create template
        template_file = create_generic_mapper_template()
        
        print(f"\n" + "="*80)
        print("GENERIC MAPPING CREATION COMPLETE")
        print("="*80)
        print(f"✅ Generic mapping file: {generic_mapping_file}")
        print(f"✅ Template documentation: {template_file}")
        print(f"✅ Total generic mappings: {len(generic_mappings)}")
        
        print(f"\nKEY IMPROVEMENTS:")
        print(f"  📝 Removed specific Q1/Q2 values")
        print(f"  📝 Focused on field relationships and transformations")
        print(f"  📝 Added generic field categories")
        print(f"  📝 Standardized mapping types")
        print(f"  📝 Included transformation rules")
        print(f"  📝 Created reusable validation methods")
        
        print(f"\n🎯 This generic mapping can now be used for:")
        print(f"  - Different time periods (Q3, Q4, etc.)")
        print(f"  - Different companies with similar structure")
        print(f"  - Different data sources with same field relationships")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
