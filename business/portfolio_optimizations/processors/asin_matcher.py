"""ASIN matcher processor for Organize Top Campaigns optimization."""

import pandas as pd
import numpy as np
from typing import Dict, List
import logging
from ..constants import (
    SHEET_CAMPAIGNS_CLEANED, SHEET_PRODUCT_AD,
    COL_ENTITY, COL_CAMPAIGN_ID, COL_OPERATION,
    ENTITY_CAMPAIGN, ENTITY_PRODUCT_AD
)

COL_ASIN_PA = "ASIN PA"
COL_ASIN = "ASIN"


class AsinMatcher:
    """Matches ASINs between Campaign and Product Ad sheets using VLOOKUP logic."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def process(self, all_sheets: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """
        Add ASIN PA column to Campaign sheet with VLOOKUP logic.
        
        Step per spec:
        5a. Create ASIN PA column with VLOOKUP logic
        
        Args:
            all_sheets: Dictionary of sheet name to DataFrame
            
        Returns:
            Updated sheets with ASIN PA column added
        """
        self.logger.info("Starting ASIN matching process")
        
        # Work on copies
        updated_sheets = {}
        for sheet_name, df in all_sheets.items():
            updated_sheets[sheet_name] = df.copy()
        
        campaigns_df = updated_sheets[SHEET_CAMPAIGNS_CLEANED]
        product_ad_df = updated_sheets.get(SHEET_PRODUCT_AD)
        
        if product_ad_df is None:
            raise ValueError(f"Required sheet {SHEET_PRODUCT_AD} not found")
        
        # Add ASIN PA column
        self._add_asin_pa_column(campaigns_df, product_ad_df)
        
        self.logger.info("ASIN matching process complete")
        return updated_sheets
    
    def _add_asin_pa_column(self, campaigns_df: pd.DataFrame, product_ad_df: pd.DataFrame) -> None:
        """Add ASIN PA column to the right of Operation column with blue header."""
        self.logger.info("Adding ASIN PA column with VLOOKUP logic")
        
        # Find Operation column position
        operation_col_idx = campaigns_df.columns.get_loc(COL_OPERATION)
        
        # Insert ASIN PA column to the right of Operation column (position 3)
        # Per spec: "מוסיפים עמודה מימין לעמודה Operation"
        asin_pa_position = operation_col_idx + 1  # Right after Operation
        campaigns_df.insert(asin_pa_position, COL_ASIN_PA, "")
        
        # Create lookup dictionary from Product Ad sheet for faster matching
        product_ads = product_ad_df[product_ad_df[COL_ENTITY] == ENTITY_PRODUCT_AD].copy()
        
        # Create Campaign ID -> ASIN mapping
        asin_lookup = {}
        for idx, row in product_ads.iterrows():
            campaign_id = str(row[COL_CAMPAIGN_ID])
            asin = str(row[COL_ASIN]) if pd.notna(row[COL_ASIN]) else ""
            
            # If multiple ASINs for same campaign, take the first one (VLOOKUP behavior)
            if campaign_id not in asin_lookup:
                asin_lookup[campaign_id] = asin
        
        # Apply VLOOKUP logic to each campaign row
        matches_found = 0
        for idx, row in campaigns_df.iterrows():
            if row[COL_ENTITY] == ENTITY_CAMPAIGN:
                campaign_id = str(row[COL_CAMPAIGN_ID])
                
                # Look up ASIN for this Campaign ID
                asin = asin_lookup.get(campaign_id, "")
                campaigns_df.at[idx, COL_ASIN_PA] = asin
                
                if asin:
                    matches_found += 1
        
        self.logger.info(f"ASIN PA column added: {matches_found} ASIN matches found")
        
        # Note: Blue header coloring will be handled by the excel writer
        # The writer should detect ASIN PA column and apply blue formatting