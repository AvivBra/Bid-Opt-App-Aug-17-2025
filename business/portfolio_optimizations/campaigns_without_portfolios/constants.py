"""Constants for Campaigns Without Portfolios optimization."""

# Target portfolio ID for campaigns without portfolio
TARGET_PORTFOLIO_ID = "84453417629173"

# Entity type to filter
TARGET_ENTITY = "Campaign"

# Minimal required columns for Campaigns Without Portfolios optimization
# Based on PRD: we only need to identify campaigns (Entity=Campaign) and update their Portfolio ID
REQUIRED_COLUMNS = [
    "Entity",           # To identify Campaign rows
    "Portfolio ID",     # To find empty portfolio IDs and update them  
    "Operation",        # To set operation to 'update'
    "Campaign ID"       # To identify specific campaigns
]

# Optional columns that are commonly present but not required
OPTIONAL_COLUMNS = [
    "Campaign Name (Informational only)",
    "Campaign State",
    "Campaign Daily Budget",
    "Ad Group ID",
    "Keyword ID", 
    "Product Targeting ID",
    "State"
]

# Update operation
UPDATE_OPERATION = "update"

# Messages
SUCCESS_MESSAGES = {
    "validation_passed": "✅ Validation passed for Campaigns Without Portfolios",
    "processing_complete": "✅ Successfully processed campaigns without portfolios",
    "no_campaigns_found": "ℹ️ No campaigns without portfolio found",
    "campaigns_updated": "✅ Updated {count} campaigns without portfolio"
}

ERROR_MESSAGES = {
    "missing_columns": "❌ Missing required columns for Campaigns Without Portfolios",
    "processing_failed": "❌ Failed to process campaigns without portfolios",
    "invalid_data": "❌ Invalid data format in campaigns sheet"
}

# Highlighting
HIGHLIGHT_COLOR = "FFFF00"  # Yellow for updated rows
