"""Output formatter for bid optimization results."""

import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging


class OutputFormatter:
    """
    Formats optimization results for Excel output.
    
    Handles:
    - Creating separate sheets for different entity types
    - Adding helper columns in the correct position
    - Marking rows with bid range issues
    - Ensuring Operation column is set to "Update"
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Helper columns to add (in order)
        self.helper_columns = [
            'Old Bid',
            'calc1', 
            'calc2',
            'Target CPA',
            'Base Bid',
            'Adj. CPA',
            'Max BA'
        ]
        
        # Valid bid range
        self.min_bid = 0.02
        self.max_bid = 4.00
        
    def format_for_output(self, optimization_results: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """
        Format optimization results for Excel output.
        
        Args:
            optimization_results: Dictionary of DataFrames from optimization
            
        Returns:
            Dictionary of formatted DataFrames ready for Excel writing
        """
        
        formatted_sheets = {}
        
        for sheet_name, df in optimization_results.items():
            if df.empty:
                continue
                
            # Process based on sheet type
            if 'targeting' in sheet_name.lower() or 'keyword' in sheet_name.lower():
                # Main sheet - gets helper columns
                formatted_df = self._format_targeting_sheet(df)
                formatted_sheets['Clean Zero Sales'] = formatted_df
                
            elif 'bidding' in sheet_name.lower():
                # Bidding Adjustment - no helper columns
                formatted_df = self._format_bidding_sheet(df)
                formatted_sheets['Bidding Adjustment Zero Sales'] = formatted_df
                
            elif 'product' in sheet_name.lower() and 'ad' in sheet_name.lower():
                # Product Ad - no helper columns
                formatted_df = self._format_product_ad_sheet(df)
                formatted_sheets['Product Ad Zero Sales'] = formatted_df
                
            else:
                # Default formatting
                formatted_df = self._format_default_sheet(df)
                formatted_sheets[sheet_name] = formatted_df
        
        return formatted_sheets
    
    def _format_targeting_sheet(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Format the main targeting sheet with helper columns.
        
        Adds 7 helper columns to the left of Bid column (column 28).
        """
        
        df = df.copy()
        
        # Ensure Operation is Update
        if 'Operation' in df.columns:
            df['Operation'] = 'Update'
        
        # Rearrange columns with helper columns in correct position
        df = self._arrange_columns_with_helpers(df)
        
        # Mark rows with bid issues
        df = self._mark_bid_issues(df)
        
        self.logger.info(f"Formatted targeting sheet: {len(df)} rows")
        
        return df
    
    def _format_bidding_sheet(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Format the bidding adjustment sheet without helper columns.
        """
        
        df = df.copy()
        
        # Ensure Operation is Update
        if 'Operation' in df.columns:
            df['Operation'] = 'Update'
        
        # Remove helper columns if present
        df = self._remove_helper_columns(df)
        
        self.logger.info(f"Formatted bidding sheet: {len(df)} rows")
        
        return df
    
    def _format_product_ad_sheet(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Format the product ad sheet without helper columns.
        """
        
        df = df.copy()
        
        # Ensure Operation is Update
        if 'Operation' in df.columns:
            df['Operation'] = 'Update'
        
        # Remove helper columns if present
        df = self._remove_helper_columns(df)
        
        self.logger.info(f"Formatted product ad sheet: {len(df)} rows")
        
        return df
    
    def _format_default_sheet(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Default formatting for any other sheets.
        """
        
        df = df.copy()
        
        # Ensure Operation is Update
        if 'Operation' in df.columns:
            df['Operation'] = 'Update'
        
        return df
    
    def _arrange_columns_with_helpers(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Arrange columns with helper columns in the correct position.
        
        Helper columns should be inserted to the left of the Bid column (column 28).
        """
        
        # Get all columns
        all_cols = df.columns.tolist()
        
        # Find Bid column position (should be column 28 in original)
        bid_col = None
        for col in all_cols:
            if 'bid' in col.lower() and 'default' not in col.lower():
                bid_col = col
                break
        
        if not bid_col:
            self.logger.warning("Bid column not found, returning dataframe as-is")
            return df
        
        bid_index = all_cols.index(bid_col)
        
        # Separate original columns from helper columns
        original_cols = [col for col in all_cols if col not in self.helper_columns]
        existing_helpers = [col for col in self.helper_columns if col in all_cols]
        
        # Build new column order
        # Columns before Bid + Helper columns + Bid + Columns after Bid
        new_cols = (
            original_cols[:bid_index] +  # Columns before Bid
            existing_helpers +            # Helper columns
            original_cols[bid_index:]     # Bid and columns after
        )
        
        # Reorder dataframe
        return df[new_cols]
    
    def _remove_helper_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove helper columns from dataframe.
        """
        
        cols_to_keep = [col for col in df.columns if col not in self.helper_columns]
        return df[cols_to_keep]
    
    def _mark_bid_issues(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Mark rows with bid values outside the valid range.
        
        Adds 'has_error' column for Excel writer to identify rows to highlight.
        """
        
        df['has_error'] = False
        
        # Find bid column
        bid_col = None
        for col in df.columns:
            if 'bid' in col.lower() and 'default' not in col.lower() and 'old' not in col.lower():
                bid_col = col
                break
        
        if bid_col:
            # Mark rows with bid issues
            df.loc[df[bid_col] < self.min_bid, 'has_error'] = True
            df.loc[df[bid_col] > self.max_bid, 'has_error'] = True
            df.loc[df[bid_col].isna(), 'has_error'] = True
            
            error_count = df['has_error'].sum()
            if error_count > 0:
                self.logger.warning(f"Found {error_count} rows with bid range issues")
        
        return df
    
    def calculate_statistics(self, formatted_sheets: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        Calculate statistics for the formatted output.
        """
        
        stats = {
            'total_rows': 0,
            'rows_modified': 0,
            'rows_with_errors': 0,
            'sheets_created': len(formatted_sheets),
            'bid_range_issues': 0,
            'processing_timestamp': datetime.now().isoformat()
        }
        
        for sheet_name, df in formatted_sheets.items():
            stats['total_rows'] += len(df)
            
            # Count modified rows (where Old Bid != Bid)
            if 'Old Bid' in df.columns:
                bid_col = None
                for col in df.columns:
                    if 'bid' in col.lower() and 'old' not in col.lower() and 'default' not in col.lower():
                        bid_col = col
                        break
                
                if bid_col:
                    modified = df[df['Old Bid'] != df[bid_col]]
                    stats['rows_modified'] += len(modified)
            
            # Count error rows
            if 'has_error' in df.columns:
                stats['rows_with_errors'] += df['has_error'].sum()
                stats['bid_range_issues'] += df['has_error'].sum()
        
        return stats
    
    def prepare_for_excel(self, sheets_dict: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """
        Final preparation for Excel writing.
        
        Ensures all sheets are ready for Excel output.
        """
        
        prepared_sheets = {}
        
        for sheet_name, df in sheets_dict.items():
            # Remove the has_error column (used only for highlighting)
            if 'has_error' in df.columns:
                # Store error indices before removing
                error_indices = df[df['has_error'] == True].index.tolist()
                df = df.drop('has_error', axis=1)
                
                # Store error indices in dataframe attributes for Excel writer
                df.attrs['error_rows'] = error_indices
            
            prepared_sheets[sheet_name] = df
        
        return prepared_sheets
