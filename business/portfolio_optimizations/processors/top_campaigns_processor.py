"""Top campaigns processor for Organize Top Campaigns optimization."""

import pandas as pd
import numpy as np
from typing import Dict, List
import logging
from ..constants import (
    SHEET_CAMPAIGNS_CLEANED, COL_ENTITY, COL_OPERATION, ENTITY_CAMPAIGN,
    COL_PORTFOLIO_ID, COL_PORTFOLIO_NAME_INFO, OPERATION_UPDATE,
    ORGANIZE_TOP_CAMPAIGNS_PORTFOLIO_ID
)

COL_ASIN_PA = "ASIN PA"
COL_TOP = "Top"
COL_TOP_ASINS = "Top ASINs"
SHEET_TOP = "Top"


class TopCampaignsProcessor:
    """Processes Top column and creates Top sheet with template data."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.template_data = None
    
    def set_template_data(self, template_data: pd.DataFrame) -> None:
        """Set the template data to use for Top ASIN matching."""
        self.template_data = template_data
        self.logger.info(f"Template data set: {len(template_data)} ASINs")
    
    def process(self, all_sheets: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """
        Add Top column and create Top sheet with template data.
        
        Steps per spec:
        5b. Create Top column
        5c. Create Top sheet with template data
        5d. Fill Top column with VLOOKUP logic
        6. Update Portfolio IDs for matching campaigns
        
        Args:
            all_sheets: Dictionary of sheet name to DataFrame
            
        Returns:
            Updated sheets with Top column and Top sheet added
        """
        self.logger.info("Starting Top campaigns processing")
        
        if self.template_data is None:
            raise ValueError("Template data not set. Call set_template_data() first.")
        
        # Work on copies
        updated_sheets = {}
        for sheet_name, df in all_sheets.items():
            updated_sheets[sheet_name] = df.copy()
        
        campaigns_df = updated_sheets[SHEET_CAMPAIGNS_CLEANED]
        
        # Step 5b: Add Top column
        self._add_top_column(campaigns_df)
        
        # Step 5c: Create Top sheet with template data
        updated_sheets[SHEET_TOP] = self._create_top_sheet()
        
        # Step 5d: Fill Top column with VLOOKUP logic
        self._fill_top_column(campaigns_df)
        
        # Step 6: Update Portfolio IDs
        self._update_portfolio_ids(campaigns_df)
        
        self.logger.info("Top campaigns processing complete")
        return updated_sheets
    
    def _add_top_column(self, campaigns_df: pd.DataFrame) -> None:
        """Add Top column to the right of ASIN PA column."""
        self.logger.info("Adding Top column")
        
        # Find ASIN PA column position
        asin_pa_col_idx = campaigns_df.columns.get_loc(COL_ASIN_PA)
        
        # Insert Top column to the right of ASIN PA with NaN as default
        # This matches the example file where non-matching campaigns have NaN in Top column
        campaigns_df.insert(asin_pa_col_idx + 1, COL_TOP, pd.NA)
    
    def _create_top_sheet(self) -> pd.DataFrame:
        """Create Top sheet with template data."""
        self.logger.info("Creating Top sheet with template data")
        
        # Create a copy of template data for the Top sheet
        top_sheet = self.template_data.copy()
        
        # Ensure the column is named "Top ASINs"
        if COL_TOP_ASINS not in top_sheet.columns:
            # Assume first column contains the ASINs
            first_col = top_sheet.columns[0]
            top_sheet = top_sheet.rename(columns={first_col: COL_TOP_ASINS})
        
        self.logger.info(f"Top sheet created with {len(top_sheet)} ASIN entries")
        return top_sheet
    
    def _fill_top_column(self, campaigns_df: pd.DataFrame) -> None:
        """Fill Top column with V marks using VLOOKUP logic."""
        self.logger.info("Filling Top column with VLOOKUP logic")
        
        # Check if template data is empty or has no valid ASINs
        valid_template_asins = 0
        top_asins = set()
        
        for asin in self.template_data[COL_TOP_ASINS]:
            if pd.notna(asin) and str(asin).strip():
                clean_asin = str(asin).strip()
                top_asins.add(clean_asin)
                valid_template_asins += 1
        
        self.logger.info(f"Template contains {valid_template_asins} valid ASINs")
        
        # If no valid template ASINs, skip marking any campaigns
        if valid_template_asins == 0:
            self.logger.info("No valid ASINs in template - no campaigns will be marked with 'V'")
            return
        
        # Apply VLOOKUP logic to each campaign row
        matches_found = 0
        for idx, row in campaigns_df.iterrows():
            if row[COL_ENTITY] == ENTITY_CAMPAIGN:
                asin_pa = str(row[COL_ASIN_PA]).strip() if pd.notna(row[COL_ASIN_PA]) else ""
                
                # Check if ASIN PA exists in Top ASINs
                if asin_pa and asin_pa in top_asins:
                    campaigns_df.at[idx, COL_TOP] = "v"
                    matches_found += 1
                # If not found or empty, leave empty (default)
        
        self.logger.info(f"Top column filled: {matches_found} campaigns marked with 'v'")
    
    def _update_portfolio_ids(self, campaigns_df: pd.DataFrame) -> None:
        """
        Update Portfolio IDs for campaigns matching Part 2 criteria.
        
        Step 6: Portfolio ID Updates
        - Criteria 1: Top = "v" AND Portfolio Name does NOT contain "manual"
        - Criteria 2: Top = empty AND Portfolio Name contains "manual"
        - Update: Portfolio ID = 198280442127929, Operation = "update"
        """
        self.logger.info("Starting Portfolio ID updates (Step 6)")
        
        # Convert Operation column to object type to avoid dtype warnings
        if campaigns_df[COL_OPERATION].dtype != 'object':
            campaigns_df[COL_OPERATION] = campaigns_df[COL_OPERATION].astype('object')
        
        total_updates = 0
        
        # Criteria 1: Top = "v" AND Portfolio Name does NOT contain "manual"
        criteria1_mask = (
            (campaigns_df[COL_TOP] == "v") &
            (~campaigns_df[COL_PORTFOLIO_NAME_INFO].astype(str).str.contains("manual", na=False, case=False))
        )
        criteria1_campaigns = campaigns_df[criteria1_mask]
        
        # Update Portfolio ID and Operation for Criteria 1
        # Cast Portfolio ID to match column dtype (float64)
        campaigns_df.loc[criteria1_mask, COL_PORTFOLIO_ID] = float(ORGANIZE_TOP_CAMPAIGNS_PORTFOLIO_ID)
        campaigns_df.loc[criteria1_mask, COL_OPERATION] = OPERATION_UPDATE
        criteria1_count = len(criteria1_campaigns)
        total_updates += criteria1_count
        
        self.logger.info(f"Criteria 1 (Top=v, not manual): {criteria1_count} campaigns updated")
        
        # Criteria 2: Top = empty AND Portfolio Name contains "manual"
        criteria2_mask = (
            (campaigns_df[COL_TOP].isna() | (campaigns_df[COL_TOP] == "")) &
            (campaigns_df[COL_PORTFOLIO_NAME_INFO].astype(str).str.contains("manual", na=False, case=False))
        )
        criteria2_campaigns = campaigns_df[criteria2_mask]
        
        # Update Portfolio ID and Operation for Criteria 2
        # Cast Portfolio ID to match column dtype (float64)
        campaigns_df.loc[criteria2_mask, COL_PORTFOLIO_ID] = float(ORGANIZE_TOP_CAMPAIGNS_PORTFOLIO_ID)
        campaigns_df.loc[criteria2_mask, COL_OPERATION] = OPERATION_UPDATE
        criteria2_count = len(criteria2_campaigns)
        total_updates += criteria2_count
        
        self.logger.info(f"Criteria 2 (Top=empty, manual): {criteria2_count} campaigns updated")
        self.logger.info(f"Total Portfolio ID updates: {total_updates} campaigns")