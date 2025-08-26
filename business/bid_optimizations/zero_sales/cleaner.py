"""Zero Sales optimization data cleaning - FIXED VERSION."""

import pandas as pd
from typing import Dict, Any, Tuple, List
import logging
import numpy as np


class ZeroSalesCleaner:
    """
    Cleans and filters data for Zero Sales optimization.

    Process:
    1. Split by Entity type FIRST (before any filtering)
    2. Filter Units = 0 (only on Targeting)
    3. Remove excluded 'Flat' portfolios
    4. Remove portfolios marked as 'Ignore'
    5. Filter by State = enabled
    6. Validate numeric values
    """

    def __init__(self):
        self.logger = logging.getLogger("optimization.zero_sales.cleaner")

        # 13 excluded portfolios (case sensitive)
        self.excluded_portfolios = [
            "Flat 30",
            "Flat 25",
            "Flat 40",
            "Flat 25 | Opt",
            "Flat 30 | Opt",
            "Flat 20",
            "Flat 15",
            "Flat 40 | Opt",
            "Flat 20 | Opt",
            "Flat 15 | Opt",
            "Winter Clothing / Flat 15",
            "Flat 10",
            "Flat 20 | Winter Clothing",
        ]

    def clean(
        self,
        template_data: Dict[str, pd.DataFrame],
        bulk_data: pd.DataFrame,
        column_mapping: Dict[str, str],
    ) -> Tuple[Dict[str, pd.DataFrame], Dict[str, Any]]:
        """
        Clean and filter data for Zero Sales processing.

        Returns dictionary with separate sheets for Targeting, Bidding Adjustment and Product Ad.
        IMPORTANT: Never removes columns from the original 48 columns structure!
        """

        cleaning_details = {
            "input_rows": len(bulk_data),
            "entity_split": {},
            "filtering": {},
            "numeric_validation": {},
            "output_rows": {},
        }

        self.logger.info(f"Starting Zero Sales cleaning: {len(bulk_data)} input rows")

        # CRITICAL: Preserve all 48 columns throughout the process
        original_columns = bulk_data.columns.tolist()

        # STEP 1: Split by Entity type FIRST (before any filtering)
        split_data = self._split_by_entity(bulk_data, column_mapping)
        cleaning_details["entity_split"] = {
            "targeting": len(split_data.get("Targeting", pd.DataFrame())),
            "bidding_adjustment": len(
                split_data.get("Bidding Adjustment", pd.DataFrame())
            ),
            "product_ad": len(split_data.get("Product Ad", pd.DataFrame())),
        }

        # STEP 2: Apply filters ONLY to Targeting sheet
        if "Targeting" in split_data and not split_data["Targeting"].empty:
            targeting_df = split_data["Targeting"].copy()

            # Ensure all original columns are preserved
            for col in original_columns:
                if col not in targeting_df.columns:
                    targeting_df[col] = ""

            # Filter Units = 0
            targeting_df = self._filter_zero_units(targeting_df, column_mapping)
            cleaning_details["filtering"]["after_units_filter"] = len(targeting_df)

            # Remove excluded portfolios
            targeting_df = self._remove_excluded_portfolios(
                targeting_df, column_mapping
            )
            cleaning_details["filtering"]["after_excluded_filter"] = len(targeting_df)

            # Remove ignored portfolios
            targeting_df = self._remove_ignored_portfolios(
                targeting_df, template_data, column_mapping
            )
            cleaning_details["filtering"]["after_ignored_filter"] = len(targeting_df)

            # State filtering is now done in pre_validation_filter() - no duplicate filtering needed

            # Validate numeric values (NEW) - marks errors but doesn't remove rows
            targeting_df, validation_stats = self._validate_numeric_values(
                targeting_df, column_mapping
            )
            cleaning_details["numeric_validation"] = validation_stats

            # Ensure column order is preserved
            targeting_df = targeting_df[original_columns]
            split_data["Targeting"] = targeting_df

        # STEP 3: Keep all sheets with original columns
        # Ensure all sheets maintain the original 48 columns
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
    
    def pre_validation_filter(self, bulk_data: pd.DataFrame) -> pd.DataFrame:
        """
        Pre-validation filtering to remove rows with State != 'enabled'.
        
        This runs BEFORE validation to prevent validation errors for portfolios
        that exist only in paused/disabled campaigns.
        
        Args:
            bulk_data: Raw bulk data DataFrame
            
        Returns:
            Filtered DataFrame with only enabled rows
        """
        if bulk_data.empty:
            return bulk_data
            
        df = bulk_data.copy()
        initial_count = len(df)
        
        # Filter by main State column
        if 'State' in df.columns:
            df = df[df['State'].astype(str).str.lower() == 'enabled'].copy()
        
        # Filter by Campaign State  
        if 'Campaign State (Informational only)' in df.columns:
            df = df[df['Campaign State (Informational only)'].astype(str).str.lower() == 'enabled'].copy()
            
        # Filter by Ad Group State
        if 'Ad Group State (Informational only)' in df.columns:
            df = df[df['Ad Group State (Informational only)'].astype(str).str.lower() == 'enabled'].copy()
        
        filtered_count = initial_count - len(df)
        if filtered_count > 0:
            self.logger.info(f"Pre-validation filter: removed {filtered_count} non-enabled rows")
            
        return df

    def _split_by_entity(
        self, df: pd.DataFrame, column_mapping: Dict[str, str]
    ) -> Dict[str, pd.DataFrame]:
        """
        Split data by Entity type.

        Returns:
            Dictionary with keys:
            - "Targeting": Keyword + Product Targeting
            - "Bidding Adjustment": Bidding Adjustment rows
            - "Product Ad": Product Ad rows
        """

        entity_col = column_mapping.get("entity", "Entity")

        if entity_col not in df.columns:
            self.logger.error(f"Entity column '{entity_col}' not found")
            return {"Targeting": df}  # Fallback: treat all as Targeting

        result = {}

        # Targeting sheet: Keyword + Product Targeting
        targeting_mask = df[entity_col].isin(["Keyword", "Product Targeting"])
        result["Targeting"] = df[targeting_mask].copy()

        # Bidding Adjustment sheet
        ba_mask = df[entity_col] == "Bidding Adjustment"
        result["Bidding Adjustment"] = df[ba_mask].copy()

        # Product Ad sheet (KEEP - don't delete)
        pa_mask = df[entity_col] == "Product Ad"
        result["Product Ad"] = df[pa_mask].copy()

        self.logger.info(
            f"Entity split: Targeting={len(result['Targeting'])}, "
            f"BA={len(result['Bidding Adjustment'])}, "
            f"Product Ad={len(result['Product Ad'])}"
        )

        return result

    def _filter_zero_units(
        self, df: pd.DataFrame, column_mapping: Dict[str, str]
    ) -> pd.DataFrame:
        """Filter to only rows with Units = 0."""

        units_col = column_mapping.get("units", "Units")

        if units_col not in df.columns:
            self.logger.error(f"Units column '{units_col}' not found")
            return df

        # Convert to numeric and filter
        df[units_col] = pd.to_numeric(df[units_col], errors="coerce")
        zero_units_df = df[df[units_col] == 0].copy()

        filtered_count = len(df) - len(zero_units_df)
        self.logger.info(f"Filtered {filtered_count} rows with Units != 0")

        return zero_units_df

    def _remove_excluded_portfolios(
        self, df: pd.DataFrame, column_mapping: Dict[str, str]
    ) -> pd.DataFrame:
        """Remove rows from 10 excluded 'Flat' portfolios."""

        portfolio_col = column_mapping.get(
            "portfolio", "Portfolio Name (Informational only)"
        )

        if portfolio_col not in df.columns:
            self.logger.warning(f"Portfolio column '{portfolio_col}' not found")
            return df

        # Filter out excluded portfolios (case sensitive)
        excluded_mask = df[portfolio_col].isin(self.excluded_portfolios)
        filtered_df = df[~excluded_mask].copy()

        excluded_count = excluded_mask.sum()
        if excluded_count > 0:
            self.logger.info(f"Removed {excluded_count} rows from excluded portfolios")

        return filtered_df

    def _remove_ignored_portfolios(
        self,
        df: pd.DataFrame,
        template_data: Dict[str, pd.DataFrame],
        column_mapping: Dict[str, str],
    ) -> pd.DataFrame:
        """Remove rows from portfolios marked as 'Ignore' in template."""

        portfolio_col = column_mapping.get(
            "portfolio", "Portfolio Name (Informational only)"
        )

        if portfolio_col not in df.columns:
            self.logger.warning(f"Portfolio column '{portfolio_col}' not found")
            return df

        # Get Port Values sheet
        port_values = template_data.get("Port Values", pd.DataFrame())

        if port_values.empty:
            self.logger.warning("Port Values sheet is empty")
            return df

        # Find portfolios with Base Bid = 'Ignore'
        if "Base Bid" not in port_values.columns:
            self.logger.warning("Base Bid column not found in Port Values")
            return df

        # Convert Base Bid to string and check for 'Ignore' (case insensitive)
        port_values["Base Bid"] = port_values["Base Bid"].astype(str)
        ignored_mask = port_values["Base Bid"].str.lower() == "ignore"
        ignored_portfolios = port_values[ignored_mask]["Portfolio Name"].tolist()

        if ignored_portfolios:
            # Filter out ignored portfolios
            ignored_data_mask = df[portfolio_col].isin(ignored_portfolios)
            filtered_df = df[~ignored_data_mask].copy()

            ignored_count = ignored_data_mask.sum()
            if ignored_count > 0:
                self.logger.info(
                    f"Removed {ignored_count} rows from {len(ignored_portfolios)} "
                    f"ignored portfolios"
                )

            return filtered_df

        return df

    def _filter_by_state(
        self, df: pd.DataFrame, column_mapping: Dict[str, str]
    ) -> pd.DataFrame:
        """Filter to only rows with State = enabled (NEW)."""

        # Check all three state columns
        state_col = column_mapping.get("state", "State")
        campaign_state_col = column_mapping.get(
            "campaign_state", "Campaign State (Informational only)"
        )
        ad_group_state_col = column_mapping.get(
            "ad_group_state", "Ad Group State (Informational only)"
        )

        initial_count = len(df)

        # Filter by State
        if state_col in df.columns:
            df = df[df[state_col].str.lower() == "enabled"].copy()

        # Filter by Campaign State
        if campaign_state_col in df.columns:
            df = df[df[campaign_state_col].str.lower() == "enabled"].copy()

        # Filter by Ad Group State
        if ad_group_state_col in df.columns:
            df = df[df[ad_group_state_col].str.lower() == "enabled"].copy()

        filtered_count = initial_count - len(df)
        if filtered_count > 0:
            self.logger.info(f"Filtered {filtered_count} rows with State != enabled")

        return df

    def _validate_numeric_values(
        self, df: pd.DataFrame, column_mapping: Dict[str, str]
    ) -> Tuple[pd.DataFrame, Dict[str, int]]:
        """Validate and mark rows with invalid numeric values (NEW)."""

        stats = {
            "invalid_bid": 0,
            "invalid_clicks": 0,
            "invalid_units": 0,
            "invalid_percentage": 0,
            "rows_marked_error": 0,
        }

        # Columns to validate
        bid_col = column_mapping.get("bid", "Bid")
        clicks_col = column_mapping.get("clicks", "Clicks")
        units_col = column_mapping.get("units", "Units")
        percentage_col = column_mapping.get("percentage", "Percentage")

        # Track rows with errors
        error_mask = pd.Series(False, index=df.index)

        # Validate Bid
        if bid_col in df.columns:
            df[bid_col] = pd.to_numeric(df[bid_col], errors="coerce")
            invalid_bid = df[bid_col].isna()
            stats["invalid_bid"] = invalid_bid.sum()
            error_mask |= invalid_bid

        # Validate Clicks
        if clicks_col in df.columns:
            df[clicks_col] = pd.to_numeric(df[clicks_col], errors="coerce")
            invalid_clicks = df[clicks_col].isna()
            stats["invalid_clicks"] = invalid_clicks.sum()
            error_mask |= invalid_clicks

        # Validate Units (should already be numeric from _filter_zero_units)
        if units_col in df.columns:
            df[units_col] = pd.to_numeric(df[units_col], errors="coerce")
            invalid_units = df[units_col].isna()
            stats["invalid_units"] = invalid_units.sum()
            error_mask |= invalid_units

        # Validate Percentage
        if percentage_col in df.columns:
            df[percentage_col] = pd.to_numeric(df[percentage_col], errors="coerce")
            invalid_percentage = df[percentage_col].isna()
            stats["invalid_percentage"] = invalid_percentage.sum()
            error_mask |= invalid_percentage

        # Mark error rows (for later processing in processor.py)
        if bid_col in df.columns:
            df.loc[error_mask, f"{bid_col}_error"] = True

        stats["rows_marked_error"] = error_mask.sum()

        if stats["rows_marked_error"] > 0:
            self.logger.warning(
                f"Found {stats['rows_marked_error']} rows with invalid numeric values"
            )

        return df, stats

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
            if "after_units_filter" in filt:
                summary_parts.append(
                    f"After Units=0: {filt['after_units_filter']} rows"
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
