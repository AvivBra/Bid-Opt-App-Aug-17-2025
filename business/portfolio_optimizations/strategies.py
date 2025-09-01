"""Portfolio optimization strategies."""

import pandas as pd
import numpy as np
from typing import Dict, List, Any
import logging
from .contracts import OptimizationStrategy, OptimizationResult, PatchData, CellUpdate
from .contract_validator import contract_validator
from .constants import (
    SHEET_CAMPAIGNS_CLEANED, SHEET_PORTFOLIOS,
    COL_ENTITY, COL_CAMPAIGN_ID, COL_PORTFOLIO_ID, COL_PORTFOLIO_NAME,
    COL_OPERATION, COL_BUDGET_AMOUNT, COL_BUDGET_START_DATE,
    ENTITY_CAMPAIGN, ENTITY_PORTFOLIO, OPERATION_UPDATE,
    DEFAULT_PORTFOLIO_ID, DEFAULT_BUDGET_AMOUNT, DEFAULT_BUDGET_START_DATE,
    EXCLUDED_PORTFOLIO_NAMES
)


class EmptyPortfoliosStrategy(OptimizationStrategy):
    """Strategy to rename empty portfolios with numeric names."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_name(self) -> str:
        return "empty_portfolios"
    
    def get_description(self) -> str:
        return "Identifies and renames empty portfolios with sequential numeric names"
    
    def get_required_sheets(self) -> List[str]:
        return [SHEET_CAMPAIGNS_CLEANED, SHEET_PORTFOLIOS]
    
    @contract_validator
    def run(self, all_sheets: Dict[str, pd.DataFrame]) -> OptimizationResult:
        """Run the empty portfolios optimization."""
        self.logger.info("Starting Empty Portfolios optimization")
        
        # Get required sheets
        campaigns_df = all_sheets[SHEET_CAMPAIGNS_CLEANED].copy()
        portfolios_df = all_sheets[SHEET_PORTFOLIOS].copy()
        
        # Find portfolios with campaigns
        campaign_entities = campaigns_df[campaigns_df[COL_ENTITY] == ENTITY_CAMPAIGN]
        portfolios_with_campaigns = set(campaign_entities[COL_PORTFOLIO_ID].dropna().astype(str))
        
        # Find all portfolios (excluding special ones)
        all_portfolios = portfolios_df[
            (~portfolios_df[COL_PORTFOLIO_NAME].isin(EXCLUDED_PORTFOLIO_NAMES)) &
            (portfolios_df[COL_ENTITY] == ENTITY_PORTFOLIO)
        ]
        
        # Find empty portfolios
        empty_portfolios = all_portfolios[
            ~all_portfolios[COL_PORTFOLIO_ID].astype(str).isin(portfolios_with_campaigns)
        ]
        
        self.logger.info(f"Found {len(empty_portfolios)} empty portfolios")
        
        # Find existing numeric portfolio names
        existing_numeric = set()
        for name in portfolios_df[COL_PORTFOLIO_NAME]:
            if str(name).isdigit():
                existing_numeric.add(int(name))
        
        # Generate new numeric names
        updates = []
        next_number = 1
        
        for idx, row in empty_portfolios.iterrows():
            # Find next available number
            while next_number in existing_numeric:
                next_number += 1
            
            # Create update for this portfolio
            update = CellUpdate(
                row_index=idx,
                key_column=COL_PORTFOLIO_ID,
                key_value=str(row[COL_PORTFOLIO_ID]),
                cell_changes={
                    COL_PORTFOLIO_NAME: str(next_number),
                    COL_OPERATION: OPERATION_UPDATE,
                    COL_BUDGET_AMOUNT: DEFAULT_BUDGET_AMOUNT,
                    COL_BUDGET_START_DATE: DEFAULT_BUDGET_START_DATE
                }
            )
            updates.append(update)
            existing_numeric.add(next_number)
            next_number += 1
        
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
                "rows_checked": len(all_portfolios),
                "rows_updated": len(updates),
                "cells_updated": len(updates) * 4  # 4 cells per row
            },
            messages=[
                f"Found {len(empty_portfolios)} empty portfolios",
                f"Renamed {len(updates)} portfolios with numeric names"
            ]
        )
        
        self.logger.info(f"Empty Portfolios optimization complete: {len(updates)} portfolios updated")
        return result


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
        
        # Find campaigns without portfolio
        campaigns_mask = (
            (campaigns_df[COL_ENTITY] == ENTITY_CAMPAIGN) &
            (campaigns_df[COL_PORTFOLIO_ID].isna() | (campaigns_df[COL_PORTFOLIO_ID] == ""))
        )
        campaigns_without_portfolio = campaigns_df[campaigns_mask]
        
        self.logger.info(f"Found {len(campaigns_without_portfolio)} campaigns without portfolio")
        
        # Create updates
        updates = []
        for idx, row in campaigns_without_portfolio.iterrows():
            update = CellUpdate(
                row_index=idx,
                key_column=COL_CAMPAIGN_ID,
                key_value=str(row[COL_CAMPAIGN_ID]),
                cell_changes={
                    COL_PORTFOLIO_ID: DEFAULT_PORTFOLIO_ID,
                    COL_OPERATION: OPERATION_UPDATE
                }
            )
            updates.append(update)
        
        # Create patch
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
                f"Assigned {len(updates)} campaigns to default portfolio {DEFAULT_PORTFOLIO_ID}"
            ]
        )
        
        self.logger.info(f"Campaigns Without Portfolios optimization complete: {len(updates)} campaigns updated")
        return result