"""Zero Sales optimization bid processing."""

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple, List
import logging
from config.constants import MIN_BID, MAX_BID


class ZeroSalesProcessor:
    """Processes Zero Sales optimization bid calculations."""
    
    def __init__(self):
        self.logger = logging.getLogger("optimization.zero_sales.processor")
        
        # Bid range constraints
        self.min_bid = MIN_BID
        self.max_bid = MAX_BID
        
        # Processing statistics
        self.stats = {
            'case_a_count': 0,  # Target CPA empty + "up and"
            'case_b_count': 0,  # Target CPA empty + no "up and"  
            'case_c_count': 0,  # Target CPA filled + "up and"
            'case_d_count': 0,  # Target CPA filled + no "up and"
            'out_of_range_count': 0,
            'processing_errors': 0
        }
    
    def process(self, df: pd.DataFrame, column_mapping: Dict[str, str]) -> Tuple[Dict[str, pd.DataFrame], Dict[str, Any]]:
        """
        Process Zero Sales bid calculations using the 4 defined cases.
        
        The 4 cases for Zero Sales optimization:
        Case A: Target CPA is empty/null AND targeting contains "up and" -> Bid = Base Bid * 1.25  
        Case B: Target CPA is empty/null AND targeting does NOT contain "up and" -> Bid = Base Bid * 1.5
        Case C: Target CPA is filled AND targeting contains "up and" -> Bid = min(Base Bid * 1.25, Target CPA)
        Case D: Target CPA is filled AND targeting does NOT contain "up and" -> Bid = min(Base Bid * 1.5, Target CPA)
        
        Args:
            df: Cleaned data ready for processing
            column_mapping: Column name mappings
            
        Returns:
            Tuple of (result_dataframes, processing_details)
        """
        
        processing_details = {
            'input_rows': len(df),
            'processed_rows': 0,
            'case_statistics': {},
            'bid_range_issues': [],
            'errors': []
        }
        
        self.logger.info(f"Starting Zero Sales processing: {len(df)} rows")
        
        if df.empty:
            return self._create_empty_results(), processing_details
        
        # Reset statistics
        self._reset_stats()
        
        # Process each row
        processed_df = self._process_all_rows(df, column_mapping)
        
        # Generate output DataFrames
        result_dataframes = self._generate_output_dataframes(processed_df)
        
        # Compile processing details
        processing_details.update({
            'processed_rows': len(processed_df),
            'case_statistics': self.stats.copy(),
            'bid_range_issues': self._get_bid_range_issues(processed_df),
        })
        
        success_msg = f"Zero Sales processing complete: {len(processed_df)} rows processed"
        self.logger.info(success_msg)
        
        return result_dataframes, processing_details
    
    def _process_all_rows(self, df: pd.DataFrame, column_mapping: Dict[str, str]) -> pd.DataFrame:
        """Process all rows with bid calculations."""
        
        processed_df = df.copy()
        
        # Get required columns
        bid_col = column_mapping.get('bid')
        targeting_col = column_mapping.get('targeting', '')
        
        # Get template columns (should be merged during cleaning)
        base_bid_col = 'Base Bid'
        target_cpa_col = 'Target CPA'
        
        if not all(col in processed_df.columns for col in [bid_col, base_bid_col]):
            self.logger.error("Required columns missing for processing")
            return processed_df
        
        # Process each row
        for idx in processed_df.index:
            try:
                # Get row data
                base_bid = processed_df.loc[idx, base_bid_col]
                target_cpa = processed_df.loc[idx, target_cpa_col] if target_cpa_col in processed_df.columns else None
                targeting = processed_df.loc[idx, targeting_col] if targeting_col in processed_df.columns else ''
                
                # Calculate new bid
                new_bid, case, notes = self._calculate_bid_for_row(base_bid, target_cpa, targeting)
                
                # Update row
                processed_df.loc[idx, bid_col] = new_bid
                processed_df.loc[idx, 'Bid_Case'] = case
                processed_df.loc[idx, 'Calculation_Notes'] = notes
                
                # Update statistics
                self._update_case_stats(case)
                
                # Check bid range
                if new_bid < self.min_bid or new_bid > self.max_bid:
                    processed_df.loc[idx, 'Bid_Range_Issue'] = True
                    self.stats['out_of_range_count'] += 1
                else:
                    processed_df.loc[idx, 'Bid_Range_Issue'] = False
                
            except Exception as e:
                self.logger.error(f"Error processing row {idx}: {str(e)}")
                processed_df.loc[idx, 'Calculation_Notes'] = f"Processing error: {str(e)}"
                self.stats['processing_errors'] += 1
        
        return processed_df
    
    def _calculate_bid_for_row(self, base_bid: Any, target_cpa: Any, targeting: str) -> Tuple[float, str, str]:
        """
        Calculate new bid for a single row using the 4 cases.
        
        Returns:
            Tuple of (new_bid, case_name, calculation_notes)
        """
        
        # Parse base bid
        try:
            base_bid_val = float(base_bid) if pd.notna(base_bid) and str(base_bid).lower() != 'ignore' else 0.5
        except (ValueError, TypeError):
            base_bid_val = 0.5  # Default fallback
        
        # Parse target CPA
        target_cpa_val = None
        target_cpa_filled = False
        
        if pd.notna(target_cpa) and str(target_cpa).strip() != '':
            try:
                target_cpa_val = float(target_cpa)
                target_cpa_filled = True
            except (ValueError, TypeError):
                pass
        
        # Check targeting for "up and"
        targeting_str = str(targeting).lower() if pd.notna(targeting) else ''
        has_up_and = 'up and' in targeting_str
        
        # Apply the 4 cases
        if not target_cpa_filled and has_up_and:
            # Case A: Target CPA empty + "up and" -> Base Bid * 1.25
            new_bid = base_bid_val * 1.25
            case = 'A'
            notes = f"Case A: Base Bid ({base_bid_val}) * 1.25 = {new_bid} (CPA empty + 'up and')"
        
        elif not target_cpa_filled and not has_up_and:
            # Case B: Target CPA empty + no "up and" -> Base Bid * 1.5
            new_bid = base_bid_val * 1.5
            case = 'B'
            notes = f"Case B: Base Bid ({base_bid_val}) * 1.5 = {new_bid} (CPA empty + no 'up and')"
        
        elif target_cpa_filled and has_up_and:
            # Case C: Target CPA filled + "up and" -> min(Base Bid * 1.25, Target CPA)
            calculated_bid = base_bid_val * 1.25
            new_bid = min(calculated_bid, target_cpa_val)
            case = 'C'
            notes = f"Case C: min(Base Bid ({base_bid_val}) * 1.25, CPA ({target_cpa_val})) = {new_bid} ('up and' + CPA limit)"
        
        elif target_cpa_filled and not has_up_and:
            # Case D: Target CPA filled + no "up and" -> min(Base Bid * 1.5, Target CPA)
            calculated_bid = base_bid_val * 1.5
            new_bid = min(calculated_bid, target_cpa_val)
            case = 'D'
            notes = f"Case D: min(Base Bid ({base_bid_val}) * 1.5, CPA ({target_cpa_val})) = {new_bid} (no 'up and' + CPA limit)"
        
        else:
            # Fallback case (should not happen)
            new_bid = base_bid_val
            case = 'F'
            notes = f"Fallback: Using Base Bid ({base_bid_val}) unchanged"
        
        # Round to 2 decimal places
        new_bid = round(new_bid, 2)
        
        return new_bid, case, notes
    
    def _generate_output_dataframes(self, processed_df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Generate the required output DataFrames."""
        
        results = {}
        
        if processed_df.empty:
            return self._create_empty_results()
        
        # Targeting sheet - includes all original columns + helper columns
        targeting_df = processed_df.copy()
        results['Targeting'] = targeting_df
        
        # Bidding Adjustment sheet - only columns needed for Amazon upload
        required_cols = []
        
        # Find essential columns for bid upload
        for col in processed_df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in [
                'campaign', 'ad group', 'targeting', 'match type', 'bid', 'operation'
            ]):
                required_cols.append(col)
        
        # Add operation column if not exists
        if 'Operation' not in processed_df.columns:
            processed_df['Operation'] = 'Update'
            required_cols.append('Operation')
        
        # Create bidding adjustment sheet
        if required_cols:
            bidding_adjustment_df = processed_df[required_cols].copy()
        else:
            # Fallback - use all columns
            bidding_adjustment_df = processed_df.copy()
        
        results['Bidding Adjustment'] = bidding_adjustment_df
        
        return results
    
    def _create_empty_results(self) -> Dict[str, pd.DataFrame]:
        """Create empty result DataFrames."""
        return {
            'Targeting': pd.DataFrame(),
            'Bidding Adjustment': pd.DataFrame()
        }
    
    def _reset_stats(self):
        """Reset processing statistics."""
        for key in self.stats:
            self.stats[key] = 0
    
    def _update_case_stats(self, case: str):
        """Update case statistics."""
        case_key = f'case_{case.lower()}_count'
        if case_key in self.stats:
            self.stats[case_key] += 1
    
    def _get_bid_range_issues(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Get list of rows with bid range issues."""
        
        issues = []
        
        if 'Bid_Range_Issue' not in df.columns:
            return issues
        
        issue_rows = df[df['Bid_Range_Issue'] == True]
        
        for idx in issue_rows.index[:10]:  # Limit to first 10 issues
            row_data = issue_rows.loc[idx]
            bid_col = None
            
            # Find bid column
            for col in df.columns:
                if 'bid' in col.lower() and col not in ['Base Bid', 'Original_Bid']:
                    bid_col = col
                    break
            
            if bid_col:
                issue = {
                    'row_index': idx,
                    'bid_value': row_data[bid_col],
                    'case': row_data.get('Bid_Case', ''),
                    'notes': row_data.get('Calculation_Notes', ''),
                    'range_min': self.min_bid,
                    'range_max': self.max_bid
                }
                issues.append(issue)
        
        return issues
    
    def get_processing_summary(self, processing_details: Dict[str, Any]) -> str:
        """Generate human-readable processing summary."""
        
        summary_lines = [
            f"Zero Sales Processing Summary:",
            f"Rows processed: {processing_details.get('processed_rows', 0)}"
        ]
        
        # Case statistics
        case_stats = processing_details.get('case_statistics', {})
        if case_stats:
            summary_lines.append("Calculation cases:")
            summary_lines.append(f"  Case A (CPA empty + 'up and'): {case_stats.get('case_a_count', 0)}")
            summary_lines.append(f"  Case B (CPA empty + no 'up and'): {case_stats.get('case_b_count', 0)}")
            summary_lines.append(f"  Case C (CPA filled + 'up and'): {case_stats.get('case_c_count', 0)}")
            summary_lines.append(f"  Case D (CPA filled + no 'up and'): {case_stats.get('case_d_count', 0)}")
        
        # Issues
        out_of_range = case_stats.get('out_of_range_count', 0)
        if out_of_range > 0:
            summary_lines.append(f"Bid range issues: {out_of_range} (will be highlighted in pink)")
        
        errors = case_stats.get('processing_errors', 0)
        if errors > 0:
            summary_lines.append(f"Processing errors: {errors}")
        
        return "\n".join(summary_lines)