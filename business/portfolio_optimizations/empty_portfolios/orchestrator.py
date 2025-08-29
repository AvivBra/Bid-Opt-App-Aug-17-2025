"""Orchestrator for Empty Portfolios optimization."""

import pandas as pd
from typing import Dict, Tuple, Optional, Any
import logging
from io import BytesIO

from .validator import EmptyPortfoliosValidator
from .cleaner import EmptyPortfoliosCleaner
from .processor import EmptyPortfoliosProcessor
from .output_formatter import EmptyPortfoliosOutputFormatter


class EmptyPortfoliosOrchestrator:
    """Orchestrates the Empty Portfolios optimization process."""
    
    def __init__(self):
        self.name = "Empty Portfolios"
        self.logger = logging.getLogger("empty_portfolios.orchestrator")
        
        # Initialize components
        self.validator = EmptyPortfoliosValidator()
        self.cleaner = EmptyPortfoliosCleaner()
        self.processor = EmptyPortfoliosProcessor()
        self.formatter = EmptyPortfoliosOutputFormatter()
        
        # Processing details
        self._validation_details = {}
        self._cleaning_details = {}
        self._processing_details = {}
    
    def run_optimization(
        self,
        bulk_data: Dict[str, pd.DataFrame]
    ) -> Tuple[bool, str, Optional[bytes]]:
        """
        Run the complete Empty Portfolios optimization.
        
        Args:
            bulk_data: Dictionary with sheet names as keys and DataFrames as values
            
        Returns:
            Tuple of (success, message, output_bytes)
        """
        try:
            # Step 1: Validation
            self.logger.info("Starting validation...")
            is_valid, validation_msg, validation_details = self.validator.validate(bulk_data)
            self._validation_details = validation_details
            
            if not is_valid:
                self.logger.error(f"Validation failed: {validation_msg}")
                return False, validation_msg, None
            
            self.logger.info(f"Validation passed: {validation_msg}")
            
            # Step 2: Cleaning
            self.logger.info("Starting data cleaning...")
            cleaned_data, cleaning_details = self.cleaner.clean(bulk_data)
            self._cleaning_details = cleaning_details
            
            self.logger.info(f"Cleaning complete: {cleaning_details['entity_campaign_count']} campaigns")
            
            # Step 3: Processing
            self.logger.info("Starting optimization processing...")
            processed_data = self.processor.process(cleaned_data)
            self._processing_details = self.processor.get_processing_stats()
            
            empty_count = self._processing_details.get("empty_portfolios_count", 0)
            self.logger.info(f"Processing complete: {empty_count} empty portfolios found")
            
            # Step 4: Generate output
            self.logger.info("Generating output file...")
            output_bytes = self._generate_output(processed_data)
            
            # Success message
            success_msg = self._generate_success_message()
            
            return True, success_msg, output_bytes
            
        except Exception as e:
            error_msg = f"Optimization error: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg, None
    
    def _generate_output(self, processed_data: Dict[str, pd.DataFrame]) -> bytes:
        """Generate Excel output file."""
        output = BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Format and write output
            self.formatter.format_output(processed_data, writer)
        
        output.seek(0)
        return output.read()
    
    def _generate_success_message(self) -> str:
        """Generate detailed success message."""
        empty_count = self._processing_details.get("empty_portfolios_count", 0)
        
        if empty_count == 0:
            return "✓ Processing complete. No empty portfolios found."
        
        msg_parts = [
            f"✓ Processing complete",
            f"✓ Found and updated {empty_count} empty portfolios",
            f"✓ Assigned new numeric names (1-{empty_count})",
            f"✓ Highlighted updated rows in yellow"
        ]
        
        return "\n".join(msg_parts)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get processing statistics."""
        return {
            "validation_details": self._validation_details,
            "cleaning_details": self._cleaning_details,
            "processing_details": self._processing_details,
            "optimization_name": self.name
        }
    
    def get_required_columns(self) -> list:
        """Get list of required columns."""
        from .constants import REQUIRED_COLUMNS
        return REQUIRED_COLUMNS
    
    def get_description(self) -> str:
        """Get optimization description."""
        return (
            "Empty Portfolios optimization identifies portfolios without any campaigns "
            "and assigns them numeric names for easy identification. It updates the "
            "Portfolio Name to the smallest available number and marks them for update."
        )
