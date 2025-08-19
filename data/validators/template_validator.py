"""Template file validation utilities."""

import pandas as pd
from typing import Tuple, List, Dict, Any
from config.constants import (
    TEMPLATE_REQUIRED_SHEETS, 
    TEMPLATE_PORT_VALUES_COLUMNS,
    MIN_BASE_BID,
    MAX_BASE_BID,
    MIN_TARGET_CPA,
    MAX_TARGET_CPA
)


class TemplateValidator:
    """Validates template files and their data."""
    
    def __init__(self):
        self.required_sheets = TEMPLATE_REQUIRED_SHEETS
        self.required_columns = TEMPLATE_PORT_VALUES_COLUMNS
    
    def validate_complete(self, data_dict: Dict[str, pd.DataFrame]) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Complete validation of template data.
        
        Returns:
            Tuple of (is_valid, message, validation_details)
        """
        
        validation_results = {
            'structure_valid': False,
            'data_valid': False,
            'portfolio_count': 0,
            'ignore_count': 0,
            'issues': [],
            'warnings': []
        }
        
        # Structure validation
        structure_valid, structure_msg = self._validate_structure(data_dict)
        validation_results['structure_valid'] = structure_valid
        
        if not structure_valid:
            validation_results['issues'].append(structure_msg)
            return False, structure_msg, validation_results
        
        # Data validation
        port_values_df = data_dict['Port Values']
        data_valid, data_msg, data_details = self._validate_data(port_values_df)
        
        validation_results['data_valid'] = data_valid
        validation_results.update(data_details)
        
        if not data_valid:
            validation_results['issues'].append(data_msg)
            return False, data_msg, validation_results
        
        # Success message
        total_portfolios = validation_results['portfolio_count']
        ignore_count = validation_results['ignore_count']
        active_count = total_portfolios - ignore_count
        
        success_msg = f"Template valid: {total_portfolios} portfolios ({active_count} active, {ignore_count} ignored)"
        
        return True, success_msg, validation_results
    
    def _validate_structure(self, data_dict: Dict[str, pd.DataFrame]) -> Tuple[bool, str]:
        """Validate the structure of template data."""
        
        # Check required sheets
        missing_sheets = []
        for sheet in self.required_sheets:
            if sheet not in data_dict or data_dict[sheet] is None:
                missing_sheets.append(sheet)
        
        if missing_sheets:
            return False, f"Missing required sheets: {', '.join(missing_sheets)}"
        
        # Check Port Values columns
        port_values_df = data_dict['Port Values']
        expected_cols = set(self.required_columns)
        actual_cols = set(port_values_df.columns)
        
        missing_cols = expected_cols - actual_cols
        if missing_cols:
            return False, f"Port Values missing columns: {', '.join(missing_cols)}"
        
        return True, "Template structure is valid"
    
    def _validate_data(self, df: pd.DataFrame) -> Tuple[bool, str, Dict[str, Any]]:
        """Validate the data content of Port Values sheet."""
        
        details = {
            'portfolio_count': 0,
            'ignore_count': 0,
            'issues': [],
            'warnings': []
        }
        
        # Remove empty rows
        df_clean = df.dropna(subset=['Portfolio Name']).copy()
        df_clean = df_clean[df_clean['Portfolio Name'].astype(str).str.strip() != '']
        
        if df_clean.empty:
            return False, "No valid portfolios found in template", details
        
        details['portfolio_count'] = len(df_clean)
        
        # Check for duplicate portfolio names
        duplicates = df_clean[df_clean['Portfolio Name'].duplicated()]
        if not duplicates.empty:
            dup_names = duplicates['Portfolio Name'].tolist()
            details['issues'].append(f"Duplicate portfolios: {', '.join(dup_names)}")
            return False, f"Duplicate portfolio names found: {', '.join(dup_names)}", details
        
        # Validate each row
        validation_errors = []
        
        for idx, row in df_clean.iterrows():
            portfolio_name = str(row['Portfolio Name']).strip()
            base_bid = str(row['Base Bid']).strip()
            target_cpa = str(row['Target CPA']).strip()
            
            # Portfolio name validation
            if not portfolio_name or portfolio_name == 'nan':
                validation_errors.append(f"Row {idx+1}: Empty portfolio name")
                continue
            
            if len(portfolio_name) > 255:
                validation_errors.append(f"Row {idx+1}: Portfolio name too long (max 255 chars)")
            
            # Base Bid validation
            if base_bid.lower() == 'ignore':
                details['ignore_count'] += 1
            else:
                try:
                    bid_value = float(base_bid)
                    if not (MIN_BASE_BID <= bid_value <= MAX_BASE_BID):
                        validation_errors.append(
                            f"Row {idx+1}: Base Bid {bid_value} out of range ({MIN_BASE_BID}-{MAX_BASE_BID})"
                        )
                except ValueError:
                    validation_errors.append(f"Row {idx+1}: Invalid Base Bid '{base_bid}'")
            
            # Target CPA validation (optional field)
            if target_cpa and target_cpa != 'nan':
                try:
                    cpa_value = float(target_cpa)
                    if not (MIN_TARGET_CPA <= cpa_value <= MAX_TARGET_CPA):
                        validation_errors.append(
                            f"Row {idx+1}: Target CPA {cpa_value} out of range ({MIN_TARGET_CPA}-{MAX_TARGET_CPA})"
                        )
                except ValueError:
                    validation_errors.append(f"Row {idx+1}: Invalid Target CPA '{target_cpa}'")
        
        # Check if at least one portfolio is not ignored
        active_portfolios = details['portfolio_count'] - details['ignore_count']
        if active_portfolios == 0:
            validation_errors.append("All portfolios are set to 'Ignore' - at least one must be active")
        
        if validation_errors:
            details['issues'].extend(validation_errors)
            return False, "; ".join(validation_errors[:3]) + ("..." if len(validation_errors) > 3 else ""), details
        
        # Warnings for common issues
        if details['ignore_count'] > details['portfolio_count'] * 0.5:
            details['warnings'].append(f"Many portfolios ignored ({details['ignore_count']}/{details['portfolio_count']})")
        
        return True, "Template data is valid", details
    
    def get_portfolio_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get summary statistics for portfolios in template."""
        
        if df is None or df.empty:
            return {'total': 0, 'active': 0, 'ignored': 0}
        
        # Clean data
        df_clean = df.dropna(subset=['Portfolio Name']).copy()
        df_clean = df_clean[df_clean['Portfolio Name'].astype(str).str.strip() != '']
        
        total = len(df_clean)
        ignored = len(df_clean[df_clean['Base Bid'].astype(str).str.lower() == 'ignore'])
        active = total - ignored
        
        # Get bid statistics for active portfolios
        active_df = df_clean[df_clean['Base Bid'].astype(str).str.lower() != 'ignore']
        
        bid_stats = {}
        if not active_df.empty:
            try:
                bids = pd.to_numeric(active_df['Base Bid'], errors='coerce').dropna()
                if not bids.empty:
                    bid_stats = {
                        'min_bid': float(bids.min()),
                        'max_bid': float(bids.max()),
                        'avg_bid': float(bids.mean())
                    }
            except:
                pass
        
        return {
            'total': total,
            'active': active,
            'ignored': ignored,
            'bid_stats': bid_stats
        }