"""Numeric value validation utilities for bid optimizations."""

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple, List, Optional
import logging


class NumericValidator:
    """Validates and processes numeric columns in bid optimization data."""

    def __init__(self):
        self.logger = logging.getLogger("common.numeric_validator")
        
        # Numeric columns to validate
        self.numeric_columns = {
            "bid": {"name": "Bid", "min": 0.02, "max": 4.00},
            "clicks": {"name": "Clicks", "min": 0, "max": None},
            "units": {"name": "Units", "min": 0, "max": None},
            "percentage": {"name": "Percentage", "min": 0, "max": 100},
            "impressions": {"name": "Impressions", "min": 0, "max": None},
            "spend": {"name": "Spend", "min": 0, "max": None},
            "sales": {"name": "Sales", "min": 0, "max": None},
            "orders": {"name": "Orders", "min": 0, "max": None},
        }
        
        # Critical columns for Zero Sales
        self.critical_columns = ["Bid", "Clicks", "Units", "Percentage"]

    def validate_numeric_columns(
        self,
        df: pd.DataFrame,
        columns_to_validate: Optional[List[str]] = None,
        column_mapping: Optional[Dict[str, str]] = None,
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Validate numeric columns and mark invalid rows.

        Args:
            df: DataFrame to validate
            columns_to_validate: Specific columns to validate (default: critical columns)
            column_mapping: Optional column name mapping

        Returns:
            Tuple of (processed_dataframe, validation_details)
        """

        if columns_to_validate is None:
            columns_to_validate = self.critical_columns

        details = {
            "total_rows": len(df),
            "columns_validated": [],
            "invalid_counts": {},
            "out_of_range_counts": {},
            "rows_with_errors": 0,
            "errors_by_column": {},
        }

        # Track rows with any error
        error_mask = pd.Series(False, index=df.index)
        df["_has_numeric_error"] = False

        for col_key, col_info in self.numeric_columns.items():
            # Get actual column name
            if column_mapping and col_key in column_mapping:
                col_name = column_mapping[col_key]
            else:
                col_name = col_info["name"]

            if col_name not in df.columns or col_name not in columns_to_validate:
                continue

            details["columns_validated"].append(col_name)

            # Convert to numeric
            original_values = df[col_name].copy()
            df[col_name] = pd.to_numeric(df[col_name], errors="coerce")

            # Check for non-numeric values
            invalid_mask = df[col_name].isna() & original_values.notna()
            invalid_count = invalid_mask.sum()
            
            if invalid_count > 0:
                details["invalid_counts"][col_name] = invalid_count
                error_mask |= invalid_mask
                
                # Mark specific error
                df.loc[invalid_mask, f"{col_name}_invalid"] = True
                
                self.logger.warning(
                    f"Found {invalid_count} non-numeric values in {col_name}"
                )

            # Check range if specified
            min_val = col_info.get("min")
            max_val = col_info.get("max")
            
            out_of_range_mask = pd.Series(False, index=df.index)
            
            if min_val is not None:
                below_min = df[col_name] < min_val
                out_of_range_mask |= below_min
                
                if below_min.sum() > 0:
                    df.loc[below_min, f"{col_name}_below_min"] = True
            
            if max_val is not None:
                above_max = df[col_name] > max_val
                out_of_range_mask |= above_max
                
                if above_max.sum() > 0:
                    df.loc[above_max, f"{col_name}_above_max"] = True
            
            out_of_range_count = out_of_range_mask.sum()
            if out_of_range_count > 0:
                details["out_of_range_counts"][col_name] = out_of_range_count
                error_mask |= out_of_range_mask

        # Mark rows with any error
        df["_has_numeric_error"] = error_mask
        details["rows_with_errors"] = error_mask.sum()

        if details["rows_with_errors"] > 0:
            self.logger.info(
                f"Found {details['rows_with_errors']} rows with numeric errors"
            )

        return df, details

    def mark_error_rows(
        self,
        df: pd.DataFrame,
        bid_column: str = "Bid",
        error_value: str = "Error",
    ) -> pd.DataFrame:
        """
        Mark rows with numeric errors by setting Bid column to 'Error'.

        Args:
            df: DataFrame to process
            bid_column: Name of Bid column
            error_value: Value to set for error rows

        Returns:
            DataFrame with errors marked
        """

        if "_has_numeric_error" in df.columns and bid_column in df.columns:
            error_rows = df["_has_numeric_error"] == True
            df.loc[error_rows, bid_column] = error_value
            
            error_count = error_rows.sum()
            if error_count > 0:
                self.logger.info(
                    f"Marked {error_count} rows with '{error_value}' in {bid_column}"
                )

        return df

    def validate_critical_columns(
        self, df: pd.DataFrame, column_mapping: Optional[Dict[str, str]] = None
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Check if critical columns exist and are valid.

        Args:
            df: DataFrame to validate
            column_mapping: Optional column name mapping

        Returns:
            Tuple of (is_valid, message, details)
        """

        details = {
            "missing_columns": [],
            "invalid_columns": [],
            "valid_columns": [],
        }

        is_valid = True
        messages = []

        for col in self.critical_columns:
            # Get actual column name
            if column_mapping and col.lower() in column_mapping:
                actual_col = column_mapping[col.lower()]
            else:
                actual_col = col

            if actual_col not in df.columns:
                details["missing_columns"].append(actual_col)
                messages.append(f"Missing critical column: {actual_col}")
                is_valid = False
            else:
                # Check if column has valid numeric data
                numeric_values = pd.to_numeric(df[actual_col], errors="coerce")
                invalid_count = numeric_values.isna().sum()
                
                if invalid_count == len(df):
                    details["invalid_columns"].append(actual_col)
                    messages.append(f"Column {actual_col} has no valid numeric values")
                    is_valid = False
                else:
                    details["valid_columns"].append(actual_col)

        if is_valid:
            return True, "All critical columns validated", details
        else:
            return False, "; ".join(messages), details

    def fix_numeric_values(
        self,
        df: pd.DataFrame,
        fill_value: float = 0,
        columns: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """
        Fix invalid numeric values by replacing with fill_value.

        Args:
            df: DataFrame to process
            fill_value: Value to use for invalid entries
            columns: Specific columns to fix (default: all numeric columns)

        Returns:
            DataFrame with fixed values
        """

        if columns is None:
            columns = [col["name"] for col in self.numeric_columns.values()]

        fixed_count = 0

        for col in columns:
            if col in df.columns:
                before = df[col].isna().sum()
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(fill_value)
                after = df[col].isna().sum()
                fixed = before - after
                
                if fixed > 0:
                    fixed_count += fixed
                    self.logger.info(f"Fixed {fixed} invalid values in {col}")

        if fixed_count > 0:
            self.logger.info(f"Total fixed values: {fixed_count}")

        return df

    def get_numeric_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Get summary statistics for numeric columns.

        Args:
            df: DataFrame to analyze

        Returns:
            Dictionary with summary statistics
        """

        summary = {
            "total_rows": len(df),
            "numeric_columns": {},
        }

        for col_info in self.numeric_columns.values():
            col_name = col_info["name"]
            
            if col_name in df.columns:
                numeric_values = pd.to_numeric(df[col_name], errors="coerce")
                
                col_summary = {
                    "count": numeric_values.notna().sum(),
                    "invalid": numeric_values.isna().sum(),
                    "min": numeric_values.min() if numeric_values.notna().any() else None,
                    "max": numeric_values.max() if numeric_values.notna().any() else None,
                    "mean": numeric_values.mean() if numeric_values.notna().any() else None,
                    "zeros": (numeric_values == 0).sum(),
                }
                
                summary["numeric_columns"][col_name] = col_summary

        return summary