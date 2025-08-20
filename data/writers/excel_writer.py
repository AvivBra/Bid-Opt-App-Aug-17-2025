"""Excel writer for output files - UPDATED for proper formatting."""

import pandas as pd
from io import BytesIO
from typing import Dict, Optional, List, Any
import logging
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows
from datetime import datetime


class ExcelWriter:
    """
    Writes optimization results to Excel files with proper formatting.

    Features:
    - Creates multi-sheet Excel files
    - Applies pink highlighting to error rows
    - Formats numbers as text for long IDs
    - Centers all cell values
    - No borders on cells
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # Pink color for error highlighting
        self.error_fill = PatternFill(
            start_color="FFE4E1", end_color="FFE4E1", fill_type="solid"
        )

        # Header formatting (optional - you can remove if not wanted)
        self.header_fill = PatternFill(
            start_color="E0E0E0", end_color="E0E0E0", fill_type="solid"
        )

        self.header_font = Font(bold=True)

        # Center alignment for all cells
        self.center_alignment = Alignment(horizontal="center", vertical="center")

        # No borders
        self.no_border = Border()

    def write_excel(
        self, sheets_dict: Dict[str, pd.DataFrame], filename: Optional[str] = None
    ) -> BytesIO:
        """
        Write multiple DataFrames to an Excel file with proper formatting.

        Args:
            sheets_dict: Dictionary mapping sheet names to DataFrames
            filename: Optional filename (for logging purposes)

        Returns:
            BytesIO object containing the Excel file
        """

        output = BytesIO()

        try:
            # Create workbook
            wb = Workbook()

            # Remove default sheet
            if "Sheet" in wb.sheetnames:
                wb.remove(wb["Sheet"])

            # Add each dataframe as a sheet
            for sheet_name, df in sheets_dict.items():
                if not isinstance(df, pd.DataFrame):
                    self.logger.warning(f"Skipping {sheet_name}: not a DataFrame")
                    continue

                if df.empty:
                    self.logger.warning(f"Skipping empty sheet: {sheet_name}")
                    continue

                # Create worksheet
                ws = wb.create_sheet(title=self._clean_sheet_name(sheet_name))

                # Write dataframe to worksheet
                self._write_dataframe_to_sheet(ws, df)

                # Apply formatting
                self._format_worksheet(ws, df)

                # Highlight error rows if present
                if hasattr(df, "attrs") and "error_rows" in df.attrs:
                    self._highlight_error_rows(ws, df.attrs["error_rows"])

            # Save workbook to BytesIO
            wb.save(output)
            output.seek(0)

            self.logger.info(
                f"Successfully created Excel file with {len(sheets_dict)} sheets"
            )

        except Exception as e:
            self.logger.error(f"Error creating Excel file: {str(e)}")
            raise

        return output

    def _clean_sheet_name(self, name: str) -> str:
        """
        Clean sheet name to meet Excel requirements.

        Excel sheet names must be <= 31 characters and cannot contain: : \ / ? * [ ]
        """

        # Remove invalid characters
        invalid_chars = [":", "\\", "/", "?", "*", "[", "]"]
        for char in invalid_chars:
            name = name.replace(char, "")

        # Truncate to 31 characters
        if len(name) > 31:
            name = name[:31]

        return name

    def _write_dataframe_to_sheet(self, ws, df: pd.DataFrame):
        """
        Write a DataFrame to an Excel worksheet.
        """

        # Write headers
        for col_idx, col_name in enumerate(df.columns, 1):
            cell = ws.cell(row=1, column=col_idx, value=str(col_name))
            cell.font = self.header_font
            cell.alignment = self.center_alignment
            cell.border = self.no_border

        # Write data
        for row_idx, row in enumerate(df.itertuples(index=False), 2):
            for col_idx, value in enumerate(row, 1):
                cell = ws.cell(row=row_idx, column=col_idx)

                # Convert value to appropriate type
                if pd.isna(value):
                    cell.value = ""
                elif isinstance(value, (int, float)):
                    # Check if it's a long ID (more than 10 digits)
                    if abs(value) > 9999999999:  # More than 10 digits
                        # Format as text to prevent scientific notation
                        cell.value = str(int(value))
                        cell.number_format = "@"  # Text format
                    else:
                        cell.value = value
                        # Regular number format with 3 decimal places for bid values
                        col_name = df.columns[col_idx - 1]
                        if "bid" in col_name.lower() or col_name in [
                            "calc1",
                            "calc2",
                            "Target CPA",
                            "Base Bid",
                            "Adj. CPA",
                        ]:
                            cell.number_format = "0.000"
                else:
                    cell.value = str(value)

                # Apply center alignment and no border
                cell.alignment = self.center_alignment
                cell.border = self.no_border

    def _format_worksheet(self, ws, df: pd.DataFrame):
        """
        Apply formatting to the worksheet.
        """

        # Auto-adjust column widths
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter

            for cell in column:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass

            adjusted_width = min(max_length + 2, 50)  # Cap at 50 characters
            ws.column_dimensions[column_letter].width = adjusted_width

        # Special handling for ID columns - make them wider
        for col_idx, col_name in enumerate(df.columns, 1):
            if (
                "id" in col_name.lower()
                or "campaign" in col_name.lower()
                or "group" in col_name.lower()
            ):
                column_letter = ws.cell(row=1, column=col_idx).column_letter
                ws.column_dimensions[column_letter].width = max(
                    20, ws.column_dimensions[column_letter].width
                )

        # Ensure Old Bid column is properly positioned and formatted
        if "Old Bid" in df.columns and "Bid" in df.columns:
            old_bid_idx = df.columns.get_loc("Old Bid") + 1
            bid_idx = df.columns.get_loc("Bid") + 1

            # The processor should have already arranged columns correctly
            # Just ensure formatting is applied
            for row in range(2, ws.max_row + 1):
                old_bid_cell = ws.cell(row=row, column=old_bid_idx)
                bid_cell = ws.cell(row=row, column=bid_idx)

                # Both should have same number format
                old_bid_cell.number_format = "0.000"
                bid_cell.number_format = "0.000"

    def _highlight_error_rows(self, ws, error_indices: List[int]):
        """
        Highlight rows with errors in pink.

        Args:
            ws: Worksheet object
            error_indices: List of row indices to highlight (0-based from DataFrame)
        """

        for idx in error_indices:
            # Convert DataFrame index to Excel row (add 2: +1 for 0-based to 1-based, +1 for header)
            excel_row = idx + 2

            # Apply pink fill to entire row
            for col in range(1, ws.max_column + 1):
                cell = ws.cell(row=excel_row, column=col)
                cell.fill = self.error_fill

    def create_working_file(
        self, optimization_results: Dict[str, Dict[str, pd.DataFrame]]
    ) -> BytesIO:
        """
        Create a Working File with all optimization results.

        Args:
            optimization_results: Nested dict of optimization name -> sheet name -> DataFrame

        Returns:
            BytesIO object containing the Working File
        """

        # Flatten the nested dictionary
        all_sheets = {}

        for opt_name, sheets in optimization_results.items():
            for sheet_name, df in sheets.items():
                # Use sheet name directly if it already includes optimization name
                if opt_name.lower() in sheet_name.lower():
                    final_sheet_name = sheet_name
                else:
                    final_sheet_name = f"{sheet_name} - {opt_name}"

                all_sheets[final_sheet_name] = df

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"Working_File_{timestamp}.xlsx"

        self.logger.info(f"Creating Working File: {filename}")

        return self.write_excel(all_sheets, filename)

    def create_clean_file(
        self, optimization_results: Dict[str, Dict[str, pd.DataFrame]]
    ) -> BytesIO:
        """
        Create a Clean File (currently same as Working File).

        In future phases, this will remove helper columns.

        Args:
            optimization_results: Nested dict of optimization name -> sheet name -> DataFrame

        Returns:
            BytesIO object containing the Clean File
        """

        # For now, Clean File is same as Working File
        # In future, will remove helper columns here

        self.logger.info("Creating Clean File (currently same as Working File)")

        return self.create_working_file(optimization_results)
