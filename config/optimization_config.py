"""Optimization configuration settings."""

from typing import Dict, List, Any


# Bid value constraints
BID_CONSTRAINTS = {
    'min_bid': 0.02,
    'max_bid': 4.00,
    'precision': 2  # Decimal places
}

# Portfolio exclusions
EXCLUDED_PORTFOLIOS = [
    "Flat 30",
    "Flat 25",
    "Flat 40",
    "Flat 25 | Opt",
    "Flat 30 | Opt",
    "Flat 20",
    "Flat 15",
    "Flat 40 | Opt",
    "Flat 20 | Opt",
    "Flat 15 | Opt"
]

# Zero Sales optimization settings
ZERO_SALES_CONFIG = {
    'name': 'Zero Sales',
    'enabled': True,
    'description': 'Optimize bids for products with zero sales',
    
    # Calculation multipliers
    'multipliers': {
        'with_up_and': 1.25,      # Case A and C
        'without_up_and': 1.5      # Case B and D
    },
    
    # Entity types to process
    'target_entities': [
        'Keyword',
        'Product Targeting'
    ],
    
    # Entity types for separate sheets (no helper columns)
    'separate_entities': [
        'Bidding Adjustment',
        'Product Ad'
    ],
    
    # Required columns for validation
    'required_columns': [
        'Entity',
        'Portfolio Name (Informational only)',
        'Units',
        'Bid',
        'Operation'
    ],
    
    # Optional but recommended columns
    'recommended_columns': [
        'Clicks',
        'Campaign Name',
        'Ad Group Name',
        'Keyword Text',
        'Product Targeting Expression'
    ],
    
    # Helper columns configuration
    'helper_columns': {
        'enabled': True,
        'columns': [
            'Old Bid',
            'calc1',
            'calc2', 
            'Target CPA',
            'Base Bid',
            'Adj. CPA',
            'Max BA'
        ],
        'insert_position': 'before_bid'  # Insert before Bid column
    }
}

# Future optimizations (TBC - To Be Configured)
FUTURE_OPTIMIZATIONS = {
    'portfolio_bid': {
        'name': 'Portfolio Bid Optimization',
        'enabled': False,
        'description': 'TBC - Coming in Phase 2'
    },
    'budget_optimization': {
        'name': 'Budget Optimization',
        'enabled': False,
        'description': 'TBC - Coming in Phase 2'
    },
    'keyword_optimization': {
        'name': 'Keyword Optimization',
        'enabled': False,
        'description': 'TBC - Coming in Phase 2'
    },
    'asin_targeting': {
        'name': 'ASIN Targeting',
        'enabled': False,
        'description': 'TBC - Coming in Phase 2'
    },
    'dayparting': {
        'name': 'Dayparting',
        'enabled': False,
        'description': 'TBC - Coming in Phase 3'
    },
    'placement_optimization': {
        'name': 'Placement Optimization',
        'enabled': False,
        'description': 'TBC - Coming in Phase 3'
    },
    'negative_keyword': {
        'name': 'Negative Keyword',
        'enabled': False,
        'description': 'TBC - Coming in Phase 3'
    },
    'search_term': {
        'name': 'Search Term Optimization',
        'enabled': False,
        'description': 'TBC - Coming in Phase 3'
    },
    'product_attribute': {
        'name': 'Product Attribute Targeting',
        'enabled': False,
        'description': 'TBC - Coming in Phase 4'
    },
    'competitor_analysis': {
        'name': 'Competitor Analysis',
        'enabled': False,
        'description': 'TBC - Coming in Phase 4'
    },
    'seasonal_adjustment': {
        'name': 'Seasonal Adjustment',
        'enabled': False,
        'description': 'TBC - Coming in Phase 4'
    },
    'roi_optimization': {
        'name': 'ROI Optimization',
        'enabled': False,
        'description': 'TBC - Coming in Phase 4'
    },
    'multi_country': {
        'name': 'Multi-Country Optimization',
        'enabled': False,
        'description': 'TBC - Coming in Phase 5'
    }
}

# All optimizations list for UI
ALL_OPTIMIZATIONS = [
    ZERO_SALES_CONFIG,
    *FUTURE_OPTIMIZATIONS.values()
]

# Excel formatting configuration
EXCEL_FORMATTING = {
    'error_color': 'FFE4E1',  # Light pink for errors
    'header_color': 'E0E0E0',  # Light gray for headers
    'max_sheet_name_length': 31,
    'freeze_header': True,
    'auto_column_width': True,
    'number_format': {
        'bid': '0.00',
        'currency': '$#,##0.00',
        'percentage': '0.00%',
        'integer': '#,##0'
    }
}

# File naming configuration
FILE_NAMING = {
    'working_file': {
        'prefix': 'Working_File',
        'include_timestamp': True,
        'timestamp_format': '%Y%m%d_%H%M',
        'extension': '.xlsx'
    },
    'clean_file': {
        'prefix': 'Clean_File',
        'include_timestamp': True,
        'timestamp_format': '%Y%m%d_%H%M',
        'extension': '.xlsx'
    }
}

# Processing configuration
PROCESSING_CONFIG = {
    'max_rows_per_sheet': 1000000,  # Excel limit is ~1M rows
    'chunk_size': 10000,  # Process in chunks for large files
    'progress_update_interval': 1000,  # Update progress every N rows
    'error_handling': {
        'continue_on_error': True,
        'max_errors': 1000,
        'log_errors': True
    }
}

# Validation thresholds
VALIDATION_THRESHOLDS = {
    'min_portfolios': 1,
    'max_portfolios': 10000,
    'warn_many_ignored': 10,  # Warn if more than N portfolios set to "Ignore"
    'max_file_size_mb': 40,
    'max_template_size_mb': 1
}

# Column mappings for flexibility
COLUMN_MAPPINGS = {
    'portfolio': [
        'Portfolio Name (Informational only)',
        'Portfolio Name',
        'Portfolio'
    ],
    'units': [
        'Units',
        'Units Sold',
        'Conversions'
    ],
    'bid': [
        'Bid',
        'Max CPC',
        'Max Bid'
    ],
    'clicks': [
        'Clicks',
        'Click-throughs'
    ],
    'entity': [
        'Entity',
        'Record Type'
    ]
}

# UI Configuration
UI_CONFIG = {
    'show_all_optimizations': True,  # Show disabled optimizations in UI
    'disabled_message': 'Coming Soon',
    'max_file_preview_rows': 100,
    'enable_dark_mode': True,
    'sidebar_width': 200,
    'main_content_max_width': 800
}

def get_optimization_config(optimization_name: str) -> Dict[str, Any]:
    """
    Get configuration for a specific optimization.
    
    Args:
        optimization_name: Name of the optimization
        
    Returns:
        Configuration dictionary for the optimization
    """
    
    if optimization_name.lower() == 'zero sales':
        return ZERO_SALES_CONFIG
    
    # Check future optimizations
    for key, config in FUTURE_OPTIMIZATIONS.items():
        if config['name'].lower() == optimization_name.lower():
            return config
    
    return {}

def get_enabled_optimizations() -> List[Dict[str, Any]]:
    """
    Get list of currently enabled optimizations.
    
    Returns:
        List of enabled optimization configurations
    """
    
    enabled = []
    
    if ZERO_SALES_CONFIG['enabled']:
        enabled.append(ZERO_SALES_CONFIG)
    
    for config in FUTURE_OPTIMIZATIONS.values():
        if config.get('enabled', False):
            enabled.append(config)
    
    return enabled

def is_portfolio_excluded(portfolio_name: str) -> bool:
    """
    Check if a portfolio is in the exclusion list.
    
    Args:
        portfolio_name: Name of the portfolio
        
    Returns:
        True if portfolio should be excluded
    """
    
    return portfolio_name in EXCLUDED_PORTFOLIOS

def get_bid_limits() -> tuple:
    """
    Get the min and max bid limits.
    
    Returns:
        Tuple of (min_bid, max_bid)
    """
    
    return BID_CONSTRAINTS['min_bid'], BID_CONSTRAINTS['max_bid']

def validate_bid_value(bid: float) -> bool:
    """
    Check if a bid value is within valid range.
    
    Args:
        bid: Bid value to validate
        
    Returns:
        True if bid is valid
    """
    
    if pd.isna(bid):
        return False
    
    return BID_CONSTRAINTS['min_bid'] <= bid <= BID_CONSTRAINTS['max_bid']
