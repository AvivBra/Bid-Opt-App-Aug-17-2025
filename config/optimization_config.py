"""Optimization configuration settings."""

from typing import Dict, List, Any


# Bid value constraints
BID_CONSTRAINTS = {
    "min_bid": 0.02,
    "max_bid": 4.00,
    "precision": 2,  # Decimal places
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
    "Flat 15 | Opt",
]

# Zero Sales optimization settings
ZERO_SALES_CONFIG = {
    "name": "Zero Sales",
    "enabled": True,
    "description": "Optimize bids for products with zero sales",
    # Calculation multipliers
    "multipliers": {
        "with_up_and": 1.25,  # Case A and C
        "without_up_and": 1.5,  # Case B and D
    },
    # Entity types to process
    "target_entities": ["Keyword", "Product Targeting"],
    # Entity types for separate sheets (no helper columns)
    "separate_entities": ["Bidding Adjustment", "Product Ad"],
    # Required columns for validation
    "required_columns": [
        "Entity",
        "Portfolio Name (Informational only)",
        "Units",
        "Bid",
        "Operation",
    ],
    # Optional but recommended columns
    "recommended_columns": [
        "Clicks",
        "Campaign Name",
        "Ad Group Name",
        "Keyword Text",
        "Product Targeting Expression",
    ],
    # Helper columns configuration
    "helper_columns": {
        "enabled": True,
        "columns": [
            "Old Bid",
            "calc1",
            "calc2",
            "Target CPA",
            "Base Bid",
            "Adj. CPA",
            "Max BA",
        ],
        "insert_position": "before_bid",  # Insert before Bid column
    },
}

# Bids 30 Days optimization settings (NEW)
BIDS_30_DAYS_CONFIG = {
    "name": "Bids 30 Days",
    "enabled": True,  # Set to True to enable in Phase 5
    "description": "Optimize bids for products with sales in last 30 days",
    # Filtering criteria
    "filters": {
        "units_min": 1,  # units > 0
        "additional_condition": "units > 2 OR clicks > 30",
        "state": "enabled",
        "exclude_portfolios": EXCLUDED_PORTFOLIOS,
        "exclude_ignore": True,  # Exclude portfolios with Base Bid = 'Ignore'
    },
    # Calculation thresholds
    "thresholds": {
        "calc2_threshold": 1.1,
        "conversion_rate_threshold": 0.08,
        "units_for_max_bid": 3,
        "min_bid": 0.02,
        "max_bid": 1.25,  # Different from Zero Sales
    },
    # Max Bid values
    "max_bid_values": {
        "low_units": 0.8,  # When units < 3
        "high_units": 1.25,  # When units >= 3
    },
    # Multipliers
    "multipliers": {
        "up_and": 0.5,  # When campaign contains "up and"
        "old_bid": 1.1,  # For Old Bid * 1.1 calculation
    },
    # Entity types (same as Zero Sales)
    "target_entities": ["Keyword", "Product Targeting"],
    "separate_entities": ["Bidding Adjustment", "Product Ad"],
    # Required columns for validation
    "required_columns": [
        "Entity",
        "Portfolio Name (Informational only)",
        "Units",
        "Bid",
        "Clicks",
        "Campaign Name (Informational only)",
        "Campaign ID",
        "Match Type",
        "Product Targeting Expression",
        "Percentage",
        "Conversion Rate",
        "State",
        "Campaign State (Informational only)",
        "Ad Group State (Informational only)",
        "Operation",
    ],
    # Helper columns configuration (10 columns)
    "helper_columns": {
        "enabled": True,
        "columns": [
            "Max BA",
            "Base Bid",
            "Target CPA",
            "Adj. CPA",
            "Old Bid",
            "Temp Bid",
            "Max_Bid",
            "calc3",
            "calc2",
            "calc1",
        ],
        "insert_position": "custom",  # Custom positioning for Bids 30
    },
    # Output sheets
    "output_sheets": [
        "Targeting",  # 58 columns
        "Bidding Adjustment",  # 48 columns
        "For Harvesting",  # 58 columns (NULL Target CPA)
    ],
    # Highlighting configuration
    "highlighting": {
        "pink_rows": {
            "conversion_rate_low": 0.08,
            "bid_out_of_range": [0.02, 1.25],
            "calculation_errors": True,
        },
        "blue_headers": True,  # Highlight participating column headers
    },
}

# Future optimizations (TBC - To Be Configured)
FUTURE_OPTIMIZATIONS = {
    "portfolio_bid": {
        "name": "Portfolio Bid Optimization",
        "enabled": False,
        "description": "TBC - Coming in Phase 2",
    },
    "budget_optimization": {
        "name": "Budget Optimization",
        "enabled": False,
        "description": "TBC - Coming in Phase 2",
    },
    "keyword_optimization": {
        "name": "Keyword Optimization",
        "enabled": False,
        "description": "TBC - Coming in Phase 2",
    },
    "asin_targeting": {
        "name": "ASIN Targeting",
        "enabled": False,
        "description": "TBC - Coming in Phase 2",
    },
    "dayparting": {
        "name": "Dayparting",
        "enabled": False,
        "description": "TBC - Coming in Phase 3",
    },
    "placement_optimization": {
        "name": "Placement Optimization",
        "enabled": False,
        "description": "TBC - Coming in Phase 3",
    },
    "negative_keyword": {
        "name": "Negative Keyword",
        "enabled": False,
        "description": "TBC - Coming in Phase 3",
    },
    "search_term": {
        "name": "Search Term Optimization",
        "enabled": False,
        "description": "TBC - Coming in Phase 3",
    },
    "product_attribute": {
        "name": "Product Attribute Targeting",
        "enabled": False,
        "description": "TBC - Coming in Phase 4",
    },
    "competitor_analysis": {
        "name": "Competitor Analysis",
        "enabled": False,
        "description": "TBC - Coming in Phase 4",
    },
    "seasonal_adjustment": {
        "name": "Seasonal Adjustment",
        "enabled": False,
        "description": "TBC - Coming in Phase 4",
    },
    "roi_optimization": {
        "name": "ROI Optimization",
        "enabled": False,
        "description": "TBC - Coming in Phase 4",
    },
    "multi_country": {
        "name": "Multi-Country Optimization",
        "enabled": False,
        "description": "TBC - Coming in Phase 5",
    },
}

# All optimizations list for UI
ALL_OPTIMIZATIONS = [
    ZERO_SALES_CONFIG,
    BIDS_30_DAYS_CONFIG,  # Added Bids 30 Days
    *FUTURE_OPTIMIZATIONS.values(),
]

# Excel formatting configuration
EXCEL_FORMATTING = {
    "error_color": "FFE4E1",  # Light pink for errors
    "header_color": "E0E0E0",  # Light gray for headers
    "blue_header_color": "87CEEB",  # Light blue for participating columns (NEW)
    "max_sheet_name_length": 31,
    "freeze_header": True,
    "auto_column_width": True,
    "number_format": {
        "bid": "0.000",  # Changed to 3 decimal places
        "currency": "$#,##0.00",
        "percentage": "0.00%",
        "integer": "#,##0",
    },
}

# File naming configuration
FILE_NAMING = {
    "working_file": {
        "prefix": "Working_File",
        "include_timestamp": True,
        "timestamp_format": "%Y%m%d_%H%M",
        "extension": ".xlsx",
    },
    "clean_file": {
        "prefix": "Clean_File",
        "include_timestamp": True,
        "timestamp_format": "%Y%m%d_%H%M",
        "extension": ".xlsx",
    },
}

# Processing configuration
PROCESSING_CONFIG = {
    "max_rows_per_sheet": 1000000,  # Excel limit is ~1M rows
    "chunk_size": 10000,  # Process in chunks for large files
    "progress_update_interval": 1000,  # Update progress every N rows
    "error_handling": {
        "continue_on_error": True,
        "max_errors": 1000,
        "log_errors": True,
    },
}

# Validation thresholds
VALIDATION_THRESHOLDS = {
    "min_portfolios": 1,
    "max_portfolios": 10000,
    "warn_many_ignored": 10,  # Warn if more than N portfolios set to "Ignore"
    "max_file_size_mb": 40,
    "max_template_size_mb": 1,
}

# Column mappings for flexibility
COLUMN_MAPPINGS = {
    "portfolio": ["Portfolio Name (Informational only)", "Portfolio Name", "Portfolio"],
    "units": ["Units", "Units Sold", "Conversions"],
    "bid": ["Bid", "Max CPC", "Max Bid"],
    "clicks": ["Clicks", "Click-throughs"],
    "entity": ["Entity", "Record Type"],
    "conversion_rate": ["Conversion Rate", "CVR", "Conv Rate"],
    "campaign_id": ["Campaign ID", "Campaign Id"],
    "campaign_name": ["Campaign Name (Informational only)", "Campaign Name"],
    "percentage": ["Percentage", "Bid Adjustment"],
    "match_type": ["Match Type", "Matching Type"],
    "product_targeting": ["Product Targeting Expression", "Product Target"],
}

# UI Configuration
UI_CONFIG = {
    "show_all_optimizations": True,  # Show disabled optimizations in UI
    "disabled_message": "Coming Soon",
    "max_file_preview_rows": 100,
    "enable_dark_mode": True,
    "sidebar_width": 200,
    "main_content_max_width": 800,
    "single_optimization_only": True,  # Only one optimization at a time (NEW)
}


def get_optimization_config(optimization_name: str) -> Dict[str, Any]:
    """
    Get configuration for a specific optimization.

    Args:
        optimization_name: Name of the optimization

    Returns:
        Configuration dictionary for the optimization
    """

    if optimization_name.lower() == "zero sales":
        return ZERO_SALES_CONFIG

    if optimization_name.lower() == "bids 30 days":
        return BIDS_30_DAYS_CONFIG

    # Check future optimizations
    for key, config in FUTURE_OPTIMIZATIONS.items():
        if config["name"].lower() == optimization_name.lower():
            return config

    return {}


def get_enabled_optimizations() -> List[Dict[str, Any]]:
    """
    Get list of currently enabled optimizations.

    Returns:
        List of enabled optimization configurations
    """

    enabled = []

    if ZERO_SALES_CONFIG["enabled"]:
        enabled.append(ZERO_SALES_CONFIG)

    if BIDS_30_DAYS_CONFIG["enabled"]:
        enabled.append(BIDS_30_DAYS_CONFIG)

    for config in FUTURE_OPTIMIZATIONS.values():
        if config.get("enabled", False):
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


def get_bid_limits(optimization_name: str = "zero_sales") -> tuple:
    """
    Get the min and max bid limits for a specific optimization.

    Args:
        optimization_name: Name of the optimization

    Returns:
        Tuple of (min_bid, max_bid)
    """

    if optimization_name.lower() == "bids 30 days":
        config = BIDS_30_DAYS_CONFIG
        return config["thresholds"]["min_bid"], config["thresholds"]["max_bid"]

    return BID_CONSTRAINTS["min_bid"], BID_CONSTRAINTS["max_bid"]


def validate_bid_value(bid: float, optimization_name: str = "zero_sales") -> bool:
    """
    Check if a bid value is within valid range for specific optimization.

    Args:
        bid: Bid value to validate
        optimization_name: Name of the optimization

    Returns:
        True if bid is valid
    """

    import pandas as pd

    if pd.isna(bid):
        return False

    min_bid, max_bid = get_bid_limits(optimization_name)

    return min_bid <= bid <= max_bid


def get_helper_columns(optimization_name: str) -> List[str]:
    """
    Get helper columns for a specific optimization.

    Args:
        optimization_name: Name of the optimization

    Returns:
        List of helper column names
    """

    config = get_optimization_config(optimization_name)

    if config and "helper_columns" in config:
        return config["helper_columns"].get("columns", [])

    return []


def should_enable_bulk_30() -> bool:
    """
    Check if Bulk 30 button should be enabled.

    Returns:
        True if Bids 30 Days is enabled
    """

    return BIDS_30_DAYS_CONFIG.get("enabled", False)
