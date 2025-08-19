"""System constants for Bid Optimizer application."""

# File size limits
MAX_TEMPLATE_SIZE_MB = 1
MAX_BULK_SIZE_MB = 40

# Row limits
MAX_ROWS = 500_000

# Column requirements
BULK_REQUIRED_COLUMNS = 48
TEMPLATE_REQUIRED_SHEETS = ["Port Values", "Top ASINs"]
TEMPLATE_PORT_VALUES_COLUMNS = ["Portfolio Name", "Base Bid", "Target CPA"]

# Bid value ranges
MIN_BID = 0.02
MAX_BID = 1.25
MIN_BASE_BID = 0.02
MAX_BASE_BID = 4.0
MIN_TARGET_CPA = 0.01
MAX_TARGET_CPA = 4.0

# Bulk file sheet name
BULK_SHEET_NAME = "Sponsored Products Campaigns"

# Processing timeouts (seconds)
SMALL_FILE_TIMEOUT = 120  # Up to 10k rows
MEDIUM_FILE_TIMEOUT = 120  # Up to 100k rows  
LARGE_FILE_TIMEOUT = 300  # Up to 500k rows

# UI constants
SIDEBAR_WIDTH = 200
MAX_CONTENT_WIDTH = 800
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 44

# Colors (matching .streamlit/config.toml)
COLORS = {
    "background": "#0A0A0A",
    "sidebar": "#171717", 
    "card": "#171717",
    "text": "#E5E5E5",
    "accent": "#8B5CF6",
    "alert_bg": "#404040",
    "pink_highlight": "#FFE4E1"
}

# File naming
OUTPUT_FILE_PREFIX = "Auto Optimized Bulk | Working |"
TIMESTAMP_FORMAT = "%Y-%m-%d | %H-%M"