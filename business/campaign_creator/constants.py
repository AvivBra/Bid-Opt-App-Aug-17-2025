"""Constants for Campaign Creator module."""

# Campaign template sheet and columns
CAMPAIGN_CONFIG_SHEET = "Campaign Configuration"

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
    "Halloween Expanded Bid"
]

# Campaign types
CAMPAIGN_TYPES = {
    "testing": {
        "name": "Testing",
        "bid_column": "Testing Bid",
        "match_type": "exact",
        "targeting": "keyword"
    },
    "testing_pt": {
        "name": "Testing PT",
        "bid_column": "Testing PT Bid",
        "match_type": "exact",
        "targeting": "product"
    },
    "phrase": {
        "name": "Phrase",
        "bid_column": "Phrase Bid",
        "match_type": "phrase",
        "targeting": "keyword"
    },
    "broad": {
        "name": "Broad",
        "bid_column": "Broad Bid",
        "match_type": "broad",
        "targeting": "keyword"
    },
    "expanded": {
        "name": "Expanded",
        "bid_column": "Expanded Bid",
        "match_type": "broad",
        "targeting": "keyword"
    },
    "halloween_testing": {
        "name": "Halloween Testing",
        "bid_column": "Halloween Testing Bid",
        "match_type": "exact",
        "targeting": "keyword"
    },
    "halloween_testing_pt": {
        "name": "Halloween Testing PT",
        "bid_column": "Halloween Testing PT Bid",
        "match_type": "exact",
        "targeting": "product"
    },
    "halloween_phrase": {
        "name": "Halloween Phrase",
        "bid_column": "Halloween Phrase Bid",
        "match_type": "phrase",
        "targeting": "keyword"
    },
    "halloween_broad": {
        "name": "Halloween Broad",
        "bid_column": "Halloween Broad Bid",
        "match_type": "broad",
        "targeting": "keyword"
    },
    "halloween_expanded": {
        "name": "Halloween Expanded",
        "bid_column": "Halloween Expanded Bid",
        "match_type": "broad",
        "targeting": "product"
    }
}

# Bid constraints
DEFAULT_BID = 0.30
MIN_BID = 0.02
MAX_BID = 10.00

# Campaign settings
DEFAULT_CAMPAIGN_STATUS = "enabled"
DEFAULT_AD_GROUP_STATUS = "enabled"
DEFAULT_KEYWORD_STATUS = "enabled"
DEFAULT_DAILY_BUDGET = 50.00
MIN_DAILY_BUDGET = 1.00
MAX_DAILY_BUDGET = 21474836.47

# Campaign configuration
DEFAULT_TARGETING_TYPE = "manual"
DEFAULT_BIDDING_STRATEGY = "manual"
DEFAULT_CAMPAIGN_TYPE = "sponsoredProducts"

# Amazon bulk file columns for campaign creation
AMAZON_BULK_COLUMNS = [
    "Record ID",
    "Record Type",
    "Campaign ID",
    "Campaign",
    "Campaign Daily Budget",
    "Portfolio ID",
    "Campaign Start Date",
    "Campaign End Date",
    "Campaign Targeting Type",
    "Ad Group",
    "Max Bid",
    "Keyword or Product Targeting",
    "Product Targeting ID",
    "Match Type",
    "SKU",
    "Campaign Status",
    "Ad Group Status",
    "Status",
    "Bidding Strategy",
    "Placement Type",
    "Increase bids by placement"
]