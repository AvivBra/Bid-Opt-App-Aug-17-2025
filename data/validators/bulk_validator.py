"""Bulk file validation utilities."""

import pandas as pd
from typing import Tuple, Dict, Any, List
from config.constants import BULK_REQUIRED_COLUMNS, BULK_SHEET_NAME, MAX_ROWS


class BulkValidator:
    """Validates bulk files and their data for optimization processing."""

    def __init__(self):
        self.required_columns = BULK_REQUIRED_COLUMNS
        self.required_sheet = BULK_SHEET_NAME

        # Critical columns for Zero Sales optimization - FIXED: using exact column name
        self.zero_sales_columns = [
            "Portfolio Name (Informational only)",  # FIXED: exact column name
            "units",
            "bid",
            "clicks",
            "campaign",
            "ad group",
            "targeting",
            "match type",
        ]

    def validate_complete(
        self, df: pd.DataFrame, filename: str = ""
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Complete validation of bulk file data.

        Returns:
            Tuple of (is_valid, message, validation_details)
        """

        validation_results = {
            "structure_valid": False,
            "data_valid": False,
            "row_count": 0,
            "column_count": 0,
            "zero_sales_ready": False,
            "issues": [],
            "warnings": [],
            "column_mapping": {},
        }

        if df is None or df.empty:
            validation_results["issues"].append("DataFrame is empty")
            return False, "Bulk file is empty", validation_results

        # Basic structure validation
        validation_results["row_count"] = len(df)
        validation_results["column_count"] = len(df.columns)

        structure_valid, structure_msg = self._validate_structure(df, filename)
        validation_results["structure_valid"] = structure_valid

        if not structure_valid:
            validation_results["issues"].append(structure_msg)
            return False, structure_msg, validation_results

        # Simplified data content validation - NO HEAVY LOOPS
        data_valid, data_msg, data_details = self._validate_data_content_simple(df)
        validation_results["data_valid"] = data_valid
        validation_results.update(data_details)

        if not data_valid:
            validation_results["issues"].append(data_msg)
            return False, data_msg, validation_results

        # Zero Sales specific validation
        zero_sales_ready, zero_msg, column_mapping = (
            self._validate_zero_sales_requirements(df)
        )
        validation_results["zero_sales_ready"] = zero_sales_ready
        validation_results["column_mapping"] = column_mapping

        if not zero_sales_ready:
            validation_results["warnings"].append(
                f"Zero Sales optimization may not work: {zero_msg}"
            )

        # Success message
        success_msg = f"Bulk file valid: {validation_results['row_count']:,} rows, {validation_results['column_count']} columns"

        return True, success_msg, validation_results

    def _validate_structure(self, df: pd.DataFrame, filename: str) -> Tuple[bool, str]:
        """Validate basic file structure."""

        # Check column count
        if self.required_columns and len(df.columns) != self.required_columns:
            return (
                False,
                f"Expected {self.required_columns} columns, found {len(df.columns)}",
            )

        # Check row count
        if len(df) > MAX_ROWS:
            return False, f"File exceeds {MAX_ROWS:,} rows limit: {len(df):,} rows"

        # Check for Portfolio Name column - FIXED: using exact column name
        if "Portfolio Name (Informational only)" not in df.columns:
            # Fallback: look for any column containing "portfolio"
            portfolio_col_found = False
            for col in df.columns:
                if "portfolio" in col.lower():
                    portfolio_col_found = True
                    break

            if not portfolio_col_found:
                return False, "Portfolio Name (Informational only) column not found"

        return True, "Structure valid"

    def _validate_data_content_simple(
        self, df: pd.DataFrame
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """Simple data content validation without heavy loops."""

        details = {
            "entity_types": [],
            "portfolio_count": 0,
            "campaign_count": 0,
        }

        try:
            # Quick checks using vectorized operations
            if "Entity" in df.columns:
                details["entity_types"] = df["Entity"].dropna().unique().tolist()[:10]

            # FIXED: using exact column name
            if "Portfolio Name (Informational only)" in df.columns:
                details["portfolio_count"] = df[
                    "Portfolio Name (Informational only)"
                ].nunique()
            else:
                # Fallback: look for any column containing "portfolio"
                for col in df.columns:
                    if "portfolio" in col.lower():
                        details["portfolio_count"] = df[col].nunique()
                        break

            if "Campaign Name" in df.columns:
                details["campaign_count"] = df["Campaign Name"].nunique()

            # Basic completeness check
            if details["portfolio_count"] == 0:
                return False, "No portfolios found in data", details

            return True, "Data content valid", details

        except Exception as e:
            return False, f"Data validation error: {str(e)}", details

    def _validate_zero_sales_requirements(
        self, df: pd.DataFrame
    ) -> Tuple[bool, str, Dict[str, str]]:
        """Check if bulk file has required columns for Zero Sales optimization."""

        column_mapping = {}
        missing_columns = []

        # Map required columns (case-insensitive matching)
        df_columns_lower = {col.lower(): col for col in df.columns}

        # FIXED: Check for exact portfolio column name first
        if "Portfolio Name (Informational only)" in df.columns:
            column_mapping["portfolio"] = "Portfolio Name (Informational only)"
        else:
            # Fallback: look for column containing "portfolio"
            for col_lower, col_original in df_columns_lower.items():
                if "portfolio" in col_lower:
                    column_mapping["portfolio"] = col_original
                    break

        # Map other columns
        column_requirements = {
            "units": ["units", "unit"],
            "bid": ["bid", "max bid"],
            "clicks": ["clicks", "click"],
            "campaign": ["campaign", "campaign name"],
        }

        for req_name, keywords in column_requirements.items():
            found = False
            for keyword in keywords:
                for col_lower, col_original in df_columns_lower.items():
                    if keyword in col_lower:
                        column_mapping[req_name] = col_original
                        found = True
                        break
                if found:
                    break
            if not found:
                missing_columns.append(req_name)

        # Check critical columns
        if "portfolio" not in column_mapping:
            missing_columns.insert(0, "Portfolio Name (Informational only)")

        if missing_columns:
            return (
                False,
                f"Missing columns: {', '.join(missing_columns)}",
                column_mapping,
            )

        return True, "All required columns found", column_mapping

    def quick_validate_bulk(self, df: pd.DataFrame) -> Tuple[bool, str, Dict[str, Any]]:
        """Quick validation without detailed analysis."""

        if df is None or df.empty:
            return False, "File is empty", {}

        basic_info = {
            "rows": len(df),
            "columns": len(df.columns),
            "has_portfolio": "Portfolio Name (Informational only)" in df.columns,
            "has_units": any("unit" in col.lower() for col in df.columns),
        }

        if basic_info["columns"] != self.required_columns:
            return (
                False,
                f"Expected {self.required_columns} columns, found {basic_info['columns']}",
                basic_info,
            )

        return True, "Quick validation passed", basic_info
