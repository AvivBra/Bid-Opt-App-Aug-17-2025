"""Campaigns without portfolios optimization strategy."""

import pandas as pd
import numpy as np
from typing import Dict, List, Any
import logging
from ..contracts import OptimizationStrategy, OptimizationResult, PatchData, CellUpdate
from ..contract_validator import contract_validator
from ..constants import (
    SHEET_CAMPAIGNS_CLEANED, SHEET_PORTFOLIOS,
    COL_ENTITY, COL_CAMPAIGN_ID, COL_PORTFOLIO_ID, COL_PORTFOLIO_NAME,
    COL_OPERATION, COL_BUDGET_AMOUNT, COL_BUDGET_START_DATE,
    ENTITY_CAMPAIGN, ENTITY_PORTFOLIO, OPERATION_UPDATE,
    DEFAULT_PORTFOLIO_ID, DEFAULT_BUDGET_AMOUNT, DEFAULT_BUDGET_START_DATE,
    EXCLUDED_PORTFOLIO_NAMES
)


class CampaignsWithoutPortfoliosStrategy(OptimizationStrategy):
    """Strategy to assign campaigns without portfolios to a default portfolio."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_name(self) -> str:
        return "campaigns_without_portfolios"
    
    def get_description(self) -> str:
        return "Assigns campaigns without portfolios to a default portfolio"
    
    def get_required_sheets(self) -> List[str]:
        return [SHEET_CAMPAIGNS_CLEANED]
    
    @contract_validator  
    def run(self, all_sheets: Dict[str, pd.DataFrame]) -> OptimizationResult:
        """Run the campaigns without portfolios optimization."""
        self.logger.info("Starting Campaigns Without Portfolios optimization")
        
        # Get campaigns sheet
        campaigns_df = all_sheets[SHEET_CAMPAIGNS_CLEANED].copy()
        
        # Apply EXACT specification criteria per PRD/Portfilio Optimizer/Logic/Campaigns w:o Portfolios logic.md
        # Lines 15-19: Find campaigns where:
        # - Tab: Campaign (this sheet)
        # - Entity: Campaign  
        # - Portfolio ID: Empty (ריק)
        campaigns_without_portfolio = campaigns_df[
            (campaigns_df[COL_ENTITY] == ENTITY_CAMPAIGN) &
            ((campaigns_df[COL_PORTFOLIO_ID] == '') | 
             (campaigns_df[COL_PORTFOLIO_ID].isna()) |
             (campaigns_df[COL_PORTFOLIO_ID] == 'nan'))
        ]
        
        self.logger.info(f"Using proper specification criteria:")
        self.logger.info(f"  - Entity = 'Campaign' AND Portfolio ID = Empty")
        self.logger.info(f"  - Found matches: {len(campaigns_without_portfolio)} campaigns")
        
        if len(campaigns_without_portfolio) > 0:
            found_campaign_ids = list(campaigns_without_portfolio[COL_CAMPAIGN_ID].astype(str))
            self.logger.info(f"  - Matched Campaign IDs: {found_campaign_ids}")
        else:
            self.logger.info("No campaigns found matching specification criteria - this is expected for this input data")
        
        self.logger.info(f"Found {len(campaigns_without_portfolio)} campaigns without portfolio")
        
        # Update campaigns per specification steps 2-3
        updates = []
        for idx, row in campaigns_without_portfolio.iterrows():
            update = CellUpdate(
                row_index=None,
                key_column=COL_CAMPAIGN_ID,
                key_value=str(row[COL_CAMPAIGN_ID]),
                cell_changes={
                    COL_PORTFOLIO_ID: DEFAULT_PORTFOLIO_ID,
                    COL_OPERATION: OPERATION_UPDATE
                }
            )
            updates.append(update)
        
        # Apply updates directly to the data to get updated campaigns for Terminal sheet
        updated_campaigns_df = campaigns_df.copy()
        
        # Apply the updates first
        for update in updates:
            # Find the row by Campaign ID
            mask = updated_campaigns_df[COL_CAMPAIGN_ID].astype(str) == update.key_value
            matching_rows = updated_campaigns_df[mask]
            
            if len(matching_rows) > 0:
                row_idx = matching_rows.index[0]
                # Apply the updates
                for column, new_value in update.cell_changes.items():
                    updated_campaigns_df.at[row_idx, column] = new_value
        
        # Step 4: Create Terminal sheet and move updated campaigns there
        # Only create Terminal sheet if campaigns were found and updated
        if len(campaigns_without_portfolio) > 0:
            target_campaign_ids = list(campaigns_without_portfolio[COL_CAMPAIGN_ID].astype(str))
            self._create_terminal_sheet(all_sheets, updated_campaigns_df, target_campaign_ids)
        else:
            # No campaigns found - create empty Terminal sheet per specification
            self._create_empty_terminal_sheet(all_sheets)
        
        # Create patch for remaining updates (the orchestrator will still apply these)
        patch = PatchData(
            sheet_name=SHEET_CAMPAIGNS_CLEANED,
            updates=updates
        )
        
        # Create result
        result = OptimizationResult(
            result_type="campaigns",
            merge_keys=[COL_CAMPAIGN_ID],
            patch=patch,
            metrics={
                "rows_checked": len(campaigns_df[campaigns_df[COL_ENTITY] == ENTITY_CAMPAIGN]),
                "rows_updated": len(updates),
                "cells_updated": len(updates) * 2  # 2 cells per row
            },
            messages=[
                f"Found {len(campaigns_without_portfolio)} campaigns without portfolio",
                f"Updated {len(updates)} campaigns and moved them to Terminal sheet"
            ]
        )
        
        self.logger.info(f"Campaigns Without Portfolios optimization complete: {len(updates)} campaigns updated")
        return result
    
    def _create_terminal_sheet(self, all_sheets: Dict[str, pd.DataFrame], updated_campaigns_df: pd.DataFrame, target_campaign_ids: List[str]) -> None:
        """
        Step 4: Create Terminal sheet and move updated campaigns there.
        
        Per PRD specification:
        - Create a new sheet named "Terminal"  
        - Move only the campaigns that were updated in this optimization
        - Ensure updated campaigns exist only in Terminal, not in Campaign sheet
        """
        self.logger.info("Step 4: Creating Terminal sheet and moving updated campaigns")
        
        campaigns_df = all_sheets[SHEET_CAMPAIGNS_CLEANED]
        
        # Find campaigns that match our target IDs (these are the ones we updated)
        terminal_campaigns_mask = (
            (campaigns_df[COL_ENTITY] == ENTITY_CAMPAIGN) & 
            (campaigns_df[COL_CAMPAIGN_ID].astype(str).isin(target_campaign_ids))
        )
        
        terminal_campaigns = campaigns_df[terminal_campaigns_mask].copy()
        remaining_campaigns = campaigns_df[~terminal_campaigns_mask].copy()
        
        # Apply the updates to terminal campaigns (Portfolio ID and Operation)
        for idx, row in terminal_campaigns.iterrows():
            terminal_campaigns.at[idx, COL_PORTFOLIO_ID] = DEFAULT_PORTFOLIO_ID
            terminal_campaigns.at[idx, COL_OPERATION] = OPERATION_UPDATE
        
        # Create Terminal sheet with updated campaigns
        all_sheets["Terminal"] = terminal_campaigns
        
        # Update Campaign sheet to remove moved campaigns  
        all_sheets[SHEET_CAMPAIGNS_CLEANED] = remaining_campaigns
        
        self.logger.info(f"Created Terminal sheet with {len(terminal_campaigns)} campaigns")
        self.logger.info(f"Remaining Campaign sheet has {len(remaining_campaigns)} campaigns")
    
    def _create_empty_terminal_sheet(self, all_sheets: Dict[str, pd.DataFrame]) -> None:
        """
        Create empty Terminal sheet when no campaigns match the specification criteria.
        
        Per PRD specification:
        - Create Terminal sheet even if no campaigns are found
        - Use same structure as Campaign sheet but with 0 rows
        """
        self.logger.info("Creating empty Terminal sheet (no campaigns match specification criteria)")
        
        campaigns_df = all_sheets[SHEET_CAMPAIGNS_CLEANED]
        
        # Create empty Terminal sheet with same columns as Campaign sheet
        empty_terminal = pd.DataFrame(columns=campaigns_df.columns)
        
        # Create Terminal sheet 
        all_sheets["Terminal"] = empty_terminal
        
        self.logger.info("Created empty Terminal sheet (0 campaigns)")
        self.logger.info(f"Campaign sheet unchanged: {len(campaigns_df)} campaigns")