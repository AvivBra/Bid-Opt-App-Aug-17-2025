"""Empty portfolios optimization strategy."""

import pandas as pd
import numpy as np
from typing import Dict, List, Any
import logging
from ..contracts import OptimizationStrategy, OptimizationResult, PatchData, CellUpdate
from ..contract_validator import contract_validator
from ..constants import (
    SHEET_CAMPAIGNS_CLEANED, SHEET_PORTFOLIOS,
    COL_ENTITY, COL_CAMPAIGN_ID, COL_PORTFOLIO_ID, COL_PORTFOLIO_NAME,
    COL_OLD_PORTFOLIO_NAME, COL_CAMP_COUNT, COL_OPERATION, 
    COL_BUDGET_AMOUNT, COL_BUDGET_START_DATE, COL_BUDGET_POLICY,
    ENTITY_CAMPAIGN, ENTITY_PORTFOLIO, OPERATION_UPDATE,
    BUDGET_POLICY_NO_CAP, EXCLUDED_PORTFOLIO_NAMES
)


class EmptyPortfoliosStrategy(OptimizationStrategy):
    """Strategy to rename empty portfolios with numeric names following exact 6-step logic."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_name(self) -> str:
        return "empty_portfolios"
    
    def get_description(self) -> str:
        return "Identifies and renames empty portfolios with sequential numeric names using 6-step logic"
    
    def get_required_sheets(self) -> List[str]:
        return [SHEET_CAMPAIGNS_CLEANED, SHEET_PORTFOLIOS]
    
    @contract_validator
    def run(self, all_sheets: Dict[str, pd.DataFrame]) -> OptimizationResult:
        """Run the empty portfolios optimization using exact 6-step logic."""
        self.logger.info("Starting Empty Portfolios optimization with 6-step logic")
        
        # Get required sheets
        campaigns_df = all_sheets[SHEET_CAMPAIGNS_CLEANED].copy()
        portfolios_df = all_sheets[SHEET_PORTFOLIOS].copy()
        
        # Step 1: Add Camp Count column to Portfolios sheet
        self.logger.info("Step 1: Adding Camp Count column")
        if COL_CAMP_COUNT not in portfolios_df.columns:
            portfolios_df[COL_CAMP_COUNT] = 0
        
        # Step 2: Calculate campaign counts for each portfolio using COUNTIFS logic
        self.logger.info("Step 2: Calculating campaign counts using COUNTIFS logic")
        self._calculate_campaign_counts_countifs(portfolios_df, campaigns_df)
        
        # Step 3: Create Old Portfolio Name column and backup original names
        self.logger.info("Step 3: Creating Old Portfolio Name column and backing up names")
        if COL_OLD_PORTFOLIO_NAME not in portfolios_df.columns:
            portfolios_df[COL_OLD_PORTFOLIO_NAME] = portfolios_df[COL_PORTFOLIO_NAME]
        
        # Step 4: Find empty portfolios and assign new numeric names
        self.logger.info("Step 4: Finding empty portfolios and assigning new names")
        empty_portfolios_mask = self._find_empty_portfolios(portfolios_df)
        
        if not empty_portfolios_mask.any():
            self.logger.info("No empty portfolios found that need renaming")
            return self._create_empty_result()
        
        # Generate new numeric names
        new_names = self._generate_new_numeric_names(portfolios_df, empty_portfolios_mask.sum())
        
        # Apply new names to empty portfolios
        empty_portfolio_indices = portfolios_df[empty_portfolios_mask].index
        portfolios_df.loc[empty_portfolios_mask, COL_PORTFOLIO_NAME] = new_names
        
        self.logger.info(f"Found {len(empty_portfolio_indices)} empty portfolios to rename")
        
        # Create updates for ALL portfolio rows to populate new columns
        updates = []
        
        # First, update all portfolio rows with Camp Count and Old Portfolio Name
        for idx, row in portfolios_df.iterrows():
            if row[COL_ENTITY] == ENTITY_PORTFOLIO:
                cell_changes = {
                    COL_OLD_PORTFOLIO_NAME: str(row[COL_OLD_PORTFOLIO_NAME]),
                    COL_CAMP_COUNT: str(int(row[COL_CAMP_COUNT]))  # Convert to string to match expected format
                }
                
                # Steps 5 & 6: For empty portfolios, add additional changes
                if idx in empty_portfolio_indices:
                    new_name = new_names[list(empty_portfolio_indices).index(idx)]
                    cell_changes[COL_PORTFOLIO_NAME] = new_name
                    cell_changes[COL_OPERATION] = OPERATION_UPDATE
                    cell_changes[COL_BUDGET_POLICY] = BUDGET_POLICY_NO_CAP
                    
                    # Step 6: Clear budget fields if they have values
                    if pd.notna(row[COL_BUDGET_AMOUNT]) and str(row[COL_BUDGET_AMOUNT]).strip():
                        cell_changes[COL_BUDGET_AMOUNT] = ""
                    
                    if pd.notna(row[COL_BUDGET_START_DATE]) and str(row[COL_BUDGET_START_DATE]).strip():
                        cell_changes[COL_BUDGET_START_DATE] = ""
                
                update = CellUpdate(
                    row_index=idx,
                    key_column=COL_PORTFOLIO_ID,
                    key_value=str(row[COL_PORTFOLIO_ID]),
                    cell_changes=cell_changes
                )
                updates.append(update)
        
        # Create patch
        patch = PatchData(
            sheet_name=SHEET_PORTFOLIOS,
            updates=updates
        )
        
        # Create result
        result = OptimizationResult(
            result_type="portfolios",
            merge_keys=[COL_PORTFOLIO_ID],
            patch=patch,
            metrics={
                "rows_checked": len(portfolios_df[portfolios_df[COL_ENTITY] == ENTITY_PORTFOLIO]),
                "rows_updated": len(updates),
                "cells_updated": sum(len(update.cell_changes) for update in updates),
                "empty_portfolios_found": len(empty_portfolio_indices),
                "portfolios_renamed": len(updates)
            },
            messages=[
                f"Analyzed {len(portfolios_df)} portfolio rows",
                f"Found {len(empty_portfolio_indices)} empty portfolios (Camp Count = 0)",
                f"Renamed {len(updates)} portfolios with numeric names",
                f"Updated Budget Policy to 'No Cap' for modified portfolios",
                f"Cleared budget fields where necessary"
            ]
        )
        
        self.logger.info(f"Empty Portfolios optimization complete: {len(updates)} portfolios updated")
        return result
    
    def _calculate_campaign_counts_countifs(self, portfolios_df: pd.DataFrame, campaigns_df: pd.DataFrame) -> None:
        """Calculate campaign counts using COUNTIFS logic (Step 2)."""
        # Filter to Campaign entities only
        campaign_entities = campaigns_df[campaigns_df[COL_ENTITY] == ENTITY_CAMPAIGN]
        
        # For each portfolio, count campaigns with matching Portfolio ID
        for idx, row in portfolios_df.iterrows():
            if row[COL_ENTITY] == ENTITY_PORTFOLIO:
                portfolio_id = str(row[COL_PORTFOLIO_ID])
                
                # COUNTIFS equivalent: count campaigns where Portfolio ID matches
                matching_campaigns = campaign_entities[
                    campaign_entities[COL_PORTFOLIO_ID].astype(str) == portfolio_id
                ]
                count = len(matching_campaigns)
                
                portfolios_df.at[idx, COL_CAMP_COUNT] = count
    
    def _find_empty_portfolios(self, portfolios_df: pd.DataFrame) -> pd.Series:
        """Find portfolios that meet empty criteria (Step 4)."""
        # Condition 1: Camp Count = 0
        condition1 = portfolios_df[COL_CAMP_COUNT] == 0
        
        # Condition 2: Portfolio Name is not "Paused", "Terminal", "Top Terminal", or a number
        condition2_excluded_names = ~portfolios_df[COL_PORTFOLIO_NAME].isin(EXCLUDED_PORTFOLIO_NAMES)
        condition2_not_number = ~portfolios_df[COL_PORTFOLIO_NAME].astype(str).str.isdigit()
        condition2 = condition2_excluded_names & condition2_not_number
        
        # Only Portfolio entities
        portfolio_entity_condition = portfolios_df[COL_ENTITY] == ENTITY_PORTFOLIO
        
        return portfolio_entity_condition & condition1 & condition2
    
    def _generate_new_numeric_names(self, portfolios_df: pd.DataFrame, count_needed: int) -> List[str]:
        """Generate new numeric names that don't exist yet (Step 4)."""
        # Find all existing numeric portfolio names
        existing_numeric = set()
        for name in portfolios_df[COL_PORTFOLIO_NAME]:
            name_str = str(name).strip()
            if name_str.isdigit():
                existing_numeric.add(int(name_str))
        
        # Generate new numeric names starting from 1
        new_names = []
        next_number = 1
        
        for _ in range(count_needed):
            # Find next available number
            while next_number in existing_numeric:
                next_number += 1
            
            new_names.append(str(next_number))
            existing_numeric.add(next_number)
            next_number += 1
        
        return new_names
    
    def _create_empty_result(self) -> OptimizationResult:
        """Create empty result when no changes are needed."""
        return OptimizationResult(
            result_type="portfolios",
            merge_keys=[COL_PORTFOLIO_ID],
            patch=PatchData(sheet_name=SHEET_PORTFOLIOS, updates=[]),
            metrics={
                "rows_checked": 0,
                "rows_updated": 0,
                "cells_updated": 0,
                "empty_portfolios_found": 0,
                "portfolios_renamed": 0
            },
            messages=["No empty portfolios found that need renaming"]
        )