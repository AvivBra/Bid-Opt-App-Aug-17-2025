"""Orchestrator for Empty Portfolios optimization."""

import pandas as pd
from typing import Dict, Tuple, Any, Optional
import logging
from .validator import EmptyPortfoliosValidator
from .cleaner import EmptyPortfoliosCleaner
from .processor import EmptyPortfoliosProcessor
from .output_formatter import EmptyPortfoliosOutputFormatter
from .constants import SUCCESS_MESSAGES, ERROR_MESSAGES


class EmptyPortfoliosOrchestrator:
    """Orchestrates the Empty Portfolios optimization workflow."""

    def __init__(self):
        self.logger = logging.getLogger("empty_portfolios.orchestrator")
        self.validator = EmptyPortfoliosValidator()
        self.cleaner = EmptyPortfoliosCleaner()
        self.processor = EmptyPortfoliosProcessor()
        self.output_formatter = EmptyPortfoliosOutputFormatter()

    def run(
        self, bulk_data: Dict[str, pd.DataFrame], combined_mode: bool = True
    ) -> Tuple[Optional[pd.DataFrame], Dict[str, Any]]:
        """
        Run the complete Empty Portfolios optimization.

        Args:
            bulk_data: Dictionary with sheet names as keys and DataFrames as values
            combined_mode: Whether this is running in combined mode (standardized parameter)

        Returns:
            Tuple of (processed_dataframe, processing_details)
        """
        details = {"validation": {}, "cleaning": {}, "processing": {}, "summary": {}}

        try:
            # Step 1: Validation
            self.logger.info("Starting validation...")
            is_valid, validation_details = self.validator.validate(bulk_data)
            details["validation"] = validation_details

            if not is_valid:
                self.logger.error("Validation failed")
                details["summary"]["error"] = ERROR_MESSAGES["missing_columns"]
                details["summary"]["success"] = False
                return None, details

            self.logger.info(SUCCESS_MESSAGES["validation_passed"])

            # Step 2: Cleaning
            self.logger.info("Cleaning data...")
            cleaned_data, cleaning_details = self.cleaner.clean(bulk_data)
            details["cleaning"] = cleaning_details

            # Step 3: Processing
            self.logger.info("Processing campaigns without portfolios...")
            processed_data = self.processor.process(cleaned_data, combined_mode)

            # Get processing statistics
            details["processing"] = self.processor.get_processing_stats()

            # Step 4: Format output for combined mode
            self.logger.info("Formatting output...")
            if combined_mode:
                # FIX: Return the full dataframe with ONLY the updated rows marked
                # The processor already updated the full dataframe
                output_df = processed_data["Sponsored Products Campaigns Full"]

                # Store the updated indices in details for the results_manager
                details["updated_indices"] = self.processor.get_updated_indices()

                self.logger.info(
                    f"Returning full DataFrame with {len(details['updated_indices'])} updated rows"
                )
            else:
                # If standalone, format for direct output
                output_df = self.output_formatter.format_output(processed_data)

            # Summary
            campaigns_updated = details["processing"].get("campaigns_updated", 0)
            if campaigns_updated > 0:
                details["summary"]["message"] = SUCCESS_MESSAGES[
                    "campaigns_updated"
                ].format(count=campaigns_updated)
                self.logger.info(f"Successfully updated {campaigns_updated} campaigns")
            else:
                details["summary"]["message"] = SUCCESS_MESSAGES["no_campaigns_found"]
                self.logger.info("No campaigns without portfolios found")

            details["summary"]["success"] = True

            return output_df, details

        except Exception as e:
            self.logger.error(f"Orchestration failed: {str(e)}")
            details["summary"]["error"] = (
                f"{ERROR_MESSAGES['processing_failed']}: {str(e)}"
            )
            details["summary"]["success"] = False
            return None, details

    def get_updated_indices(self) -> list:
        """
        Get indices of rows that were updated.

        Returns:
            List of row indices that were modified
        """
        return self.processor.get_updated_indices()
