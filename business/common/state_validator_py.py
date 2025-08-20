"""State validation utilities for bid optimizations."""

import pandas as pd
from typing import Dict, Any, Tuple, Optional
import logging


class StateValidator:
    """Validates and filters data based on State columns."""

    def __init__(self):
        self.logger = logging.getLogger("common.state_validator")
        
        # Valid state values
        self.valid_states = ["enabled", "paused", "archived"]
        
        # State columns to check
        self.state_columns = [
            "State",
            "Campaign State (Informational only)",
            "Ad Group State (Informational only)",
        ]

    def filter_enabled_only(
        self, df: pd.DataFrame, column_mapping: Optional[Dict[str, str]] = None
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Filter to only rows where all State columns are 'enabled'.

        Args:
            df: DataFrame to filter
            column_mapping: Optional column name mapping

        Returns:
            Tuple of (filtered_dataframe, filter_details)
        """

        details = {
            "original_rows": len(df),
            "filtered_by_state": 0,
            "filtered_by_campaign_state": 0,
            "filtered_by_ad_group_state": 0,
            "remaining_rows": 0,
        }

        if df.empty:
            return df, details

        # Get column names from mapping or use defaults
        if column_mapping:
            state_col = column_mapping.get("state", "State")
            campaign_state_col = column_mapping.get(
                "campaign_state", "Campaign State (Informational only)"
            )
            ad_group_state_col = column_mapping.get(
                "ad_group_state", "Ad Group State (Informational only)"
            )
        else:
            state_col = "State"
            campaign_state_col = "Campaign State (Informational only)"
            ad_group_state_col = "Ad Group State (Informational only)"

        filtered_df = df.copy()

        # Filter by State
        if state_col in filtered_df.columns:
            before = len(filtered_df)
            filtered_df = filtered_df[
                filtered_df[state_col].str.lower() == "enabled"
            ]
            details["filtered_by_state"] = before - len(filtered_df)

        # Filter by Campaign State
        if campaign_state_col in filtered_df.columns:
            before = len(filtered_df)
            filtered_df = filtered_df[
                filtered_df[campaign_state_col].str.lower() == "enabled"
            ]
            details["filtered_by_campaign_state"] = before - len(filtered_df)

        # Filter by Ad Group State
        if ad_group_state_col in filtered_df.columns:
            before = len(filtered_df)
            filtered_df = filtered_df[
                filtered_df[ad_group_state_col].str.lower() == "enabled"
            ]
            details["filtered_by_ad_group_state"] = before - len(filtered_df)

        details["remaining_rows"] = len(filtered_df)
        total_filtered = details["original_rows"] - details["remaining_rows"]

        if total_filtered > 0:
            self.logger.info(
                f"Filtered {total_filtered} rows with State != enabled"
            )

        return filtered_df, details

    def validate_state_columns(
        self, df: pd.DataFrame, column_mapping: Optional[Dict[str, str]] = None
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Validate that State columns exist and contain valid values.

        Args:
            df: DataFrame to validate
            column_mapping: Optional column name mapping

        Returns:
            Tuple of (is_valid, message, details)
        """

        details = {
            "state_columns_found": [],
            "invalid_values": {},
            "missing_columns": [],
        }

        # Get column names
        if column_mapping:
            columns_to_check = [
                column_mapping.get("state", "State"),
                column_mapping.get(
                    "campaign_state", "Campaign State (Informational only)"
                ),
                column_mapping.get(
                    "ad_group_state", "Ad Group State (Informational only)"
                ),
            ]
        else:
            columns_to_check = self.state_columns

        is_valid = True
        messages = []

        for col in columns_to_check:
            if col in df.columns:
                details["state_columns_found"].append(col)
                
                # Check for invalid values
                unique_values = df[col].dropna().str.lower().unique()
                invalid = [v for v in unique_values if v not in self.valid_states]
                
                if invalid:
                    details["invalid_values"][col] = invalid
                    messages.append(f"Invalid values in {col}: {invalid}")
                    is_valid = False
            else:
                details["missing_columns"].append(col)

        if not details["state_columns_found"]:
            return False, "No State columns found", details

        if is_valid:
            return True, "All State columns validated", details
        else:
            return False, "; ".join(messages), details

    def mark_disabled_rows(
        self, df: pd.DataFrame, column_mapping: Optional[Dict[str, str]] = None
    ) -> pd.DataFrame:
        """
        Mark rows that are disabled in any State column.

        Adds a '_is_disabled' column to the DataFrame.

        Args:
            df: DataFrame to process
            column_mapping: Optional column name mapping

        Returns:
            DataFrame with added '_is_disabled' column
        """

        # Get column names
        if column_mapping:
            columns_to_check = [
                column_mapping.get("state", "State"),
                column_mapping.get(
                    "campaign_state", "Campaign State (Informational only)"
                ),
                column_mapping.get(
                    "ad_group_state", "Ad Group State (Informational only)"
                ),
            ]
        else:
            columns_to_check = self.state_columns

        # Initialize disabled mask
        is_disabled = pd.Series(False, index=df.index)

        # Check each State column
        for col in columns_to_check:
            if col in df.columns:
                is_disabled |= df[col].str.lower() != "enabled"

        df["_is_disabled"] = is_disabled

        disabled_count = is_disabled.sum()
        if disabled_count > 0:
            self.logger.info(f"Marked {disabled_count} rows as disabled")

        return df

    def get_state_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Get summary of State values in the DataFrame.

        Args:
            df: DataFrame to analyze

        Returns:
            Dictionary with State value counts
        """

        summary = {
            "total_rows": len(df),
            "state_columns": {},
        }

        for col in self.state_columns:
            if col in df.columns:
                value_counts = df[col].str.lower().value_counts().to_dict()
                summary["state_columns"][col] = value_counts

        return summary