"""Bids 30 Days optimization validator."""

import pandas as pd
from typing import Tuple, Dict, Any
import logging

from business.bid_optimizations.zero_sales.validator import ZeroSalesValidator
from .constants import (
    EXCLUDED_PORTFOLIOS,
    UNITS_THRESHOLD,
    CLICKS_THRESHOLD,
    CONVERSION_RATE_COLUMN_POSITION
)


class Bids30DaysValidator(ZeroSalesValidator):
    """
    Validates data for Bids 30 Days optimization processing.
    
    Inherits from ZeroSalesValidator as validation is identical,
    but checks for different criteria specific to Bids 30 Days.
    """
    
    def __init__(self):
        """Initialize Bids 30 Days validator."""
        super().__init__()
        self.logger = logging.getLogger("optimization.bids_30_days.validator")
        
        # Override name for logging
        self.optimization_name = "Bids 30 Days"
        
        # Additional required columns for Bids 30 Days
        self.additional_required = {
            "conversion_rate": ["conversion rate", "cvr", "conv rate"],
            "percentage": ["percentage", "bid adjustment"],
            "match_type": ["match type", "matching type"],
            "product_targeting": ["product targeting expression", "product target"],
            "campaign_id": ["campaign id"],
            "campaign_state": ["campaign state (informational only)", "campaign state"],
            "ad_group_state": ["ad group state (informational only)", "ad group state"],
            "state": ["state", "status"]
        }
    
    def validate(
        self, 
        template_data: Dict[str, pd.DataFrame], 
        bulk_data: pd.DataFrame
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Validate all data for Bids 30 Days optimization.
        
        Validation is identical to Zero Sales but checks for:
        - units > 0 (instead of units = 0)
        - Additional condition: units > 2 OR clicks > 30
        - Conversion Rate column exists (position 55)
        - All state columns for filtering
        
        Args:
            template_data: Dictionary containing template sheets
            bulk_data: Bulk campaign data DataFrame
            
        Returns:
            Tuple of (is_valid, message, details)
        """
        
        details = {
            "template_valid": False,
            "bulk_valid": False,
            "data_compatibility": False,
            "bids_30_candidates": 0,
            "column_mapping": {},
            "has_conversion_rate": False
        }
        
        # Validate template (same as Zero Sales)
        template_valid, template_msg, template_details = self._validate_template(
            template_data
        )
        details["template_valid"] = template_valid
        details.update(template_details)
        
        if not template_valid:
            return False, f"Template validation failed: {template_msg}", details
        
        # Validate bulk data structure with additional columns
        bulk_valid, bulk_msg, column_mapping = self._validate_bulk_extended(bulk_data)
        details["bulk_valid"] = bulk_valid
        details["column_mapping"] = column_mapping
        
        if not bulk_valid:
            return False, f"Bulk validation failed: {bulk_msg}", details
        
        # Check data compatibility (same as Zero Sales)
        compat_valid, compat_msg = self._check_compatibility(
            template_data, bulk_data, column_mapping
        )
        details["data_compatibility"] = compat_valid
        
        if not compat_valid:
            return False, f"Data compatibility issue: {compat_msg}", details
        
        # Check for Bids 30 Days specific data
        has_valid_data = self._check_bids_30_data(bulk_data, column_mapping)
        details["has_bids_30_data"] = has_valid_data
        
        if not has_valid_data:
            return False, "No rows meeting Bids 30 Days criteria found", details
        
        # Check for Conversion Rate column (critical for Bids 30)
        has_cvr = self._check_conversion_rate_column(bulk_data, column_mapping)
        details["has_conversion_rate"] = has_cvr
        
        if not has_cvr:
            return False, "Conversion Rate column not found (expected at position 55)", details
        
        # Count candidates
        candidates = self._count_candidates(bulk_data, column_mapping)
        details["bids_30_candidates"] = candidates
        
        if candidates == 0:
            return False, "No valid candidates for Bids 30 Days processing", details
        
        return True, f"Validation successful: {candidates} candidates found", details
    
    def _validate_bulk_extended(
        self, 
        bulk_data: pd.DataFrame
    ) -> Tuple[bool, str, Dict[str, str]]:
        """
        Validate bulk data with additional columns required for Bids 30 Days.
        
        Args:
            bulk_data: Bulk DataFrame to validate
            
        Returns:
            Tuple of (is_valid, message, column_mapping)
        """
        
        # First run base validation from parent class
        base_valid, base_msg, column_mapping = self._validate_bulk(bulk_data)
        
        if not base_valid:
            return False, base_msg, column_mapping
        
        # Check for additional required columns
        missing_critical = []
        df_cols_lower = {col.lower(): col for col in bulk_data.columns}
        
        # Map additional columns
        for col_key, keywords in self.additional_required.items():
            if col_key not in column_mapping:
                found = False
                for keyword in keywords:
                    for col_lower, col_original in df_cols_lower.items():
                        if keyword in col_lower:
                            column_mapping[col_key] = col_original
                            found = True
                            break
                    if found:
                        break
                
                if not found and col_key in ['conversion_rate', 'percentage', 'match_type']:
                    missing_critical.append(col_key)
        
        if missing_critical:
            return (
                False, 
                f"Critical columns for Bids 30 Days missing: {', '.join(missing_critical)}", 
                column_mapping
            )
        
        return True, "Extended bulk validation passed", column_mapping
    
    def _check_bids_30_data(
        self, 
        bulk_data: pd.DataFrame, 
        column_mapping: Dict[str, str]
    ) -> bool:
        """
        Check if there's valid Bids 30 Days data to process.
        
        Criteria:
        - units > 0
        - units > 2 OR clicks > 30
        
        Args:
            bulk_data: Bulk DataFrame
            column_mapping: Column name mapping
            
        Returns:
            True if valid data exists
        """
        
        units_col = column_mapping.get("units")
        clicks_col = column_mapping.get("clicks")
        
        if not units_col or not clicks_col:
            return False
        
        # Convert to numeric
        bulk_data[units_col] = pd.to_numeric(bulk_data[units_col], errors='coerce')
        bulk_data[clicks_col] = pd.to_numeric(bulk_data[clicks_col], errors='coerce')
        
        # Check main condition: units > 0
        units_positive = bulk_data[bulk_data[units_col] > 0]
        
        if units_positive.empty:
            return False
        
        # Check additional condition: units > 2 OR clicks > 30
        valid_rows = units_positive[
            (units_positive[units_col] > UNITS_THRESHOLD) | 
            (units_positive[clicks_col] > CLICKS_THRESHOLD)
        ]
        
        return len(valid_rows) > 0
    
    def _check_conversion_rate_column(
        self, 
        bulk_data: pd.DataFrame, 
        column_mapping: Dict[str, str]
    ) -> bool:
        """
        Check if Conversion Rate column exists.
        
        Should be at position 55 in original bulk file.
        
        Args:
            bulk_data: Bulk DataFrame
            column_mapping: Column name mapping
            
        Returns:
            True if column exists
        """
        
        # Check if already mapped
        if "conversion_rate" in column_mapping:
            return True
        
        # Check by position (55th column, 0-indexed = 54)
        if len(bulk_data.columns) >= CONVERSION_RATE_COLUMN_POSITION:
            # Get column at position 55 (1-based) = index 54 (0-based)
            col_at_55 = bulk_data.columns[CONVERSION_RATE_COLUMN_POSITION - 1]
            
            # Check if it contains conversion rate data
            if "conversion" in col_at_55.lower() or "cvr" in col_at_55.lower():
                column_mapping["conversion_rate"] = col_at_55
                return True
        
        # Search for conversion rate column by name
        for col in bulk_data.columns:
            if "conversion rate" in col.lower() or "cvr" in col.lower():
                column_mapping["conversion_rate"] = col
                return True
        
        return False
    
    def _count_candidates(
        self, 
        bulk_data: pd.DataFrame, 
        column_mapping: Dict[str, str]
    ) -> int:
        """
        Count valid candidates for Bids 30 Days processing.
        
        Args:
            bulk_data: Bulk DataFrame
            column_mapping: Column name mapping
            
        Returns:
            Number of valid candidate rows
        """
        
        units_col = column_mapping.get("units")
        clicks_col = column_mapping.get("clicks")
        portfolio_col = column_mapping.get("portfolio")
        
        if not all([units_col, clicks_col, portfolio_col]):
            return 0
        
        # Convert to numeric
        bulk_data[units_col] = pd.to_numeric(bulk_data[units_col], errors='coerce')
        bulk_data[clicks_col] = pd.to_numeric(bulk_data[clicks_col], errors='coerce')
        
        # Filter: units > 0
        candidates = bulk_data[bulk_data[units_col] > 0].copy()
        
        # Filter: units > 2 OR clicks > 30
        candidates = candidates[
            (candidates[units_col] > UNITS_THRESHOLD) | 
            (candidates[clicks_col] > CLICKS_THRESHOLD)
        ]
        
        # Exclude flat portfolios
        candidates = candidates[~candidates[portfolio_col].isin(EXCLUDED_PORTFOLIOS)]
        
        return len(candidates)
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """
        Get summary of validation requirements.
        
        Returns:
            Dictionary with validation criteria
        """
        
        return {
            "optimization": "Bids 30 Days",
            "main_criteria": {
                "units": "> 0",
                "additional": "units > 2 OR clicks > 30"
            },
            "required_columns": {
                "base": list(self.required_columns.keys()),
                "additional": list(self.additional_required.keys())
            },
            "excluded_portfolios": len(EXCLUDED_PORTFOLIOS),
            "special_requirements": [
                "Conversion Rate column at position 55",
                "All State columns (State, Campaign State, Ad Group State)",
                "Percentage column for Max BA calculation",
                "Match Type for Exact matching",
                "Product Targeting Expression for ASIN detection"
            ]
        }
    
    def _check_compatibility(
        self,
        template_data: Dict[str, pd.DataFrame],
        bulk_data: pd.DataFrame,
        column_mapping: Dict[str, str],
    ) -> Tuple[bool, str]:
        """Check if template and bulk data are compatible - Bids 30 Days version."""

        if "portfolio" not in column_mapping:
            return False, "Portfolio column not found in bulk data"

        portfolio_col = column_mapping["portfolio"]
        port_values = template_data.get("Port Values", pd.DataFrame())

        if port_values.empty:
            return False, "Port Values sheet is empty"

        # Get unique portfolios from both files
        template_portfolios = set(port_values["Portfolio Name"].dropna().astype(str))
        bulk_portfolios = set(bulk_data[portfolio_col].dropna().astype(str))

        # Remove excluded portfolios from check (use Bids 30 Days constants)
        excluded = set(EXCLUDED_PORTFOLIOS)

        bulk_portfolios_to_check = bulk_portfolios - excluded
        missing_in_template = bulk_portfolios_to_check - template_portfolios

        if missing_in_template:
            missing_list = sorted(list(missing_in_template))  # Sort alphabetically
            # Format with one portfolio per line for better readability
            formatted_list = '\n'.join(f"- {portfolio}" for portfolio in missing_list)
            return (
                False,
                f"Portfolios in bulk not found in template:\n{formatted_list}",
            )

        return True, "Data compatible"