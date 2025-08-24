"""Bids 30 Days optimization bid processing."""

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple, List, Optional
import logging

from .constants import (
    MIN_BID,
    MAX_BID,
    CALC2_THRESHOLD,
    CONVERSION_RATE_THRESHOLD,
    UNITS_THRESHOLD_FOR_MAX_BID,
    MAX_BID_LOW_UNITS,
    MAX_BID_HIGH_UNITS,
    UP_AND_MULTIPLIER,
    OLD_BID_MULTIPLIER,
    MATCH_TYPE_EXACT,
    ERROR_CALCULATION,
    ERROR_NULL,
    ERROR_MISSING_VALUE,
    HELPER_COLUMNS,
)


class Bids30DaysProcessor:
    """Processes Bids 30 Days optimization bid calculations."""

    def __init__(self):
        self.logger = logging.getLogger("optimization.bids_30_days.processor")

        # FIXED: Use correct ASIN pattern
        self.ASIN_PATTERN = 'asin="B0'

        # Processing statistics
        self.stats = {
            "rows_processed": 0,
            "rows_modified": 0,
            "null_target_cpa": 0,
            "moved_to_harvesting": 0,
            "cvr_below_threshold": 0,
            "bid_out_of_range": 0,
            "calculation_errors": 0,
        }

    def process(
        self,
        targeting_df: pd.DataFrame,
        port_values_df: pd.DataFrame,
        bidding_adjustment_df: pd.DataFrame,
        column_mapping: Dict[str, str],
    ) -> Tuple[Dict[str, pd.DataFrame], Dict[str, Any]]:
        """
        Process Bids 30 Days bid calculations using 8 defined steps.

        Args:
            targeting_df: Targeting data (already filtered)
            port_values_df: Port Values from template
            bidding_adjustment_df: Bidding Adjustment data for Max BA calculation
            column_mapping: Column name mapping

        Returns:
            Tuple of (sheets_dict, processing_details)
        """

        processing_details = {
            "input_rows": len(targeting_df),
            "processed_rows": 0,
            "statistics": {},
            "errors": [],
        }

        self.logger.info(f"Starting Bids 30 Days processing: {len(targeting_df)} rows")

        if targeting_df.empty:
            return {}, processing_details

        # Reset statistics
        self._reset_stats()

        # STEP 0: Create empty helper columns
        processed_df = self._create_helper_columns(targeting_df.copy())

        # STEP 1: Fill base columns
        processed_df = self._fill_base_columns(
            processed_df, port_values_df, bidding_adjustment_df, column_mapping
        )

        # STEP 2: Separate NULL Target CPA to For Harvesting
        targeting_with_cpa, for_harvesting = self._separate_null_target_cpa(
            processed_df, column_mapping
        )

        if targeting_with_cpa.empty:
            # All rows have NULL Target CPA
            result = {"For Harvesting": for_harvesting}
            processing_details["processed_rows"] = len(for_harvesting)
            processing_details["statistics"] = self.stats.copy()
            return result, processing_details

        # Continue processing rows with Target CPA
        processed_df = targeting_with_cpa

        # STEP 3: Calculate calc1 and calc2
        processed_df = self._calculate_calc_values(processed_df, column_mapping)

        # STEP 4: Determine Temp Bid
        processed_df = self._determine_temp_bid(processed_df, column_mapping)

        # STEP 5: Calculate Max Bid
        processed_df = self._calculate_max_bid(processed_df, column_mapping)

        # STEP 6: Calculate calc3
        processed_df = self._calculate_calc3(processed_df)

        # STEP 7: Calculate final Bid
        processed_df = self._calculate_final_bid(processed_df, column_mapping)

        # STEP 8: Mark rows for pink highlighting
        processed_df = self._mark_rows_for_coloring(processed_df, column_mapping)

        # Set Operation = Update
        processed_df["Operation"] = "Update"

        # Create result dictionary
        result = {"Targeting": processed_df}

        # Add For Harvesting sheet if exists
        if not for_harvesting.empty:
            for_harvesting["Operation"] = "Update"
            result["For Harvesting"] = for_harvesting

        # Update processing details
        processing_details["processed_rows"] = len(processed_df)
        processing_details["statistics"] = self.stats.copy()

        self.logger.info(
            f"Completed: {len(processed_df)} rows processed, "
            f"{len(for_harvesting)} moved to For Harvesting"
        )

        return result, processing_details

    def _reset_stats(self):
        """Reset processing statistics."""
        for key in self.stats:
            self.stats[key] = 0

    def _create_helper_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Step 0: Create empty helper columns."""

        for col in HELPER_COLUMNS:
            if col not in df.columns:
                df[col] = 0.0

        return df

    def _fill_base_columns(
        self,
        df: pd.DataFrame,
        port_values_df: pd.DataFrame,
        ba_df: pd.DataFrame,
        column_mapping: Dict[str, str],
    ) -> pd.DataFrame:
        """
        Step 1: Fill base columns.

        - Old Bid = Copy current Bid value
        - Target CPA = VLOOKUP from Template
        - Base Bid = VLOOKUP from Template
        - Max BA = MAX(Percentage) per Campaign ID
        - Adj. CPA = Target CPA / (1 + Max BA/100)
        """

        # Copy Old Bid
        bid_col = column_mapping.get("bid", "Bid")
        if bid_col in df.columns:
            df["Old Bid"] = df[bid_col].copy()
        else:
            df["Old Bid"] = 0.0

        # Initialize Target CPA and Base Bid columns with default values
        df["Target CPA"] = np.nan
        df["Base Bid"] = 0.5  # Default base bid

        # Merge with template data if available
        portfolio_col = column_mapping.get(
            "portfolio", "Portfolio Name (Informational only)"
        )
        if (
            portfolio_col in df.columns
            and not port_values_df.empty
            and "Portfolio Name" in port_values_df.columns
        ):
            # Prepare template data
            template_cols_to_use = []
            if "Portfolio Name" in port_values_df.columns:
                template_cols_to_use.append("Portfolio Name")
            if "Base Bid" in port_values_df.columns:
                template_cols_to_use.append("Base Bid")
            if "Target CPA" in port_values_df.columns:
                template_cols_to_use.append("Target CPA")

            if template_cols_to_use:
                template_subset = port_values_df[template_cols_to_use].copy()

                # Convert Base Bid and Target CPA to numeric if they exist
                if "Base Bid" in template_subset.columns:
                    template_subset["Base Bid_temp"] = pd.to_numeric(
                        template_subset["Base Bid"], errors="coerce"
                    )
                if "Target CPA" in template_subset.columns:
                    template_subset["Target CPA_temp"] = pd.to_numeric(
                        template_subset["Target CPA"], errors="coerce"
                    )

                # Merge
                df = pd.merge(
                    df,
                    template_subset,
                    left_on=portfolio_col,
                    right_on="Portfolio Name",
                    how="left",
                    suffixes=("", "_template"),
                )

                # Update Base Bid and Target CPA from merged data
                if "Base Bid_temp" in df.columns:
                    df["Base Bid"] = df["Base Bid_temp"].fillna(0.5)
                    df.drop("Base Bid_temp", axis=1, inplace=True)
                if "Target CPA_temp" in df.columns:
                    df["Target CPA"] = df[
                        "Target CPA_temp"
                    ]  # Keep NaN values for NULL Target CPA
                    df.drop("Target CPA_temp", axis=1, inplace=True)

                # Clean up duplicate Portfolio Name column if it exists
                if "Portfolio Name" in df.columns and portfolio_col != "Portfolio Name":
                    df.drop("Portfolio Name", axis=1, inplace=True)

        # Initialize Max BA column
        df["Max BA"] = 0.0

        # Calculate Max BA from Bidding Adjustment data
        campaign_col = column_mapping.get("campaign_id", "Campaign ID")
        percentage_col = column_mapping.get("percentage", "Percentage")

        if (
            not ba_df.empty
            and campaign_col in ba_df.columns
            and percentage_col in ba_df.columns
        ):
            ba_df[percentage_col] = pd.to_numeric(
                ba_df[percentage_col], errors="coerce"
            )
            max_ba_map = ba_df.groupby(campaign_col)[percentage_col].max().to_dict()

            if campaign_col in df.columns:
                df["Max BA"] = df[campaign_col].map(max_ba_map).fillna(0)

        # Initialize Adj. CPA column
        df["Adj. CPA"] = np.nan

        # Calculate Adj. CPA only for rows with Target CPA
        for idx in df.index:
            target_cpa = df.at[idx, "Target CPA"]
            max_ba = df.at[idx, "Max BA"]

            if pd.notna(target_cpa) and max_ba >= 0:
                df.at[idx, "Adj. CPA"] = target_cpa / (1 + max_ba / 100)

        return df

    def _separate_null_target_cpa(
        self, df: pd.DataFrame, column_mapping: Dict[str, str]
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Step 2: Separate rows with NULL Target CPA to For Harvesting sheet.
        """

        null_mask = pd.isna(df["Target CPA"])

        for_harvesting = df[null_mask].copy()
        targeting_with_cpa = df[~null_mask].copy()

        self.stats["null_target_cpa"] = len(for_harvesting)
        self.stats["moved_to_harvesting"] = len(for_harvesting)

        return targeting_with_cpa, for_harvesting

    def _calculate_calc_values(
        self, df: pd.DataFrame, column_mapping: Dict[str, str]
    ) -> pd.DataFrame:
        """
        Step 3: Calculate calc1 and calc2 based on campaign name.
        """

        campaign_name_col = column_mapping.get(
            "campaign_name", "Campaign Name (Informational only)"
        )
        clicks_col = column_mapping.get("clicks", "Clicks")
        units_col = column_mapping.get("units", "Units")

        for idx in df.index:
            try:
                row = df.loc[idx]

                adj_cpa = row.get("Adj. CPA", 0)
                old_bid = row.get("Old Bid", 0)
                campaign_name = str(row.get(campaign_name_col, ""))
                clicks = pd.to_numeric(row.get(clicks_col, 0), errors="coerce")
                units = pd.to_numeric(row.get(units_col, 1), errors="coerce")

                # Handle division by zero
                if units == 0 or pd.isna(units):
                    units = 1

                # Check for "up and" in campaign name
                has_up_and = "up and" in campaign_name.lower()

                if has_up_and:
                    calc1 = adj_cpa * UP_AND_MULTIPLIER / (clicks / units)
                else:
                    calc1 = adj_cpa / (clicks / units)

                calc2 = calc1 / old_bid if old_bid != 0 else 0

                df.at[idx, "calc1"] = calc1
                df.at[idx, "calc2"] = calc2

            except Exception as e:
                self.logger.error(
                    f"Error calculating calc values for row {idx}: {str(e)}"
                )
                df.at[idx, "calc1"] = 0
                df.at[idx, "calc2"] = 0
                self.stats["calculation_errors"] += 1

        return df

    def _determine_temp_bid(
        self, df: pd.DataFrame, column_mapping: Dict[str, str]
    ) -> pd.DataFrame:
        """
        Step 4: Determine Temp Bid based on calc2 threshold and conditions.
        """

        bid_col = column_mapping.get("bid", "Bid")
        match_type_col = column_mapping.get("match_type", "Match Type")
        product_targeting_col = column_mapping.get(
            "product_targeting", "Product Targeting Expression"
        )

        for idx in df.index:
            try:
                row = df.loc[idx]

                calc1 = row.get("calc1", 0)
                calc2 = row.get("calc2", 0)
                old_bid = row.get("Old Bid", 0)
                match_type = str(row.get(match_type_col, ""))
                product_targeting = str(row.get(product_targeting_col, ""))

                # Check calc2 threshold
                if calc2 < CALC2_THRESHOLD:
                    # Bid = calc1 (FINAL)
                    df.at[idx, bid_col] = calc1
                    df.at[idx, "Temp Bid"] = 0  # Not used
                else:
                    # calc2 >= 1.1
                    is_exact = match_type.lower() == MATCH_TYPE_EXACT.lower()
                    # FIXED: Use correct ASIN pattern with quote
                    has_asin = 'asin="B0' in product_targeting

                    if is_exact or has_asin:
                        # Temp_Bid = calc1 (continue to step 5)
                        df.at[idx, "Temp Bid"] = calc1
                    else:
                        # Bid = Old Bid * 1.1 (FINAL)
                        df.at[idx, bid_col] = old_bid * OLD_BID_MULTIPLIER
                        df.at[idx, "Temp Bid"] = 0  # Not used

            except Exception as e:
                self.logger.error(f"Error determining Temp Bid for row {idx}: {str(e)}")
                df.at[idx, bid_col] = ERROR_CALCULATION
                self.stats["calculation_errors"] += 1

        return df

    def _calculate_max_bid(
        self, df: pd.DataFrame, column_mapping: Dict[str, str]
    ) -> pd.DataFrame:
        """
        Step 5: Calculate Max Bid for rows with Temp Bid.
        """

        units_col = column_mapping.get("units", "Units")

        for idx in df.index:
            try:
                row = df.loc[idx]

                temp_bid = row.get("Temp Bid", 0)

                # Only calculate if Temp Bid exists
                if temp_bid > 0:
                    units = pd.to_numeric(row.get(units_col, 0), errors="coerce")
                    max_ba = pd.to_numeric(row.get("Max BA", 0), errors="coerce")

                    # Handle NaN values
                    if pd.isna(units):
                        units = 0
                    if pd.isna(max_ba):
                        max_ba = 0

                    # Determine Max_Bid based on units
                    if units < UNITS_THRESHOLD_FOR_MAX_BID:
                        max_bid_base = MAX_BID_LOW_UNITS
                    else:
                        max_bid_base = MAX_BID_HIGH_UNITS

                    # Apply Max BA adjustment
                    denominator = 1 + max_ba / 100
                    max_bid = max_bid_base / denominator

                    df.at[idx, "Max_Bid"] = max_bid
                else:
                    df.at[idx, "Max_Bid"] = 0

            except Exception as e:
                self.logger.error(f"Error calculating Max Bid for row {idx}: {str(e)}")
                df.at[idx, "Max_Bid"] = 0
                self.stats["calculation_errors"] += 1

        return df

    def _calculate_calc3(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Step 6: Calculate calc3 = Temp Bid - Max Bid.
        """

        for idx in df.index:
            temp_bid = df.at[idx, "Temp Bid"]
            max_bid = df.at[idx, "Max_Bid"]

            if temp_bid > 0 and max_bid > 0:
                df.at[idx, "calc3"] = temp_bid - max_bid
            else:
                df.at[idx, "calc3"] = 0

        return df

    def _calculate_final_bid(
        self, df: pd.DataFrame, column_mapping: Dict[str, str]
    ) -> pd.DataFrame:
        """
        Step 7: Calculate final Bid for rows with Max Bid.

        FIXED LOGIC:
        IF calc3 < 0 (Temp_Bid < Max_Bid):
            Bid = Temp_Bid
        ELSE (Temp_Bid >= Max_Bid):
            Bid = Max_Bid
        """

        bid_col = column_mapping.get("bid", "Bid")

        for idx in df.index:
            try:
                row = df.loc[idx]

                temp_bid = row.get("Temp Bid", 0)
                max_bid = row.get("Max_Bid", 0)
                calc3 = row.get("calc3", 0)

                # Only process if we have Temp Bid and Max Bid
                if temp_bid > 0 and max_bid > 0:
                    # FIXED LOGIC - REVERSED
                    if calc3 < 0:
                        # calc3 < 0 means Temp_Bid < Max_Bid
                        # Bid = Temp_Bid
                        df.at[idx, bid_col] = temp_bid
                    else:
                        # calc3 >= 0 means Temp_Bid >= Max_Bid
                        # Bid = Max_Bid
                        df.at[idx, bid_col] = max_bid

                # Round to 3 decimal places
                current_bid = df.at[idx, bid_col]
                if isinstance(current_bid, (int, float)):
                    df.at[idx, bid_col] = round(current_bid, 3)

            except Exception as e:
                self.logger.error(
                    f"Error calculating final Bid for row {idx}: {str(e)}"
                )
                df.at[idx, bid_col] = ERROR_CALCULATION
                self.stats["calculation_errors"] += 1

        self.stats["rows_processed"] = len(df)
        self.stats["rows_modified"] = len(df[df["Old Bid"] != df[bid_col]])

        return df

    def _mark_rows_for_coloring(
        self, df: pd.DataFrame, column_mapping: Dict[str, str]
    ) -> pd.DataFrame:
        """
        Step 8: Mark rows for pink highlighting.

        Conditions:
        - Conversion Rate < 0.08
        - Bid < 0.02
        - Bid > 1.25
        - Calculation errors
        """

        bid_col = column_mapping.get("bid", "Bid")
        cvr_col = column_mapping.get("conversion_rate", "Conversion Rate")

        # Initialize marking column
        df["_needs_highlight"] = False

        for idx in df.index:
            try:
                row = df.loc[idx]
                needs_highlight = False

                # Check Conversion Rate
                if cvr_col in df.columns:
                    cvr = pd.to_numeric(row.get(cvr_col, 0), errors="coerce")
                    if pd.notna(cvr) and cvr < CONVERSION_RATE_THRESHOLD:
                        needs_highlight = True
                        self.stats["cvr_below_threshold"] += 1

                # Check Bid range
                bid = row.get(bid_col)
                if isinstance(bid, (int, float)):
                    if bid < MIN_BID or bid > MAX_BID:
                        needs_highlight = True
                        self.stats["bid_out_of_range"] += 1
                elif bid in [ERROR_CALCULATION, ERROR_NULL]:
                    needs_highlight = True

                df.at[idx, "_needs_highlight"] = needs_highlight

            except Exception as e:
                self.logger.error(f"Error marking row {idx} for coloring: {str(e)}")
                df.at[idx, "_needs_highlight"] = True

        return df
