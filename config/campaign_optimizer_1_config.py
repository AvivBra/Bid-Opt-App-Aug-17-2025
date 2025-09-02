"""Campaign Optimizer 1 configuration settings."""

# Processing settings
PROCESSING_TIMEOUT_SECONDS = 300  # 5 minutes
MAX_FILE_SIZE_MB = 50

# Validation settings
REQUIRED_SHEETS = ["Sponsored Products Campaigns"]
REQUIRED_COLUMNS = [
    "Entity",
    "Units", 
    "ACOS",
    "Daily Budget",
    "State",
    "Campaign State (Informational only)",
    "Ad Group State (Informational only)"
]

# Output settings
OUTPUT_SHEETS = ["Campaign", "Sheet3"]
OUTPUT_FILE_PREFIX = "campaign-optimizer-1"

# UI settings
PAGE_TITLE = "Campaign Optimizer 1"
CHECKBOX_LABEL = "7 Days Budgets"
PROCESS_BUTTON_LABEL = "Bulk 7"

# Business logic settings
ACOS_THRESHOLD = 0.17
BUDGET_VALUES = {
    "minimum": 1,
    "medium": 3, 
    "high": 5
}

# Error messages
ERROR_MESSAGES = {
    "file_too_large": f"File size exceeds {MAX_FILE_SIZE_MB}MB limit",
    "invalid_format": "File must be an Excel (.xlsx) file",
    "missing_sheet": "Required sheet '{}' not found",
    "missing_columns": "Required columns missing: {}",
    "processing_timeout": f"Processing exceeded {PROCESSING_TIMEOUT_SECONDS} seconds",
    "no_campaign_data": "No campaign data found after filtering"
}

# Success messages  
SUCCESS_MESSAGES = {
    "file_uploaded": "File uploaded and validated successfully",
    "processing_complete": "Campaign optimization completed successfully",
    "ready_for_download": "Results ready for download"
}