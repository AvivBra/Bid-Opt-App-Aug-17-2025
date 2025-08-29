"""Validator for Campaigns Without Portfolios optimization."""

import pandas as pd
from typing import Dict, Tuple, Any
import logging
from .constants import REQUIRED_COLUMNS


class CampaignsWithoutPortfoliosValidator:
    """Validates data for Campaigns Without Portfolios optimization."""
    
    def __init__(self):
        self.logger = logging.getLogger("campaigns_without_portfolios.validator")
    
    def validate(self, bulk_data: Dict[str, pd.DataFrame]) -> Tuple[bool, Dict[str, Any]]:
        """
        Validate the bulk data for processing.
        
        Args:
            bulk_data: Dictionary with sheet names as keys and DataFrames as values
            
        Returns:
            Tuple of (is_valid, validation_details)
        """
        details = {
            "campaigns_sheet_exists": False,
            "has_required_columns": False,
            "missing_columns": [],
            "total_rows": 0,
            "entity_campaign_rows": 0,
            "has_portfolio_id_column": False,
            "has_operation_column": False
        }
        
        try:
            # Check if Sponsored Products Campaigns sheet exists
            if "Sponsored Products Campaigns" not in bulk_data:
                self.logger.error("Missing 'Sponsored Products Campaigns' sheet")
                details["error"] = "Missing required sheet: Sponsored Products Campaigns"
                return False, details
            
            details["campaigns_sheet_exists"] = True
            campaigns_df = bulk_data["Sponsored Products Campaigns"]
            details["total_rows"] = len(campaigns_df)
            
            # Check for required columns
            missing_columns = []
            for col in REQUIRED_COLUMNS:
                if col not in campaigns_df.columns:
                    missing_columns.append(col)
            
            if missing_columns:
                details["missing_columns"] = missing_columns
                self.logger.error(f"Missing columns: {missing_columns}")
                return False, details
            
            details["has_required_columns"] = True
            
            # Specific checks for critical columns
            if "Portfolio ID" in campaigns_df.columns:
                details["has_portfolio_id_column"] = True
            else:
                self.logger.error("Missing critical column: Portfolio ID")
                return False, details
            
            if "Operation" in campaigns_df.columns:
                details["has_operation_column"] = True
            else:
                self.logger.error("Missing critical column: Operation")
                return False, details
            
            # Check Entity column and count Campaign entities
            if "Entity" in campaigns_df.columns:
                entity_campaign_mask = campaigns_df["Entity"] == "Campaign"
                details["entity_campaign_rows"] = entity_campaign_mask.sum()
                
                if details["entity_campaign_rows"] == 0:
                    self.logger.warning("No rows with Entity = 'Campaign' found")
                    details["warning"] = "No campaign entities found to process"
            else:
                self.logger.error("Missing Entity column")
                return False, details
            
            # Check Campaign ID column exists
            if "Campaign ID" not in campaigns_df.columns:
                self.logger.error("Missing Campaign ID column")
                return False, details
            
            # All validations passed
            self.logger.info(
                f"Validation passed: {details['total_rows']} total rows, "
                f"{details['entity_campaign_rows']} campaign entities"
            )
            
            return True, details
            
        except Exception as e:
            self.logger.error(f"Validation error: {str(e)}")
            details["error"] = str(e)
            return False, details
    
    def validate_portfolio_id_format(self, portfolio_id: Any) -> bool:
        """
        Validate if a portfolio ID has correct format.
        
        Args:
            portfolio_id: The portfolio ID to validate
            
        Returns:
            True if valid format, False otherwise
        """
        if pd.isna(portfolio_id):
            return False
        
        # Convert to string and check if it's numeric
        str_id = str(portfolio_id).strip()
        
        # Remove .0 if present (from Excel float conversion)
        if str_id.endswith('.0'):
            str_id = str_id[:-2]
        
        # Check if it's a valid numeric ID
        return str_id.isdigit() and len(str_id) > 0
