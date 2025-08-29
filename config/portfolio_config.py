"""Configuration for Portfolio Optimizer."""

# Portfolio Optimizer settings
PORTFOLIO_OPTIMIZER_CONFIG = {
    "name": "Portfolio Optimizer",
    "version": "2.0.0",
    "description": "Factory-based portfolio optimization system with dynamic optimization discovery",
    "architecture": "factory_pattern",
    "enabled_optimizations": ["empty_portfolios", "campaigns_without_portfolios"],
    "future_optimizations": [
        "portfolio_budget_optimization",
        "portfolio_performance_analysis", 
        "portfolio_consolidation",
        "portfolio_campaign_distribution"
    ],
    "factory_config": {
        "auto_discovery": True,
        "base_path": "business/portfolio_optimizations",
        "orchestrator_pattern": "*Orchestrator",
        "required_methods": ["run", "get_description"]
    }
}

# Empty Portfolios optimization configuration
EMPTY_PORTFOLIOS_CONFIG = {
    "name": "Empty Portfolios",
    "enabled": True,
    "description": "Identify and rename empty portfolios with numeric names",
    "display_name": "Empty Portfolios",
    "category": "portfolio_management",
    "result_type": "portfolios",
    "priority": 1,
    "dependencies": [],
    "conflicts": [],
    "help_text": "Finds portfolios that don't contain any campaigns and assigns them sequential numeric names (1, 2, 3, etc.) for easy identification and management.",
    
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

# Campaigns without Portfolios optimization configuration
CAMPAIGNS_WITHOUT_PORTFOLIOS_CONFIG = {
    "name": "Campaigns w/o Portfolios",
    "enabled": True,
    "description": "Update campaigns without portfolios to assign them to a specific portfolio",
    "display_name": "Campaigns w/o Portfolios",
    "category": "campaign_management", 
    "result_type": "campaigns",
    "priority": 2,
    "dependencies": [],
    "conflicts": [],
    "help_text": "Identifies campaigns that are not assigned to any portfolio and automatically assigns them to the specified target portfolio (ID: 84453417629173) with update operation.",
    
    # Required sheets for validation
    "required_sheets": [
        "Sponsored Products Campaigns"
    ],
    
    # Required columns for Sponsored Products Campaigns sheet
    "required_campaigns_columns": [
        "Portfolio ID",
        "Entity",
        "Operation",
        "Campaign ID"
    ],
    
    # Processing configuration
    "processing": {
        "target_entity": "Campaign",
        "update_operation": "update", 
        "target_portfolio_id": "84453417629173",  # Portfolio ID to assign
        "highlight_color": "FFFF00",  # Yellow
        "empty_value": "",
        "filter_empty_portfolio_id": True
    },
    
    # Output configuration
    "output": {
        "sheets_to_include": [
            "Sponsored Products Campaigns"
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
        "no_portfolio_id": "Portfolio ID column not found in {}",
        "no_entity_column": "Entity column not found in Sponsored Products Campaigns sheet", 
        "file_too_large": "File size exceeds maximum limit of 40MB",
        "too_many_rows": "File contains more than 500,000 rows"
    },
    
    # Success messages
    "success_messages": {
        "validation_passed": "Validation successful: {} campaigns found",
        "campaigns_found": "Found {} campaigns without portfolios",
        "processing_complete": "Processing complete: {} campaigns updated",
        "file_ready": "Output file ready for download"
    },
    
    # Info messages
    "info_messages": {
        "processing_start": "Starting Campaigns w/o Portfolios optimization...",
        "validating": "Validating input files...",
        "searching_campaigns": "Searching for campaigns without portfolios...",
        "updating": "Updating campaigns with portfolio ID...",
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

# Optimization Registry - maps internal names to configurations
OPTIMIZATION_REGISTRY = {
    "empty_portfolios": EMPTY_PORTFOLIOS_CONFIG,
    "campaigns_without_portfolios": CAMPAIGNS_WITHOUT_PORTFOLIOS_CONFIG
}

# Helper functions for factory integration
def get_optimization_config(optimization_name: str) -> dict:
    """Get configuration for a specific optimization."""
    return OPTIMIZATION_REGISTRY.get(optimization_name, {})

def get_enabled_optimizations() -> dict:
    """Get all enabled optimizations."""
    return {
        name: config for name, config in OPTIMIZATION_REGISTRY.items()
        if config.get("enabled", True)
    }

def get_optimization_display_name(optimization_name: str) -> str:
    """Get display name for an optimization."""
    config = get_optimization_config(optimization_name)
    return config.get("display_name", optimization_name)

def get_optimization_help_text(optimization_name: str) -> str:
    """Get help text for an optimization."""
    config = get_optimization_config(optimization_name)
    return config.get("help_text", config.get("description", "No description available"))

def get_optimization_category(optimization_name: str) -> str:
    """Get category for an optimization."""
    config = get_optimization_config(optimization_name)
    return config.get("category", "general")
