"""Constants for Bids 30 Days optimization."""

# Bid constraints
MIN_BID = 0.02
MAX_BID = 1.25  # Note: Different from Zero Sales (4.00)

# Calculation thresholds
CALC2_THRESHOLD = 1.1
CONVERSION_RATE_THRESHOLD = 0.08
UNITS_THRESHOLD_FOR_MAX_BID = 3
CLICKS_THRESHOLD = 30
UNITS_THRESHOLD = 2

# Max Bid values (before adjustment)
MAX_BID_LOW_UNITS = 0.8
MAX_BID_HIGH_UNITS = 1.25

# Multipliers
UP_AND_MULTIPLIER = 0.5
OLD_BID_MULTIPLIER = 1.1

# Column names for helper columns (in order)
HELPER_COLUMNS = [
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
]

# Sheet names for output
SHEET_TARGETING = "Targeting"
SHEET_BIDDING_ADJUSTMENT = "Bidding Adjustment"
SHEET_FOR_HARVESTING = "For Harvesting"

# Entity types
ENTITY_KEYWORD = "Keyword"
ENTITY_PRODUCT_TARGETING = "Product Targeting"
ENTITY_BIDDING_ADJUSTMENT = "Bidding Adjustment"
ENTITY_PRODUCT_AD = "Product Ad"

# Match types
MATCH_TYPE_EXACT = "Exact"

# Product targeting patterns - FIXED
ASIN_PATTERN = 'asin="B0'  # Looking for asin="B0 (with quote)

# State values
STATE_ENABLED = "enabled"

# Error messages for Bid column
ERROR_CALCULATION = "Calculation Error"
ERROR_NULL = "Null Error"
ERROR_MISSING_VALUE = "Missing Value in {column}"

# Column positions in original bulk (1-based)
CONVERSION_RATE_COLUMN_POSITION = 55

# Excluded portfolios (same as Zero Sales)
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
