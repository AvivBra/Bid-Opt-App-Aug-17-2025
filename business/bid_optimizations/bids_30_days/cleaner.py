"""Bids 30 Days optimization data cleaning."""

import pandas as pd
from typing import Dict, Any, Tuple, List
import logging
import numpy as np

from business.bid_optimizations.zero_sales.cleaner import ZeroSalesCleaner
from .constants import (
    EXCLUDED_PORTFOLIOS,
    UNITS_THRESHOLD,
    CLICKS_THRESHOLD,
    STATE_ENABLED,
    ENTITY_KEYWORD,
    ENTITY_PRODUCT_TARGETING,
    ENTITY_BIDDING_ADJUSTMENT,
    ENTITY_PRODUCT_AD
)


class Bids30DaysCleaner(ZeroSalesCleaner):
    """
    Cleans and filters data for Bids 30 Days optimization.
    
    Process:
    1. Split by Entity type FIRST (before any filtering)
    2. Filter units > 0 AND (units > 2 OR clicks > 30) - Different from Zero Sales
    3. Remove excluded 'Flat' portfolios (same as Zero Sales)
    4. Remove portfolios marked as 'Ignore' (same as Zero Sales)
    5. Filter by State = enabled (same as Zero Sales)
    6. Validate numeric values (same as Zero Sales)
    """
    
    def __init__(self):
        """Initialize Bids 30 Days cleaner."""
        super().__init__()
        self.logger = logging.getLogger("optimization.bids_30_days.cleaner")
    
    def clean(
        self,
        template_data: Dict[str, pd.DataFrame],
        bulk_data: pd.DataFrame,
        column_mapping: Dict[str, str]
    ) -> Tuple[Dict[str, pd.DataFrame], Dict[str, Any]]:
        """
        Clean and filter data for Bids 30 Days processing.
        
        Returns dictionary with separate sheets for Targeting, Bidding Adjustment and Product Ad.
        IMPORTANT: Never removes columns from the original 48 columns structure!
        
        Args:
            template_data: Dictionary containing template sheets
            bulk_data: Bulk campaign data DataFrame
            column_mapping: Column name mapping
            
        Returns:
            Tuple of (sheets_dict, cleaning_details)
        """
        
        cleaning_details = {
            "input_rows": len(bulk_data),
            "entity_split": {},
            "filtering": {},
            "numeric_validation": {},
            "output_rows": {}
        }
        
        self.logger.info(f"Starting Bids 30 Days cleaning: {len(bulk_data)} input rows")
        
        # CRITICAL: Preserve all 48 columns throughout the process
        original_columns = bulk_data.columns.tolist()
        
        # STEP 1: Split by Entity type FIRST (before any filtering)
        split_data = self._split_by_entity(bulk_data, column_mapping)
        cleaning_details["entity_split"] = {
            "targeting": len(split_data.get("Targeting", pd.DataFrame())),
            "bidding_adjustment": len(split_data.get("Bidding Adjustment", pd.DataFrame())),
            "product_ad": len(split_data.get("Product Ad", pd.DataFrame()))
        }
        
        # STEP 2: Apply filters ONLY to Targeting sheet
        if "Targeting" in split_data and not split_data["Targeting"].empty:
            targeting_df = split_data["Targeting"].copy()
            
            # Ensure all original columns are preserved
            for col in original_columns:
                if col not in targeting_df.columns:
                    targeting_df[col] = ""
            
            # Filter units > 0 AND (units > 2 OR clicks > 30) - DIFFERENT FROM ZERO SALES
            targeting_df = self._filter_bids_30_criteria(targeting_df, column_mapping)
            cleaning_details["filtering"]["after_criteria_filter"] = len(targeting_df)
            
            # Remove excluded portfolios (same as Zero Sales)
            targeting_df = self._remove_excluded_portfolios(targeting_df, column_mapping)
            cleaning_details["filtering"]["after_excluded_filter"] = len(targeting_df)
            
            # Remove ignored portfolios (same as Zero Sales)
            targeting_df = self._remove_ignored_portfolios(
                targeting_df, template_data, column_mapping
            )
            cleaning_details["filtering"]["after_ignored_filter"] = len(targeting_df)
            
            # State filtering is now done in pre_validation_filter() - no duplicate filtering needed
            
            # Validate numeric values (same as Zero Sales)
            targeting_df, validation_stats = self._validate_numeric_values(
                targeting_df, column_mapping
            )
            cleaning_details["numeric_validation"] = validation_stats
            
            # Ensure column order is preserved
            targeting_df = targeting_df[original_columns]
            split_data["Targeting"] = targeting_df
        
        # STEP 3: Keep all sheets with original columns
        for sheet_name in split_data:
            if sheet_name in split_data:
                df = split_data[sheet_name]
                # Preserve original columns
                for col in original_columns:
                    if col not in df.columns:
                        df[col] = ""
                split_data[sheet_name] = df[original_columns]
        
        # Final row counts
        cleaning_details["output_rows"] = {
            sheet: len(df) for sheet, df in split_data.items()
        }
        
        total_output = sum(len(df) for df in split_data.values())
        self.logger.info(
            f"Cleaning complete: {len(bulk_data)} -> {total_output} rows "
            f"({len(split_data)} sheets)"
        )
        
        return split_data, cleaning_details
    
    def _filter_bids_30_criteria(
        self, 
        df: pd.DataFrame, 
        column_mapping: Dict[str, str]
    ) -> pd.DataFrame:
        """
        Filter by Bids 30 Days specific criteria.
        
        Criteria:
        - units > 0
        - units > 2 OR clicks > 30
        
        Args:
            df: DataFrame to filter
            column_mapping: Column name mapping
            
        Returns:
            Filtered DataFrame
        """
        
        units_col = column_mapping.get("units", "Units")
        clicks_col = column_mapping.get("clicks", "Clicks")
        
        if units_col not in df.columns or clicks_col not in df.columns:
            self.logger.error(f"Units or Clicks column not found")
            return df
        
        # Convert to numeric
        df[units_col] = pd.to_numeric(df[units_col], errors='coerce')
        df[clicks_col] = pd.to_numeric(df[clicks_col], errors='coerce')
        
        # Filter: units > 0
        filtered_df = df[df[units_col] > 0].copy()
        
        initial_count = len(filtered_df)
        
        # Additional filter: units > 2 OR clicks > 30
        filtered_df = filtered_df[
            (filtered_df[units_col] > UNITS_THRESHOLD) | 
            (filtered_df[clicks_col] > CLICKS_THRESHOLD)
        ]
        
        filtered_count = initial_count - len(filtered_df)
        
        self.logger.info(
            f"Filtered {filtered_count} rows not meeting Bids 30 criteria "
            f"(units > {UNITS_THRESHOLD} OR clicks > {CLICKS_THRESHOLD})"
        )
        
        return filtered_df
    
    def get_cleaning_summary(self, cleaning_details: Dict[str, Any]) -> str:
        """Generate a human-readable cleaning summary."""
        
        summary_parts = []
        
        # Input
        summary_parts.append(f"Input: {cleaning_details.get('input_rows', 0)} rows")
        
        # Entity split
        if "entity_split" in cleaning_details:
            split = cleaning_details["entity_split"]
            summary_parts.append(
                f"Split: Targeting={split.get('targeting', 0)}, "
                f"BA={split.get('bidding_adjustment', 0)}, "
                f"Product Ad={split.get('product_ad', 0)}"
            )
        
        # Filtering
        if "filtering" in cleaning_details:
            filt = cleaning_details["filtering"]
            if "after_criteria_filter" in filt:
                summary_parts.append(
                    f"After Bids 30 criteria: {filt['after_criteria_filter']} rows"
                )
            if "after_excluded_filter" in filt:
                summary_parts.append(
                    f"After removing Flat: {filt['after_excluded_filter']} rows"
                )
            if "after_ignored_filter" in filt:
                summary_parts.append(
                    f"After removing Ignore: {filt['after_ignored_filter']} rows"
                )
            if "after_state_filter" in filt:
                summary_parts.append(
                    f"After State filter: {filt['after_state_filter']} rows"
                )
        
        # Numeric validation
        if "numeric_validation" in cleaning_details:
            validation = cleaning_details["numeric_validation"]
            if validation.get("rows_marked_error", 0) > 0:
                summary_parts.append(
                    f"Numeric errors: {validation['rows_marked_error']} rows marked"
                )
        
        # Output
        if "output_rows" in cleaning_details:
            output = cleaning_details["output_rows"]
            total = sum(output.values())
            summary_parts.append(f"Output: {total} rows in {len(output)} sheets")
        
        return " | ".join(summary_parts)