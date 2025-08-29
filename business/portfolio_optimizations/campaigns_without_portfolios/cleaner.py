"""Cleaner for Campaigns Without Portfolios optimization."""

import pandas as pd
from typing import Dict, Tuple, Any
import logging
from .constants import TARGET_ENTITY


class CampaignsWithoutPortfoliosCleaner:
    """Cleans and prepares data for Campaigns Without Portfolios optimization."""
    
    def __init__(self):
        self.logger = logging.getLogger("campaigns_without_portfolios.cleaner")
    
    def clean(self, bulk_data: Dict[str, pd.DataFrame]) -> Tuple[Dict[str, pd.DataFrame], Dict[str, Any]]:
        """
        Clean and filter data for processing.
        
        Args:
            bulk_data: Dictionary with sheet names as keys and DataFrames as values
            
        Returns:
            Tuple of (cleaned_data, cleaning_details)
        """
        details = {
            "original_campaigns": 0,
            "filtered_campaigns": 0,
            "entity_campaign_count": 0,
            "campaigns_without_portfolio": 0
        }
        
        try:
            cleaned_data = {}
            
            # Get the campaigns sheet
            campaigns_df = bulk_data["Sponsored Products Campaigns"].copy()
            
            details["original_campaigns"] = len(campaigns_df)
            
            # Filter campaigns to only Entity = Campaign
            campaigns_filtered = campaigns_df[campaigns_df["Entity"] == TARGET_ENTITY].copy()
            details["entity_campaign_count"] = len(campaigns_filtered)
            details["filtered_campaigns"] = details["original_campaigns"] - details["entity_campaign_count"]
            
            self.logger.info(f"Filtered to {len(campaigns_filtered)} campaigns with Entity = '{TARGET_ENTITY}'")
            
            # Clean Portfolio IDs - ensure they're strings and handle NaN/empty values
            if "Portfolio ID" in campaigns_filtered.columns:
                # Convert to string, but keep NaN as NaN
                campaigns_filtered["Portfolio ID"] = campaigns_filtered["Portfolio ID"].apply(
                    lambda x: str(x).strip() if pd.notna(x) and str(x).strip() != '' else None
                )
                
                # Remove .0 decimal formatting from numeric IDs
                campaigns_filtered["Portfolio ID"] = campaigns_filtered["Portfolio ID"].apply(
                    lambda x: x.replace('.0', '') if pd.notna(x) and x.endswith('.0') else x
                )
                
                # Count campaigns without portfolio
                details["campaigns_without_portfolio"] = campaigns_filtered["Portfolio ID"].isna().sum()
            
            self.logger.info(f"Found {details['campaigns_without_portfolio']} campaigns without portfolio")
            
            # Store cleaned data
            cleaned_data["Sponsored Products Campaigns"] = campaigns_filtered
            
            # Also include the full original dataframe for output
            cleaned_data["Sponsored Products Campaigns Full"] = campaigns_df
            
            return cleaned_data, details
            
        except Exception as e:
            self.logger.error(f"Error during cleaning: {str(e)}")
            raise
    
    def _is_empty_portfolio_id(self, value) -> bool:
        """
        Check if Portfolio ID is empty or invalid.
        
        Args:
            value: The Portfolio ID value to check
            
        Returns:
            True if the value is empty/invalid, False otherwise
        """
        if pd.isna(value):
            return True
        
        str_value = str(value).strip()
        if str_value == '' or str_value.lower() in ['nan', 'none', 'null']:
            return True
        
        return False
