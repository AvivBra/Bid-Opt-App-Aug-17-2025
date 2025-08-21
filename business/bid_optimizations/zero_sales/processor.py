"""Zero Sales optimization bid processing - FIXED according to specification."""

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple, List
import logging
from config.constants import MIN_BID, MAX_BID


class ZeroSalesProcessor:
    """Processes Zero Sales optimization bid calculations."""

    def __init__(self):
        self.logger = logging.getLogger("optimization.zero_sales.processor")

        # Bid range constraints - FIXED: Changed from 4.00 to 1.25
        self.min_bid = MIN_BID  # 0.02
        self.max_bid = 4  # FIXED: Specification says 1.25, not 4.00

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
        self,
        targeting_df: pd.DataFrame,
        port_values_df: pd.DataFrame,
        bidding_adjustment_df: pd.DataFrame,
        column_mapping: Dict[str, str],
    ) -> Tuple[Dict[str, pd.DataFrame], Dict[str, Any]]:
        """
        Process Zero Sales bid calculations using the 4 defined cases.

        Args:
            targeting_df: Targeting data (already filtered)
            port_values_df: Port Values from template
            bidding_adjustment_df: Bidding Adjustment data for Max BA calculation
            column_mapping: Column name mapping
        """

        processing_details = {
            "input_rows": len(targeting_df),
            "processed_rows": 0,
            "case_statistics": {},
            "errors": [],
        }

        self.logger.info(f"Starting Zero Sales processing: {len(targeting_df)} rows")

        if targeting_df.empty:
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

        # STEP 1: Calculate Max BA for each Campaign ID
        max_ba_map = self._calculate_max_ba(bidding_adjustment_df, column_mapping)

        # STEP 2: Merge template data with targeting data
        processed_df = self._merge_with_template(
            targeting_df, port_values_df, column_mapping
        )

        # STEP 3: Add Max BA column
        campaign_col = column_mapping.get("campaign_id", "Campaign ID")
        if campaign_col in processed_df.columns:
            processed_df["Max BA"] = (
                processed_df[campaign_col].map(max_ba_map).fillna(0)
            )
        else:
            processed_df["Max BA"] = 0

        # STEP 4: Calculate Adj. CPA
        processed_df["Adj. CPA"] = processed_df.apply(
            lambda row: self._calculate_adj_cpa(row), axis=1
        )

        # STEP 5: Calculate new bids for all rows (Old Bid will be saved inside this function)
        processed_df = self._calculate_all_bids(processed_df, column_mapping)

        # STEP 6: Add remaining helper columns and arrange them
        processed_df = self._add_helper_columns(processed_df)

        # STEP 7: Set Operation = Update
        processed_df["Operation"] = "Update"

        # Create result dictionary
        result = {"Targeting": processed_df}

        # Update processing details
        processing_details["processed_rows"] = len(processed_df)
        processing_details["case_statistics"] = self.stats.copy()

        self.logger.info(f"Completed: {len(processed_df)} rows processed")

        return result, processing_details

    def _calculate_max_ba(
        self, ba_df: pd.DataFrame, column_mapping: Dict[str, str]
    ) -> Dict[str, float]:
        """Calculate maximum Percentage for each Campaign ID from Bidding Adjustment data."""

        if ba_df.empty:
            return {}

        campaign_col = column_mapping.get("campaign_id", "Campaign ID")
        percentage_col = column_mapping.get("percentage", "Percentage")

        if campaign_col not in ba_df.columns or percentage_col not in ba_df.columns:
            self.logger.warning("Campaign ID or Percentage column not found in BA data")
            return {}

        # Convert Percentage to numeric
        ba_df[percentage_col] = pd.to_numeric(ba_df[percentage_col], errors="coerce")

        # Group by Campaign ID and get max Percentage
        max_ba = ba_df.groupby(campaign_col)[percentage_col].max().to_dict()

        self.logger.info(f"Calculated Max BA for {len(max_ba)} campaigns")

        return max_ba

    def _merge_with_template(
        self,
        df: pd.DataFrame,
        port_values_df: pd.DataFrame,
        column_mapping: Dict[str, str],
    ) -> pd.DataFrame:
        """Merge targeting data with template portfolio data."""

        merged = df.copy()

        # Find portfolio column
        portfolio_col = column_mapping.get(
            "portfolio", "Portfolio Name (Informational only)"
        )

        if portfolio_col not in merged.columns:
            self.logger.error(f"Portfolio column '{portfolio_col}' not found")
            return merged

        # Merge with Port Values
        if not port_values_df.empty and "Portfolio Name" in port_values_df.columns:
            # Prepare template data for merge
            template_cols = ["Portfolio Name", "Base Bid", "Target CPA"]
            template_subset = port_values_df[template_cols].copy()

            # Convert Base Bid to numeric (handle 'Ignore' values)
            template_subset["Base Bid"] = pd.to_numeric(
                template_subset["Base Bid"], errors="coerce"
            )
            template_subset["Target CPA"] = pd.to_numeric(
                template_subset["Target CPA"], errors="coerce"
            )

            # Merge
            merged = pd.merge(
                merged,
                template_subset,
                left_on=portfolio_col,
                right_on="Portfolio Name",
                how="left",
            )

            # Clean up duplicate column
            if "Portfolio Name" in merged.columns and portfolio_col != "Portfolio Name":
                merged.drop("Portfolio Name", axis=1, inplace=True)

        return merged

    def _calculate_adj_cpa(self, row: pd.Series) -> float:
        """Calculate Adjusted CPA = Target CPA / (1 + Max BA/100)."""

        target_cpa = row.get("Target CPA", np.nan)
        max_ba = row.get("Max BA", 0)

        if pd.isna(target_cpa):
            return np.nan

        return target_cpa / (1 + max_ba / 100)

    def _calculate_all_bids(
        self, df: pd.DataFrame, column_mapping: Dict[str, str]
    ) -> pd.DataFrame:
        """Calculate new bids for all rows using the 4 cases."""

        processed = df.copy()

        # FIXED: Save Old Bid directly from "Bid" column without mapping
        if "Bid" in processed.columns:
            processed["Old Bid"] = processed["Bid"].copy()
        else:
            self.logger.warning("Column 'Bid' not found, Old Bid will be empty")
            processed["Old Bid"] = 0.0

        # Find relevant columns for calculations
        bid_col = column_mapping.get("bid", "Bid")
        campaign_name_col = column_mapping.get(
            "campaign_name", "Campaign Name (Informational only)"
        )
        clicks_col = column_mapping.get("clicks", "Clicks")

        # Initialize calculation columns
        processed["calc1"] = 0.0
        processed["calc2"] = 0.0

        # Process each row
        for idx in processed.index:
            try:
                row = processed.loc[idx]

                # Get values
                base_bid = row.get("Base Bid", 0.5)
                target_cpa = row.get("Target CPA", np.nan)
                adj_cpa = row.get("Adj. CPA", np.nan)
                clicks = row.get(clicks_col, 0)
                campaign_name = row.get(campaign_name_col, "")
                max_ba = row.get("Max BA", 0)

                # Convert to float
                clicks = float(clicks) if pd.notna(clicks) else 0
                base_bid = float(base_bid) if pd.notna(base_bid) else 0.5

                # Check if campaign name contains "up and"
                has_up_and = "up and" in str(campaign_name).lower()

                # Determine case and calculate bid
                if pd.isna(target_cpa):
                    if has_up_and:
                        # Case A: No Target CPA + "up and"
                        new_bid = base_bid * 0.5
                        case = "A"
                    else:
                        # Case B: No Target CPA + no "up and"
                        new_bid = base_bid / (1 + max_ba / 100)
                        case = "B"

                    # No calc1/calc2 for cases A/B
                    processed.at[idx, "calc1"] = 0
                    processed.at[idx, "calc2"] = 0

                else:
                    # Has Target CPA
                    if has_up_and:
                        # Case C: Has Target CPA + "up and"
                        calc1 = adj_cpa * 0.5 / (clicks + 1)
                        calc2 = calc1 - (base_bid * 0.5)

                        if calc2 <= 0:
                            new_bid = calc1
                        else:
                            new_bid = base_bid * 0.5

                        case = "C"
                        processed.at[idx, "calc1"] = calc1
                        processed.at[idx, "calc2"] = calc2

                    else:
                        # Case D: Has Target CPA + no "up and"
                        calc1 = adj_cpa / (clicks + 1)
                        calc2 = calc1 - (base_bid / (1 + max_ba / 100))

                        if calc2 <= 0:
                            new_bid = calc1
                        else:
                            new_bid = base_bid / (1 + max_ba / 100)

                        case = "D"
                        processed.at[idx, "calc1"] = calc1
                        processed.at[idx, "calc2"] = calc2

                # Round to 3 decimal places
                new_bid = round(new_bid, 3)  # Round to 3 decimal places

                # Update row
                processed.at[idx, bid_col] = new_bid  # Update Bid column

                # Check if bid is out of range for error marking
                if new_bid < self.min_bid or new_bid > self.max_bid:
                    self.stats["out_of_range_count"] += 1

                # Update case statistics
                self.stats[f"case_{case.lower()}_count"] += 1

            except Exception as e:
                self.logger.error(f"Error processing row {idx}: {str(e)}")
                self.stats["processing_errors"] += 1

        return processed

    def _add_helper_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Ensure all 7 helper columns are present in the correct order.

        Helper columns (in order):
        1. Old Bid
        2. calc1
        3. calc2
        4. Target CPA
        5. Base Bid
        6. Adj. CPA
        7. Max BA
        """

        df_with_helpers = df.copy()

        # Ensure all helper columns exist
        helper_columns = [
            "Old Bid",
            "calc1",
            "calc2",
            "Target CPA",
            "Base Bid",
            "Adj. CPA",
            "Max BA",
        ]

        for col in helper_columns:
            if col not in df_with_helpers.columns:
                df_with_helpers[col] = 0.0

        # Reorder columns to place helpers before Bid column
        bid_col_index = (
            df_with_helpers.columns.get_loc("Bid")
            if "Bid" in df_with_helpers.columns
            else -1
        )

        if bid_col_index > 0:
            # Get column order
            cols_before_bid = list(df_with_helpers.columns[:bid_col_index])
            cols_after_bid = list(df_with_helpers.columns[bid_col_index:])

            # Remove helper columns from their current positions
            for col in helper_columns:
                if col in cols_before_bid:
                    cols_before_bid.remove(col)
                if col in cols_after_bid:
                    cols_after_bid.remove(col)

            # Insert helper columns before Bid
            new_column_order = cols_before_bid + helper_columns + cols_after_bid

            # Reorder dataframe
            df_with_helpers = df_with_helpers[new_column_order]

        return df_with_helpers
