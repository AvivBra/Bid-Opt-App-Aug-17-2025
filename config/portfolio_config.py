"""Configuration for Portfolio Optimizer."""

# Portfolio Optimizer settings
PORTFOLIO_OPTIMIZER_CONFIG = {
    "name": "Portfolio Optimizer",
    "version": "1.0.0",
    "description": "Optimize portfolio structure and management",
    "enabled_optimizations": ["Empty Portfolios"],
    "future_optimizations": [
        "Portfolio Budget Optimization",
        "Portfolio Performance Analysis",
        "Portfolio Consolidation",
        "Portfolio Campaign Distribution"
    ]
}

# Empty Portfolios optimization configuration
EMPTY_PORTFOLIOS_CONFIG = {
    "name": "Empty Portfolios",
    "enabled": True,
    "description": "Identify and rename empty portfolios with numeric names",
    
    # Required sheets for validation
    "required_sheets": [
        "Sponsored Products Campaigns",
        "Portfolios"
    ],
    
    # Required columns for Sponsored Products Campaigns sheet
    "required_campaigns_columns": [
        "Portfolio ID",
        "Entity",
        "Operation",
        "Campaign ID"
    ],
    
    # Required columns for Portfolios sheet
    "required_portfolios_columns": [
        "Portfolio ID",
        "Portfolio Name",
        "Operation",
        "Budget Amount",
        "Budget Start Date"
    ],
    
    # Processing configuration
    "processing": {
        "target_entity": "Campaign",
        "update_operation": "update",
        "highlight_color": "FFFF00",  # Yellow
        "empty_value": "",
        "min_portfolio_number": 1,
        "max_portfolio_number": 9999
    },
    
    # Output configuration
    "output": {
        "sheets_to_include": [
            "Sponsored Products Campaigns",
            "Portfolios"
        ],
        "add_summary_sheet": True,
        "highlight_modified_rows": True
    },
    
    # Validation thresholds
    "validation": {
        "max_file_size_mb": 40,
        "max_rows": 500000,
        "min_rows": 1
    },
    
    # Error messages
    "error_messages": {
        "missing_sheet": "Missing required sheet: {}",
        "missing_columns": "Missing columns in {}: {}",
        "empty_campaigns": "Sponsored Products Campaigns sheet has no data",
        "empty_portfolios": "Portfolios sheet has no data",
        "no_portfolio_id": "Portfolio ID column not found in {}",
        "no_portfolio_name": "Portfolio Name column not found in Portfolios sheet",
        "file_too_large": "File size exceeds maximum limit of 40MB",
        "too_many_rows": "File contains more than 500,000 rows"
    },
    
    # Success messages
    "success_messages": {
        "validation_passed": "Validation successful: {} campaigns, {} portfolios found",
        "empty_found": "Found {} empty portfolios",
        "processing_complete": "Processing complete: {} portfolios renamed",
        "file_ready": "Output file ready for download"
    },
    
    # Info messages
    "info_messages": {
        "processing_start": "Starting Empty Portfolios optimization...",
        "validating": "Validating input files...",
        "searching_empty": "Searching for empty portfolios...",
        "renaming": "Renaming empty portfolios...",
        "generating_output": "Generating output file..."
    }
}

# File handling configuration
FILE_CONFIG = {
    "supported_formats": ["xlsx", "csv"],
    "max_file_size_mb": 40,
    "encoding": "utf-8",
    "excel_engine": "openpyxl"
}

# UI Configuration
UI_CONFIG = {
    "show_progress_bar": True,
    "auto_download": False,
    "show_statistics": True,
    "allow_reset": True
}

# Logging configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "portfolio_optimizer.log"
}
