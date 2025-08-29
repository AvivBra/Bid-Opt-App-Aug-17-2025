"""Base class for portfolio optimization algorithms."""

from abc import ABC, abstractmethod
from typing import Dict, Tuple, Optional, Any
import pandas as pd
import logging


class PortfolioBaseOptimization(ABC):
    """Abstract base class for portfolio optimization algorithms."""
    
    def __init__(self, name: str):
        """
        Initialize the base optimization.
        
        Args:
            name: Name of the optimization algorithm
        """
        self.name = name
        self.logger = logging.getLogger(f"portfolio_optimization.{name}")
        self._validation_details = {}
        self._processing_details = {}
        self._statistics = {}
    
    @abstractmethod
    def validate(self, bulk_data: Dict[str, pd.DataFrame]) -> Tuple[bool, str]:
        """
        Validate input data for the optimization.
        
        Args:
            bulk_data: Dictionary of DataFrames from bulk file
            
        Returns:
            Tuple of (success, message)
        """
        pass
    
    @abstractmethod
    def process(self, bulk_data: Dict[str, pd.DataFrame]) -> Tuple[bool, str, Optional[Dict[str, pd.DataFrame]]]:
        """
        Process the optimization algorithm.
        
        Args:
            bulk_data: Dictionary of DataFrames from bulk file
            
        Returns:
            Tuple of (success, message, processed_data)
        """
        pass
    
    @abstractmethod
    def format_output(self, processed_data: Dict[str, pd.DataFrame]) -> bytes:
        """
        Format processed data for output.
        
        Args:
            processed_data: Dictionary of processed DataFrames
            
        Returns:
            Formatted output as bytes (Excel file)
        """
        pass
    
    def run_optimization(
        self,
        bulk_data: Dict[str, pd.DataFrame]
    ) -> Tuple[bool, str, Optional[bytes]]:
        """
        Run the complete optimization pipeline.
        
        Args:
            bulk_data: Dictionary of DataFrames from bulk file
            
        Returns:
            Tuple of (success, message, output_bytes)
        """
        try:
            # Step 1: Validate
            self.logger.info(f"Starting {self.name} optimization")
            valid, validation_msg = self.validate(bulk_data)
            
            if not valid:
                self.logger.error(f"Validation failed: {validation_msg}")
                return False, validation_msg, None
            
            self.logger.info("Validation passed")
            
            # Step 2: Process
            success, process_msg, processed_data = self.process(bulk_data)
            
            if not success:
                self.logger.error(f"Processing failed: {process_msg}")
                return False, process_msg, None
            
            self.logger.info("Processing completed successfully")
            
            # Step 3: Format output
            if processed_data:
                output_bytes = self.format_output(processed_data)
                self.logger.info(f"{self.name} optimization completed successfully")
                return True, f"{self.name} optimization completed successfully", output_bytes
            else:
                return False, "No data to output", None
                
        except Exception as e:
            self.logger.error(f"Error in {self.name} optimization: {str(e)}", exc_info=True)
            return False, f"Error: {str(e)}", None
    
    def get_validation_details(self) -> Dict[str, Any]:
        """Get detailed validation results."""
        return self._validation_details
    
    def get_processing_details(self) -> Dict[str, Any]:
        """Get detailed processing results."""
        return self._processing_details
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get optimization statistics."""
        return self._statistics
    
    def _update_statistics(self, key: str, value: Any) -> None:
        """Update optimization statistics."""
        self._statistics[key] = value
    
    def _log_dataframe_info(self, df: pd.DataFrame, name: str) -> None:
        """Log DataFrame information for debugging."""
        self.logger.debug(f"{name} shape: {df.shape}")
        self.logger.debug(f"{name} columns: {df.columns.tolist()}")
        self.logger.debug(f"{name} dtypes: {df.dtypes.to_dict()}")
        self.logger.debug(f"{name} null counts: {df.isnull().sum().to_dict()}")
