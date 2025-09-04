"""Ads Count processor for Organize Top Campaigns optimization."""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import logging
from ..constants import (
    SHEET_CAMPAIGNS_CLEANED, SHEET_PRODUCT_AD,
    COL_ENTITY, COL_CAMPAIGN_ID, COL_PORTFOLIO_NAME_INFO, COL_OPERATION,
    ENTITY_CAMPAIGN, ENTITY_PRODUCT_AD
)

COL_ADS_COUNT = "Ads Count"

# Portfolio names to ignore during processing
IGNORED_PORTFOLIO_NAMES = ["Pause", "Terminal", "Top Terminal"]

# Portfolio name patterns to ignore (Step 4: keep but exclude from transformations)
DELETE_PATTERNS = ["Flat", "Same", "Defense", "Offense"]  # Keeping same name for compatibility


class AdsCountProcessor:
    """Processes Ads Count column and filters rows per Organize Top Campaigns spec."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def process(self, all_sheets: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """
        Process Ads Count column and apply filtering logic.
        
        Steps per spec:
        3. Add Ads Count column with COUNTIFS logic
        4. Delete additional rows based on portfolio patterns
        
        Args:
            all_sheets: Dictionary of sheet name to DataFrame
            
        Returns:
            Updated sheets with Ads Count column and filtered rows
        """
        self.logger.info("Starting Ads Count processing")
        
        # Work on copies
        updated_sheets = {}
        for sheet_name, df in all_sheets.items():
            updated_sheets[sheet_name] = df.copy()
        
        campaigns_df = updated_sheets[SHEET_CAMPAIGNS_CLEANED]
        product_ad_df = updated_sheets.get(SHEET_PRODUCT_AD)
        
        if product_ad_df is None:
            raise ValueError(f"Required sheet {SHEET_PRODUCT_AD} not found")
        
        # Step 3: Add Ads Count column and populate with COUNTIFS logic
        self._add_ads_count_column(campaigns_df, product_ad_df)
        
        # Filter rows based on Ads Count and ignore rules
        campaigns_df_filtered = self._filter_by_ads_count(campaigns_df)
        
        # Step 4: Delete additional rows based on portfolio patterns
        campaigns_df_final = self._filter_by_portfolio_patterns(campaigns_df_filtered)
        
        # Step 5: Keep the Ads Count column in the final output (per spec requirement)
        # The Ads Count column should remain visible in the final output file
        self.logger.info("Keeping Ads Count column in final output as per spec")
        
        updated_sheets[SHEET_CAMPAIGNS_CLEANED] = campaigns_df_final
        
        self.logger.info(f"Ads Count processing complete: {len(campaigns_df)} -> {len(campaigns_df_final)} rows")
        return updated_sheets
    
    def _add_ads_count_column(self, campaigns_df: pd.DataFrame, product_ad_df: pd.DataFrame) -> None:
        """Add Ads Count column to the right of Campaign ID column."""
        self.logger.info("Adding Ads Count column with COUNTIFS logic")
        
        # Find Campaign ID column position to match expected order
        # Expected: Operation, Campaign ID, Ads Count, ASIN PA, Top
        campaign_id_col_idx = campaigns_df.columns.get_loc(COL_CAMPAIGN_ID)
        
        # Insert Ads Count column to the right of Campaign ID
        campaigns_df.insert(campaign_id_col_idx + 1, COL_ADS_COUNT, 0)
        
        # Filter Product Ad sheet to only Product Ad entities
        product_ads = product_ad_df[product_ad_df[COL_ENTITY] == ENTITY_PRODUCT_AD].copy()
        
        # Calculate COUNTIFS for each campaign row
        for idx, row in campaigns_df.iterrows():
            if row[COL_ENTITY] == ENTITY_CAMPAIGN:
                campaign_id = str(row[COL_CAMPAIGN_ID])
                
                # Count occurrences in Product Ad sheet with same Campaign ID
                matching_ads = product_ads[
                    product_ads[COL_CAMPAIGN_ID].astype(str) == campaign_id
                ]
                count = len(matching_ads)
                
                campaigns_df.at[idx, COL_ADS_COUNT] = count
    
    def _filter_by_ads_count(self, campaigns_df: pd.DataFrame) -> pd.DataFrame:
        """Filter rows based on Ads Count and ignore rules."""
        self.logger.info("Filtering rows based on Ads Count and ignore rules")
        
        # Identify rows to ignore
        ignore_mask = campaigns_df[COL_PORTFOLIO_NAME_INFO].isin(IGNORED_PORTFOLIO_NAMES)
        
        # Identify rows to delete (Ads Count > 1 and not in ignore list)
        delete_mask = (campaigns_df[COL_ADS_COUNT] > 1) & (~ignore_mask)
        
        # Keep rows that are not marked for deletion
        filtered_df = campaigns_df[~delete_mask].copy()
        
        self.logger.info(f"Filtered {delete_mask.sum()} rows with Ads Count > 1 (ignored {ignore_mask.sum()} rows)")
        return filtered_df
    
    def _filter_by_portfolio_patterns(self, campaigns_df: pd.DataFrame) -> pd.DataFrame:
        """Apply Step 4: Ignore rows with portfolio name patterns (keep them but exclude from transformations)."""
        self.logger.info("Step 4: Identifying rows to ignore based on portfolio name patterns")
        
        # No filtering/deletion in Step 4 - campaigns with patterns are now IGNORED, not deleted
        # Per updated specification: "מתעלמים גם מכל שורה..." (Also ignore any row...)
        # This means keep all campaigns but mark pattern-based ones as ignored for transformations
        
        pattern_ignore_count = 0
        for pattern in DELETE_PATTERNS:
            pattern_mask = campaigns_df[COL_PORTFOLIO_NAME_INFO].str.contains(pattern, na=False)
            pattern_ignore_count += pattern_mask.sum()
        
        self.logger.info(f"Step 4 complete: {pattern_ignore_count} rows with patterns {DELETE_PATTERNS} will be ignored (kept but excluded from transformations)")
        
        # Return all campaigns - no deletion in Step 4 anymore
        return campaigns_df.copy()