"""Configuration for Campaign Creator module."""

# Campaign types and their configurations
CAMPAIGN_TYPES = {
    "Testing": {
        "display_name": "Testing",
        "bid_column": "Testing Bid",
        "match_type": "exact",
        "targeting": "keyword",
        "prefix": "Testing",
        "daily_budget": 5.00,
        "default_bid": 0.30,
        "requires_rova": True
    },
    "Testing PT": {
        "display_name": "Testing PT",
        "bid_column": "Testing PT Bid",
        "match_type": "exact",
        "targeting": "product",
        "prefix": "Testing PT",
        "daily_budget": 5.00,
        "default_bid": 0.30,
        "requires_rova": False
    },
    "Phrase": {
        "display_name": "Phrase",
        "bid_column": "Phrase Bid",
        "match_type": "phrase",
        "targeting": "keyword",
        "prefix": "Phrase",
        "daily_budget": 10.00,
        "default_bid": 0.25,
        "requires_rova": True
    },
    "Broad": {
        "display_name": "Broad",
        "bid_column": "Broad Bid",
        "match_type": "broad",
        "targeting": "keyword",
        "prefix": "Broad",
        "daily_budget": 10.00,
        "default_bid": 0.20,
        "requires_rova": True
    },
    "Expanded": {
        "display_name": "Expanded",
        "bid_column": "Expanded Bid",
        "match_type": "broad",
        "targeting": "product",
        "prefix": "Expanded",
        "daily_budget": 15.00,
        "default_bid": 0.20,
        "requires_rova": False
    },
    "Halloween Testing": {
        "display_name": "Halloween Testing",
        "bid_column": "Halloween Testing Bid",
        "match_type": "exact",
        "targeting": "keyword",
        "prefix": "Testing | Halloween",
        "daily_budget": 1.00,
        "default_bid": 0.15,
        "requires_rova": True
    },
    "Halloween Testing PT": {
        "display_name": "Halloween Testing PT",
        "bid_column": "Halloween Testing PT Bid",
        "match_type": "exact",
        "targeting": "product",
        "prefix": "Testing PT | Halloween",
        "daily_budget": 1.00,
        "default_bid": 0.15,
        "requires_rova": False
    },
    "Halloween Phrase": {
        "display_name": "Halloween Phrase",
        "bid_column": "Halloween Phrase Bid",
        "match_type": "phrase",
        "targeting": "keyword",
        "prefix": "Phrase | Halloween",
        "daily_budget": 2.00,
        "default_bid": 0.12,
        "requires_rova": True
    },
    "Halloween Broad": {
        "display_name": "Halloween Broad",
        "bid_column": "Halloween Broad Bid",
        "match_type": "broad",
        "targeting": "keyword",
        "prefix": "Broad | Halloween",
        "daily_budget": 2.00,
        "default_bid": 0.10,
        "requires_rova": True
    },
    "Halloween Expanded": {
        "display_name": "Halloween Expanded",
        "bid_column": "Halloween Expanded Bid",
        "match_type": "broad",
        "targeting": "product",
        "prefix": "Expanded | Halloween",
        "daily_budget": 3.00,
        "default_bid": 0.10,
        "requires_rova": False
    }
}

# Keyword campaigns (require Data Rova for CVR and sales data)
KEYWORD_CAMPAIGNS = {
    "Testing",
    "Phrase",
    "Broad",
    "Halloween Testing",
    "Halloween Phrase",
    "Halloween Broad"
}

# Product Targeting campaigns (work with ASINs)
PT_CAMPAIGNS = {
    "Testing PT",
    "Expanded",
    "Halloween Testing PT",
    "Halloween Expanded"
}

# Data validation thresholds
VALIDATION_THRESHOLDS = {
    "cvr_threshold": 0.08,  # Minimum conversion rate for keywords
    "sales_threshold": 0,    # Minimum sales for keywords
    "max_bid": 10.00,        # Maximum allowed bid
    "min_bid": 0.02,         # Minimum allowed bid
    "max_daily_budget": 1000.00,  # Maximum daily budget
    "min_daily_budget": 1.00      # Minimum daily budget
}

# Template column mappings
TEMPLATE_COLUMNS = {
    "asin": "My ASIN",
    "product_type": "Product Type",
    "niche": "Niche",
    "testing_bid": "Testing Bid",
    "testing_pt_bid": "Testing PT Bid",
    "phrase_bid": "Phrase Bid",
    "broad_bid": "Broad Bid",
    "expanded_bid": "Expanded Bid",
    "halloween_testing_bid": "Halloween Testing Bid",
    "halloween_testing_pt_bid": "Halloween Testing PT Bid",
    "halloween_phrase_bid": "Halloween Phrase Bid",
    "halloween_broad_bid": "Halloween Broad Bid",
    "halloween_expanded_bid": "Halloween Expanded Bid"
}

# Session table column names
SESSION_TABLE_COLUMNS = {
    "target": "target",
    "asin": "ASIN",
    "product_type": "Product Type",
    "niche": "Niche",
    "campaign_type": "Campaign type",
    "bid": "Bid",
    "kw_cvr": "kw cvr",
    "kw_sales": "kw sales"
}

# Amazon bulk file column configuration
BULK_FILE_COLUMNS = [
    "Product",
    "Entity",
    "Operation",
    "Campaign ID",
    "Ad Group ID",
    "Portfolio ID",
    "Ad ID",
    "Keyword ID",
    "Product Targeting ID",
    "Campaign Name",
    "Ad Group Name",
    "Start Date",
    "End Date",
    "Targeting Type",
    "State",
    "Daily Budget",
    "SKU",
    "ASIN",
    "Ad Group Default Bid",
    "Bid",
    "Keyword Text",
    "Native Language Keyword",
    "Native Language Locale",
    "Match Type",
    "Bidding Strategy",
    "Placement",
    "Percentage",
    "Product Targeting Expression"
]

# Entity types for bulk file
ENTITY_TYPES = {
    "campaign": "Campaign",
    "ad_group": "Ad Group",
    "product_ad": "Product Ad",
    "keyword": "Keyword",
    "product_targeting": "Product Targeting"
}

# Default values for bulk file
BULK_DEFAULTS = {
    "product": "Sponsored Products",
    "operation": "Create",
    "targeting_type": "MANUAL",
    "state": "enabled",
    "bidding_strategy": "Dynamic bids - down only",
    "portfolio_id": "",
    "ad_id": "",
    "keyword_id": "",
    "product_targeting_id": "",
    "end_date": "",
    "sku": "",
    "native_language_keyword": "",
    "native_language_locale": "",
    "placement": "",
    "percentage": "",
    "product_targeting_expression": ""
}

# File naming configuration
FILE_NAMING = {
    "prefix": "Campaign_Bulk",
    "date_format": "%Y%m%d_%H%M%S",
    "extension": ".xlsx"
}

# Logging configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}

# Validation messages
VALIDATION_MESSAGES = {
    "empty_template": "Template file is empty",
    "missing_columns": "Template missing required columns: {columns}",
    "no_valid_bids": "No valid bids found in template",
    "missing_asin": "Missing ASIN in row {row}",
    "missing_product_type": "Missing Product Type in row {row}",
    "missing_niche": "Missing Niche in row {row}",
    "invalid_bid": "Invalid bid value in row {row}: {value}",
    "no_targets": "No targets (keywords or ASINs) found",
    "no_valid_keywords": "No keywords meet CVR/sales thresholds",
    "data_rova_required": "Data Rova file required for keyword campaigns",
    "session_table_empty": "Session table is empty after filtering"
}

# Success messages
SUCCESS_MESSAGES = {
    "validation_passed": "Validation passed successfully",
    "processing_complete": "Processing completed successfully",
    "file_created": "Campaign bulk file created: {filename}",
    "campaigns_processed": "{count} campaigns processed",
    "keywords_added": "{count} keywords added",
    "asins_added": "{count} ASINs added"
}