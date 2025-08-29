"""Orchestrator for Campaigns Without Portfolios optimization."""

import pandas as pd
from typing import Dict, Tuple, Any, Optional
import logging
from .validator import CampaignsWithoutPortfoliosValidator
from .cleaner import CampaignsWithoutPortfoliosCleaner
from .processor import CampaignsWithoutPortfoliosProcessor
from .output_formatter import CampaignsWithoutPortfoliosOutputFormatter
from .constants import SUCCESS_MESSAGES, ERROR_MESSAGES


class CampaignsWithoutPortfoliosOrchestrator:
    """Orchestrates the Campaigns Without Portfolios optimization workflow."""
    
    def __init__(self):
        self.logger = logging.getLogger("campaigns_without_portfolios.orchestrator")
        self.validator = CampaignsWithoutPortfoliosValidator()
        self.cleaner = CampaignsWithoutPortfoliosCleaner()
        self.processor = CampaignsWithoutPortfoliosProcessor()
        self.output_formatter = CampaignsWithoutPortfoliosOutputFormatter()
        
    def run(
        self,
        bulk_data: Dict[str, pd.DataFrame],
        combined_with_empty_portfolios: bool = False
    ) -> Tuple[Optional[pd.DataFrame], Dict[str, Any]]:
        """
        Run the complete Campaigns Without Portfolios optimization.
        
        Args:
            bulk_data: Dictionary with sheet names as keys and DataFrames as values
            combined_with_empty_portfolios: Whether this is running with Empty Portfolios
            
        Returns:
            Tuple of (processed_dataframe, processing_details)
        """
        details = {
            "validation": {},
            "cleaning": {},
            "processing": {},
            "summary": {}
        }
        
        try:
            # Step 1: Validation
            self.logger.info("Starting validation...")
            is_valid, validation_details = self.validator.validate(bulk_data)
            details["validation"] = validation_details
            
            if not is_valid:
                self.logger.error("Validation failed")
                details["summary"]["error"] = ERROR_MESSAGES["missing_columns"]
                return None, details
            
            self.logger.info(SUCCESS_MESSAGES["validation_passed"])
            
            # Step 2: Cleaning
            self.logger.info("Cleaning data...")
            cleaned_data, cleaning_details = self.cleaner.clean(bulk_data)
            details["cleaning"] = cleaning_details
            
            # Step 3: Processing
            self.logger.info("Processing campaigns without portfolios...")
            processed_data = self.processor.process(
                cleaned_data,
                combined_with_empty_portfolios
            )
            
            # Get processing statistics
            details["processing"] = self.processor.get_processing_stats()
            
            # Step 4: Format output
            self.logger.info("Formatting output...")
            if combined_with_empty_portfolios:
                # If combined, return processed data for merging
                output_df = processed_data["Sponsored Products Campaigns Full"]
            else:
                # If standalone, format for direct output
                output_df = self.output_formatter.format_output(processed_data)
            
            # Summary
            campaigns_updated = details["processing"].get("campaigns_updated", 0)
            if campaigns_updated > 0:
                details["summary"]["message"] = SUCCESS_MESSAGES["campaigns_updated"].format(
                    count=campaigns_updated
                )
            else:
                details["summary"]["message"] = SUCCESS_MESSAGES["no_campaigns_found"]
            
            details["summary"]["success"] = True
            
            return output_df, details
            
        except Exception as e:
            self.logger.error(f"Orchestration failed: {str(e)}")
            details["summary"]["error"] = f"{ERROR_MESSAGES['processing_failed']}: {str(e)}"
            details["summary"]["success"] = False
            return None, details
    
    def get_updated_indices(self) -> list:
        """
        Get indices of rows that were updated.
        
        Returns:
            List of row indices that were modified
        """
        return self.processor.get_updated_indices()
