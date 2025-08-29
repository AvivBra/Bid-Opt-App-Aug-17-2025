"""Processor for Campaigns Without Portfolios optimization."""

import pandas as pd
import numpy as np
from typing import Dict, List, Any
import logging
from .constants import TARGET_PORTFOLIO_ID, UPDATE_OPERATION, TARGET_ENTITY


class CampaignsWithoutPortfoliosProcessor:
    """Processes Campaigns Without Portfolios optimization logic."""
    
    def __init__(self):
        self.logger = logging.getLogger("campaigns_without_portfolios.processor")
        self.updated_indices = []
        self.processing_stats = {}
    
    def process(
        self,
        cleaned_data: Dict[str, pd.DataFrame],
        combined_with_empty_portfolios: bool = False
    ) -> Dict[str, pd.DataFrame]:
        """
        Process the optimization logic.
        
        Args:
            cleaned_data: Dictionary with cleaned DataFrames
            combined_with_empty_portfolios: Whether running with Empty Portfolios
            
        Returns:
            Dictionary with processed DataFrames
        """
        # Get the filtered campaigns (Entity = Campaign only)
        campaigns_filtered = cleaned_data["Sponsored Products Campaigns"].copy()
        
        # Get the full campaigns dataframe for output
        campaigns_full = cleaned_data["Sponsored Products Campaigns Full"].copy()
        
        # Reset updated indices
        self.updated_indices = []
        
        # Find campaigns without portfolio (in filtered data)
        campaigns_without_portfolio_mask = campaigns_filtered["Portfolio ID"].isna()
        campaigns_without_portfolio = campaigns_filtered[campaigns_without_portfolio_mask]
        
        self.logger.info(f"Found {len(campaigns_without_portfolio)} campaigns without portfolio")
        
        # Get the indices of these campaigns in the full dataframe
        if len(campaigns_without_portfolio) > 0:
            # Find matching rows in the full dataframe
            for idx, row in campaigns_without_portfolio.iterrows():
                # Find this campaign in the full dataframe
                mask = (
                    (campaigns_full["Entity"] == TARGET_ENTITY) &
                    (campaigns_full["Campaign ID"] == row["Campaign ID"])
                )
                full_indices = campaigns_full[mask].index.tolist()
                
                if full_indices:
                    full_idx = full_indices[0]
                    # Update Portfolio ID
                    campaigns_full.at[full_idx, "Portfolio ID"] = TARGET_PORTFOLIO_ID
                    # Set Operation to update
                    campaigns_full.at[full_idx, "Operation"] = UPDATE_OPERATION
                    # Track updated index
                    self.updated_indices.append(full_idx)
            
            self.logger.info(f"Updated {len(self.updated_indices)} campaigns with portfolio ID {TARGET_PORTFOLIO_ID}")
        
        # Store processing statistics
        self.processing_stats = {
            "total_campaigns": len(campaigns_filtered),
            "campaigns_without_portfolio": len(campaigns_without_portfolio),
            "campaigns_updated": len(self.updated_indices)
        }
        
        # Return processed data
        return {
            "Sponsored Products Campaigns": campaigns_filtered,
            "Sponsored Products Campaigns Full": campaigns_full
        }
    
    def get_updated_indices(self) -> List[int]:
        """
        Get the indices of rows that were updated.
        
        Returns:
            List of row indices that were modified
        """
        return self.updated_indices
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """
        Get processing statistics.
        
        Returns:
            Dictionary with processing statistics
        """
        return self.processing_stats
    
    def merge_with_empty_portfolios_results(
        self,
        campaigns_df: pd.DataFrame,
        empty_portfolios_indices: List[int]
    ) -> pd.DataFrame:
        """
        Merge with Empty Portfolios optimization results if running combined.
        
        Args:
            campaigns_df: Current processed campaigns DataFrame
            empty_portfolios_indices: Indices updated by Empty Portfolios
            
        Returns:
            Merged DataFrame
        """
        # The dataframes are already working on the same base,
        # so we just need to track all updated indices
        all_updated_indices = list(set(self.updated_indices + empty_portfolios_indices))
        
        self.logger.info(
            f"Combined optimization: {len(all_updated_indices)} total rows updated "
            f"({len(empty_portfolios_indices)} from Empty Portfolios, "
            f"{len(self.updated_indices)} from Campaigns Without Portfolios)"
        )
        
        # Update the tracked indices
        self.updated_indices = all_updated_indices
        
        return campaigns_df
