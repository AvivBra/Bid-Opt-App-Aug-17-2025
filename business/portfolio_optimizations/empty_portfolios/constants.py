"""Constants for Empty Portfolios optimization."""

# Required sheets in bulk file
REQUIRED_SHEETS = [
    "Sponsored Products Campaigns",
    "Portfolios"
]

# Required columns in Sponsored Products Campaigns sheet (minimal set for Empty Portfolios)
REQUIRED_COLUMNS = [
    "Portfolio ID",           # Essential - for matching between Portfolios and Campaigns sheets
    "Entity",                # Essential - to filter for "Campaign" entities
    "Operation",             # Standard bulk requirement for updates
    "Campaign ID",           # Helpful for processing and identification
]

# Optional columns that enhance functionality but are not required
OPTIONAL_COLUMNS = [
    "Campaign Name (Informational only)",
    "Portfolio Name (Informational only)", 
    "Campaign State",
    "Campaign State (Informational only)",
    "State",
    # All other standard bulk columns are optional
]

# Entity type to filter
TARGET_ENTITY = "Campaign"

# Portfolio names to exclude from empty portfolio optimization
EXCLUDED_PORTFOLIO_NAMES = ["Paused", "Terminal"]

# Columns to update in Portfolios sheet for empty portfolios
PORTFOLIO_UPDATE_COLUMNS = {
    "Operation": "update",
    "Budget Amount": "",
    "Budget Start Date": ""
}

# Color for highlighting empty portfolios
EMPTY_PORTFOLIO_COLOR = "FFFF00"  # Yellow

# Error messages
ERROR_MESSAGES = {
    "missing_sheet": "Missing required sheet: {}",
    "missing_columns": "Missing columns in Sponsored Products Campaigns: {}",
    "empty_campaigns": "Sponsored Products Campaigns sheet has no data",
    "empty_portfolios": "Portfolios sheet has no data",
    "no_portfolio_id": "Portfolio ID column not found in {}",
    "no_portfolio_name": "Portfolio Name column not found in Portfolios sheet"
}

# Success messages
SUCCESS_MESSAGES = {
    "validation_passed": "Validation successful: {} campaigns, {} portfolios found",
    "empty_found": "Found {} empty portfolios",
    "processing_complete": "Processing complete: {} portfolios updated"
}
