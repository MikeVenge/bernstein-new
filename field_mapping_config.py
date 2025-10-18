#!/usr/bin/env python3
"""
Field Mapping Configuration

This file contains the semantic mappings between source and destination terminology
to handle cases where the same concept is called by different names.

Author: AI Assistant
Date: October 2025
"""

from typing import Dict
from difflib import SequenceMatcher
import pandas as pd

# Section/Category Mappings
# Maps source section names to destination section names
SECTION_MAPPINGS = {
    # Revenue breakdowns
    "revenue by application": "end market breakdown",
    "revenue by product": "segment breakdown", 
    "revenue by region": "region breakdown",
    "revenue by region (% of total)": "region mix (%)",
    "revenue by application (% of total)": "end market mix (%)",
    "revenue by product (% of total)": "segment mix (%)",
    
    # Financial statements
    "key metrics": "segment information",
    "income statement": "consolidated income statement",
    "balance sheet": "consolidated balance sheet", 
    "cash flows": "consolidated cash flow statement",
    
    # Asset categories
    "long-lived assets by region": "property, plant, and equipment",
    "employees by region": "employees",
    "employees by function": "employees",
    
    # Other categories
    "total backlog of orders": "backlog",
    "revenue from five largest customers": "supplement information"
}

# Field Name Mappings
# Maps source field names to destination field names when they differ
FIELD_NAME_MAPPINGS = {
    # Geographic regions
    "north america": "united states and other north america",
    "other europe": "other including eastern europe/cis", 
    "other asia": "other asian countries",
    
    # Financial metrics
    "net sales": "net sales",
    "operating income (loss)": "operating income",
    "income (loss) before provision for income taxes": "income before provision for income taxes",
    "net income (loss)": "net income",
    
    # Product categories
    "materials processing": "materials processing",
    "other applications": "other application, of which",
    "advanced applications": "advanced applications",
    "communications": "communications", 
    "medical": "medical",
    
    # Laser types
    "high-power cw lasers (1 kilowatt or greater)": "high-power cw lasers (1 kilowatt or greater)",
    "medium-power cw lasers (less than 1 kilowatt)": "medium-power cw lasers (less than 1 kilowatt)",
    "pulsed lasers": "pulsed lasers",
    "qcw lasers": "qcw lasers",
    "laser and non-laser systems": "systems",
    
    # Balance sheet items
    "cash and cash equivalents": "cash and cash equivalents",
    "accounts receivable, net": "accounts receivable, net",
    "inventories": "inventories",
    "total assets": "total assets",
    "total liabilities": "total liabilities",
    
    # Cash flow items
    "depreciation and amortization": "depreciation and amortization",
    "stock-based compensation": "stock-based compensation",
    "deferred income taxes": "deferred income taxes",
    
    # Employee categories
    "research and development": "r&d",
    "manufacturing operations": "manufacturing operations", 
    "sales, service and marketing": "sales, service and marketing",
    "general and administrative": "general and administraative"  # Note: typo in destination
}

# Value Type Mappings
# Helps distinguish between absolute values and percentages
VALUE_TYPE_MAPPINGS = {
    "absolute": {
        "revenue by region": "segment information",
        "revenue by application": "end market breakdown", 
        "revenue by product": "segment breakdown"
    },
    "percentage": {
        "revenue by region (% of total)": "region mix (%)",
        "revenue by application (% of total)": "end market mix (%)",
        "revenue by product (% of total)": "segment mix (%)"
    }
}

# Scoping Translation Rules
# Maps source scoping patterns to destination scoping patterns
SCOPING_TRANSLATIONS = {
    # Revenue patterns
    "revenue_statement.geographic_breakdown": "financial_statements.geographic_data",
    "revenue_statement.geographic_breakdown_percent": "segment_information.region_mix",
    "revenue_statement.application_breakdown": "segment_information.end_market_breakdown",
    "revenue_statement.application_breakdown_percent": "segment_information.end_market_mix", 
    "revenue_statement.product_breakdown": "segment_information.segment_breakdown",
    "revenue_statement.product_breakdown_percent": "segment_information.segment_mix",
    
    # Financial statement patterns
    "income_statement.revenue": "consolidated_income_statement",
    "income_statement.expenses": "consolidated_income_statement",
    "income_statement.profitability": "consolidated_income_statement",
    "balance_sheet.assets": "consolidated_balance_sheet",
    "balance_sheet.liabilities": "consolidated_balance_sheet",
    "balance_sheet.equity": "consolidated_balance_sheet",
    "cashflow_statement.operating_activities": "cash_flows_from_operating_activities",
    "cashflow_statement.investing_activities": "cash_flows_from_investing_activities", 
    "cashflow_statement.financing_activities": "cash_flows_from_financing_activities",
    
    # Operations patterns
    "operations.employee_distribution": "employees",
    "operations.employee_metrics": "employees",
    "operations.customer_metrics": "supplement_information"
}


def normalize_section_name(section_name) -> str:
    """
    Normalize section names using the mapping configuration.
    """
    if not section_name or pd.isna(section_name):
        return ""
    
    normalized = str(section_name).lower().strip()
    
    # Apply section mappings
    if normalized in SECTION_MAPPINGS:
        return SECTION_MAPPINGS[normalized]
    
    return normalized


def normalize_field_name(field_name) -> str:
    """
    Normalize field names using the mapping configuration.
    """
    if not field_name or pd.isna(field_name):
        return ""
    
    normalized = str(field_name).lower().strip()
    
    # Apply field name mappings
    if normalized in FIELD_NAME_MAPPINGS:
        return FIELD_NAME_MAPPINGS[normalized]
    
    return normalized


def translate_scoping_pattern(source_scope: str) -> str:
    """
    Translate source scoping pattern to destination scoping pattern.
    """
    if not source_scope:
        return ""
    
    scope_lower = source_scope.lower()
    
    # Try each translation pattern
    for source_pattern, dest_pattern in SCOPING_TRANSLATIONS.items():
        if source_pattern in scope_lower:
            return scope_lower.replace(source_pattern, dest_pattern)
    
    return scope_lower


def get_semantic_equivalence_score(source_field: Dict, dest_field: Dict) -> float:
    """
    Calculate semantic equivalence score using configuration mappings.
    """
    source_name = str(source_field['original_field_name']).lower()
    dest_name = str(dest_field['original_field_name']).lower()
    source_scope = str(source_field['enhanced_scoped_name']).lower()
    dest_scope = str(dest_field['enhanced_scoped_name']).lower()
    
    score = 0.0
    
    # Field name equivalence (highest priority)
    normalized_source = normalize_field_name(source_name)
    normalized_dest = normalize_field_name(dest_name)
    
    if normalized_source == normalized_dest:
        score += 0.5  # Exact normalized match
    else:
        # String similarity on normalized names
        similarity = SequenceMatcher(None, normalized_source, normalized_dest).ratio()
        score += similarity * 0.4
    
    # Section context equivalence
    source_section_raw = source_field.get('section_context', '')
    dest_section_raw = dest_field.get('section_context', '')
    
    source_section = str(source_section_raw).lower() if source_section_raw and not pd.isna(source_section_raw) else ''
    dest_section = str(dest_section_raw).lower() if dest_section_raw and not pd.isna(dest_section_raw) else ''
    
    normalized_source_section = normalize_section_name(source_section)
    normalized_dest_section = normalize_section_name(dest_section)
    
    if normalized_source_section == normalized_dest_section:
        score += 0.3
    
    # Scoping pattern equivalence
    translated_source_scope = translate_scoping_pattern(source_scope)
    if translated_source_scope in dest_scope or dest_scope in translated_source_scope:
        score += 0.2
    
    return min(score, 1.0)


# Export the main functions for use in other scripts
__all__ = [
    'SECTION_MAPPINGS',
    'FIELD_NAME_MAPPINGS', 
    'VALUE_TYPE_MAPPINGS',
    'SCOPING_TRANSLATIONS',
    'normalize_section_name',
    'normalize_field_name',
    'translate_scoping_pattern',
    'get_semantic_equivalence_score'
]
