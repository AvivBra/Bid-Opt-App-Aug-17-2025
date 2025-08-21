"""Zero Sales optimization validator."""

import pandas as pd
from typing import Tuple, Dict, Any
import logging


class ZeroSalesValidator:
    """Validates data for Zero Sales optimization processing."""

    def __init__(self):
        self.logger = logging.getLogger("optimization.zero_sales.validator")

        # Required columns for Zero Sales - FIXED: using exact column name
        self.required_columns = {
            "portfolio": ["Portfolio Name (Informational only)", "portfolio"],
            "units": ["units", "unit"],
            "bid": ["bid", "max bid"],
            "clicks": ["clicks", "click"],
            "campaign": ["campaign", "campaign name", "campaign id"],
            "entity": ["entity", "entity type"],
        }

    def validate(
        self, template_data: Dict[str, pd.DataFrame], bulk_data: pd.DataFrame
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Validate all data for Zero Sales optimization.

        Returns:
            Tuple of (is_valid, message, details)
        """

        details = {
            "template_valid": False,
            "bulk_valid": False,
            "data_compatibility": False,
            "zero_sales_candidates": 0,
            "column_mapping": {},
        }

        # Validate template
        template_valid, template_msg, template_details = self._validate_template(
            template_data
        )
        details["template_valid"] = template_valid
        details.update(template_details)

        if not template_valid:
            return False, f"Template validation failed: {template_msg}", details

        # Validate bulk data structure
        bulk_valid, bulk_msg, column_mapping = self._validate_bulk(bulk_data)
        details["bulk_valid"] = bulk_valid
        details["column_mapping"] = column_mapping

        if not bulk_valid:
            return False, f"Bulk validation failed: {bulk_msg}", details

        # Check data compatibility
        compat_valid, compat_msg = self._check_compatibility(
            template_data, bulk_data, column_mapping
        )
        details["data_compatibility"] = compat_valid

        if not compat_valid:
            return False, f"Data compatibility issue: {compat_msg}", details

        # Check for zero sales data
        has_zero_sales = self._check_zero_sales_data(bulk_data, column_mapping)
        details["has_zero_sales_data"] = has_zero_sales

        if not has_zero_sales:
            return False, "No rows with Units = 0 found for processing", details

        # Count candidates
        if "units" in column_mapping:
            units_col = column_mapping["units"]
            details["zero_sales_candidates"] = len(bulk_data[bulk_data[units_col] == 0])

        return True, "Validation successful", details

    def _validate_template(
        self, template_data: Dict[str, pd.DataFrame]
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """Validate template data structure and content."""

        details = {"template_portfolios": [], "ignored_portfolios": []}

        # Check Port Values sheet
        if "Port Values" not in template_data:
            return False, "Port Values sheet not found", details

        port_values = template_data["Port Values"]

        if port_values.empty:
            return False, "Port Values sheet is empty", details

        # Check required columns
        required_cols = ["Portfolio Name", "Base Bid", "Target CPA"]
        missing_cols = [col for col in required_cols if col not in port_values.columns]

        if missing_cols:
            return False, f"Missing columns: {', '.join(missing_cols)}", details

        # Extract portfolio info
        portfolios = port_values["Portfolio Name"].dropna().tolist()
        details["template_portfolios"] = portfolios

        # Find ignored portfolios
        ignored = port_values[
            port_values["Base Bid"].astype(str).str.lower() == "ignore"
        ]["Portfolio Name"].tolist()
        details["ignored_portfolios"] = ignored

        if len(ignored) == len(portfolios):
            return False, "All portfolios are set to 'Ignore'", details

        return True, "Template validation passed", details

    def _validate_bulk(
        self, bulk_data: pd.DataFrame
    ) -> Tuple[bool, str, Dict[str, str]]:
        """Validate bulk data structure."""

        if bulk_data.empty:
            return False, "Bulk data is empty", {}

        column_mapping = {}
        missing_critical = []

        # FIXED: Check for exact portfolio column name first
        if "Portfolio Name (Informational only)" in bulk_data.columns:
            column_mapping["portfolio"] = "Portfolio Name (Informational only)"
        else:
            missing_critical.append("Portfolio Name (Informational only)")

        # FIXED: Check for exact Bid column
        if "Bid" in bulk_data.columns:
            column_mapping["bid"] = "Bid"
        else:
            missing_critical.append("Bid")

        # Map other columns using flexible matching
        df_cols_lower = {col.lower(): col for col in bulk_data.columns}

        # Map units column
        if "units" not in column_mapping:
            found = False
            for keyword in self.required_columns["units"]:
                for col_lower, col_original in df_cols_lower.items():
                    if keyword in col_lower:
                        column_mapping["units"] = col_original
                        found = True
                        break
                if found:
                    break
            if not found:
                missing_critical.append("units")

        # Map clicks column
        if "clicks" not in column_mapping:
            found = False
            for keyword in self.required_columns["clicks"]:
                for col_lower, col_original in df_cols_lower.items():
                    if keyword in col_lower:
                        column_mapping["clicks"] = col_original
                        found = True
                        break
                if found:
                    break

        # Map campaign column
        if "campaign" not in column_mapping:
            found = False
            for keyword in self.required_columns["campaign"]:
                for col_lower, col_original in df_cols_lower.items():
                    if keyword in col_lower:
                        column_mapping["campaign"] = col_original
                        found = True
                        break
                if found:
                    break

        # Map entity column
        if "entity" not in column_mapping:
            found = False
            for keyword in self.required_columns["entity"]:
                for col_lower, col_original in df_cols_lower.items():
                    if keyword in col_lower:
                        column_mapping["entity"] = col_original
                        found = True
                        break
                if found:
                    break

        if missing_critical:
            return (
                False,
                f"Critical columns missing: {', '.join(missing_critical)}",
                column_mapping,
            )

        return True, "Bulk structure valid", column_mapping

    def _check_zero_sales_data(
        self, bulk_data: pd.DataFrame, column_mapping: Dict[str, str]
    ) -> bool:
        """Check if there's zero sales data to process."""

        if "units" not in column_mapping:
            return False

        units_col = column_mapping["units"]

        # Check for rows with Units = 0
        zero_units = bulk_data[bulk_data[units_col] == 0]

        return len(zero_units) > 0

    def _check_compatibility(
        self,
        template_data: Dict[str, pd.DataFrame],
        bulk_data: pd.DataFrame,
        column_mapping: Dict[str, str],
    ) -> Tuple[bool, str]:
        """Check if template and bulk data are compatible."""

        if "portfolio" not in column_mapping:
            return False, "Portfolio column not found in bulk data"

        portfolio_col = column_mapping["portfolio"]
        port_values = template_data.get("Port Values", pd.DataFrame())

        if port_values.empty:
            return False, "Port Values sheet is empty"

        # Get unique portfolios from both files
        template_portfolios = set(port_values["Portfolio Name"].dropna().astype(str))
        bulk_portfolios = set(bulk_data[portfolio_col].dropna().astype(str))

        # Remove excluded portfolios from check
        excluded = {
            "Flat 30",
            "Flat 25",
            "Flat 40",
            "Flat 25 | Opt",
            "Flat 30 | Opt",
            "Flat 20",
            "Flat 15",
            "Flat 40 | Opt",
            "Flat 20 | Opt",
            "Flat 15 | Opt",
        }

        bulk_portfolios_to_check = bulk_portfolios - excluded
        missing_in_template = bulk_portfolios_to_check - template_portfolios

        if missing_in_template:
            missing_list = list(missing_in_template)[:5]  # Show first 5
            return (
                False,
                f"Portfolios in bulk not found in template: {', '.join(missing_list)}",
            )

        return True, "Data compatible"
