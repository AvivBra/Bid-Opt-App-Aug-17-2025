"""Bulk file validation utilities."""

import pandas as pd
from typing import Tuple, Optional
from config.constants import BULK_REQUIRED_COLUMNS, MAX_ROWS


class BulkValidator:
    """Validates bulk files for optimization processing."""

    def __init__(self):
        """Initialize the bulk validator."""
        self.required_columns = BULK_REQUIRED_COLUMNS
        self.max_rows = MAX_ROWS

    def validate(self, df: pd.DataFrame) -> Tuple[bool, str]:
        """
        Validate bulk file DataFrame.

        Args:
            df: DataFrame to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if DataFrame is empty
        if df is None or df.empty:
            return False, "Bulk file is empty"

        # Check column count
        if len(df.columns) != self.required_columns:
            return (
                False,
                f"Invalid column count. Expected {self.required_columns}, got {len(df.columns)}",
            )

        # Check row count
        if len(df) > self.max_rows:
            return (
                False,
                f"Too many rows. Maximum allowed: {self.max_rows:,}, got {len(df):,}",
            )

        # Check for required columns (relaxed for now)
        critical_columns = [
            "Entity",
            "Operation",
            "Campaign ID",
            "Ad Group ID",
            "Portfolio ID",
            "Bid",
            "Units",
            "Clicks",
        ]

        # Check if any critical column pattern exists
        found_critical = 0
        for col in critical_columns:
            if any(col.lower() in str(c).lower() for c in df.columns):
                found_critical += 1

        if found_critical < 4:  # At least 4 critical columns should be found
            return False, "Missing critical columns for optimization"

        return True, f"Bulk file valid: {len(df):,} rows"

    def validate_complete(
        self, df: pd.DataFrame, filename: str = ""
    ) -> Tuple[bool, str, dict]:
        """
        Complete validation with detailed results.

        Args:
            df: DataFrame to validate
            filename: Optional filename for context

        Returns:
            Tuple of (is_valid, message, details)
        """
        details = {
            "row_count": len(df) if df is not None else 0,
            "column_count": len(df.columns) if df is not None else 0,
            "filename": filename,
            "issues": [],
        }

        is_valid, message = self.validate(df)

        if not is_valid:
            details["issues"].append(message)

        return is_valid, message, details

    def check_sheet_name(
        self, excel_file, expected_sheet: str = "Sponsored Products Campaigns"
    ) -> bool:
        """
        Check if the expected sheet exists in Excel file.

        Args:
            excel_file: Excel file object
            expected_sheet: Expected sheet name

        Returns:
            True if sheet exists
        """
        try:
            excel_data = pd.ExcelFile(excel_file)
            return expected_sheet in excel_data.sheet_names
        except:
            return False
