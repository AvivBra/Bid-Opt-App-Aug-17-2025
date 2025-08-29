"""Optimization configuration settings."""

from typing import Dict, List, Any, Optional
import pandas as pd


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
    "Winter Clothing / Flat 15",
    "Flat 10",
    "Flat 20 | Winter Clothing",
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

# Bids 30 Days optimization settings (ENABLED NOW!)
BIDS_30_DAYS_CONFIG = {
    "name": "Bids 30 Days",
    "enabled": True,  # CHANGED TO True - NOW ACTIVE!
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

# Bids 60 Days optimization settings
BIDS_60_DAYS_CONFIG = {
    "name": "Bids 60 Days",
    "enabled": True,
    "description": "Optimize bids for products with sales in last 60 days",
    # Filtering criteria
    "filters": {
        "units_min": 0,  # units > 0
        "state": "enabled",
        "exclude_portfolios": EXCLUDED_PORTFOLIOS,
        "exclude_ignore": True,  # Exclude portfolios with Base Bid = 'Ignore'
        "exclude_delete_for_60": True,  # Exclude IDs from Delete for 60 sheet
    },
    # Calculation thresholds
    "thresholds": {
        "calc2_threshold": 1.1,
        "conversion_rate_threshold": 0.08,  # 8%
        "units_for_max_bid": 3,
        "min_bid": 0.02,
        "max_bid": 1.25,  # Different from Zero Sales (4.00)
    },
    # Max Bid values based on units
    "max_bid_values": {
        "low_units": 0.8,   # When units < 3
        "high_units": 1.25, # When units >= 3
    },
    # Multipliers
    "multipliers": {
        "up_and": 0.5,  # When campaign contains "up and"
        "old_bid": 1.1, # For Old Bid * 1.1 calculation
    },
    # Entity types (same as Zero Sales and 30 Days)
    "target_entities": ["Keyword", "Product Targeting"],
    "separate_entities": ["Bidding Adjustment", "Product Ad"],
    # Required columns for validation
    "required_columns": [
        "Entity",
        "Units",
        "Bid", 
        "State",
        "Campaign ID",
    ],
    # Helper columns configuration (10 columns)
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
            "Temp Bid",
            "Max_Bid",
            "calc3"
        ],
        "insert_position": "before_bid",  # Insert before Bid column
    },
    # Output sheets
    "output_sheets": [
        "Targeting",         # 58 columns (48 original + 10 helper)
        "Bidding Adjustment", # 48 columns (original only)
        "For Harvesting",    # 58 columns (NULL Target CPA rows)
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

# Empty Portfolios optimization settings
EMPTY_PORTFOLIOS_CONFIG = {
    "name": "Empty Portfolios",
    "enabled": True,
    "description": "Optimize empty portfolios by assigning numeric names for easy identification",
    # Required sheets for validation
    "required_sheets": [
        "Sponsored Products Campaigns",
        "Portfolios"
    ],
    # Required columns for validation (from constants.py)
    "required_columns": [
        "Campaign ID", "Campaign", "Campaign Name (Informational only)",
        "Portfolio ID", "Portfolio Name (Informational only)",
        "Campaign State", "Campaign State (Informational only)",
        "Campaign Daily Budget", "Campaign Start Date", "Campaign End Date",
        "Campaign Targeting Type", "Ad Group ID", "Ad Group",
        "Ad Group Name (Informational only)", "Ad Group State (Informational only)",
        "Ad Group Default Bid", "Ad Group Default Bid (Informational only)",
        "Bid Adjustment", "Placement Type", "Increase bids by placement",
        "Entity", "Operation", "Keyword ID", "Keyword Text",
        "Product Targeting ID", "Product Targeting Expression", "Match Type",
        "State", "Bid", "Keyword Bid (Informational only)",
        "Campaign ID (Read only)", "Ad Group ID (Read only)",
        "Keyword ID (Read only)", "Product Targeting ID (Read only)",
        "Impressions", "Clicks", "Spend", "Sales", "Orders", "Units",
        "Conversion Rate", "ACOS", "CPC", "ROAS", "Bidding Strategy",
        "Campaign Budget Type", "Product Ad ID", "SKU"
    ],
    # Entity types to process
    "target_entities": ["Campaign"],
    # Processing configuration
    "processing": {
        "filter_entity": "Campaign",
        "update_operation": "update",
        "highlight_color": "FFFF00"  # Yellow
    },
    # No helper columns for Empty Portfolios
    "helper_columns": {
        "enabled": False,
        "columns": []
    },
    # Output sheets
    "output_sheets": [
        "Sponsored Products Campaigns",
        "Portfolios",
        "Summary"
    ]
}

# Campaigns without Portfolios optimization settings
CAMPAIGNS_WITHOUT_PORTFOLIOS_CONFIG = {
    "name": "Campaigns w/o Portfolios",
    "enabled": True,
    "description": "Update campaigns without portfolios to assign them to a specific portfolio (84453417629173)",
    # Required sheets for validation
    "required_sheets": [
        "Sponsored Products Campaigns"
    ],
    # Required columns for validation
    "required_columns": [
        "Entity", "Portfolio ID", "Operation", "Campaign ID"
    ],
    # Entity types to process
    "target_entities": ["Campaign"],
    # Processing configuration
    "processing": {
        "filter_entity": "Campaign", 
        "update_operation": "update",
        "target_portfolio_id": "84453417629173",
        "highlight_color": "FFFF00"  # Yellow
    },
    # No helper columns for Campaigns without Portfolios
    "helper_columns": {
        "enabled": False,
        "columns": []
    },
    # Output sheets
    "output_sheets": [
        "Sponsored Products Campaigns",
        "Summary"
    ]
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
    BIDS_60_DAYS_CONFIG,  # Added Bids 60 Days
    EMPTY_PORTFOLIOS_CONFIG,  # Added Empty Portfolios
    CAMPAIGNS_WITHOUT_PORTFOLIOS_CONFIG,  # Added Campaigns without Portfolios
    *FUTURE_OPTIMIZATIONS.values(),
]

# ============================================================================
# EXCEL FORMATTING CONFIGURATION - GLOBAL SETTINGS
# ============================================================================

# Columns that should ALWAYS be formatted as text to prevent scientific notation
TEXT_FORMAT_COLUMNS = [
    "Campaign ID",
    "Ad Group ID",
    "Portfolio ID",
    "Keyword ID",
    "Product Targeting ID",
    "Campaign Id",
    "Ad Group Id",
    "Portfolio Id",
    "Keyword Id",
    "Product Targeting Id",
    "ASIN",
    "SKU",
    "Item ID",
    "Order ID",
    "Customer ID",
    "Transaction ID",
]

# The main Bid column - helper columns will be inserted BEFORE this
BID_COLUMN_NAME = "Bid"

# Standard row height for all rows (in Excel points)
STANDARD_ROW_HEIGHT = 15

# Column width settings - ALL columns will have same width
COLUMN_WIDTH_SETTINGS = {
    "standard_width": 15,  # All columns will be this width
    "min_width": 8,
    "max_width": 50,
    "use_uniform_width": True,  # Set to True to make all columns same width
}

# Excel formatting configuration
EXCEL_FORMATTING = {
    "error_color": "FFE4E1",  # Light pink for errors
    "header_color": "E0E0E0",  # Light gray for headers
    "blue_header_color": "87CEEB",  # Light blue for participating columns
    "max_sheet_name_length": 31,
    "freeze_header": True,
    "auto_column_width": False,  # Changed to False - use uniform width
    "number_format": {
        "bid": "0.000",  # 3 decimal places
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
    "single_optimization_only": True,  # Only one optimization at a time
}

# ============================================================================
# EXCEL FORMATTING FUNCTIONS - DO NOT MODIFY FOR NEW OPTIMIZATIONS
# ============================================================================


def apply_text_format_before_write(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert ID columns to string format before writing to Excel.
    This prevents Excel from converting long numbers to scientific notation.

    ALWAYS call this function before writing DataFrame to Excel!

    Args:
        df: DataFrame to process

    Returns:
        DataFrame with ID columns converted to strings
    """
    df_copy = df.copy()

    for col in df_copy.columns:
        if should_format_as_text(col):
            # Convert to string and preserve all digits
            if col in df_copy.columns:
                # Handle NaN values
                mask = df_copy[col].notna()

                # Convert to string, removing decimal points for integers
                def safe_convert_to_string(x):
                    try:
                        if pd.isna(x):
                            return ""
                        elif hasattr(x, '__iter__') and not isinstance(x, str):
                            # Handle array/list data - convert to string representation
                            return str(x)
                        elif isinstance(x, (int, float)) and not isinstance(x, bool):
                            if x == int(x):
                                return str(int(x))
                            else:
                                return str(x)
                        else:
                            return str(x)
                    except (ValueError, TypeError, OverflowError):
                        return str(x)
                
                # Use .loc with proper boolean indexing to avoid the warning
                if mask.any():
                    df_copy.loc[mask, col] = df_copy.loc[mask, col].apply(safe_convert_to_string)

    return df_copy


def should_format_as_text(column_name: str) -> bool:
    """
    Check if column should be formatted as text.

    Args:
        column_name: Name of the column

    Returns:
        True if column should be text formatted
    """
    # Check explicit list
    if column_name in TEXT_FORMAT_COLUMNS:
        return True

    # Check patterns
    patterns = ["ID", "Id", "ASIN", "SKU", "Code", "Number"]
    return any(pattern in column_name for pattern in patterns)


def get_helper_column_position(original_columns: List[str]) -> int:
    """
    Get the position where helper columns should be inserted.
    Helper columns ALWAYS go immediately BEFORE the Bid column.

    Args:
        original_columns: List of original column names

    Returns:
        Index position for helper column insertion
    """
    try:
        # Find Bid column position
        bid_index = original_columns.index(BID_COLUMN_NAME)
        return bid_index  # Insert before Bid
    except ValueError:
        # If Bid not found, try alternative names
        for alt_name in ["Max CPC", "Max Bid", "Default Bid"]:
            try:
                return original_columns.index(alt_name)
            except ValueError:
                continue
        # Default to position 10 if no bid column found
        return 10


def arrange_columns_with_helpers(
    df: pd.DataFrame, original_columns: List[str], helper_columns: List[str]
) -> pd.DataFrame:
    """
    Arrange DataFrame columns with helper columns in correct position.
    Helper columns will be placed immediately BEFORE the Bid column.

    Args:
        df: DataFrame to arrange
        original_columns: List of original column names
        helper_columns: List of helper column names

    Returns:
        DataFrame with columns in correct order
    """
    # Get position for helper columns
    insert_position = get_helper_column_position(original_columns)

    # Split original columns
    before_bid = original_columns[:insert_position]
    from_bid_onwards = original_columns[insert_position:]

    # Build final column order
    final_order = before_bid + helper_columns + from_bid_onwards

    # Ensure all columns exist in DataFrame
    for col in final_order:
        if col not in df.columns:
            df[col] = ""

    # Return with correct column order
    return df[final_order]


def apply_uniform_column_widths(worksheet, column_count: int):
    """
    Apply uniform width to all columns in worksheet.

    Args:
        worksheet: Openpyxl worksheet object
        column_count: Number of columns
    """
    from openpyxl.utils import get_column_letter

    if COLUMN_WIDTH_SETTINGS["use_uniform_width"]:
        width = COLUMN_WIDTH_SETTINGS["standard_width"]
        for col_idx in range(1, column_count + 1):
            col_letter = get_column_letter(col_idx)
            worksheet.column_dimensions[col_letter].width = width


def apply_standard_row_heights(worksheet, row_count: int):
    """
    Apply standard height to all rows.

    Args:
        worksheet: Openpyxl worksheet object
        row_count: Number of rows (excluding header)
    """
    for row_idx in range(1, row_count + 2):  # +2 for header and 1-based index
        worksheet.row_dimensions[row_idx].height = STANDARD_ROW_HEIGHT


# ============================================================================
# ORIGINAL HELPER FUNCTIONS
# ============================================================================


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
        
    if optimization_name.lower() == "bids 60 days":
        return BIDS_60_DAYS_CONFIG
        
    if optimization_name.lower() == "empty portfolios":
        return EMPTY_PORTFOLIOS_CONFIG
        
    if optimization_name.lower() == "campaigns w/o portfolios":
        return CAMPAIGNS_WITHOUT_PORTFOLIOS_CONFIG

    # Check future optimizations
    for config in FUTURE_OPTIMIZATIONS.values():
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
        
    if BIDS_60_DAYS_CONFIG["enabled"]:
        enabled.append(BIDS_60_DAYS_CONFIG)
        
    if EMPTY_PORTFOLIOS_CONFIG["enabled"]:
        enabled.append(EMPTY_PORTFOLIOS_CONFIG)
        
    if CAMPAIGNS_WITHOUT_PORTFOLIOS_CONFIG["enabled"]:
        enabled.append(CAMPAIGNS_WITHOUT_PORTFOLIOS_CONFIG)

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
        
    if optimization_name.lower() == "bids 60 days":
        config = BIDS_60_DAYS_CONFIG
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
