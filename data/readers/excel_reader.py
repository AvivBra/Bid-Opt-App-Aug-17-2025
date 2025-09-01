"""Excel file reading utilities."""

import pandas as pd
import io
from typing import Dict, Tuple, Optional
from config.constants import TEMPLATE_REQUIRED_SHEETS, BULK_SHEET_NAME
from .template_reader import TemplateReader


class ExcelReader:
    """Handles reading Excel files for the application."""
    
    def __init__(self):
        self.template_reader = TemplateReader()

    def read_template_file(
        self, file_data: bytes
    ) -> Tuple[bool, str, Optional[Dict[str, pd.DataFrame]]]:
        """
        Read template Excel file and return DataFrames.

        Returns:
            Tuple of (success, message, data_dict)
        """
        try:
            # Read all sheets
            excel_data = pd.read_excel(io.BytesIO(file_data), sheet_name=None)

            # Only require Port Values sheet (Top ASINs and Delete for 60 are optional)
            if "Port Values" not in excel_data:
                return False, "Missing required sheet: Port Values", None

            # Clean and validate Port Values data
            port_values_df = excel_data["Port Values"]
            cleaned_port_values, validation_msg = self._clean_port_values(
                port_values_df
            )

            if not validation_msg.startswith("Success"):
                return False, validation_msg, None

            # Return cleaned data (Top ASINs and Delete for 60 are optional)
            cleaned_data = {
                "Port Values": cleaned_port_values,
                "Top ASINs": excel_data.get(
                    "Top ASINs", pd.DataFrame()
                ),  # Empty DataFrame if not present
                "Delete for 60": excel_data.get(
                    "Delete for 60", pd.DataFrame()
                ),  # Empty DataFrame if not present
            }

            return (
                True,
                f"Template loaded: {len(cleaned_port_values)} portfolios",
                cleaned_data,
            )

        except Exception as e:
            return False, f"Error reading template file: {str(e)}", None

    def read_bulk_file(
        self, file_data: bytes, filename: str = ""
    ) -> Tuple[bool, str, Optional[pd.DataFrame]]:
        """
        Read bulk Excel file and return DataFrame.

        Returns:
            Tuple of (success, message, dataframe)
        """
        try:
            # Determine file type
            is_csv = filename.lower().endswith(".csv")

            if is_csv:
                # Handle CSV files
                try:
                    df = pd.read_csv(io.BytesIO(file_data))
                except UnicodeDecodeError:
                    # Try different encoding
                    df = pd.read_csv(io.BytesIO(file_data), encoding="latin-1")
            else:
                # Handle Excel files - try to find the correct sheet
                excel_data = pd.read_excel(io.BytesIO(file_data), sheet_name=None)

                if BULK_SHEET_NAME in excel_data:
                    df = excel_data[BULK_SHEET_NAME]
                else:
                    # Look for similar sheet names
                    available_sheets = list(excel_data.keys())
                    possible_sheets = [
                        s for s in available_sheets if "campaign" in s.lower()
                    ]

                    if possible_sheets:
                        df = excel_data[possible_sheets[0]]
                        sheet_msg = f"Using sheet '{possible_sheets[0]}' (expected '{BULK_SHEET_NAME}')"
                    else:
                        return (
                            False,
                            f"Sheet '{BULK_SHEET_NAME}' not found. Available: {available_sheets}",
                            None,
                        )

            # Basic validation
            if df.empty:
                return False, "Bulk file is empty", None

            # Check row count
            row_count = len(df)
            if row_count > 500_000:
                return False, f"Too many rows: {row_count:,} (max: 500,000)", None

            return (
                True,
                f"Bulk file loaded: {row_count:,} rows, {len(df.columns)} columns",
                df,
            )

        except Exception as e:
            return False, f"Error reading bulk file: {str(e)}", None

    def _clean_port_values(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, str]:
        """Clean and validate Port Values DataFrame."""

        try:
            # Remove completely empty rows
            df = df.dropna(how="all")

            # Remove instruction/example rows (containing brackets)
            df = df[
                ~df.astype(str).apply(
                    lambda x: x.str.contains(r"\[.*\]", na=False).any(), axis=1
                )
            ]

            # Remove rows with example text
            example_keywords = ["example", "replace", "your portfolio"]
            for keyword in example_keywords:
                df = df[
                    ~df.astype(str).apply(
                        lambda x: x.str.lower().str.contains(keyword, na=False).any(),
                        axis=1,
                    )
                ]

            # Reset index
            df = df.reset_index(drop=True)

            if df.empty:
                return df, "Error: No valid data found after cleaning"

            return df, f"Success: Cleaned {len(df)} portfolios"

        except Exception as e:
            return df, f"Error during cleaning: {str(e)}"
    
    def read_top_asins_template(
        self, file_data: bytes, filename: str = "template.xlsx"
    ) -> Tuple[bool, str, Optional[pd.DataFrame]]:
        """
        Read Top ASINs template file.
        
        Args:
            file_data: File bytes
            filename: Original filename
            
        Returns:
            Tuple of (success, message, template_dataframe)
        """
        try:
            template_df = self.template_reader.read_template(file_data, filename)
            
            if not self.template_reader.validate_top_asins_template(template_df):
                return False, "Template validation failed", None
            
            # Extract and normalize Top ASINs
            clean_asins_df = self.template_reader.extract_top_asins(template_df)
            
            return True, f"Template loaded: {len(clean_asins_df)} ASINs", clean_asins_df
            
        except ValueError as e:
            return False, str(e), None
        except Exception as e:
            return False, f"Error reading template: {str(e)}", None
