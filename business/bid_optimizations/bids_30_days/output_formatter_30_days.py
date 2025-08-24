"""Output formatter for Bids 30 Days optimization."""

import pandas as pd
from typing import Dict, List, Tuple, Any, Optional
import logging
from io import BytesIO

from business.processors.excel_base_formatter import ExcelBaseFormatter
from .constants import HELPER_COLUMNS


class Bids30DaysOutputFormatter(ExcelBaseFormatter):
    """
    Formats output specifically for Bids 30 Days optimization.
    Inherits all formatting from ExcelBaseFormatter.
    """

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("optimization.bids_30_days.formatter")

        # Column order for output (48 original + 10 helper = 58 total)
        self.helper_columns = HELPER_COLUMNS

        # Columns that should be highlighted in blue
        self.participating_columns = [
            "Portfolio Name (Informational only)",
            "Units",
            "Clicks",
            "Campaign Name (Informational only)",
            "Campaign ID",
            "Match Type",
            "Product Targeting Expression",
            "Percentage",
            "Conversion Rate",
            "Bid",
        ] + self.helper_columns

    def format_sheets(
        self, sheets_dict: Dict[str, pd.DataFrame], original_columns: List[str]
    ) -> Dict[str, pd.DataFrame]:
        """
        Format sheets for Bids 30 Days output.

        Handles:
        - Targeting sheet (58 columns with helpers)
        - Bidding Adjustment sheet (48 columns, no helpers)
        - For Harvesting sheet (58 columns with helpers)

        Args:
            sheets_dict: Dictionary of DataFrames from processor
            original_columns: Original 48 columns from bulk file

        Returns:
            Formatted sheets dictionary
        """
        formatted_sheets = {}

        for sheet_name, df in sheets_dict.items():
            if sheet_name in ["Targeting", "For Harvesting"]:
                # These sheets get helper columns
                formatted_df = self._format_with_helpers(df, original_columns)
            elif sheet_name == "Bidding Adjustment":
                # This sheet keeps only original columns
                formatted_df = self._format_without_helpers(df, original_columns)
            else:
                # Any other sheet - keep as is
                formatted_df = df.copy()

            formatted_sheets[sheet_name] = formatted_df

        return formatted_sheets

    def _format_with_helpers(
        self, df: pd.DataFrame, original_columns: List[str]
    ) -> pd.DataFrame:
        """
        Format sheet with helper columns using base class method.
        """
        # Ensure all helper columns exist
        for col in self.helper_columns:
            if col not in df.columns:
                df[col] = ""

        # Ensure all original columns exist
        for col in original_columns:
            if col not in df.columns:
                df[col] = ""

        # Use base class method to arrange columns
        formatted_df = self.arrange_columns_with_helpers(
            df, original_columns, self.helper_columns
        )

        # Mark rows for highlighting
        formatted_df = self.mark_rows_for_highlighting(formatted_df)

        return formatted_df

    def _format_without_helpers(
        self, df: pd.DataFrame, original_columns: List[str]
    ) -> pd.DataFrame:
        """
        Format sheet without helper columns (48 columns only).
        """
        # Ensure all original columns exist
        for col in original_columns:
            if col not in df.columns:
                df[col] = ""

        # Return with original column order
        return df[original_columns].copy()

    def mark_rows_for_highlighting(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Override: Mark rows that need pink highlighting.

        Conditions for pink:
        - Conversion Rate < 0.08
        - Bid < 0.02 or Bid > 1.25
        - Bid contains error message
        """
        # Create a copy to avoid SettingWithCopyWarning
        df = df.copy()

        # Initialize highlight column if not exists
        if "_needs_highlight" not in df.columns:
            df["_needs_highlight"] = False

        # Check Conversion Rate
        if "Conversion Rate" in df.columns:
            cvr_mask = pd.to_numeric(df["Conversion Rate"], errors="coerce") < 0.08
            df.loc[cvr_mask, "_needs_highlight"] = True

        # Check Bid range
        if "Bid" in df.columns:
            bid_numeric = pd.to_numeric(df["Bid"], errors="coerce")
            bid_out_of_range = (bid_numeric < 0.02) | (bid_numeric > 1.25)
            df.loc[bid_out_of_range, "_needs_highlight"] = True

            # Check for error messages in Bid
            bid_errors = (
                df["Bid"]
                .astype(str)
                .str.contains("Error|Null|Missing", case=False, na=False)
            )
            df.loc[bid_errors, "_needs_highlight"] = True

        return df

    def get_blue_header_columns(self) -> List[str]:
        """
        Override: Return list of columns that should have blue headers.
        """
        return self.participating_columns

    def create_excel_file(
        self,
        sheets_dict: Dict[str, pd.DataFrame],
        highlight_rows: bool = True,
        highlight_headers: bool = True,
    ) -> BytesIO:
        """
        Create Excel file with formatting using base class.
        """
        # Use base class method with our blue columns
        return self.write_to_excel_with_formatting(
            sheets_dict,
            highlight_errors=highlight_rows,
            highlight_headers=highlight_headers,
            blue_header_columns=self.get_blue_header_columns(),
        )

    def create_clean_file(self, sheets_dict: Dict[str, pd.DataFrame]) -> BytesIO:
        """
        Create clean file with minimal columns.
        """
        clean_sheets = self._create_clean_sheets(sheets_dict)

        # Use base class method without highlighting
        return self.write_to_excel_with_formatting(
            clean_sheets, highlight_errors=False, highlight_headers=False
        )

    def _create_clean_sheets(
        self, sheets: Dict[str, pd.DataFrame]
    ) -> Dict[str, pd.DataFrame]:
        """
        Create clean sheets with minimal columns.
        """
        clean_sheets = {}

        # Essential columns for clean file
        essential_columns = [
            "Entity",
            "Campaign ID",
            "Ad Group ID",
            "Portfolio Name (Informational only)",
            "Campaign Name (Informational only)",
            "Ad Group Name",
            "Keyword ID",
            "Keyword Text",
            "Match Type",
            "Product Targeting ID",
            "Product Targeting Expression",
            "Bid",
            "Operation",
        ]

        for sheet_name, df in sheets.items():
            if sheet_name == "For Harvesting":
                # For Harvesting keeps more columns
                analysis_columns = essential_columns + [
                    "Units",
                    "Clicks",
                    "Impressions",
                    "Spend",
                    "Sales",
                    "Orders",
                    "Conversion Rate",
                    "ACOS",
                    "CPC",
                ]
                columns_to_keep = [col for col in analysis_columns if col in df.columns]
            else:
                columns_to_keep = [
                    col for col in essential_columns if col in df.columns
                ]

            clean_sheets[sheet_name] = df[columns_to_keep].copy()

        return clean_sheets

    def get_summary_stats(self, sheets_dict: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        Get summary statistics for the output.
        """
        stats = {"total_sheets": len(sheets_dict), "sheets": {}}

        for sheet_name, df in sheets_dict.items():
            sheet_stats = {"rows": len(df), "columns": len(df.columns)}

            # Count highlighted rows
            if "_needs_highlight" in df.columns:
                sheet_stats["highlighted_rows"] = df["_needs_highlight"].sum()

            # Count For Harvesting specific stats
            if sheet_name == "For Harvesting":
                sheet_stats["null_target_cpa"] = len(df)

            # Count error rows in Targeting
            if sheet_name == "Targeting" and "Bid" in df.columns:
                bid_errors = (
                    df["Bid"]
                    .astype(str)
                    .str.contains("Error|Null|Missing", case=False, na=False)
                    .sum()
                )
                sheet_stats["bid_errors"] = bid_errors

                # Count CVR issues
                if "Conversion Rate" in df.columns:
                    cvr_low = (
                        pd.to_numeric(df["Conversion Rate"], errors="coerce") < 0.08
                    ).sum()
                    sheet_stats["cvr_below_threshold"] = cvr_low

            stats["sheets"][sheet_name] = sheet_stats

        return stats
