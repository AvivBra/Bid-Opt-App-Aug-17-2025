"""Application constants and configuration values."""

from typing import List

# File size limits
MAX_FILE_SIZE_MB = 40  # For bulk files
MAX_BULK_FILE_SIZE_MB = 40
MAX_BULK_SIZE_MB = 40
MAX_TEMPLATE_SIZE_MB = 1  # For template files
MAX_TEMPLATE_FILE_SIZE_MB = 1

# Row limits
MAX_ROWS = 500000
MAX_BULK_ROWS = 500000

# Column requirements
REQUIRED_COLUMNS = 48  # Number of required columns in bulk files
BULK_REQUIRED_COLUMNS = 48

# Template structure
TEMPLATE_REQUIRED_SHEETS = ["Port Values", "Top ASINs", "Delete for 60"]
TEMPLATE_PORT_VALUES_COLUMNS = ["Portfolio Name", "Base Bid", "Target CPA"]
TEMPLATE_TOP_ASINS_COLUMNS = ["ASIN"]
TEMPLATE_DELETE_FOR_60_COLUMNS = ["Keyword ID", "Product Targeting ID"]

# Bulk file structure
BULK_SHEET_NAME = "Sponsored Products Campaigns"

# Bid constraints
MIN_BID = 0.02
MAX_BID = 4.00
DEFAULT_BID = 0.5
MIN_BASE_BID = 0.02
MAX_BASE_BID = 4.00
MIN_TARGET_CPA = 0.01
MAX_TARGET_CPA = 9999.99

# Zero Sales Optimization Constants
ZERO_SALES_CONSTANTS = {
    "CASE_A_MULTIPLIER": 0.5,  # For empty Target CPA with "up and"
    "CASE_B_MULTIPLIER": 1.0,  # For empty Target CPA without "up and"
    "CASE_C_MULTIPLIER": 0.7,  # For Target CPA present with "up and"
    "CASE_D_MULTIPLIER": 0.9,  # For Target CPA present without "up and"
    "CPC_THRESHOLD": 0.09,  # Threshold for CPC comparison
    "MAX_BA_MULTIPLIER": 1.4,  # Multiplier for Max BA calculation
}

# Excluded portfolios (Flat portfolios)
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

# Entity types
VALID_ENTITY_TYPES = ["Keyword", "Product Targeting", "Bidding Adjustment"]

# Column names in bulk file
PORTFOLIO_NAME_COLUMN = "Portfolio Name (Informational only)"
ENTITY_COLUMN = "Entity"
OPERATION_COLUMN = "Operation"
BID_COLUMN = "Bid"
UNITS_COLUMN = "Units"
CLICKS_COLUMN = "Clicks"
PERCENTAGE_COLUMN = "Percentage"
STATE_COLUMN = "State"
CAMPAIGN_STATE_COLUMN = "Campaign State (Informational only)"
AD_GROUP_STATE_COLUMN = "Ad Group State (Informational only)"

# Helper columns for Zero Sales
HELPER_COLUMNS = [
    "Old Bid",
    "calc1",
    "calc2",
    "Target CPA",
    "Base Bid",
    "Adj. CPA",
    "Max BA",
]

# File naming
OUTPUT_FILE_PREFIX = "Auto Optimized Bulk"
WORKING_FILE_SUFFIX = "Working"
CLEAN_FILE_SUFFIX = "Clean"

# Colors for UI
COLORS = {
    "primary": "#CCCCCC",
    "secondary": "#EEEEEE",
    "background": "#0F0F0F",
    "sidebar": "#1A1A1A",
    "card": "#1A1A1A",
    "surface": "#1A1A1A",
    "accent": "#DDDDDD",
    "alert_bg": "#404040",
    "text": "#FFFFFF",
    "error": "#EF4444",
    "success": "#10B981",
    "warning": "#F59E0B",
    "info": "#3B82F6",
}

# UI Constants
SIDEBAR_WIDTH = 200
MAX_CONTENT_WIDTH = 800
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 40

# Processing
CHUNK_SIZE = 10000
PROCESSING_TIMEOUT_SECONDS = 300  # 5 minutes
SMALL_FILE_TIMEOUT = 120
MEDIUM_FILE_TIMEOUT = 120
LARGE_FILE_TIMEOUT = 300
OUTPUT_FILE_PREFIX = "Auto Optimized Bulk"
TIMESTAMP_FORMAT = "%Y-%m-%d | %H-%M"

# Validation messages
VALIDATION_MESSAGES = {
    "MISSING_PORTFOLIOS": "Missing portfolios found - Reupload Full Template",
    "ALL_VALID": "All portfolios valid",
    "IGNORED_PORTFOLIOS": "portfolios marked as 'Ignore' will be skipped",
    "FILE_TOO_LARGE": "File exceeds size limit",
    "INVALID_COLUMNS": "Invalid column structure",
    "NO_DATA": "No data to process",
}
