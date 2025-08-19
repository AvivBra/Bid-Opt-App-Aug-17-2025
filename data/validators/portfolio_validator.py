"""Portfolio validation between template and bulk files."""

import pandas as pd
from typing import Tuple, Dict, Any, List, Set
from business.common.excluded_portfolios import get_excluded_portfolios


class PortfolioValidator:
    """Validates portfolio matching between template and bulk files."""
    
    def __init__(self):
        self.excluded_portfolios = get_excluded_portfolios()
    
    def validate_portfolio_matching(
        self, 
        template_data: Dict[str, pd.DataFrame], 
        bulk_data: pd.DataFrame
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Validate portfolio matching between template and bulk files.
        
        Returns:
            Tuple of (is_valid, message, validation_details)
        """
        
        details = {
            'template_portfolios': [],
            'bulk_portfolios': [],
            'matching_portfolios': [],
            'missing_in_bulk': [],
            'missing_in_template': [],
            'excluded_portfolios': [],
            'zero_sales_candidates': 0,
            'processing_ready': False,
            'warnings': [],
            'info': []
        }
        
        # Get template portfolios
        try:
            template_port_values = template_data.get('Port Values')
            if template_port_values is None or template_port_values.empty:
                return False, "No portfolio data found in template", details
            
            template_portfolios = set(
                template_port_values['Portfolio Name']
                .astype(str)
                .str.strip()
                .dropna()
            )
            details['template_portfolios'] = sorted(list(template_portfolios))
            
        except Exception as e:
            return False, f"Error reading template portfolios: {str(e)}", details
        
        # Get bulk portfolios
        try:
            portfolio_col = self._find_portfolio_column(bulk_data)
            if portfolio_col is None:
                return False, "No portfolio column found in bulk file", details
            
            bulk_portfolios = set(
                bulk_data[portfolio_col]
                .astype(str)
                .str.strip()
                .dropna()
            )
            details['bulk_portfolios'] = sorted(list(bulk_portfolios))
            
        except Exception as e:
            return False, f"Error reading bulk portfolios: {str(e)}", details
        
        # Analyze matching
        details['matching_portfolios'] = sorted(list(template_portfolios & bulk_portfolios))
        details['missing_in_bulk'] = sorted(list(template_portfolios - bulk_portfolios))
        details['missing_in_template'] = sorted(list(bulk_portfolios - template_portfolios))
        
        # Filter out excluded portfolios from missing analysis
        excluded_set = set(self.excluded_portfolios)
        details['excluded_portfolios'] = sorted(list(
            (template_portfolios | bulk_portfolios) & excluded_set
        ))
        
        # Adjust missing counts by removing excluded portfolios
        details['missing_in_bulk'] = [
            p for p in details['missing_in_bulk'] 
            if p not in excluded_set
        ]
        
        # Count zero sales candidates
        details['zero_sales_candidates'] = self._count_zero_sales_candidates(bulk_data)
        
        # Validation logic
        if len(details['matching_portfolios']) == 0:
            return False, "No matching portfolios found between template and bulk file", details
        
        # Check if enough portfolios for meaningful processing
        active_template_portfolios = len([
            p for p in template_portfolios 
            if p not in excluded_set
        ])
        
        if len(details['matching_portfolios']) < active_template_portfolios * 0.5:
            details['warnings'].append(
                f"Only {len(details['matching_portfolios'])} of {active_template_portfolios} "
                f"template portfolios found in bulk file"
            )
        
        # Set processing readiness
        details['processing_ready'] = (
            len(details['matching_portfolios']) > 0 and
            details['zero_sales_candidates'] > 0
        )
        
        # Generate summary message
        success_msg = (
            f"Portfolio validation complete: "
            f"{len(details['matching_portfolios'])} matching portfolios, "
            f"{details['zero_sales_candidates']} zero sales candidates"
        )
        
        return True, success_msg, details
    
    def _find_portfolio_column(self, df: pd.DataFrame) -> str:
        """Find the portfolio column in bulk data."""
        
        portfolio_keywords = ['portfolio', 'port']
        
        for col in df.columns:
            col_lower = col.lower()
            for keyword in portfolio_keywords:
                if keyword in col_lower:
                    return col
        
        return None
    
    def _count_zero_sales_candidates(self, df: pd.DataFrame) -> int:
        """Count rows with zero units (zero sales candidates)."""
        
        units_col = None
        units_keywords = ['units', 'unit']
        
        for col in df.columns:
            col_lower = col.lower()
            for keyword in units_keywords:
                if keyword in col_lower:
                    units_col = col
                    break
            if units_col:
                break
        
        if units_col is None:
            return 0
        
        try:
            # Convert to numeric and count zeros
            units_numeric = pd.to_numeric(df[units_col], errors='coerce')
            return (units_numeric == 0).sum()
        except Exception:
            return 0
    
    def get_portfolio_analysis(
        self, 
        template_data: Dict[str, pd.DataFrame], 
        bulk_data: pd.DataFrame
    ) -> Dict[str, Any]:
        """Get detailed portfolio analysis for UI display."""
        
        analysis = {
            'template_summary': {},
            'bulk_summary': {},
            'matching_summary': {},
            'recommendations': []
        }
        
        # Validate first
        valid, msg, details = self.validate_portfolio_matching(template_data, bulk_data)
        
        if not valid:
            analysis['error'] = msg
            return analysis
        
        # Template analysis
        template_portfolios = set(details['template_portfolios'])
        excluded_set = set(self.excluded_portfolios)
        
        template_active = template_portfolios - excluded_set
        template_ignored = self._get_ignored_portfolios(template_data)
        
        analysis['template_summary'] = {
            'total': len(template_portfolios),
            'active': len(template_active),
            'ignored': len(template_ignored),
            'excluded': len(template_portfolios & excluded_set)
        }
        
        # Bulk analysis
        analysis['bulk_summary'] = {
            'total_portfolios': len(details['bulk_portfolios']),
            'total_rows': len(bulk_data),
            'zero_sales_candidates': details['zero_sales_candidates']
        }
        
        # Matching analysis
        analysis['matching_summary'] = {
            'matches': len(details['matching_portfolios']),
            'missing_in_bulk': len(details['missing_in_bulk']),
            'processing_ready': details['processing_ready']
        }
        
        # Generate recommendations
        if len(details['missing_in_bulk']) > 0:
            analysis['recommendations'].append(
                f"Consider removing {len(details['missing_in_bulk'])} "
                f"portfolios from template that aren't in bulk file"
            )
        
        if details['zero_sales_candidates'] == 0:
            analysis['recommendations'].append(
                "No zero sales candidates found - Zero Sales optimization may not be useful"
            )
        
        if analysis['template_summary']['ignored'] > analysis['template_summary']['active']:
            analysis['recommendations'].append(
                "Most portfolios are set to 'Ignore' - consider activating more portfolios"
            )
        
        return analysis
    
    def _get_ignored_portfolios(self, template_data: Dict[str, pd.DataFrame]) -> Set[str]:
        """Get set of portfolios marked as 'Ignore' in template."""
        
        try:
            port_values = template_data.get('Port Values')
            if port_values is None:
                return set()
            
            ignored_mask = port_values['Base Bid'].astype(str).str.lower() == 'ignore'
            ignored_portfolios = port_values[ignored_mask]['Portfolio Name'].astype(str).str.strip()
            
            return set(ignored_portfolios)
            
        except Exception:
            return set()
    
    def generate_portfolio_report(
        self, 
        template_data: Dict[str, pd.DataFrame], 
        bulk_data: pd.DataFrame
    ) -> str:
        """Generate a text report of portfolio validation."""
        
        valid, msg, details = self.validate_portfolio_matching(template_data, bulk_data)
        
        report_lines = [
            "=== PORTFOLIO VALIDATION REPORT ===",
            "",
            f"Validation Status: {'PASSED' if valid else 'FAILED'}",
            f"Message: {msg}",
            "",
            f"Template Portfolios: {len(details.get('template_portfolios', []))}",
            f"Bulk Portfolios: {len(details.get('bulk_portfolios', []))}",
            f"Matching Portfolios: {len(details.get('matching_portfolios', []))}",
            f"Missing in Bulk: {len(details.get('missing_in_bulk', []))}",
            f"Zero Sales Candidates: {details.get('zero_sales_candidates', 0)}",
            "",
            f"Processing Ready: {'YES' if details.get('processing_ready', False) else 'NO'}",
        ]
        
        if details.get('warnings'):
            report_lines.extend([
                "",
                "WARNINGS:",
                *[f"• {w}" for w in details['warnings']]
            ])
        
        if details.get('missing_in_bulk'):
            report_lines.extend([
                "",
                "PORTFOLIOS NOT FOUND IN BULK:",
                *[f"• {p}" for p in details['missing_in_bulk'][:5]]
            ])
            if len(details['missing_in_bulk']) > 5:
                report_lines.append(f"• ... and {len(details['missing_in_bulk']) - 5} more")
        
        return "\n".join(report_lines)