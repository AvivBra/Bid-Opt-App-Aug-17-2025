"""Zero Sales optimization bid processing - SIMPLIFIED."""

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple, List
import logging
from config.constants import MIN_BID, MAX_BID


class ZeroSalesProcessor:
    """Processes Zero Sales optimization bid calculations."""

    def __init__(self):
        self.logger = logging.getLogger("optimization.zero_sales.processor")

        # Bid range constraints
        self.min_bid = MIN_BID  # 0.02
        self.max_bid = MAX_BID  # 4.00

        # Processing statistics
        self.stats = {
            "case_a_count": 0,
            "case_b_count": 0,
            "case_c_count": 0,
            "case_d_count": 0,
            "out_of_range_count": 0,
            "processing_errors": 0,
        }

    def process(
        self, df: pd.DataFrame, template_data: pd.DataFrame
    ) -> Tuple[Dict[str, pd.DataFrame], Dict[str, Any]]:
        """
        Process Zero Sales bid calculations using the 4 defined cases.

        SIMPLIFIED VERSION - Direct and efficient processing.
        """

        processing_details = {
            "input_rows": len(df),
            "processed_rows": 0,
            "case_statistics": {},
            "errors": [],
        }

        self.logger.info(f"Starting Zero Sales processing: {len(df)} rows")

        if df.empty:
            return {}, processing_details

        # Reset statistics
        self.stats = {
            "case_a_count": 0,
            "case_b_count": 0,
            "case_c_count": 0,
            "case_d_count": 0,
            "out_of_range_count": 0,
            "processing_errors": 0,
        }

        # Merge template data with bulk data
        processed_df = self._merge_with_template(df, template_data)

        # Apply bid calculations
        processed_df = self._calculate_all_bids(processed_df)

        # Split into output sheets
        result = self._split_to_sheets(processed_df)

        # Update processing details
        processing_details["processed_rows"] = len(processed_df)
        processing_details["case_statistics"] = self.stats.copy()

        self.logger.info(f"Completed: {len(processed_df)} rows processed")

        return result, processing_details

    def _merge_with_template(
        self, df: pd.DataFrame, template_data: pd.DataFrame
    ) -> pd.DataFrame:
        """Merge bulk data with template portfolio data."""

        merged = df.copy()

        # Find portfolio column in bulk data
        portfolio_col = None
        for col in df.columns:
            if "portfolio" in col.lower():
                portfolio_col = col
                break

        if portfolio_col and not template_data.empty:
            # Merge with template on portfolio name
            template_cols = ["Portfolio Name", "Base Bid", "Target CPA"]
            template_subset = template_data[template_cols].copy()
            template_subset.columns = ["Portfolio_Template", "Base Bid", "Target CPA"]

            merged = pd.merge(
                merged,
                template_subset,
                left_on=portfolio_col,
                right_on="Portfolio_Template",
                how="left",
            )

            # Clean up
            if "Portfolio_Template" in merged.columns:
                merged.drop("Portfolio_Template", axis=1, inplace=True)

        return merged

    def _calculate_all_bids(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate new bids for all rows."""

        processed = df.copy()

        # Find relevant columns
        bid_col = self._find_column(processed, ["bid", "max bid"])
        campaign_col = self._find_column(processed, ["campaign"])

        if not bid_col:
            self.logger.error("Bid column not found")
            return processed

        # Add calculation columns
        processed["New_Bid"] = 0.0
        processed["Bid_Case"] = ""
        processed["Bid_Error"] = False

        # Process each row
        for idx in processed.index:
            try:
                new_bid, case = self._calculate_single_bid(processed.loc[idx])

                processed.at[idx, "New_Bid"] = new_bid
                processed.at[idx, "Bid_Case"] = case

                # Update stats
                self.stats[f"case_{case.lower()}_count"] += 1

                # Check range
                if new_bid < self.min_bid or new_bid > self.max_bid:
                    processed.at[idx, "Bid_Error"] = True
                    self.stats["out_of_range_count"] += 1

            except Exception as e:
                self.logger.error(f"Error processing row {idx}: {str(e)}")
                processed.at[idx, "Bid_Error"] = True
                self.stats["processing_errors"] += 1

        # Update the original bid column with new bid
        processed[bid_col] = processed["New_Bid"]

        return processed

    def _calculate_single_bid(self, row: pd.Series) -> Tuple[float, str]:
        """
        Calculate bid for a single row using the 4 cases.

        Case A: No Target CPA + campaign contains "up and" -> Base Bid * 0.5
        Case B: No Target CPA + campaign doesn't contain "up and" -> Base Bid
        Case C: Has Target CPA + campaign contains "up and" -> Complex calculation
        Case D: Has Target CPA + campaign doesn't contain "up and" -> Complex calculation
        """

        # Get values
        base_bid = self._get_numeric_value(row, "Base Bid", 0.5)
        target_cpa = self._get_numeric_value(row, "Target CPA", None)

        # Check campaign name for "up and"
        campaign_name = ""
        for col in row.index:
            if "campaign" in col.lower() and "informational" in col.lower():
                campaign_name = str(row[col]).lower()
                break

        has_up_and = "up and" in campaign_name
        has_target_cpa = target_cpa is not None and target_cpa > 0

        # Apply cases
        if not has_target_cpa and has_up_and:
            # Case A
            new_bid = base_bid * 0.5
            case = "A"
        elif not has_target_cpa and not has_up_and:
            # Case B
            new_bid = base_bid
            case = "B"
        elif has_target_cpa and has_up_and:
            # Case C - Complex calculation (simplified for now)
            new_bid = min(base_bid * 1.2, target_cpa * 0.3)
            case = "C"
        else:
            # Case D - Complex calculation (simplified for now)
            new_bid = min(base_bid * 1.5, target_cpa * 0.4)
            case = "D"

        # Ensure within range
        new_bid = max(self.min_bid, min(new_bid, self.max_bid))

        return round(new_bid, 2), case

    def _split_to_sheets(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Split processed data into output sheets."""

        result = {}

        # Find entity column
        entity_col = self._find_column(df, ["entity"])

        if entity_col:
            # Keywords and Product Targeting sheet
            targeting_entities = ["Keyword", "Product Targeting"]
            targeting_df = df[df[entity_col].isin(targeting_entities)].copy()

            if not targeting_df.empty:
                # Add 7 helper columns as per spec
                targeting_df = self._add_helper_columns(targeting_df)
                result["Targeting"] = targeting_df

            # Bidding Adjustment sheet
            bidding_df = df[df[entity_col] == "Bidding Adjustment"].copy()
            if not bidding_df.empty:
                result["Bidding Adjustment"] = bidding_df
        else:
            # If no entity column, put all in Targeting
            df_copy = df.copy()
            df_copy = self._add_helper_columns(df_copy)
            result["Targeting"] = df_copy

        # Set Operation to Update for all sheets
        for sheet_name in result:
            result[sheet_name]["Operation"] = "Update"

        return result

    def _add_helper_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add 7 helper columns to Targeting sheet."""

        df_with_helpers = df.copy()

        # Add helper columns with placeholder values
        df_with_helpers["Max BA used"] = 0.0
        df_with_helpers["Max BA - Informational"] = 0.0
        df_with_helpers["Adj CPA"] = 0.0
        df_with_helpers["30% of ADJ CPA"] = 0.0
        df_with_helpers["125% Base"] = df_with_helpers.get("Base Bid", 0) * 1.25
        df_with_helpers["Max Bid Helper"] = 0.0
        df_with_helpers["Min Bid Helper"] = 0.0

        return df_with_helpers

    def _find_column(self, df: pd.DataFrame, keywords: List[str]) -> str:
        """Find column by keywords."""

        for col in df.columns:
            col_lower = col.lower()
            for keyword in keywords:
                if keyword.lower() in col_lower:
                    return col
        return None

    def _get_numeric_value(
        self, row: pd.Series, col_name: str, default: float
    ) -> float:
        """Safely get numeric value from row."""

        if col_name not in row.index:
            return default

        val = row[col_name]

        if pd.isna(val) or str(val).lower() == "ignore":
            return default

        try:
            return float(val)
        except:
            return default
