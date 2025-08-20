"""Zero Sales optimization orchestrator."""

import pandas as pd
from typing import Dict, Any, Tuple, Optional, List
import logging

from business.bid_optimizations.base_optimization import BaseOptimization
from business.bid_optimizations.zero_sales.validator import ZeroSalesValidator
from business.bid_optimizations.zero_sales.cleaner import ZeroSalesCleaner
from business.bid_optimizations.zero_sales.processor import ZeroSalesProcessor


class ZeroSalesOptimization(BaseOptimization):
    """
    Zero Sales optimization implementation.
    
    Identifies products with 0 units sold and optimizes their bids using 4 calculation cases:
    - Case A: Target CPA empty + "up and" -> Base Bid * 1.25
    - Case B: Target CPA empty + no "up and" -> Base Bid * 1.5  
    - Case C: Target CPA filled + "up and" -> min(Base Bid * 1.25, Target CPA)
    - Case D: Target CPA filled + no "up and" -> min(Base Bid * 1.5, Target CPA)
    """
    
    def __init__(self):
        super().__init__("Zero Sales")
        
        # Initialize components
        self.validator = ZeroSalesValidator()
        self.cleaner = ZeroSalesCleaner()
        self.processor = ZeroSalesProcessor()
        
        # Store validation and cleaning results for processing
        self._validation_details = {}
        self._cleaning_details = {}
    
    def validate(self, template_data: Dict[str, pd.DataFrame], bulk_data: pd.DataFrame) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Validate data requirements for Zero Sales optimization.
        
        Checks for:
        - Required columns (Portfolio, Units, Bid, Clicks)
        - Template portfolio data
        - Zero sales candidates (Units = 0)
        - Data quality
        """
        
        self.logger.info("Starting Zero Sales validation")
        
        valid, msg, details = self.validator.validate(template_data, bulk_data)
        
        # Store validation details for later use
        self._validation_details = details.copy()
        
        if valid:
            self.logger.info(f"Zero Sales validation passed: {msg}")
        else:
            self.logger.error(f"Zero Sales validation failed: {msg}")
        
        return valid, msg, details
    
    def clean(self, template_data: Dict[str, pd.DataFrame], bulk_data: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Clean and filter data for Zero Sales processing.
        
        Applies filters:
        - Removes 10 'Flat' portfolios
        - Removes portfolios marked as 'Ignore' in template  
        - Filters to only rows with Units = 0
        - Adds helper columns and template data mapping
        """
        
        self.logger.info("Starting Zero Sales data cleaning")
        
        # Get column mapping from validation
        column_mapping = self._validation_details.get('column_mapping', {})
        
        if not column_mapping:
            self.logger.error("Column mapping not available from validation")
            return pd.DataFrame(), {'error': 'Column mapping missing'}
        
        cleaned_df, cleaning_details = self.cleaner.clean(template_data, bulk_data, column_mapping)
        
        # Store cleaning details for later use
        self._cleaning_details = cleaning_details.copy()
        
        if cleaned_df.empty:
            self.logger.warning("No data remaining after cleaning")
        else:
            self.logger.info(f"Zero Sales cleaning complete: {len(cleaned_df)} rows remaining")
        
        return cleaned_df, cleaning_details
    
    def process(self, template_data: Dict[str, pd.DataFrame], bulk_data: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Process Zero Sales bid calculations.
        
        Applies the 4 calculation cases to determine new bid values:
        - Analyzes Target CPA and targeting content
        - Calculates new bids based on Base Bid multipliers
        - Applies Target CPA limits where applicable
        - Generates Targeting and Bidding Adjustment sheets
        """
        
        self.logger.info("Starting Zero Sales bid processing")
        
        # Get column mapping from validation
        column_mapping = self._validation_details.get('column_mapping', {})
        
        if not column_mapping:
            self.logger.error("Column mapping not available for processing")
            return {}
        
        results, processing_details = self.processor.process(bulk_data, column_mapping)
        
        # Update statistics
        case_stats = processing_details.get('case_statistics', {})
        self.stats.update({
            'rows_processed': processing_details.get('processed_rows', 0),
            'rows_modified': processing_details.get('processed_rows', 0),
            'case_a': case_stats.get('case_a_count', 0),
            'case_b': case_stats.get('case_b_count', 0),
            'case_c': case_stats.get('case_c_count', 0),
            'case_d': case_stats.get('case_d_count', 0),
            'bid_range_issues': case_stats.get('out_of_range_count', 0),
            'errors': case_stats.get('processing_errors', 0)
        })
        
        if results:
            self.logger.info(f"Zero Sales processing complete: {len(results)} output sheets generated")
        else:
            self.logger.error("Zero Sales processing returned no results")
        
        return results
    
    def get_required_columns(self) -> List[str]:
        """Get list of required columns for Zero Sales optimization."""
        return [
            'Portfolio (or similar)',
            'Units (or similar)', 
            'Bid/Max CPC (or similar)',
            'Clicks (optional but recommended)'
        ]
    
    def get_optional_columns(self) -> List[str]:
        """Get list of optional columns for Zero Sales optimization."""
        return [
            'Campaign',
            'Ad Group', 
            'Targeting/Keyword/ASIN',
            'Match Type'
        ]
    
    def get_description(self) -> str:
        """Get description of Zero Sales optimization."""
        return (
            "Zero Sales optimization identifies products with 0 units sold and adjusts their bids "
            "using 4 calculation cases based on Target CPA values and targeting content. "
            "Filters out excluded portfolios and applies Base Bid multipliers (1.25x or 1.5x) "
            "with optional Target CPA limits."
        )
    
    def get_detailed_results(self) -> Dict[str, Any]:
        """Get detailed results including validation, cleaning, and processing details."""
        
        return {
            'optimization_name': self.name,
            'description': self.get_description(),
            'validation_details': self._validation_details,
            'cleaning_details': self._cleaning_details, 
            'processing_statistics': self.get_statistics(),
            'required_columns': self.get_required_columns(),
            'optional_columns': self.get_optional_columns()
        }
    
    def _generate_success_message(self) -> str:
        """Generate detailed success message."""
        
        stats = self.get_statistics()
        
        return (
            f"Zero Sales optimization complete: "
            f"{stats.get('rows_processed', 0)} rows processed "
            f"(A:{stats.get('case_a', 0)}, B:{stats.get('case_b', 0)}, "
            f"C:{stats.get('case_c', 0)}, D:{stats.get('case_d', 0)})"
        )
    
    def get_case_breakdown(self) -> Dict[str, Any]:
        """Get detailed breakdown of calculation cases."""
        
        stats = self.get_statistics()
        
        return {
            'case_a': {
                'name': 'Case A',
                'description': 'Target CPA empty + "up and" targeting',
                'calculation': 'Base Bid × 1.25',
                'count': stats.get('case_a', 0)
            },
            'case_b': {
                'name': 'Case B', 
                'description': 'Target CPA empty + no "up and" targeting',
                'calculation': 'Base Bid × 1.5',
                'count': stats.get('case_b', 0)
            },
            'case_c': {
                'name': 'Case C',
                'description': 'Target CPA filled + "up and" targeting', 
                'calculation': 'min(Base Bid × 1.25, Target CPA)',
                'count': stats.get('case_c', 0)
            },
            'case_d': {
                'name': 'Case D',
                'description': 'Target CPA filled + no "up and" targeting',
                'calculation': 'min(Base Bid × 1.5, Target CPA)', 
                'count': stats.get('case_d', 0)
            }
        }
