"""Organize Top Campaigns optimization strategy."""

import pandas as pd
import numpy as np
from typing import Dict, List, Any
import logging
from ..contracts import OptimizationStrategy, OptimizationResult, PatchData, CellUpdate
from ..contract_validator import contract_validator
from ..constants import (
    SHEET_CAMPAIGNS_CLEANED, SHEET_PORTFOLIOS, SHEET_PRODUCT_AD,
    COL_ENTITY, COL_CAMPAIGN_ID, ENTITY_CAMPAIGN
)
from ..processors import AdsCountProcessor, AsinMatcher, TopCampaignsProcessor


class OrganizeTopCampaignsStrategy(OptimizationStrategy):
    """Strategy to organize top campaigns with template-based ASIN matching."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.template_data = None
    
    def get_name(self) -> str:
        return "organize_top_campaigns"
    
    def get_description(self) -> str:
        return "Organizes campaigns based on top ASINs template with filtering and ASIN matching"
    
    def get_required_sheets(self) -> List[str]:
        return [SHEET_CAMPAIGNS_CLEANED, SHEET_PORTFOLIOS, SHEET_PRODUCT_AD]
    
    def set_template_data(self, template_data: pd.DataFrame) -> None:
        """Set the template data for ASIN matching."""
        self.template_data = template_data
        self.logger.info(f"Template data set: {len(template_data)} ASINs")
    
    @contract_validator
    def run(self, all_sheets: Dict[str, pd.DataFrame]) -> OptimizationResult:
        """Run the Organize Top Campaigns optimization."""
        self.logger.info("Starting Organize Top Campaigns optimization")
        
        if self.template_data is None:
            raise ValueError("Template data not set. Call set_template_data() first.")
        
        # Validate required sheets
        for sheet in self.get_required_sheets():
            if sheet not in all_sheets:
                raise ValueError(f"Required sheet '{sheet}' not found")
        
        # Track original row count
        original_campaigns = all_sheets[SHEET_CAMPAIGNS_CLEANED].copy()
        original_campaign_rows = len(original_campaigns[original_campaigns[COL_ENTITY] == ENTITY_CAMPAIGN])
        
        # Process through the pipeline
        updated_sheets = all_sheets.copy()
        
        # Step 3 & 4: Process Ads Count and filter rows
        ads_processor = AdsCountProcessor()
        updated_sheets = ads_processor.process(updated_sheets)
        
        # Step 5a: Add ASIN PA column with VLOOKUP
        asin_matcher = AsinMatcher()
        updated_sheets = asin_matcher.process(updated_sheets)
        
        # Step 5b-5d: Add Top column and create Top sheet
        top_processor = TopCampaignsProcessor()
        top_processor.set_template_data(self.template_data)
        updated_sheets = top_processor.process(updated_sheets)
        
        # Calculate what changed
        final_campaigns = updated_sheets[SHEET_CAMPAIGNS_CLEANED]
        final_campaign_rows = len(final_campaigns[final_campaigns[COL_ENTITY] == ENTITY_CAMPAIGN])
        
        # Count new columns added
        new_columns = ["Ads Count", "ASIN PA", "Top"]
        columns_added = sum(1 for col in new_columns if col in final_campaigns.columns)
        
        # Count campaigns with v marks
        campaigns_with_v = 0
        if "Top" in final_campaigns.columns:
            campaigns_with_v = len(final_campaigns[
                (final_campaigns[COL_ENTITY] == ENTITY_CAMPAIGN) & 
                (final_campaigns["Top"] == "v")
            ])
        
        # Create updates for the changes (this is mainly structural - new columns)
        updates = []
        
        # Since this optimization primarily adds columns and filters rows,
        # rather than updating existing cells, we'll track the structural changes
        for idx, row in final_campaigns.iterrows():
            if row[COL_ENTITY] == ENTITY_CAMPAIGN:
                cell_changes = {}
                
                # Add the new column values
                for col in new_columns:
                    if col in final_campaigns.columns:
                        cell_changes[col] = str(row[col]) if pd.notna(row[col]) else ""
                
                if cell_changes:
                    update = CellUpdate(
                        row_index=idx,
                        key_column=COL_CAMPAIGN_ID,
                        key_value=str(row[COL_CAMPAIGN_ID]),
                        cell_changes=cell_changes
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
                "rows_checked": original_campaign_rows,
                "rows_updated": len(updates),
                "cells_updated": sum(len(update.cell_changes) for update in updates),
                "rows_filtered": original_campaign_rows - final_campaign_rows,
                "columns_added": columns_added,
                "campaigns_with_v_marks": campaigns_with_v,
                "template_asins": len(self.template_data)
            },
            messages=[
                f"Processed {original_campaign_rows} campaign rows",
                f"Added {columns_added} new columns: {', '.join(new_columns[:columns_added])}",
                f"Filtered {original_campaign_rows - final_campaign_rows} rows based on portfolio rules and ads count",
                f"Found {campaigns_with_v} campaigns matching top ASINs template",
                f"Created Top sheet with {len(self.template_data)} template ASINs",
                "Applied COUNTIFS logic for Ads Count column",
                "Applied VLOOKUP logic for ASIN PA and Top columns"
            ]
        )
        
        # Store the updated sheets for access by the orchestrator
        self._updated_sheets = updated_sheets
        
        self.logger.info(f"Organize Top Campaigns optimization complete: {len(updates)} campaigns processed")
        return result
    
    def get_updated_sheets(self) -> Dict[str, pd.DataFrame]:
        """Get the updated sheets after processing."""
        if not hasattr(self, '_updated_sheets'):
            raise ValueError("Strategy has not been run yet")
        return self._updated_sheets