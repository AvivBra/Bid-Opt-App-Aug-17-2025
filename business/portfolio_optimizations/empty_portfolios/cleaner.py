"""Cleaner for Empty Portfolios optimization."""

import pandas as pd
from typing import Dict, Tuple, Any
import logging
from .constants import TARGET_ENTITY


class EmptyPortfoliosCleaner:
    """Cleans and prepares data for Empty Portfolios optimization."""
    
    def __init__(self):
        self.logger = logging.getLogger("empty_portfolios.cleaner")
    
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
            "portfolios_count": 0
        }
        
        try:
            cleaned_data = {}
            
            # Get the sheets
            campaigns_df = bulk_data["Sponsored Products Campaigns"].copy()
            portfolios_df = bulk_data["Portfolios"].copy()
            
            details["original_campaigns"] = len(campaigns_df)
            details["portfolios_count"] = len(portfolios_df)
            
            # Filter campaigns to only Entity = Campaign
            campaigns_filtered = campaigns_df[campaigns_df["Entity"] == TARGET_ENTITY].copy()
            details["entity_campaign_count"] = len(campaigns_filtered)
            details["filtered_campaigns"] = details["original_campaigns"] - details["entity_campaign_count"]
            
            self.logger.info(f"Filtered to {len(campaigns_filtered)} campaigns with Entity = '{TARGET_ENTITY}'")
            
            # Clean Portfolio IDs - ensure they're strings and remove decimal formatting
            if "Portfolio ID" in campaigns_filtered.columns:
                # Convert to string and remove .0 decimal formatting
                campaigns_filtered["Portfolio ID"] = campaigns_filtered["Portfolio ID"].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
            
            if "Portfolio ID" in portfolios_df.columns:
                # Convert to string and remove .0 decimal formatting  
                portfolios_df["Portfolio ID"] = portfolios_df["Portfolio ID"].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
            
            # Clean Portfolio Names
            if "Portfolio Name" in portfolios_df.columns:
                portfolios_df["Portfolio Name"] = portfolios_df["Portfolio Name"].astype(str).str.strip()
            
            # Ensure required columns exist in Portfolios for updates
            if "Operation" not in portfolios_df.columns:
                portfolios_df["Operation"] = ""
            
            if "Budget Amount" not in portfolios_df.columns:
                portfolios_df["Budget Amount"] = ""
            
            if "Budget Start Date" not in portfolios_df.columns:
                portfolios_df["Budget Start Date"] = ""
            
            # Store cleaned data
            cleaned_data["Sponsored Products Campaigns"] = campaigns_filtered
            cleaned_data["Portfolios"] = portfolios_df
            
            self.logger.info(f"Cleaning complete: {details['entity_campaign_count']} campaigns, {details['portfolios_count']} portfolios")
            
            return cleaned_data, details
            
        except Exception as e:
            self.logger.error(f"Cleaning error: {str(e)}")
            raise
