"""UI text constants and messages."""

# Application titles and headers
APP_TITLE = "BID OPTIMIZER"
WELCOME_MESSAGE = "Welcome to Bid Optimizer"
WELCOME_SUBTITLE = (
    "Upload your Template and Bulk files to get started with optimization."
)

# Campaign Creator titles
CAMPAIGN_APP_TITLE = "CAMPAIGN CREATOR"
CAMPAIGN_WELCOME_MESSAGE = "Welcome to Campaign Creator"
CAMPAIGN_WELCOME_SUBTITLE = (
    "Upload your Template file to create new campaigns bulk file."
)

# Section headers
UPLOAD_SECTION_TITLE = "Upload Files"
VALIDATION_SECTION_TITLE = "Data Validation"
OUTPUT_SECTION_TITLE = "Output Files"

# Button labels
DOWNLOAD_TEMPLATE_BUTTON = "Download Template"
UPLOAD_TEMPLATE_BUTTON = "Upload Template"
UPLOAD_BULK_60_BUTTON = "Upload Bulk 60"
UPLOAD_BULK_7_BUTTON = "Upload Bulk 7"
UPLOAD_BULK_30_BUTTON = "Upload Bulk 30"
PROCESS_FILES_BUTTON = "Process Files"
DOWNLOAD_WORKING_BUTTON = "Download Working File"
DOWNLOAD_CLEAN_BUTTON = "Download Clean File"
RESET_BUTTON = "Reset Session"

# Campaign specific buttons
UPLOAD_DATA_ROVA_BUTTON = "Data Rova"
UPLOAD_DATA_DIVE_BUTTON = "Data Dive"
DOWNLOAD_CAMPAIGN_BULK_BUTTON = "Download Campaign Bulk File"

# File upload help text
TEMPLATE_UPLOAD_HELP = (
    "Excel file with Port Values, Top ASINs, and Delete for 60 sheets"
)
BULK_UPLOAD_HELP = "Excel or CSV file with Sponsored Products Campaigns data"
CAMPAIGN_TEMPLATE_UPLOAD_HELP = "Excel file with campaign configuration"
DATA_ROVA_UPLOAD_HELP = "Data Rova file for campaign creation"
DATA_DIVE_UPLOAD_HELP = "Data Dive file for campaign creation"

# Status messages
TEMPLATE_SUCCESS = "Template loaded successfully"
BULK_SUCCESS = "Bulk file loaded successfully"
VALIDATION_SUCCESS = "All validations passed"
PROCESSING_SUCCESS = "Files processed successfully"
CAMPAIGN_TEMPLATE_SUCCESS = "Campaign template loaded successfully"
DATA_ROVA_SUCCESS = "Data Rova loaded successfully"
DATA_DIVE_SUCCESS = "Data Dive loaded successfully"

# Error messages
FILE_TOO_LARGE = "File size exceeds maximum limit"
INVALID_FILE_TYPE = "Invalid file type"
MISSING_SHEETS = "Required sheets missing from Excel file"
INVALID_COLUMNS = "Required columns missing or incorrect"
DUPLICATE_PORTFOLIOS = "Duplicate portfolio names found"
INVALID_BID_VALUES = "Invalid bid values detected"
NO_FILES_UPLOADED = "Please upload required files first"

# Warning messages
MANY_IGNORED_PORTFOLIOS = "Warning: Many portfolios set to 'Ignore'"
LARGE_FILE_WARNING = "Large file - processing may take several minutes"

# Info messages
BULK_7_TBC = "Bulk 7 days - Coming in future phases"
BULK_30_TBC = "Bulk 30 days - Coming in future phases"
CAMPAIGNS_TBC = "Campaigns Optimizer - Coming in Phase 2+"
CLEAN_FILE_TBC = "Clean file generation - Coming in future phases"

# Optimization names
OPTIMIZATION_ZERO_SALES = "Zero Sales"
OPTIMIZATION_PORTFOLIO_BID = "Portfolio Bid Optimization"
OPTIMIZATION_BUDGET = "Budget Optimization"
OPTIMIZATION_KEYWORD = "Keyword Optimization"
OPTIMIZATION_ASIN = "ASIN Targeting"
OPTIMIZATION_60_DAYS = "60 Days Optimization"
OPTIMIZATION_CAMPAIGN_CREATOR = "Campaign Creator"
OPTIMIZATION_EMPTY_PORTFOLIOS = "Empty Portfolios"  # ADDED
OPTIMIZATION_CAMPAIGNS_WITHOUT_PORTFOLIOS = "Campaigns w/o Portfolios"  # ADDED

# Validation messages
VALIDATION_PORTFOLIO_MATCH = "Portfolio matching validation"
VALIDATION_ZERO_SALES_DATA = "Zero sales data validation"
VALIDATION_BID_RANGES = "Bid value range validation"
VALIDATION_REQUIRED_COLUMNS = "Required columns validation"
VALIDATION_CAMPAIGN_TEMPLATE = "Campaign template validation"
VALIDATION_EMPTY_PORTFOLIOS = "Empty portfolios validation"  # ADDED
VALIDATION_CAMPAIGNS_WITHOUT_PORTFOLIOS = "Campaigns without portfolios validation"  # ADDED

# Progress messages
PROGRESS_READING_FILES = "Reading uploaded files..."
PROGRESS_VALIDATING_DATA = "Validating data integrity..."
PROGRESS_PROCESSING_OPTIMIZATIONS = "Processing optimizations..."
PROGRESS_GENERATING_OUTPUT = "Generating output files..."
PROGRESS_FINALIZING = "Finalizing results..."
PROGRESS_CREATING_CAMPAIGNS = "Creating campaign bulk file..."
PROGRESS_FINDING_EMPTY = "Finding empty portfolios..."  # ADDED
PROGRESS_UPDATING_CAMPAIGNS = "Updating campaigns without portfolios..."  # ADDED

# Help text
HELP_TEMPLATE_STRUCTURE = """
Template file should contain:
- Port Values sheet with Portfolio Name, Base Bid, Target CPA columns
- Top ASINs sheet (can be empty for Phase 1)
- Delete for 60 sheet with Keyword ID and Product Targeting ID columns (optional)
- Portfolio names must match those in Bulk file
- Base Bid: 0.02-4.00 or 'Ignore'
- Target CPA: 0.01-4.00 or empty
"""

HELP_BULK_STRUCTURE = """
Bulk file requirements:
- Excel file with 'Sponsored Products Campaigns' sheet
- CSV files also supported
- Exactly 48 columns required
- Maximum 500,000 rows
- Must contain Units and Portfolio columns for Zero Sales optimization
"""

HELP_ZERO_SALES = """
Zero Sales Optimization:
- Identifies products with 0 units sold
- Calculates new bid based on 4 scenarios
- Filters out 10 predefined 'Flat' portfolios
- Skips portfolios marked as 'Ignore'
- Adds helper columns to output file
"""

HELP_60_DAYS = """
60 Days Optimization:
- Uses Keyword IDs and Product Targeting IDs from Delete for 60 sheet
- Applies optimization for 60-day period
- Processes items marked for deletion or modification
"""

HELP_CAMPAIGN_CREATOR = """
Campaign Creator:
- Creates new campaign bulk files for Amazon Ads
- Processes template with campaign configuration
- Generates bulk file ready for upload
- Validates campaign structure and settings
"""

# Empty Portfolios help text - ADDED
HELP_EMPTY_PORTFOLIOS = """
Empty Portfolios Optimization:
- Identifies portfolios without any campaigns
- Renames empty portfolios with numeric names
- Updates Portfolio Name to smallest available number
- Sets Operation to 'update' for empty portfolios
- Highlights modified rows in yellow
- Filters campaigns sheet to Entity = Campaign only
"""

# Campaigns without Portfolios help text - ADDED
HELP_CAMPAIGNS_WITHOUT_PORTFOLIOS = """
Campaigns w/o Portfolios Optimization:
- Identifies campaigns without assigned portfolios (empty Portfolio ID)
- Updates campaigns to assign them to Portfolio ID: 84453417629173
- Sets Operation to 'update' for affected campaigns
- Highlights modified rows in yellow
- Filters to Entity = Campaign in Sponsored Products Campaigns sheet
- Works on campaigns that currently have blank/empty Portfolio ID
"""
