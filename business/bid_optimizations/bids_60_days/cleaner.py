"""Data cleaning for Bids 60 Days optimization."""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Any, List, Optional
from .constants import (
    EXCLUDED_PORTFOLIOS,
    TARGET_ENTITIES,
    SEPARATE_ENTITIES,
    UNITS_THRESHOLD
)


class Bids60DaysCleaner:
    """Handles data cleaning for Bids 60 Days optimization."""
    
    def __init__(self):
        self.stats = {
            'rows_before': 0,
            'rows_after': 0,
            'rows_removed_units': 0,
            'rows_removed_portfolio': 0,
            'rows_removed_delete_60': 0,
            'rows_removed_state': 0,
            'rows_removed_ignore': 0
        }
    
    def clean(self, 
              template_data: Dict[str, pd.DataFrame], 
              bulk_data: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Clean and filter data for Bids 60 Days optimization.
        
        Args:
            template_data: Dictionary containing template sheets
            bulk_data: Bulk campaign data DataFrame
            
        Returns:
            Tuple of (cleaned_data, cleaning_stats)
        """
        self.stats['rows_before'] = len(bulk_data)
        
        # Create a copy to avoid modifying original
        df = bulk_data.copy()
        
        # Step 1: Split by Entity type
        targeting_df, bidding_df = self._split_by_entity(df)
        
        # Step 2: Filter units > 0 (only on targeting data)
        targeting_df = self._filter_by_units(targeting_df)
        
        # Step 3: Remove excluded portfolios
        targeting_df = self._remove_excluded_portfolios(targeting_df)
        
        # Step 4: Remove portfolios with Base Bid = 'Ignore'
        if 'Port Values' in template_data:
            targeting_df = self._remove_ignored_portfolios(
                targeting_df, 
                template_data['Port Values']
            )
        
        # Step 5: Remove IDs from Delete for 60 sheet
        if 'Delete for 60' in template_data:
            targeting_df = self._remove_delete_for_60_ids(
                targeting_df,
                template_data['Delete for 60']
            )
        
        # State filtering is now done in pre_validation_filter() - no duplicate filtering needed
        
        # Combine targeting and bidding data back
        cleaned_data = pd.concat([targeting_df, bidding_df], ignore_index=True)
        
        self.stats['rows_after'] = len(cleaned_data)
        
        return cleaned_data, self.stats
    
    def _split_by_entity(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Split data by Entity type."""
        # Targeting entities (Keyword, Product Targeting)
        targeting_mask = df['Entity'].isin(TARGET_ENTITIES)
        targeting_df = df[targeting_mask].copy()
        
        # Bidding entities (Bidding Adjustment, Product Ad)
        bidding_mask = df['Entity'].isin(SEPARATE_ENTITIES)
        bidding_df = df[bidding_mask].copy()
        
        return targeting_df, bidding_df
    
    def _filter_by_units(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filter rows where units > 0."""
        initial_count = len(df)
        
        # Convert Units to numeric, handling any non-numeric values
        df['Units'] = pd.to_numeric(df['Units'], errors='coerce').fillna(0)
        
        # Filter units > 0
        filtered_df = df[df['Units'] > UNITS_THRESHOLD].copy()
        
        self.stats['rows_removed_units'] = initial_count - len(filtered_df)
        
        return filtered_df
    
    def _remove_excluded_portfolios(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove rows with excluded portfolio names."""
        initial_count = len(df)
        
        # DEBUG: Log initial state
        print(f"[DEBUG Portfolio Exclusion] Starting with {initial_count} rows")
        
        # Get portfolio column name (might vary)
        portfolio_col = None
        for col in ['Portfolio Name (Informational only)', 'Portfolio Name', 'Portfolio']:
            if col in df.columns:
                portfolio_col = col
                break
        
        # DEBUG: Log column detection
        print(f"[DEBUG Portfolio Exclusion] Portfolio column found: '{portfolio_col}'")
        print(f"[DEBUG Portfolio Exclusion] Available columns: {list(df.columns)}")
        
        if portfolio_col:
            # DEBUG: Log unique portfolio names in data
            unique_portfolios = df[portfolio_col].dropna().unique()
            print(f"[DEBUG Portfolio Exclusion] Unique portfolios in data ({len(unique_portfolios)}):")
            for portfolio in sorted(unique_portfolios):
                print(f"[DEBUG Portfolio Exclusion]   '{portfolio}'")
            
            # DEBUG: Log exclusion list
            print(f"[DEBUG Portfolio Exclusion] Excluded portfolios list ({len(EXCLUDED_PORTFOLIOS)}):")
            for portfolio in EXCLUDED_PORTFOLIOS:
                print(f"[DEBUG Portfolio Exclusion]   '{portfolio}'")
            
            # Check which portfolios will be excluded
            excluded_found = df[portfolio_col].isin(EXCLUDED_PORTFOLIOS)
            excluded_portfolios_found = df[excluded_found][portfolio_col].unique()
            print(f"[DEBUG Portfolio Exclusion] Portfolios being excluded ({len(excluded_portfolios_found)}):")
            for portfolio in excluded_portfolios_found:
                print(f"[DEBUG Portfolio Exclusion]   '{portfolio}' (found {(df[portfolio_col] == portfolio).sum()} rows)")
            
            # Remove excluded portfolios
            mask = ~df[portfolio_col].isin(EXCLUDED_PORTFOLIOS)
            filtered_df = df[mask].copy()
        else:
            print("[DEBUG Portfolio Exclusion] No portfolio column found - no exclusion applied")
            filtered_df = df.copy()
        
        removed_count = initial_count - len(filtered_df)
        self.stats['rows_removed_portfolio'] = removed_count
        
        print(f"[DEBUG Portfolio Exclusion] Removed {removed_count} rows, {len(filtered_df)} remaining")
        
        return filtered_df
    
    def _remove_ignored_portfolios(self, 
                                   df: pd.DataFrame, 
                                   port_values: pd.DataFrame) -> pd.DataFrame:
        """Remove portfolios marked as 'Ignore' in template."""
        initial_count = len(df)
        
        # Get portfolios with Base Bid = 'Ignore'
        ignored_portfolios = port_values[
            port_values['Base Bid'].astype(str).str.lower() == 'ignore'
        ]['Portfolio Name'].tolist()
        
        if ignored_portfolios:
            # Get portfolio column name
            portfolio_col = None
            for col in ['Portfolio Name (Informational only)', 'Portfolio Name', 'Portfolio']:
                if col in df.columns:
                    portfolio_col = col
                    break
            
            if portfolio_col:
                mask = ~df[portfolio_col].isin(ignored_portfolios)
                filtered_df = df[mask].copy()
            else:
                filtered_df = df.copy()
        else:
            filtered_df = df.copy()
        
        self.stats['rows_removed_ignore'] = initial_count - len(filtered_df)
        
        return filtered_df
    
    def _remove_delete_for_60_ids(self,
                                  df: pd.DataFrame,
                                  delete_sheet: pd.DataFrame) -> pd.DataFrame:
        """Remove rows with IDs listed in Delete for 60 sheet."""
        initial_count = len(df)
        
        # Get IDs to delete - clean conversion to avoid type mismatch
        keyword_ids_to_delete = []
        product_ids_to_delete = []
        
        if 'Keyword ID' in delete_sheet.columns:
            # Clean conversion: float -> int -> string to remove .0 suffix
            keyword_series = delete_sheet['Keyword ID'].dropna()
            keyword_ids_to_delete = [
                str(int(x)) if isinstance(x, (int, float)) and pd.notna(x) else str(x)
                for x in keyword_series
            ]
        
        if 'Product Targeting ID' in delete_sheet.columns:
            # Clean conversion for Product Targeting IDs
            product_series = delete_sheet['Product Targeting ID'].dropna()
            product_ids_to_delete = [
                str(int(x)) if isinstance(x, (int, float)) and pd.notna(x) else str(x)
                for x in product_series
            ]
        
        # DEBUG: Print what we're going to delete
        print(f"[DEBUG Delete for 60] Keyword IDs to delete: {keyword_ids_to_delete}")
        print(f"[DEBUG Delete for 60] Product Targeting IDs to delete: {product_ids_to_delete}")
        
        # Remove rows with these IDs
        filtered_df = df.copy()
        
        if keyword_ids_to_delete and 'Keyword ID' in df.columns:
            # Clean conversion of bulk data IDs
            bulk_keyword_ids = []
            for x in filtered_df['Keyword ID']:
                if pd.isna(x):
                    bulk_keyword_ids.append('NaN')  # Consistent NaN representation
                elif isinstance(x, (int, float)):
                    bulk_keyword_ids.append(str(int(x)))  # Remove .0 suffix
                else:
                    bulk_keyword_ids.append(str(x))
            
            filtered_df['Keyword ID'] = bulk_keyword_ids
            
            # DEBUG: Print bulk IDs for comparison
            print(f"[DEBUG Delete for 60] Bulk Keyword IDs (first 5): {bulk_keyword_ids[:5]}")
            
            mask = ~filtered_df['Keyword ID'].isin(keyword_ids_to_delete)
            rows_before = len(filtered_df)
            filtered_df = filtered_df[mask]
            rows_removed = rows_before - len(filtered_df)
            print(f"[DEBUG Delete for 60] Removed {rows_removed} rows with matching Keyword IDs")
        
        if product_ids_to_delete and 'Product Targeting ID' in df.columns:
            # Clean conversion of bulk data Product Targeting IDs
            bulk_product_ids = []
            for x in filtered_df['Product Targeting ID']:
                if pd.isna(x):
                    bulk_product_ids.append('NaN')  # Consistent NaN representation
                elif isinstance(x, (int, float)):
                    bulk_product_ids.append(str(int(x)))  # Remove .0 suffix
                else:
                    bulk_product_ids.append(str(x))
            
            filtered_df['Product Targeting ID'] = bulk_product_ids
            
            # DEBUG: Print bulk IDs for comparison
            print(f"[DEBUG Delete for 60] Bulk Product Targeting IDs (first 5): {bulk_product_ids[:5]}")
            
            mask = ~filtered_df['Product Targeting ID'].isin(product_ids_to_delete)
            rows_before = len(filtered_df)
            filtered_df = filtered_df[mask]
            rows_removed = rows_before - len(filtered_df)
            print(f"[DEBUG Delete for 60] Removed {rows_removed} rows with matching Product Targeting IDs")
        
        total_removed = initial_count - len(filtered_df)
        self.stats['rows_removed_delete_60'] = total_removed
        print(f"[DEBUG Delete for 60] Total rows removed: {total_removed}")
        
        return filtered_df
    
    def _filter_by_state(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filter rows where State = 'enabled'."""
        initial_count = len(df)
        
        if 'State' in df.columns:
            # Filter for enabled state only
            filtered_df = df[df['State'].str.lower() == 'enabled'].copy()
        else:
            filtered_df = df.copy()
        
        self.stats['rows_removed_state'] = initial_count - len(filtered_df)
        
        return filtered_df
    
    def pre_validation_filter(self, bulk_data: pd.DataFrame) -> pd.DataFrame:
        """
        Pre-validation filtering to remove rows with State != 'enabled'.
        
        This runs BEFORE validation to prevent validation errors for portfolios
        that exist only in paused/disabled campaigns.
        
        Args:
            bulk_data: Raw bulk data DataFrame
            
        Returns:
            Filtered DataFrame with only enabled rows
        """
        if bulk_data.empty:
            return bulk_data
            
        df = bulk_data.copy()
        initial_count = len(df)
        
        # Filter by main State column
        if 'State' in df.columns:
            df = df[df['State'].astype(str).str.lower() == 'enabled'].copy()
        
        # Filter by Campaign State  
        if 'Campaign State (Informational only)' in df.columns:
            df = df[df['Campaign State (Informational only)'].astype(str).str.lower() == 'enabled'].copy()
            
        # Filter by Ad Group State
        if 'Ad Group State (Informational only)' in df.columns:
            df = df[df['Ad Group State (Informational only)'].astype(str).str.lower() == 'enabled'].copy()
        
        filtered_count = initial_count - len(df)
        if filtered_count > 0:
            import logging
            logger = logging.getLogger("optimization.bids_60_days.cleaner")
            logger.info(f"Pre-validation filter: removed {filtered_count} non-enabled rows")
            
        return df
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cleaning statistics."""
        return self.stats
