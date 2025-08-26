"""Orchestrator for Bids 60 Days optimization."""

import pandas as pd
from typing import Dict, Tuple, Optional, Any
from io import BytesIO
import logging

from ..base_optimization import BaseOptimization
from .cleaner import Bids60DaysCleaner
from .processor import Bids60DaysProcessor
from .output_formatter import Bids60DaysOutputFormatter
from .constants import OPTIMIZATION_NAME
from data.writers.excel_writer import ExcelWriter


class Bids60DaysOptimization(BaseOptimization):
    """Orchestrates the Bids 60 Days optimization process."""
    
    def __init__(self):
        super().__init__(OPTIMIZATION_NAME)
        self.cleaner = Bids60DaysCleaner()
        self.processor = Bids60DaysProcessor()
        self.formatter = Bids60DaysOutputFormatter()
        self.excel_writer = ExcelWriter()
        
    def validate(self, 
                template_data: Dict[str, pd.DataFrame], 
                bulk_data: pd.DataFrame) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Validate data for Bids 60 Days optimization.
        
        Uses global validators - no specific validation needed.
        """
        # Basic checks
        if template_data is None or bulk_data is None:
            return False, "Missing required data files", {}
        
        if 'Port Values' not in template_data:
            return False, "Template missing Port Values sheet", {}
        
        if bulk_data.empty:
            return False, "Bulk data is empty", {}
        
        # Check for required columns in bulk
        required_columns = ['Entity', 'Units', 'Bid', 'State', 'Campaign ID']
        missing_columns = [col for col in required_columns if col not in bulk_data.columns]
        
        if missing_columns:
            return False, f"Bulk data missing columns: {missing_columns}", {}
        
        return True, "Validation passed", {"status": "valid"}
    
    def clean(self, 
             template_data: Dict[str, pd.DataFrame], 
             bulk_data: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Clean and filter data."""
        return self.cleaner.clean(template_data, bulk_data)
    
    def process(self, 
               template_data: Dict[str, pd.DataFrame], 
               bulk_data: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Process optimization and calculate new bids."""
        return self.processor.process(template_data, bulk_data)
    
    def run(self,
           template_data: Dict[str, pd.DataFrame],
           bulk_data: pd.DataFrame) -> Tuple[BytesIO, BytesIO, Dict[str, Any]]:
        """
        Run the complete Bids 60 Days optimization.
        
        Args:
            template_data: Template sheets dictionary
            bulk_data: Bulk campaign DataFrame
            
        Returns:
            Tuple of (working_file, clean_file, statistics)
        """
        try:
            self.logger.info(f"Starting {OPTIMIZATION_NAME} optimization")
            
            # Step 1: Validate
            is_valid, message, validation_details = self.validate(template_data, bulk_data)
            if not is_valid:
                raise ValueError(f"Validation failed: {message}")
            
            # Step 2: Clean
            cleaned_data, cleaning_stats = self.clean(template_data, bulk_data)
            self.logger.info(f"Cleaned data: {cleaning_stats['rows_after']} rows remaining")
            
            # Step 3: Process
            processed_sheets = self.process(template_data, cleaned_data)
            
            # Step 4: Format output
            formatted_sheets = self.formatter.format_output(processed_sheets)
            
            # Step 5: Create Excel files
            working_file = self._create_working_file(formatted_sheets)
            clean_file = self._create_clean_file(formatted_sheets)
            
            # Combine statistics
            statistics = self._combine_statistics(cleaning_stats)
            
            self.logger.info(f"Completed {OPTIMIZATION_NAME} optimization")
            
            return working_file, clean_file, statistics
            
        except Exception as e:
            self.logger.error(f"Error in {OPTIMIZATION_NAME}: {str(e)}")
            raise
    
    def _create_working_file(self, sheets_data: Dict[str, pd.DataFrame]) -> BytesIO:
        """Create working Excel file with all sheets."""
        # Use the ExcelWriter class for proper formatting
        return self.excel_writer.write_excel(sheets_data)
    
    def _create_clean_file(self, sheets_data: Dict[str, pd.DataFrame]) -> BytesIO:
        """Create clean Excel file (simplified version)."""
        # Use the ExcelWriter class for proper formatting
        return self.excel_writer.write_excel(sheets_data)
    
    def _combine_statistics(self, cleaning_stats: Dict[str, Any]) -> Dict[str, Any]:
        """Combine statistics from cleaner and processor."""
        processor_stats = self.processor.get_statistics()
        
        return {
            'optimization': OPTIMIZATION_NAME,
            'rows_before_cleaning': cleaning_stats['rows_before'],
            'rows_after_cleaning': cleaning_stats['rows_after'],
            'rows_processed': processor_stats['rows_processed'],
            'rows_modified': processor_stats['rows_modified'],
            'rows_to_harvesting': processor_stats['rows_to_harvesting'],
            'rows_with_low_cvr': processor_stats['rows_with_low_cvr'],
            'rows_with_bid_errors': processor_stats['rows_with_bid_errors'],
            'calculation_errors': processor_stats['calculation_errors']
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get optimization statistics."""
        return self._combine_statistics(self.cleaner.get_stats())
