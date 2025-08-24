"""Bids 30 Days optimization orchestrator."""

import pandas as pd
from typing import Dict, Any, Tuple, Optional, List
import logging
import time  # Added for timing

from business.bid_optimizations.base_optimization import BaseOptimization
from .validator import Bids30DaysValidator
from .cleaner import Bids30DaysCleaner
from .processor import Bids30DaysProcessor


class Bids30DaysOptimization(BaseOptimization):
    """
    Bids 30 Days optimization implementation.

    Optimizes bids for products with units > 0 that meet specific criteria.
    Uses complex calculations with Target CPA, clicks/units ratio, and Max BA.
    Creates separate "For Harvesting" sheet for rows with NULL Target CPA.
    """

    def __init__(self):
        super().__init__("Bids 30 Days")

        # Initialize components - FIXED: Now properly initialized
        self.validator = Bids30DaysValidator()
        self.cleaner = Bids30DaysCleaner()
        self.processor = Bids30DaysProcessor()

        # Store validation and cleaning results
        self._validation_details = {}
        self._cleaning_details = {}
        self._processing_details = {}

    def validate(
        self, template_data: Dict[str, pd.DataFrame], bulk_data: pd.DataFrame
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Validate data requirements for Bids 30 Days optimization.

        Validation is identical to Zero Sales but checks for different criteria:
        - Units > 0 (instead of Units = 0)
        - Additional check for units > 2 OR clicks > 30

        Args:
            template_data: Dictionary containing template sheets
            bulk_data: Bulk campaign data DataFrame

        Returns:
            Tuple of (is_valid, message, validation_details)
        """

        print(f"[DEBUG] Starting validation - Bulk data shape: {bulk_data.shape}")
        start_time = time.time()

        self.logger.info("Starting Bids 30 Days validation")

        # Use the actual validator
        valid, msg, details = self.validator.validate(template_data, bulk_data)

        # Store validation details
        self._validation_details = details.copy()

        elapsed = time.time() - start_time
        print(f"[DEBUG] Validation completed in {elapsed:.2f} seconds")

        if valid:
            self.logger.info(f"Bids 30 Days validation passed: {msg}")
        else:
            self.logger.error(f"Bids 30 Days validation failed: {msg}")

        return valid, msg, details

    def clean(
        self, template_data: Dict[str, pd.DataFrame], bulk_data: pd.DataFrame
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Clean and filter data for Bids 30 Days processing.

        Applies filters:
        - Split by Entity type (same as Zero Sales)
        - Filter: units > 0 AND (units > 2 OR clicks > 30)
        - Remove 10 'Flat' portfolios
        - Remove portfolios marked as 'Ignore'
        - Filter by State = enabled

        Args:
            template_data: Dictionary containing template sheets
            bulk_data: Bulk campaign data DataFrame

        Returns:
            Tuple of (cleaned_dataframe, cleaning_details)
        """

        print(f"[DEBUG] Starting cleaning - Input rows: {len(bulk_data)}")
        start_time = time.time()

        self.logger.info("Starting Bids 30 Days data cleaning")

        # Get column mapping from validation
        column_mapping = self._validation_details.get("column_mapping", {})

        # Use the actual cleaner
        cleaned_data, cleaning_details = self.cleaner.clean(
            template_data, bulk_data, column_mapping
        )

        # Store cleaning details
        self._cleaning_details = cleaning_details.copy()

        elapsed = time.time() - start_time

        # Log results
        if isinstance(cleaned_data, dict):
            total_rows = sum(len(df) for df in cleaned_data.values())
            print(
                f"[DEBUG] Cleaning completed in {elapsed:.2f} seconds - Output: {total_rows} rows in {len(cleaned_data)} sheets"
            )
            self.logger.info(
                f"Bids 30 Days cleaning complete: {total_rows} total rows "
                f"across {len(cleaned_data)} sheets"
            )
        else:
            print(
                f"[DEBUG] Cleaning completed in {elapsed:.2f} seconds - Output: {len(cleaned_data)} rows"
            )
            self.logger.info(
                f"Bids 30 Days cleaning complete: {len(cleaned_data)} rows"
            )

        return cleaned_data, cleaning_details

    def process(
        self, template_data: Dict[str, pd.DataFrame], bulk_data: pd.DataFrame
    ) -> Dict[str, pd.DataFrame]:
        """
        Process Bids 30 Days bid calculations.

        Processing includes:
        - 8 steps of calculations based on Target CPA and campaign conditions
        - Creating "For Harvesting" sheet for NULL Target CPA rows
        - Complex bid calculations with Temp Bid and Max Bid
        - Marking rows for pink highlighting based on multiple criteria

        Args:
            template_data: Dictionary containing template sheets
            bulk_data: Cleaned bulk campaign data

        Returns:
            Dictionary of result DataFrames with sheets:
            - Targeting: Main processed data with 58 columns
            - Bidding Adjustment: BA data with 48 columns
            - For Harvesting: Rows with NULL Target CPA
        """

        print(f"[DEBUG] Starting processing")
        start_time = time.time()

        self.logger.info("Starting Bids 30 Days bid processing")

        # Extract Port Values
        port_values_df = template_data.get("Port Values", pd.DataFrame())

        if port_values_df.empty:
            self.logger.error("Port Values sheet is empty or missing")
            return {}

        print(f"[DEBUG] Port Values shape: {port_values_df.shape}")

        # Get column mapping
        column_mapping = self._validation_details.get("column_mapping", {})

        # Process data
        if isinstance(bulk_data, dict):
            # Process each sheet
            results = {}

            # Process Targeting sheet
            if "Targeting" in bulk_data:
                targeting_df = bulk_data["Targeting"]
                print(f"[DEBUG] Processing Targeting sheet - {len(targeting_df)} rows")

                process_start = time.time()
                targeting_results, targeting_details = self.processor.process(
                    targeting_df,
                    port_values_df,
                    bulk_data.get("Bidding Adjustment", pd.DataFrame()),
                    column_mapping,
                )
                process_elapsed = time.time() - process_start
                print(
                    f"[DEBUG] Processor.process completed in {process_elapsed:.2f} seconds"
                )

                if targeting_results:
                    results.update(targeting_results)

                self._processing_details = targeting_details

            # Keep Bidding Adjustment as-is
            if "Bidding Adjustment" in bulk_data:
                ba_df = bulk_data["Bidding Adjustment"].copy()
                ba_df["Operation"] = "Update"
                results["Bidding Adjustment"] = ba_df
                print(f"[DEBUG] Added Bidding Adjustment sheet - {len(ba_df)} rows")

            # Keep Product Ad if exists
            if "Product Ad" in bulk_data:
                pa_df = bulk_data["Product Ad"].copy()
                pa_df["Operation"] = "Update"
                results["Product Ad"] = pa_df
                print(f"[DEBUG] Added Product Ad sheet - {len(pa_df)} rows")
        else:
            # Single DataFrame processing
            print(f"[DEBUG] Processing single DataFrame - {len(bulk_data)} rows")
            results, self._processing_details = self.processor.process(
                bulk_data, port_values_df, pd.DataFrame(), column_mapping
            )

        # Update statistics
        self._update_processing_stats()

        elapsed = time.time() - start_time
        print(f"[DEBUG] Total processing completed in {elapsed:.2f} seconds")

        if results:
            self.logger.info(
                f"Bids 30 Days processing complete: {len(results)} output sheets"
            )
        else:
            self.logger.error("Bids 30 Days processing returned no results")

        return results

    def _update_processing_stats(self):
        """Update processing statistics from processor details."""

        if not self._processing_details:
            return

        stats = self._processing_details.get("statistics", {})

        self.stats.update(
            {
                "rows_processed": stats.get("rows_processed", 0),
                "rows_modified": stats.get("rows_modified", 0),
                "rows_with_null_target_cpa": stats.get("null_target_cpa", 0),
                "rows_with_cvr_low": stats.get("cvr_below_threshold", 0),
                "rows_with_bid_errors": stats.get("bid_out_of_range", 0),
                "calculation_errors": stats.get("calculation_errors", 0),
                "rows_to_harvesting": stats.get("moved_to_harvesting", 0),
            }
        )

    def get_required_columns(self) -> List[str]:
        """Get list of required columns for Bids 30 Days optimization."""
        return [
            "Portfolio Name (Informational only)",
            "Units",
            "Bid",
            "Clicks",
            "Entity",
            "Campaign Name (Informational only)",
            "Campaign ID",
            "Match Type",
            "Product Targeting Expression",
            "Percentage",
            "Conversion Rate",
            "State",
            "Campaign State (Informational only)",
            "Ad Group State (Informational only)",
        ]

    def get_optional_columns(self) -> List[str]:
        """Get list of optional columns."""
        return [
            "Ad Group Name",
            "Ad Group ID",
            "Keyword Text",
            "ASIN",
            "Impressions",
            "Spend",
            "Sales",
            "Orders",
            "ACOS",
            "CPC",
            "ROAS",
        ]

    def get_description(self) -> str:
        """Get description of Bids 30 Days optimization."""
        return (
            "Bids 30 Days optimization processes products with units > 0 that meet "
            "specific criteria (units > 2 OR clicks > 30). It performs complex bid "
            "calculations using Target CPA, clicks/units ratio, and Max BA values. "
            "Creates separate 'For Harvesting' sheet for rows without Target CPA. "
            "Applies 8-step calculation process with Temp Bid and Max Bid logic."
        )

    def get_detailed_results(self) -> Dict[str, Any]:
        """Get detailed results including all processing details."""

        return {
            "optimization_name": self.name,
            "description": self.get_description(),
            "validation_details": self._validation_details,
            "cleaning_details": self._cleaning_details,
            "processing_details": self._processing_details,
            "processing_statistics": self.get_statistics(),
            "required_columns": self.get_required_columns(),
            "optional_columns": self.get_optional_columns(),
            "sheets_created": [
                "Targeting (58 columns)",
                "Bidding Adjustment (48 columns)",
                "For Harvesting (58 columns)",
            ],
        }

    def _generate_success_message(self) -> str:
        """Generate detailed success message."""

        stats = self.get_statistics()

        message_parts = [
            f"Bids 30 Days optimization complete:",
            f"{stats.get('rows_processed', 0)} rows processed",
        ]

        if stats.get("rows_to_harvesting", 0) > 0:
            message_parts.append(
                f"{stats.get('rows_to_harvesting', 0)} moved to For Harvesting"
            )

        if stats.get("rows_with_cvr_low", 0) > 0:
            message_parts.append(
                f"{stats.get('rows_with_cvr_low', 0)} rows with CVR < 8%"
            )

        if stats.get("calculation_errors", 0) > 0:
            message_parts.append(
                f"{stats.get('calculation_errors', 0)} calculation errors"
            )

        return " | ".join(message_parts)

    def get_processing_summary(self) -> Dict[str, Any]:
        """Get summary of processing steps and conditions."""

        return {
            "filtering_criteria": {
                "units": "> 0",
                "additional": "units > 2 OR clicks > 30",
                "state": "enabled",
                "excluded_portfolios": 10,
                "ignored_portfolios": "Base Bid = 'Ignore'",
            },
            "calculation_steps": {
                "step_1": "Fill base columns (Old Bid, Target CPA, Base Bid, Max BA, Adj. CPA)",
                "step_2": "Separate NULL Target CPA to For Harvesting",
                "step_3": "Calculate calc1 and calc2 based on 'up and' in campaign name",
                "step_4": "Determine Temp Bid based on calc2 threshold (1.1)",
                "step_5": "Calculate Max Bid based on units threshold (3)",
                "step_6": "Calculate calc3 = Temp Bid - Max Bid",
                "step_7": "Determine final Bid based on calc3",
                "step_8": "Mark rows for pink highlighting",
            },
            "highlighting_conditions": {
                "pink_rows": [
                    "Conversion Rate < 0.08",
                    "Bid < 0.02",
                    "Bid > 1.25",
                    "Calculation errors",
                ],
                "blue_headers": "Columns participating in processing",
            },
            "output_sheets": {
                "Targeting": "58 columns (48 original + 10 helper)",
                "Bidding Adjustment": "48 columns (original only)",
                "For Harvesting": "58 columns (NULL Target CPA rows)",
            },
        }
