"""Validator for Empty Portfolios optimization."""

import pandas as pd
from typing import Dict, Tuple, Any
import logging
from .constants import (
    REQUIRED_SHEETS,
    REQUIRED_COLUMNS,
    ERROR_MESSAGES,
    SUCCESS_MESSAGES
)


class EmptyPortfoliosValidator:
    """Validates bulk file for Empty Portfolios optimization."""
    
    def __init__(self):
        self.logger = logging.getLogger("empty_portfolios.validator")
    
    def validate(self, bulk_data: Dict[str, pd.DataFrame]) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Validate bulk file structure and content.
        
        Args:
            bulk_data: Dictionary with sheet names as keys and DataFrames as values
            
        Returns:
            Tuple of (is_valid, message, validation_details)
        """
        details = {
            "campaigns_count": 0,
            "portfolios_count": 0,
            "missing_columns": [],
            "validation_steps": []
        }
        
        try:
            # Check 1: Required sheets exist
            for sheet in REQUIRED_SHEETS:
                if sheet not in bulk_data:
                    return False, ERROR_MESSAGES["missing_sheet"].format(sheet), details
            
            details["validation_steps"].append("✓ Required sheets found")
            
            # Check 2: Validate Sponsored Products Campaigns sheet
            campaigns_df = bulk_data["Sponsored Products Campaigns"]
            
            # Check all 48 required columns
            missing_cols = [col for col in REQUIRED_COLUMNS if col not in campaigns_df.columns]
            if missing_cols:
                details["missing_columns"] = missing_cols
                return False, ERROR_MESSAGES["missing_columns"].format(", ".join(missing_cols[:5])), details
            
            details["validation_steps"].append("✓ All 48 columns present")
            
            # Check for at least one data row
            if campaigns_df.empty or len(campaigns_df) < 1:
                return False, ERROR_MESSAGES["empty_campaigns"], details
            
            details["campaigns_count"] = len(campaigns_df)
            details["validation_steps"].append(f"✓ {len(campaigns_df)} campaign rows found")
            
            # Check 3: Validate Portfolios sheet
            portfolios_df = bulk_data["Portfolios"]
            
            if portfolios_df.empty or len(portfolios_df) < 1:
                return False, ERROR_MESSAGES["empty_portfolios"], details
            
            details["portfolios_count"] = len(portfolios_df)
            details["validation_steps"].append(f"✓ {len(portfolios_df)} portfolio rows found")
            
            # Additional validation: Check for Portfolio ID columns
            if "Portfolio ID" not in campaigns_df.columns:
                return False, ERROR_MESSAGES["no_portfolio_id"].format("Campaigns"), details
            
            if "Portfolio ID" not in portfolios_df.columns:
                return False, ERROR_MESSAGES["no_portfolio_id"].format("Portfolios"), details
            
            if "Portfolio Name" not in portfolios_df.columns:
                return False, ERROR_MESSAGES["no_portfolio_name"], details
            
            details["validation_steps"].append("✓ Required ID columns present")
            
            # Success
            message = SUCCESS_MESSAGES["validation_passed"].format(
                details["campaigns_count"],
                details["portfolios_count"]
            )
            
            return True, message, details
            
        except Exception as e:
            self.logger.error(f"Validation error: {str(e)}")
            return False, f"Validation error: {str(e)}", details
