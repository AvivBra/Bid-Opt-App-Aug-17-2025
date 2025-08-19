"""Base class for all bid optimizations."""

from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Any, Tuple, Optional, List
import logging


class BaseOptimization(ABC):
    """
    Abstract base class for all bid optimizations.
    
    Each optimization must implement validate(), clean(), and process() methods.
    This ensures consistent architecture and allows for easy addition of new optimizations.
    """
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"optimization.{name}")
        
        # Processing statistics
        self.stats = {
            'rows_processed': 0,
            'rows_modified': 0,
            'rows_skipped': 0,
            'errors': 0,
            'warnings': 0
        }
    
    @abstractmethod
    def validate(self, template_data: Dict[str, pd.DataFrame], bulk_data: pd.DataFrame) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Validate that the data is suitable for this optimization.
        
        Args:
            template_data: Dictionary containing template sheets
            bulk_data: Bulk campaign data DataFrame
            
        Returns:
            Tuple of (is_valid, message, validation_details)
        """
        pass
    
    @abstractmethod
    def clean(self, template_data: Dict[str, pd.DataFrame], bulk_data: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Clean and filter the data for processing.
        
        Args:
            template_data: Dictionary containing template sheets
            bulk_data: Bulk campaign data DataFrame
            
        Returns:
            Tuple of (cleaned_bulk_data, cleaning_details)
        """
        pass
    
    @abstractmethod
    def process(self, template_data: Dict[str, pd.DataFrame], bulk_data: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Process the optimization and return result DataFrames.
        
        Args:
            template_data: Dictionary containing template sheets
            bulk_data: Cleaned bulk campaign data DataFrame
            
        Returns:
            Dictionary of result DataFrames (e.g., {'Targeting': df1, 'Bidding Adjustment': df2})
        """
        pass
    
    def run_optimization(
        self, 
        template_data: Dict[str, pd.DataFrame], 
        bulk_data: pd.DataFrame
    ) -> Tuple[bool, str, Optional[Dict[str, pd.DataFrame]]]:
        """
        Run the complete optimization process.
        
        Returns:
            Tuple of (success, message, result_dataframes)
        """
        
        try:
            # Reset statistics
            self._reset_stats()
            
            self.logger.info(f"Starting {self.name} optimization")
            
            # Step 1: Validate
            valid, msg, validation_details = self.validate(template_data, bulk_data)
            if not valid:
                return False, f"Validation failed: {msg}", None
            
            self.logger.info(f"Validation passed: {msg}")
            
            # Step 2: Clean
            cleaned_data, cleaning_details = self.clean(template_data, bulk_data)
            if cleaned_data is None or cleaned_data.empty:
                return False, "No data available after cleaning", None
            
            self.logger.info(f"Data cleaned: {len(cleaned_data)} rows remaining")
            
            # Step 3: Process
            results = self.process(template_data, cleaned_data)
            if not results:
                return False, "Processing returned no results", None
            
            self.logger.info(f"Processing complete: {len(results)} result sheets generated")
            
            # Success
            success_msg = self._generate_success_message()
            return True, success_msg, results
            
        except Exception as e:
            self.logger.error(f"Error in {self.name} optimization: {str(e)}")
            return False, f"Optimization error: {str(e)}", None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get processing statistics."""
        return self.stats.copy()
    
    def _reset_stats(self):
        """Reset processing statistics."""
        for key in self.stats:
            self.stats[key] = 0
    
    def _update_stats(self, **kwargs):
        """Update processing statistics."""
        for key, value in kwargs.items():
            if key in self.stats:
                self.stats[key] += value
    
    def _generate_success_message(self) -> str:
        """Generate success message based on statistics."""
        return (
            f"{self.name} optimization complete: "
            f"{self.stats['rows_processed']} rows processed, "
            f"{self.stats['rows_modified']} rows modified"
        )
    
    def _find_column(self, df: pd.DataFrame, keywords: List[str], required: bool = True) -> Optional[str]:
        """
        Find a column in DataFrame using keyword matching.
        
        Args:
            df: DataFrame to search
            keywords: List of keywords to search for (case-insensitive)
            required: Whether this column is required
            
        Returns:
            Column name if found, None otherwise
        """
        
        df_cols_lower = {col.lower(): col for col in df.columns}
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            
            # Direct match
            if keyword_lower in df_cols_lower:
                return df_cols_lower[keyword_lower]
            
            # Partial match
            for col_lower, col_original in df_cols_lower.items():
                if keyword_lower in col_lower:
                    return col_original
        
        if required:
            self.logger.warning(f"Required column not found. Keywords: {keywords}")
        
        return None
    
    def _validate_numeric_column(self, df: pd.DataFrame, column: str, min_val: float = None, max_val: float = None) -> Tuple[bool, str]:
        """
        Validate that a column contains valid numeric data.
        
        Returns:
            Tuple of (is_valid, message)
        """
        
        if column not in df.columns:
            return False, f"Column '{column}' not found"
        
        try:
            # Convert to numeric
            numeric_data = pd.to_numeric(df[column], errors='coerce')
            
            # Check for NaN values
            nan_count = numeric_data.isnull().sum()
            if nan_count > len(df) * 0.5:  # More than 50% NaN
                return False, f"Column '{column}' has too many non-numeric values ({nan_count}/{len(df)})"
            
            # Check range if specified
            if min_val is not None or max_val is not None:
                valid_data = numeric_data.dropna()
                if not valid_data.empty:
                    if min_val is not None and valid_data.min() < min_val:
                        return False, f"Column '{column}' has values below minimum ({min_val})"
                    if max_val is not None and valid_data.max() > max_val:
                        return False, f"Column '{column}' has values above maximum ({max_val})"
            
            return True, f"Column '{column}' validation passed"
            
        except Exception as e:
            return False, f"Error validating column '{column}': {str(e)}"
    
    def _safe_numeric_conversion(self, series: pd.Series, default_value: float = 0.0) -> pd.Series:
        """Safely convert a series to numeric, replacing errors with default value."""
        return pd.to_numeric(series, errors='coerce').fillna(default_value)
    
    def _log_data_info(self, df: pd.DataFrame, description: str = "DataFrame"):
        """Log basic information about a DataFrame."""
        self.logger.info(f"{description}: {len(df)} rows, {len(df.columns)} columns")
        if df.empty:
            self.logger.warning(f"{description} is empty")
    
    def get_required_columns(self) -> List[str]:
        """
        Get list of required columns for this optimization.
        Override in subclasses to specify requirements.
        """
        return []
    
    def get_optional_columns(self) -> List[str]:
        """
        Get list of optional columns for this optimization.
        Override in subclasses to specify optional columns.
        """
        return []
    
    def get_description(self) -> str:
        """
        Get description of what this optimization does.
        Override in subclasses to provide meaningful descriptions.
        """
        return f"{self.name} optimization"