"""Excel writer for output files."""

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
    Writes optimization results to Excel files.
    
    Features:
    - Creates multi-sheet Excel files
    - Applies pink highlighting to error rows
    - Sets column widths for readability
    - Adds headers with formatting
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Pink color for error highlighting
        self.error_fill = PatternFill(
            start_color='FFE4E1',
            end_color='FFE4E1',
            fill_type='solid'
        )
        
        # Header formatting
        self.header_fill = PatternFill(
            start_color='E0E0E0',
            end_color='E0E0E0',
            fill_type='solid'
        )
        
        self.header_font = Font(bold=True)
        
        # Border style
        self.thin_border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
    
    def write_excel(self, sheets_dict: Dict[str, pd.DataFrame], filename: Optional[str] = None) -> BytesIO:
        """
        Write multiple DataFrames to an Excel file.
        
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
            if 'Sheet' in wb.sheetnames:
                wb.remove(wb['Sheet'])
            
            # Add each dataframe as a sheet
            for sheet_name, df in sheets_dict.items():
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
                if hasattr(df, 'attrs') and 'error_rows' in df.attrs:
                    self._highlight_error_rows(ws, df.attrs['error_rows'])
            
            # Save workbook to BytesIO
            wb.save(output)
            output.seek(0)
            
            self.logger.info(f"Successfully created Excel file with {len(sheets_dict)} sheets")
            
        except Exception as e:
            self.logger.error(f"Error creating Excel file: {str(e)}")
            raise
        
        return output
    
    def create_working_file(self, optimization_results: Dict[str, Dict[str, pd.DataFrame]]) -> BytesIO:
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
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        filename = f"Working_File_{timestamp}.xlsx"
        
        self.logger.info(f"Creating Working File: {filename}")
        
        return self.write_excel(all_sheets, filename)
    
    def create_clean_file(self, optimization_results: Dict[str, Dict[str, pd.DataFrame]]) -> BytesIO:
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
    
    def _clean_sheet_name(self, name: str) -> str:
        """
        Clean sheet name to meet Excel requirements.
        
        Excel sheet names must be <= 31 characters and cannot contain: : \ / ? * [ ]
        """
        
        # Remove invalid characters
        invalid_chars = [':', '\\', '/', '?', '*', '[', ']']
        for char in invalid_chars:
            name = name.replace(char, '')
        
        # Truncate to 31 characters
        if len(name) > 31:
            name = name[:31]
        
        return name
    
    def _write_dataframe_to_sheet(self, ws, df: pd.DataFrame):
        """
        Write a DataFrame to an Excel worksheet.
        """
        
        # Write header
        for col_idx, col_name in enumerate(df.columns, 1):
            cell = ws.cell(row=1, column=col_idx)
            cell.value = col_name
            cell.font = self.header_font
            cell.fill = self.header_fill
            cell.border = self.thin_border
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # Write data
        for row_idx, row_data in enumerate(df.values, 2):
            for col_idx, value in enumerate(row_data, 1):
                cell = ws.cell(row=row_idx, column=col_idx)
                
                # Handle different data types
                if pd.isna(value):
                    cell.value = None
                elif isinstance(value, (int, float)):
                    cell.value = value
                    # Format numbers with 2 decimal places for bid values
                    if 'bid' in str(df.columns[col_idx-1]).lower():
                        cell.number_format = '0.00'
                else:
                    cell.value = str(value)
                
                cell.border = self.thin_border
    
    def _format_worksheet(self, ws, df: pd.DataFrame):
        """
        Apply formatting to worksheet.
        """
        
        # Set column widths
        self._set_column_widths(ws, df)
        
        # Freeze header row
        ws.freeze_panes = 'A2'
        
        # Set print settings
        ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
        ws.page_setup.fitToWidth = 1
        ws.page_setup.fitToHeight = False
    
    def _set_column_widths(self, ws, df: pd.DataFrame):
        """
        Set appropriate column widths based on content.
        """
        
        for col_idx, col_name in enumerate(df.columns, 1):
            # Calculate max width needed
            max_width = len(str(col_name))
            
            # Check data in column
            for value in df.iloc[:100][col_name]:  # Check first 100 rows for performance
                if pd.notna(value):
                    max_width = max(max_width, len(str(value)))
            
            # Set width (with min and max limits)
            width = min(max(max_width + 2, 10), 50)
            ws.column_dimensions[ws.cell(row=1, column=col_idx).column_letter].width = width
    
    def _highlight_error_rows(self, ws, error_row_indices: List[int]):
        """
        Highlight rows with errors in pink.
        
        Args:
            ws: Worksheet object
            error_row_indices: List of row indices (0-based from DataFrame)
        """
        
        if not error_row_indices:
            return
        
        # Convert DataFrame indices to Excel row numbers (1-based, +1 for header)
        excel_rows = [idx + 2 for idx in error_row_indices]
        
        for row_num in excel_rows:
            for cell in ws[row_num]:
                cell.fill = self.error_fill
        
        self.logger.info(f"Highlighted {len(error_row_indices)} error rows in pink")
    
    def save_to_file(self, sheets_dict: Dict[str, pd.DataFrame], filepath: str):
        """
        Save Excel file to disk (for testing).
        
        Args:
            sheets_dict: Dictionary mapping sheet names to DataFrames
            filepath: Path where to save the file
        """
        
        excel_bytes = self.write_excel(sheets_dict)
        
        with open(filepath, 'wb') as f:
            f.write(excel_bytes.getvalue())
        
        self.logger.info(f"Saved Excel file to: {filepath}")
    
    def get_file_stats(self, sheets_dict: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        Get statistics about the Excel file to be created.
        """
        
        stats = {
            'num_sheets': len(sheets_dict),
            'total_rows': sum(len(df) for df in sheets_dict.values()),
            'total_columns': sum(len(df.columns) for df in sheets_dict.values()),
            'sheet_names': list(sheets_dict.keys()),
            'estimated_size_mb': self._estimate_file_size(sheets_dict)
        }
        
        return stats
    
    def _estimate_file_size(self, sheets_dict: Dict[str, pd.DataFrame]) -> float:
        """
        Estimate the file size in MB.
        """
        
        # Rough estimation: 50 bytes per cell
        total_cells = sum(len(df) * len(df.columns) for df in sheets_dict.values())
        estimated_bytes = total_cells * 50
        estimated_mb = estimated_bytes / (1024 * 1024)
        
        return round(estimated_mb, 2)
