"""Constants for Bids 60 Days optimization."""

# Optimization name
OPTIMIZATION_NAME = "Bids 60 Days"

# Filtering thresholds
UNITS_THRESHOLD = 0  # units > 0

# Excluded portfolios (same as Zero Sales and Bids 30)
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
    "Flat 10",
    "Flat 20 | Winter Clothing",
]

# Calculation thresholds
CALC2_THRESHOLD = 1.1
CONVERSION_RATE_THRESHOLD = 0.08  # 8%
UNITS_FOR_MAX_BID = 3

# Bid limits
MIN_BID = 0.02
MAX_BID = 1.25  # Different from Zero Sales (4.00)

# Max Bid values based on units
MAX_BID_LOW_UNITS = 0.8  # When units < 3
MAX_BID_HIGH_UNITS = 1.25  # When units >= 3

# Multipliers
UP_AND_MULTIPLIER = 0.5  # When campaign contains "up and"
OLD_BID_MULTIPLIER = 1.1  # For Old Bid * 1.1 calculation

# Entity types
TARGET_ENTITIES = ["Keyword", "Product Targeting"]
SEPARATE_ENTITIES = ["Bidding Adjustment", "Product Ad"]

# Helper columns configuration
HELPER_COLUMNS = [
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
]

# Output sheets
OUTPUT_SHEETS = {
    "Targeting": 58,  # 48 original + 10 helper columns
    "Bidding Adjustment": 48,  # Original columns only
    "For Harvesting": 58  # Same as Targeting
}

# Column positions (0-indexed)
BID_COLUMN_INDEX = 27  # Column 28 in Excel (1-indexed)
CONVERSION_RATE_COLUMN_INDEX = 44  # Column 45 in Excel

# Error messages
ERROR_NULL = "Null Error"
ERROR_CALCULATION = "Calculation Error"
