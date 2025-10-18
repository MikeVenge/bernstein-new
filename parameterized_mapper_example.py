#!/usr/bin/env python3
"""
Parameterized Mapper Usage Example

Demonstrates how to use the parameterized field mapper with different parameters.

Author: AI Assistant
Date: October 2025
"""

from parameterized_field_mapper import ParameterizedFieldMapper
import sys


def example_usage_current_project():
    """Example usage with current project files."""
    
    print("="*80)
    print("EXAMPLE 1: CURRENT PROJECT MAPPING")
    print("="*80)
    
    # Current project parameters
    mapper = ParameterizedFieldMapper(
        source_file="IPGP-Financial-Data-Workbook-2024-Q2.xlsx",
        destination_file="20240725_IPGP.US-IPG Photonics.xlsx",
        mapping_file="CONSOLIDATED_FIELD_MAPPINGS.csv",
        target_column=71,  # Column BS
        output_file="EXAMPLE_POPULATED_IPGP.xlsx",
        audit_file="EXAMPLE_AUDIT_TRAIL.csv"
    )
    
    success = mapper.run()
    return success


def example_usage_different_column():
    """Example usage with different target column."""
    
    print("\n" + "="*80)
    print("EXAMPLE 2: DIFFERENT TARGET COLUMN")
    print("="*80)
    
    # Same files but different target column (e.g., Column BU = 73)
    mapper = ParameterizedFieldMapper(
        source_file="IPGP-Financial-Data-Workbook-2024-Q2.xlsx",
        destination_file="20240725_IPGP.US-IPG Photonics.xlsx",
        mapping_file="CONSOLIDATED_FIELD_MAPPINGS.csv",
        target_column=73,  # Column BU (source tracking would go to BV = 74)
        output_file="EXAMPLE_COLUMN_73_POPULATED_IPGP.xlsx",
        audit_file="EXAMPLE_COLUMN_73_AUDIT_TRAIL.csv"
    )
    
    # Just show the setup, don't actually run to avoid overwriting
    print("Setup complete - would populate Column BU (73) with source tracking in Column BV (74)")
    print("Parameters:")
    print(f"  Target column: {mapper.target_column}")
    print(f"  Source tracking column: {mapper.source_tracking_column}")
    print(f"  Output file: {mapper.output_file}")
    print(f"  Audit file: {mapper.audit_file}")
    
    return True


def show_usage_help():
    """Show usage help and examples."""
    
    print("="*80)
    print("PARAMETERIZED FIELD MAPPER USAGE")
    print("="*80)
    
    print("COMMAND LINE USAGE:")
    print("python parameterized_field_mapper.py --source SOURCE_FILE --destination DEST_FILE")
    print("                                     --mapping MAPPING_FILE --column COLUMN_NUMBER")
    print("                                     [--output OUTPUT_FILE] [--audit AUDIT_FILE]")
    
    print("\nPARAMETERS:")
    print("  --source, -s    : Path to source Excel file")
    print("  --destination, -d : Path to destination Excel file")
    print("  --mapping, -m   : Path to CSV mapping file")
    print("  --column, -c    : Target column number to populate (1-based)")
    print("  --output, -o    : Optional output file path")
    print("  --audit, -a     : Optional audit trail file path")
    
    print("\nEXAMPLES:")
    print("1. Current project:")
    print("   python parameterized_field_mapper.py \\")
    print("     --source 'IPGP-Financial-Data-Workbook-2024-Q2.xlsx' \\")
    print("     --destination '20240725_IPGP.US-IPG Photonics.xlsx' \\")
    print("     --mapping 'CONSOLIDATED_FIELD_MAPPINGS.csv' \\")
    print("     --column 71")
    
    print("\n2. Different target column:")
    print("   python parameterized_field_mapper.py \\")
    print("     --source 'IPGP-Financial-Data-Workbook-2024-Q2.xlsx' \\")
    print("     --destination '20240725_IPGP.US-IPG Photonics.xlsx' \\")
    print("     --mapping 'CONSOLIDATED_FIELD_MAPPINGS.csv' \\")
    print("     --column 75 \\")
    print("     --output 'custom_output.xlsx'")
    
    print("\n3. Different files:")
    print("   python parameterized_field_mapper.py \\")
    print("     --source 'new_source.xlsx' \\")
    print("     --destination 'new_destination.xlsx' \\")
    print("     --mapping 'custom_mappings.csv' \\")
    print("     --column 50")
    
    print("\nCOLUMN REFERENCE:")
    print("  Column 70 = BR (Q1 data)")
    print("  Column 71 = BS (Q2 data - our current target)")
    print("  Column 72 = BT (Source tracking - auto-assigned)")
    print("  Column 73 = BU")
    print("  Column 74 = BV")
    print("  etc.")


def main():
    """Main entry point for usage examples."""
    
    if len(sys.argv) > 1 and sys.argv[1] == '--help-examples':
        show_usage_help()
        return
    
    print("PARAMETERIZED FIELD MAPPER - USAGE EXAMPLES")
    print("Run with --help-examples for detailed usage information")
    
    try:
        # Run example 1
        success1 = example_usage_current_project()
        
        if success1:
            # Show example 2 setup (don't run to avoid conflicts)
            example_usage_different_column()
            
            print(f"\n" + "="*80)
            print("EXAMPLES COMPLETE")
            print("="*80)
            print("✅ Example 1: Current project mapping completed successfully")
            print("✅ Example 2: Different column setup demonstrated")
            print("\nThe parameterized mapper is ready for use with any combination of:")
            print("  - Source files")
            print("  - Destination files") 
            print("  - Mapping files")
            print("  - Target columns")
        
    except Exception as e:
        print(f"ERROR in examples: {e}")


if __name__ == "__main__":
    main()
