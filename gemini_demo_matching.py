#!/usr/bin/env python3
"""
Gemini Field Matching Demo

Demonstrates the Gemini 2.5 Pro approach for intelligent field matching.
Shows the prompt that would be sent to Gemini and simulates intelligent matching.

Author: AI Assistant
Date: October 2025
"""

import pandas as pd
import csv
from pathlib import Path
from typing import Dict, List, Tuple


def load_fields_for_gemini_demo() -> Tuple[List[Dict], List[Dict]]:
    """Load fields for Gemini demo."""
    print("Loading fields for Gemini demo...")
    
    # Load source fields (focus on Key Metrics revenue fields)
    source_file = "/Users/michaelkim/code/Bernstein/final_improved_key_metrics_mapping.csv"
    source_fields = []
    
    if Path(source_file).exists():
        source_df = pd.read_csv(source_file)
        for idx, row in source_df.iterrows():
            # Focus on revenue-related fields for demo
            if any(term in str(row['Original_Field_Name']).lower() for term in 
                   ['north america', 'germany', 'china', 'japan', 'total', 'materials', 'communications']):
                source_fields.append({
                    'source_id': f"SRC_{idx+1}",
                    'row_number': row['Row_Number'],
                    'original_field_name': row['Original_Field_Name'],
                    'section_context': row['Section_Context'] if pd.notna(row['Section_Context']) else '',
                    'enhanced_scoped_name': row['Enhanced_Scoped_Name'],
                    'q1_2024_value': row['Q1_2024_Value'] if pd.notna(row['Q1_2024_Value']) else None,
                    'q2_2024_value': row['Q2_2024_Value'] if pd.notna(row['Q2_2024_Value']) else None,
                    'is_percentage': row['Is_Percentage_Section'] if 'Is_Percentage_Section' in row else False
                })
    
    # Load destination fields (focus on segment information)
    dest_file = "/Users/michaelkim/code/Bernstein/reported_tab_comprehensive_mapping.csv"
    dest_fields = []
    
    if Path(dest_file).exists():
        dest_df = pd.read_csv(dest_file)
        for idx, row in dest_df.iterrows():
            # Focus on segment/geographic fields for demo
            if any(term in str(row['Original_Field_Name']).lower() for term in 
                   ['north america', 'germany', 'china', 'japan', 'total', 'materials', 'communications']):
                dest_fields.append({
                    'dest_id': f"DEST_{idx+1}",
                    'row_number': row['Row_Number'],
                    'original_field_name': row['Original_Field_Name'],
                    'section_context': row['Section_Context'] if pd.notna(row['Section_Context']) else '',
                    'enhanced_scoped_name': row['Enhanced_Scoped_Name']
                })
    
    print(f"Demo dataset: {len(source_fields)} source fields, {len(dest_fields)} destination fields")
    return source_fields, dest_fields


def generate_gemini_prompt_demo(source_fields: List[Dict], dest_fields: List[Dict]) -> str:
    """Generate the prompt that would be sent to Gemini."""
    
    prompt = """You are an expert financial data analyst. I need you to match source fields to destination fields based on their semantic meaning and hierarchical context.

TASK: Match each destination field to the most appropriate source field. Return ONLY a CSV with the matched pairs.

IMPORTANT RULES:
1. Each source field should map to AT MOST ONE destination field (one-to-one mapping)
2. Pay attention to percentage vs absolute value contexts:
   - "Revenue by region" (absolute values) should match "Region breakdown" 
   - "Revenue by region (% of total)" (percentages) should match "Region mix (%)"
   - "Revenue by application" should match "End market breakdown"
   - "Revenue by product" should match "Segment breakdown"
3. Geographic terms should match: "North America" ↔ "United States and other North America"
4. Only return matches where you are confident (>70% confidence)
5. Return CSV format with headers: source_id,dest_id,confidence_score,match_reason

SOURCE FIELDS (with enhanced scoping):
"""
    
    for field in source_fields:
        prompt += f"{field['source_id']}: {field['original_field_name']} | Section: {field['section_context']} | Scope: {field['enhanced_scoped_name']} | Is_Percentage: {field['is_percentage']}\n"
    
    prompt += "\nDESTINATION FIELDS (with enhanced scoping):\n"
    
    for field in dest_fields:
        prompt += f"{field['dest_id']}: {field['original_field_name']} | Section: {field['section_context']} | Scope: {field['enhanced_scoped_name']}\n"
    
    prompt += """
RETURN ONLY CSV FORMAT:
source_id,dest_id,confidence_score,match_reason

Example:
SRC_6,DEST_12,0.95,North America revenue absolute values match
SRC_16,DEST_48,0.90,North America revenue percentage values match
"""
    
    return prompt


def simulate_intelligent_matching(source_fields: List[Dict], dest_fields: List[Dict]) -> List[Dict]:
    """
    Simulate what Gemini would likely return for intelligent matching.
    This demonstrates the expected output format and logic.
    """
    print("Simulating intelligent Gemini matching...")
    
    simulated_matches = [
        # Geographic absolute values (Revenue by region → Region breakdown)
        {'source_id': 'SRC_6', 'dest_id': 'DEST_12', 'confidence_score': 0.95, 'match_reason': 'North America revenue absolute values match'},
        {'source_id': 'SRC_7', 'dest_id': 'DEST_13', 'confidence_score': 0.98, 'match_reason': 'Germany revenue absolute values match'},
        {'source_id': 'SRC_9', 'dest_id': 'DEST_15', 'confidence_score': 0.98, 'match_reason': 'China revenue absolute values match'},
        {'source_id': 'SRC_10', 'dest_id': 'DEST_16', 'confidence_score': 0.98, 'match_reason': 'Japan revenue absolute values match'},
        
        # Geographic percentage values (Revenue by region % → Region mix %)
        {'source_id': 'SRC_16', 'dest_id': 'DEST_48', 'confidence_score': 0.90, 'match_reason': 'North America revenue percentage values match'},
        {'source_id': 'SRC_17', 'dest_id': 'DEST_49', 'confidence_score': 0.92, 'match_reason': 'Germany revenue percentage values match'},
        {'source_id': 'SRC_19', 'dest_id': 'DEST_51', 'confidence_score': 0.92, 'match_reason': 'China revenue percentage values match'},
        {'source_id': 'SRC_20', 'dest_id': 'DEST_52', 'confidence_score': 0.92, 'match_reason': 'Japan revenue percentage values match'},
        
        # Application breakdown (Revenue by application → End market breakdown)
        {'source_id': 'SRC_26', 'dest_id': 'DEST_22', 'confidence_score': 0.95, 'match_reason': 'Materials Processing application absolute match'},
        {'source_id': 'SRC_29', 'dest_id': 'DEST_25', 'confidence_score': 0.98, 'match_reason': 'Communications application absolute match'},
        {'source_id': 'SRC_30', 'dest_id': 'DEST_26', 'confidence_score': 0.98, 'match_reason': 'Medical application absolute match'},
        
        # Product breakdown (Revenue by product → Segment breakdown)  
        {'source_id': 'SRC_46', 'dest_id': 'DEST_30', 'confidence_score': 0.98, 'match_reason': 'High-power CW lasers product match'},
        {'source_id': 'SRC_47', 'dest_id': 'DEST_31', 'confidence_score': 0.98, 'match_reason': 'Medium-power CW lasers product match'},
        {'source_id': 'SRC_48', 'dest_id': 'DEST_32', 'confidence_score': 0.98, 'match_reason': 'Pulsed lasers product match'},
        {'source_id': 'SRC_49', 'dest_id': 'DEST_33', 'confidence_score': 0.98, 'match_reason': 'QCW lasers product match'},
    ]
    
    return simulated_matches


def main():
    """Main entry point."""
    output_file = "/Users/michaelkim/code/Bernstein/gemini_demo_results.csv"
    
    print("="*80)
    print("GEMINI 2.5 PRO FIELD MATCHING DEMO")
    print("="*80)
    print("Demonstrating intelligent AI-based field matching")
    print(f"Output file: {output_file}")
    
    try:
        # Load fields
        source_fields, dest_fields = load_fields_for_gemini_demo()
        
        if not source_fields or not dest_fields:
            print("ERROR: Could not load field mappings")
            return
        
        # Generate the prompt that would be sent to Gemini
        prompt = generate_gemini_prompt_demo(source_fields, dest_fields)
        
        # Save prompt to file for review
        prompt_file = "/Users/michaelkim/code/Bernstein/gemini_prompt.txt"
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        print(f"Gemini prompt saved to: {prompt_file}")
        print(f"Prompt length: {len(prompt)} characters")
        
        # Simulate intelligent matching
        simulated_matches = simulate_intelligent_matching(source_fields, dest_fields)
        
        # Show the simulated matches directly
        print(f"\nSimulated Gemini Matches:")
        for match in simulated_matches:
            print(f"  {match['source_id']} → {match['dest_id']} (Score: {match['confidence_score']:.2f})")
            print(f"    Reason: {match['match_reason']}")
        
        # Create simple demo results
        enriched_matches = simulated_matches
        
        # Save demo results (simplified)
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['source_id', 'dest_id', 'confidence_score', 'match_reason'])
            writer.writeheader()
            writer.writerows(simulated_matches)
        
        print(f"\nDemo completed successfully!")
        
        print(f"\nDemo results saved to: {output_file}")
        print(f"Gemini prompt saved to: {prompt_file}")
        print("\nTo use with real Gemini API:")
        print("1. Set L2M2_API_TOKEN environment variable")
        print("2. Run: python3 gemini_field_matching.py")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
