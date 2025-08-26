"""Processing logic for Bids 60 Days optimization."""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Any, Optional
from .constants import (
    CALC2_THRESHOLD,
    CONVERSION_RATE_THRESHOLD,
    UNITS_FOR_MAX_BID,
    MIN_BID,
    MAX_BID,
    MAX_BID_LOW_UNITS,
    MAX_BID_HIGH_UNITS,
    UP_AND_MULTIPLIER,
    OLD_BID_MULTIPLIER,
    ERROR_NULL,
    ERROR_CALCULATION,
    HELPER_COLUMNS,
    TARGET_ENTITIES,
    SEPARATE_ENTITIES
)


class Bids60DaysProcessor:
    """Handles bid calculation for Bids 60 Days optimization."""
    
    def __init__(self):
        self.stats = {
            'rows_processed': 0,
            'rows_modified': 0,
            'rows_to_harvesting': 0,
            'rows_with_low_cvr': 0,
            'rows_with_bid_errors': 0,
            'calculation_errors': 0
        }
        self.for_harvesting_df = None
    
    def process(self,
                template_data: Dict[str, pd.DataFrame],
                bulk_data: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Process optimization and calculate new bids.
        
        Args:
            template_data: Dictionary containing template sheets
            bulk_data: Cleaned bulk campaign data DataFrame
            
        Returns:
            Dictionary with processed DataFrames for each sheet
        """
        # Split data by entity type
        targeting_df, bidding_df = self._split_by_entity(bulk_data)
        
        # Process targeting data (main optimization)
        if not targeting_df.empty:
            targeting_df = self._process_targeting(targeting_df, template_data)
        
        # Prepare output DataFrames
        result = {
            'Targeting': targeting_df,
            'Bidding Adjustment': bidding_df
        }
        
        # Add For Harvesting sheet if there are rows
        if self.for_harvesting_df is not None and not self.for_harvesting_df.empty:
            result['For Harvesting'] = self.for_harvesting_df
        
        return result
    
    def _split_by_entity(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Split data by Entity type."""
        targeting_mask = df['Entity'].isin(TARGET_ENTITIES)
        targeting_df = df[targeting_mask].copy()
        
        bidding_mask = df['Entity'].isin(SEPARATE_ENTITIES)
        bidding_df = df[bidding_mask].copy()
        
        return targeting_df, bidding_df
    
    def _process_targeting(self, 
                          df: pd.DataFrame,
                          template_data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Process targeting data with bid calculations."""
        # Step 0: Create helper columns
        df = self._create_helper_columns(df)
        
        # Step 1: Fill base columns from template
        df = self._fill_base_columns(df, template_data)
        
        # Step 2: Separate rows with NULL Target CPA
        df, self.for_harvesting_df = self._separate_null_target_cpa(df)
        
        # Process remaining rows
        for idx in df.index:
            try:
                # Step 3: Calculate calc1 and calc2
                df = self._calculate_calc_values(df, idx)
                
                # Step 4-7: Determine final bid based on conditions
                df = self._calculate_final_bid(df, idx)
                
                # Step 8: Mark for coloring
                df = self._mark_for_coloring(df, idx)
                
                self.stats['rows_processed'] += 1
                
            except Exception as e:
                # Handle calculation errors
                df.at[idx, 'Bid'] = ERROR_CALCULATION
                df.at[idx, '_needs_highlight'] = True
                self.stats['calculation_errors'] += 1
        
        # Add Operation column for all rows
        df['Operation'] = 'Update'
        
        return df
    
    def _create_helper_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Step 0: Create all helper columns."""
        # Store original bid
        df['Old Bid'] = df['Bid'].copy()
        
        # Initialize other helper columns
        for col in ['calc1', 'calc2', 'Target CPA', 'Base Bid', 
                   'Adj. CPA', 'Max BA', 'Temp Bid', 'Max_Bid', 'calc3']:
            if col not in df.columns:
                df[col] = np.nan
        
        # Add internal highlighting column
        df['_needs_highlight'] = False
        
        return df
    
    def _fill_base_columns(self, 
                           df: pd.DataFrame,
                           template_data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Step 1: Fill Base Bid and Target CPA from template."""
        if 'Port Values' not in template_data:
            return df
        
        port_values = template_data['Port Values']
        
        # Get portfolio column name
        portfolio_col = None
        for col in ['Portfolio Name (Informational only)', 'Portfolio Name', 'Portfolio']:
            if col in df.columns:
                portfolio_col = col
                break
        
        if not portfolio_col:
            return df
        
        # Create mapping dictionaries
        base_bid_map = dict(zip(port_values['Portfolio Name'], port_values['Base Bid']))
        target_cpa_map = dict(zip(port_values['Portfolio Name'], port_values['Target CPA']))
        
        # Fill Base Bid and Target CPA
        df['Base Bid'] = df[portfolio_col].map(base_bid_map)
        df['Target CPA'] = df[portfolio_col].map(target_cpa_map)
        
        # Convert Base Bid to numeric (handle 'Ignore' values)
        df['Base Bid'] = pd.to_numeric(df['Base Bid'], errors='coerce')
        df['Target CPA'] = pd.to_numeric(df['Target CPA'], errors='coerce')
        
        # Calculate Max BA (maximum Percentage for each Campaign ID)
        df['Max BA'] = df.groupby('Campaign ID')['Percentage'].transform('max')
        df['Max BA'] = pd.to_numeric(df['Max BA'], errors='coerce').fillna(0)
        
        return df
    
    def _separate_null_target_cpa(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Step 2: Separate rows with NULL Target CPA."""
        # Find rows with NULL Target CPA
        null_mask = df['Target CPA'].isna()
        
        # Separate DataFrames
        for_harvesting = df[null_mask].copy()
        remaining = df[~null_mask].copy()
        
        self.stats['rows_to_harvesting'] = len(for_harvesting)
        
        # Add Operation column to For Harvesting sheet
        if not for_harvesting.empty:
            for_harvesting['Operation'] = 'Update'
        
        # DEBUG: Log what goes to For Harvesting
        print(f"[DEBUG For Harvesting] Separated {len(for_harvesting)} rows to For Harvesting")
        if not for_harvesting.empty:
            # Get portfolio column name
            portfolio_col = None
            for col in ['Portfolio Name (Informational only)', 'Portfolio Name', 'Portfolio']:
                if col in for_harvesting.columns:
                    portfolio_col = col
                    break
            
            if portfolio_col:
                harvesting_portfolios = for_harvesting[portfolio_col].dropna().unique()
                print(f"[DEBUG For Harvesting] Portfolios in For Harvesting ({len(harvesting_portfolios)}):")
                for portfolio in sorted(harvesting_portfolios):
                    count = (for_harvesting[portfolio_col] == portfolio).sum()
                    print(f"[DEBUG For Harvesting]   '{portfolio}' ({count} rows)")
                
                # Check if any excluded portfolios made it to harvesting
                from .constants import EXCLUDED_PORTFOLIOS
                excluded_in_harvesting = for_harvesting[for_harvesting[portfolio_col].isin(EXCLUDED_PORTFOLIOS)]
                if not excluded_in_harvesting.empty:
                    excluded_portfolios = excluded_in_harvesting[portfolio_col].unique()
                    print(f"[DEBUG For Harvesting] ⚠️  EXCLUDED PORTFOLIOS FOUND in For Harvesting:")
                    for portfolio in excluded_portfolios:
                        count = (excluded_in_harvesting[portfolio_col] == portfolio).sum()
                        print(f"[DEBUG For Harvesting]   ⚠️  '{portfolio}' ({count} rows)")
        
        return remaining, for_harvesting
    
    def _calculate_calc_values(self, df: pd.DataFrame, idx: int) -> pd.DataFrame:
        """Step 3: Calculate calc1 and calc2."""
        try:
            # Get values with error handling
            target_cpa = df.at[idx, 'Target CPA']
            base_bid = df.at[idx, 'Base Bid']
            max_ba = df.at[idx, 'Max BA']
            campaign_name = str(df.at[idx, 'Campaign Name (Informational only)'])
            
            # Check for NULL values
            if pd.isna(target_cpa) or pd.isna(base_bid):
                df.at[idx, 'Bid'] = ERROR_NULL
                df.at[idx, '_needs_highlight'] = True
                return df
            
            # Calculate Adj. CPA
            if "up and" in campaign_name.lower():
                adj_cpa = target_cpa * UP_AND_MULTIPLIER
            else:
                adj_cpa = target_cpa
            
            df.at[idx, 'Adj. CPA'] = adj_cpa
            
            # Calculate calc1: adj_cpa / (clicks/units)
            clicks = df.at[idx, 'Clicks']
            units = df.at[idx, 'Units']
            
            if units and units != 0:
                calc1 = adj_cpa / (clicks / units)
            else:
                calc1 = 0  # Handle division by zero
            
            df.at[idx, 'calc1'] = calc1
            
            # Calculate calc2: calc1 / Old Bid
            old_bid = df.at[idx, 'Old Bid']
            if old_bid and old_bid != 0:
                calc2 = calc1 / old_bid
            else:
                calc2 = 0
            
            df.at[idx, 'calc2'] = calc2
            
        except Exception as e:
            df.at[idx, 'Bid'] = ERROR_CALCULATION
            df.at[idx, '_needs_highlight'] = True
            
        return df
    
    def _calculate_final_bid(self, df: pd.DataFrame, idx: int) -> pd.DataFrame:
        """Steps 4-7: Calculate final bid based on conditions."""
        try:
            calc2 = df.at[idx, 'calc2']
            calc1 = df.at[idx, 'calc1']
            old_bid = df.at[idx, 'Old Bid']
            match_type = str(df.at[idx, 'Match Type'])
            product_targeting = str(df.at[idx, 'Product Targeting Expression'])
            units = df.at[idx, 'Units']
            max_ba = df.at[idx, 'Max BA']
            
            # Check calc2 threshold
            if calc2 < CALC2_THRESHOLD:
                # Set Bid = calc1
                df.at[idx, 'Bid'] = calc1
            else:
                # Check if Exact match or ASIN targeting
                is_exact = match_type.lower() == 'exact'
                is_asin = 'asin="b0' in product_targeting.lower()
                
                if is_exact or is_asin:
                    # Step 4: Set Temp_Bid = calc1
                    temp_bid = calc1
                    df.at[idx, 'Temp Bid'] = temp_bid
                    
                    # Step 5: Calculate Max_Bid
                    ba_factor = 1 + (max_ba / 100) if max_ba else 1
                    
                    if units < UNITS_FOR_MAX_BID:
                        max_bid = MAX_BID_LOW_UNITS / ba_factor
                    else:
                        max_bid = MAX_BID_HIGH_UNITS / ba_factor
                    
                    df.at[idx, 'Max_Bid'] = max_bid
                    
                    # Step 6: Calculate calc3
                    calc3 = temp_bid - max_bid
                    df.at[idx, 'calc3'] = calc3
                    
                    # Step 7: Set final Bid
                    if calc3 < 0:
                        df.at[idx, 'Bid'] = temp_bid
                    else:
                        df.at[idx, 'Bid'] = max_bid
                else:
                    # Not Exact or ASIN: Bid = Old Bid * 1.1
                    df.at[idx, 'Bid'] = old_bid * OLD_BID_MULTIPLIER
            
            # Track if bid was modified
            if df.at[idx, 'Bid'] != old_bid:
                self.stats['rows_modified'] += 1
                
        except Exception as e:
            df.at[idx, 'Bid'] = ERROR_CALCULATION
            df.at[idx, '_needs_highlight'] = True
            
        return df
    
    def _mark_for_coloring(self, df: pd.DataFrame, idx: int) -> pd.DataFrame:
        """Step 8: Mark rows for pink highlighting."""
        try:
            bid = df.at[idx, 'Bid']
            cvr = df.at[idx, 'Conversion Rate']
            
            # Check if bid is error
            if isinstance(bid, str) and 'Error' in bid:
                df.at[idx, '_needs_highlight'] = True
                self.stats['rows_with_bid_errors'] += 1
                return df
            
            # Convert to numeric for comparison
            bid = pd.to_numeric(bid, errors='coerce')
            cvr = pd.to_numeric(cvr, errors='coerce')
            
            # Check CVR < 8%
            if cvr < CONVERSION_RATE_THRESHOLD:
                df.at[idx, '_needs_highlight'] = True
                self.stats['rows_with_low_cvr'] += 1
            
            # Check Bid out of range
            if bid < MIN_BID or bid > MAX_BID:
                df.at[idx, '_needs_highlight'] = True
                self.stats['rows_with_bid_errors'] += 1
                
        except Exception:
            df.at[idx, '_needs_highlight'] = True
            
        return df
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get processing statistics."""
        return self.stats
