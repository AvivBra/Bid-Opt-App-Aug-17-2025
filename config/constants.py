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
    "Adj. %",
    "Case",
    "CPC",
    "Max BA",
]

# Output file settings
OUTPUT_FILE_PREFIX = "Bid_Optimizer_Output"
TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"

# UI Display
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
MAX_DISPLAY_ROWS = 100

# Processing
CHUNK_SIZE = 10000
BATCH_SIZE = 1000

# Validation thresholds
MAX_BID_CHANGE_PERCENTAGE = 500  # Maximum allowed bid change in percentage
MIN_CLICKS_FOR_OPTIMIZATION = 10  # Minimum clicks required for optimization

# File type constants
ALLOWED_EXTENSIONS = ["xlsx", "xls", "csv"]
EXCEL_EXTENSIONS = ["xlsx", "xls"]
CSV_EXTENSIONS = ["csv"]

# Processing status
PROCESSING_STATES = ["pending", "processing", "complete", "error"]

# Error messages
ERROR_FILE_TOO_LARGE = f"File size exceeds {MAX_FILE_SIZE_MB}MB limit"
ERROR_INVALID_FORMAT = "Invalid file format. Please upload Excel or CSV file"
ERROR_MISSING_COLUMNS = "Required columns missing from file"
ERROR_NO_DATA = "No data found in file"

# Success messages
SUCCESS_TEMPLATE_GENERATED = "Template generated successfully"
SUCCESS_FILE_UPLOADED = "File uploaded successfully"
SUCCESS_PROCESSING_COMPLETE = "Processing completed successfully"

# Warning messages
WARNING_LARGE_FILE = "Large file detected. Processing may take several minutes"
WARNING_MANY_ERRORS = "Multiple validation errors detected"

# ============== CAMPAIGN CREATOR CONSTANTS ==============

# Campaign Template Configuration
CAMPAIGN_TEMPLATE_SHEET = "Campaign Configuration"
CAMPAIGN_TEMPLATE_COLUMNS = [
    "My ASIN",
    "Product Type",
    "Niche",
    "Bid",
    "Hero Keyword 1",
    "Hero Keyword 2",
    "Hero Keyword 3",
    "Hero Keyword 4",
    "Hero Keyword 5",
    "Hero Keyword 6",
    "Testing Bid",
    "Testing PT Bid",
    "Phrase Bid",
    "Broad Bid",
    "Expanded Bid",
    "Halloween Testing Bid",
    "Halloween Testing Bid",
    "Halloween Testing PT Bid",
    "Halloween Phrase Bid",
    "Halloween Broad Bid",
    "Halloween Expanded Bid",
]

# Campaign Creator file size limits
MAX_CAMPAIGN_TEMPLATE_SIZE_MB = 5
MAX_DATA_ROVA_SIZE_MB = 40
MAX_DATA_DIVE_SIZE_MB = 40

# Output file naming
CAMPAIGN_OUTPUT_PREFIX = "Campaign_Bulk"
CAMPAIGN_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"
