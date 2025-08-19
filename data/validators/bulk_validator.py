"""Bulk file validation utilities."""

import pandas as pd
from typing import Tuple, Dict, Any, List
from config.constants import BULK_REQUIRED_COLUMNS, BULK_SHEET_NAME, MAX_ROWS


class BulkValidator:
    """Validates bulk files and their data for optimization processing."""

    def __init__(self):
        self.required_columns = BULK_REQUIRED_COLUMNS
        self.required_sheet = BULK_SHEET_NAME

        # Critical columns for Zero Sales optimization
        self.zero_sales_columns = [
            "portfolio",
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

        # Check row count
        if len(df) > MAX_ROWS:
            return False, f"Too many rows: {len(df):,} (max: {MAX_ROWS:,})"

        if len(df) == 0:
            return False, "File contains no data rows"

        # Check column count (flexible based on file type)
        col_count = len(df.columns)

        if filename.lower().endswith(".xlsx"):
            # Excel files should have exactly 48 columns
            if col_count != BULK_REQUIRED_COLUMNS:
                return (
                    False,
                    f"Excel bulk file must have exactly {BULK_REQUIRED_COLUMNS} columns (found: {col_count})",
                )
        else:
            # CSV files are more flexible
            if col_count < 20:
                return False, f"Too few columns: {col_count} (expected at least 20)"
            if col_count > 100:
                return False, f"Too many columns: {col_count} (expected at most 100)"

        return True, "File structure is valid"

    def _validate_data_content_simple(
        self, df: pd.DataFrame
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        SIMPLIFIED data content validation - no heavy loops.
        """

        details = {
            "empty_rows": 0,
            "duplicate_rows": 0,
            "null_percentage": 0.0,
            "issues": [],
            "warnings": [],
        }

        # Quick check for completely empty rows
        empty_rows = df.isnull().all(axis=1).sum()
        details["empty_rows"] = empty_rows

        if empty_rows > len(df) * 0.5:  # More than 50% empty
            return False, f"Too many empty rows: {empty_rows}", details

        # Quick check for duplicates (first 1000 rows only for performance)
        sample_size = min(1000, len(df))
        duplicate_rows = df.head(sample_size).duplicated().sum()
        details["duplicate_rows"] = duplicate_rows

        if duplicate_rows > sample_size * 0.3:  # More than 30% duplicates in sample
            details["warnings"].append(
                f"Many duplicate rows found in sample: {duplicate_rows}"
            )

        # Simple null percentage - just overall, no per-column analysis
        total_cells = df.size
        null_cells = df.isnull().sum().sum()
        null_percentage = (null_cells / total_cells) * 100 if total_cells > 0 else 0
        details["null_percentage"] = null_percentage

        # Amazon bulk files normally have 60-80% nulls, so we allow high percentages
        if null_percentage > 95:
            details["warnings"].append(
                f"Very high null percentage: {null_percentage:.1f}%"
            )

        return True, "Data content is acceptable", details

    def _validate_zero_sales_requirements(
        self, df: pd.DataFrame
    ) -> Tuple[bool, str, Dict[str, str]]:
        """Validate requirements for Zero Sales optimization."""

        column_mapping = {}
        missing_columns = []

        # Map critical columns (case-insensitive search)
        df_cols_lower = {col.lower(): col for col in df.columns}

        for required_col in self.zero_sales_columns:
            mapped_col = None

            # Direct match
            if required_col in df_cols_lower:
                mapped_col = df_cols_lower[required_col]
            else:
                # Partial match - simplified
                for col_lower, col_original in df_cols_lower.items():
                    if required_col in col_lower:
                        mapped_col = col_original
                        break

            if mapped_col:
                column_mapping[required_col] = mapped_col
            else:
                missing_columns.append(required_col)

        # Check only the most critical columns
        critical_missing = []
        for critical_col in ["portfolio", "units", "bid"]:
            if critical_col not in column_mapping:
                critical_missing.append(critical_col)

        if critical_missing:
            return (
                False,
                f"Missing critical columns: {', '.join(critical_missing)}",
                column_mapping,
            )

        return (
            True,
            f"Zero Sales requirements met (mapped {len(column_mapping)} columns)",
            column_mapping,
        )

    def get_data_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get basic summary of bulk file data."""

        if df is None or df.empty:
            return {"empty": True}

        summary = {
            "empty": False,
            "rows": len(df),
            "columns": len(df.columns),
            "memory_mb": df.memory_usage(deep=True).sum() / (1024 * 1024),
            "null_percentage": (df.isnull().sum().sum() / df.size) * 100,
        }

        return summary
