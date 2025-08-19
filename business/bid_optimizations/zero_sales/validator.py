"""Zero Sales optimization validation."""

import pandas as pd
from typing import Dict, Any, Tuple, List
import logging


class ZeroSalesValidator:
    """Validates data requirements for Zero Sales optimization."""
    
    def __init__(self):
        self.logger = logging.getLogger("optimization.zero_sales.validator")
        
        # Required columns for Zero Sales optimization
        self.required_columns = {
            'portfolio': ['portfolio', 'port'],
            'units': ['units', 'unit'],
            'bid': ['bid', 'max cpc', 'cpc'],
            'clicks': ['clicks', 'click']
        }
        
        # Optional but useful columns
        self.optional_columns = {
            'campaign': ['campaign'],
            'ad_group': ['ad group', 'adgroup', 'ad-group'],
            'targeting': ['targeting', 'keyword', 'asin'],
            'match_type': ['match type', 'match-type', 'matchtype']
        }
    
    def validate(self, template_data: Dict[str, pd.DataFrame], bulk_data: pd.DataFrame) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Validate requirements for Zero Sales optimization.
        
        Returns:
            Tuple of (is_valid, message, validation_details)
        """
        
        details = {
            'column_mapping': {},
            'template_portfolios': [],
            'bulk_portfolios': [],
            'zero_units_count': 0,
            'processable_rows': 0,
            'ignored_portfolios': [],
            'issues': [],
            'warnings': []
        }
        
        self.logger.info("Starting Zero Sales validation")
        
        # Validate template data
        template_valid, template_msg, template_details = self._validate_template(template_data)
        details.update(template_details)
        
        if not template_valid:
            return False, template_msg, details
        
        # Validate bulk data structure
        bulk_valid, bulk_msg, bulk_details = self._validate_bulk_structure(bulk_data)
        details.update(bulk_details)
        
        if not bulk_valid:
            return False, bulk_msg, details
        
        # Validate data content
        content_valid, content_msg, content_details = self._validate_content(template_data, bulk_data, details['column_mapping'])
        details.update(content_details)
        
        if not content_valid:
            return False, content_msg, details
        
        # Success
        success_msg = (
            f"Zero Sales validation passed: "
            f"{details['zero_units_count']} zero sales candidates found, "
            f"{details['processable_rows']} rows ready for processing"
        )
        
        return True, success_msg, details
    
    def _validate_template(self, template_data: Dict[str, pd.DataFrame]) -> Tuple[bool, str, Dict[str, Any]]:
        """Validate template data for Zero Sales requirements."""
        
        details = {
            'template_portfolios': [],
            'ignored_portfolios': []
        }
        
        # Check Port Values sheet
        if 'Port Values' not in template_data:
            return False, "Port Values sheet not found in template", details
        
        port_values = template_data['Port Values']
        if port_values.empty:
            return False, "Port Values sheet is empty", details
        
        # Extract portfolio information
        try:
            portfolios = port_values['Portfolio Name'].astype(str).str.strip().dropna()
            details['template_portfolios'] = portfolios.tolist()
            
            # Find ignored portfolios
            base_bids = port_values['Base Bid'].astype(str).str.strip().str.lower()
            ignored_mask = base_bids == 'ignore'
            ignored_portfolios = portfolios[ignored_mask].tolist()
            details['ignored_portfolios'] = ignored_portfolios
            
            self.logger.info(f"Template: {len(details['template_portfolios'])} portfolios, {len(ignored_portfolios)} ignored")
            
        except Exception as e:
            return False, f"Error reading template portfolios: {str(e)}", details
        
        return True, "Template validation passed", details
    
    def _validate_bulk_structure(self, bulk_data: pd.DataFrame) -> Tuple[bool, str, Dict[str, Any]]:
        """Validate bulk data structure for Zero Sales requirements."""
        
        details = {'column_mapping': {}}
        
        if bulk_data.empty:
            return False, "Bulk data is empty", details
        
        # Map required columns
        missing_columns = []
        
        for req_col, keywords in self.required_columns.items():
            mapped_col = self._find_column(bulk_data, keywords)
            if mapped_col:
                details['column_mapping'][req_col] = mapped_col
                self.logger.info(f"Mapped {req_col} -> {mapped_col}")
            else:
                missing_columns.append(req_col)
        
        if missing_columns:
            return False, f"Missing required columns: {', '.join(missing_columns)}", details
        
        # Map optional columns
        for opt_col, keywords in self.optional_columns.items():
            mapped_col = self._find_column(bulk_data, keywords)
            if mapped_col:
                details['column_mapping'][opt_col] = mapped_col
                self.logger.info(f"Mapped optional {opt_col} -> {mapped_col}")
        
        return True, "Bulk structure validation passed", details
    
    def _validate_content(
        self, 
        template_data: Dict[str, pd.DataFrame], 
        bulk_data: pd.DataFrame, 
        column_mapping: Dict[str, str]
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """Validate data content for Zero Sales processing."""
        
        details = {
            'bulk_portfolios': [],
            'zero_units_count': 0,
            'processable_rows': 0,
            'issues': [],
            'warnings': []
        }
        
        # Get portfolio column
        portfolio_col = column_mapping.get('portfolio')
        units_col = column_mapping.get('units')
        bid_col = column_mapping.get('bid')
        
        if not all([portfolio_col, units_col, bid_col]):
            return False, "Critical columns not mapped", details
        
        # Validate portfolio data
        try:
            bulk_portfolios = bulk_data[portfolio_col].astype(str).str.strip().dropna()
            details['bulk_portfolios'] = bulk_portfolios.unique().tolist()
            
        except Exception as e:
            return False, f"Error reading bulk portfolios: {str(e)}", details
        
        # Validate units column
        try:
            units_series = pd.to_numeric(bulk_data[units_col], errors='coerce')
            zero_units_mask = units_series == 0
            details['zero_units_count'] = zero_units_mask.sum()
            
            if details['zero_units_count'] == 0:
                details['warnings'].append("No zero sales candidates found")
            
        except Exception as e:
            return False, f"Error validating units column: {str(e)}", details
        
        # Validate bid column
        try:
            bid_series = pd.to_numeric(bulk_data[bid_col], errors='coerce')
            valid_bids = bid_series.notna().sum()
            
            if valid_bids < len(bulk_data) * 0.8:  # Less than 80% valid bids
                details['warnings'].append(f"Many invalid bid values: {len(bulk_data) - valid_bids}")
            
        except Exception as e:
            return False, f"Error validating bid column: {str(e)}", details
        
        # Count processable rows
        try:
            # Rows with valid portfolio, zero units, and valid bid
            valid_portfolio = bulk_data[portfolio_col].notna()
            zero_units = units_series == 0
            valid_bid = bid_series.notna()
            
            processable_mask = valid_portfolio & zero_units & valid_bid
            details['processable_rows'] = processable_mask.sum()
            
            if details['processable_rows'] == 0:
                return False, "No processable rows found", details
            
        except Exception as e:
            return False, f"Error counting processable rows: {str(e)}", details
        
        return True, "Content validation passed", details
    
    def _find_column(self, df: pd.DataFrame, keywords: List[str]) -> str:
        """Find column using keywords (case-insensitive)."""
        
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
        
        return None
    
    def get_validation_summary(self, validation_details: Dict[str, Any]) -> str:
        """Generate a human-readable validation summary."""
        
        summary_lines = [
            f"Template Portfolios: {len(validation_details.get('template_portfolios', []))}",
            f"Bulk Portfolios: {len(validation_details.get('bulk_portfolios', []))}",
            f"Zero Sales Candidates: {validation_details.get('zero_units_count', 0)}",
            f"Processable Rows: {validation_details.get('processable_rows', 0)}",
            f"Ignored Portfolios: {len(validation_details.get('ignored_portfolios', []))}"
        ]
        
        if validation_details.get('warnings'):
            summary_lines.extend([
                "",
                "Warnings:",
                *[f"• {w}" for w in validation_details['warnings']]
            ])
        
        return "\n".join(summary_lines)