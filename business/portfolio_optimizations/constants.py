"""Constants for Portfolio Optimizations module."""

# Sheet names (original)
SHEET_CAMPAIGNS = "Sponsored Products Campaigns"
SHEET_PORTFOLIOS = "Portfolios"
SHEET_BRANDS = "Sponsored Brands Campaigns"

# Sheet names (after cleaning)
SHEET_CAMPAIGNS_CLEANED = "Campaigns"
SHEET_PRODUCT_AD = "Product Ad"

# Column names
COL_ENTITY = "Entity"
COL_CAMPAIGN_ID = "Campaign ID"
COL_PORTFOLIO_ID = "Portfolio ID"
COL_PORTFOLIO_NAME = "Portfolio Name"
COL_OLD_PORTFOLIO_NAME = "Old Portfolio Name"
COL_CAMP_COUNT = "Camp Count"
COL_OPERATION = "Operation"
COL_BUDGET_AMOUNT = "Budget Amount"
COL_BUDGET_START_DATE = "Budget Start Date"
COL_BUDGET_END_DATE = "Budget End Date"
COL_BUDGET_POLICY = "Budget Policy"

# Protected columns that cannot be updated
PROTECTED_COLUMNS = [
    COL_ENTITY,
    COL_CAMPAIGN_ID,
    COL_PORTFOLIO_ID
]

# Entity types
ENTITY_CAMPAIGN = "Campaign"
ENTITY_PORTFOLIO = "Portfolio"
ENTITY_PRODUCT_AD = "Product Ad"

# Operations
OPERATION_UPDATE = "update"
OPERATION_CREATE = "create"
OPERATION_DELETE = "delete"

# Default values
DEFAULT_PORTFOLIO_ID = "84453417629173"  # For campaigns without portfolios
DEFAULT_BUDGET_AMOUNT = ""
DEFAULT_BUDGET_START_DATE = ""
DEFAULT_BUDGET_END_DATE = ""
BUDGET_POLICY_NO_CAP = "No Cap"

# Excluded portfolio names
EXCLUDED_PORTFOLIO_NAMES = ["Paused", "Terminal", "Top Terminal"]

# Highlighting
HIGHLIGHT_COLOR = "FFFF00"  # Yellow for modified rows

# Limits
MAX_CELL_UPDATES = 500000
MAX_MERGE_TIME_SECONDS = 30
MAX_ROWS_PER_SHEET = 500000

# Optimization order
OPTIMIZATION_ORDER = [
    "empty_portfolios",
    "campaigns_without_portfolios"
]

# Required sheets after cleaning
REQUIRED_SHEETS_AFTER_CLEANING = [
    SHEET_PORTFOLIOS,
    SHEET_CAMPAIGNS_CLEANED,
    SHEET_PRODUCT_AD
]

# Messages
SUCCESS_MESSAGES = {
    "validation_passed": "Validation passed successfully",
    "cleaning_complete": "Data cleaning completed",
    "structure_cleaning_complete": "Data structure cleaning completed",
    "processing_complete": "Processing completed successfully",
    "merge_complete": "Results merged successfully",
    "file_created": "Output file created successfully"
}

ERROR_MESSAGES = {
    "missing_sheet": "Required sheet not found: {}",
    "missing_column": "Required column not found: {}",
    "invalid_data": "Invalid data format",
    "merge_timeout": "Merge operation timed out",
    "protected_column": "Cannot update protected column: {}",
    "optimization_failed": "Optimization failed: {}"
}