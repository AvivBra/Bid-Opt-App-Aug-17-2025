"""Zero Sales optimization validation - SIMPLIFIED."""

import pandas as pd
from typing import Tuple, Dict, Any, Optional
import logging


class ZeroSalesValidator:
    """Validates data requirements for Zero Sales optimization."""

    def __init__(self):
        self.logger = logging.getLogger("optimization.zero_sales.validator")

        # Required columns for Zero Sales
        self.required_columns = {
            "portfolio": ["portfolio"],
            "units": ["units", "unit"],
            "bid": ["bid", "max bid"],
            "clicks": ["click"],
            "campaign": ["campaign"],
            "entity": ["entity"],
        }

    def validate(
        self, template_data: Dict[str, pd.DataFrame], bulk_data: pd.DataFrame
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        SIMPLIFIED validation for Zero Sales optimization.

        Returns:
            Tuple of (is_valid, message, details)
        """

        details = {
            "template_valid": False,
            "bulk_valid": False,
            "column_mapping": {},
            "issues": [],
            "warnings": [],
        }

        # Validate template
        template_valid, template_msg, template_details = self._validate_template(
            template_data
        )
        details["template_valid"] = template_valid
        details.update(template_details)

        if not template_valid:
            return False, f"Template validation failed: {template_msg}", details

        # Validate bulk structure
        bulk_valid, bulk_msg, column_mapping = self._validate_bulk(bulk_data)
        details["bulk_valid"] = bulk_valid
        details["column_mapping"] = column_mapping

        if not bulk_valid:
            return False, f"Bulk validation failed: {bulk_msg}", details

        # Check for zero sales data
        has_zero_sales = self._check_zero_sales_data(bulk_data, column_mapping)

        if not has_zero_sales:
            details["warnings"].append("No rows with Units=0 found")

        return True, "Validation passed for Zero Sales optimization", details

    def _validate_template(
        self, template_data: Dict[str, pd.DataFrame]
    ) -> Tuple[bool, str, Dict]:
        """Validate template data."""

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

        # Map columns (case-insensitive)
        df_cols_lower = {col.lower(): col for col in bulk_data.columns}

        for req_name, keywords in self.required_columns.items():
            found = False
            for keyword in keywords:
                for col_lower, col_original in df_cols_lower.items():
                    if keyword in col_lower:
                        column_mapping[req_name] = col_original
                        found = True
                        break
                if found:
                    break

            if not found and req_name in ["units", "bid"]:
                missing_critical.append(req_name)

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
