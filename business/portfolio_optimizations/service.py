"""Service layer for portfolio optimizations."""

import pandas as pd
from io import BytesIO
from typing import Dict, List, Optional
import logging
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from .constants import HIGHLIGHT_COLOR


class PortfolioOptimizationService:
    """Service for portfolio optimization operations."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def create_output_file(
        self,
        data: Dict[str, pd.DataFrame],
        updated_indices: Dict[str, List[int]]
    ) -> bytes:
        """
        Create an Excel file with highlighted changes.
        
        Args:
            data: Dictionary of sheet name to DataFrame
            updated_indices: Dictionary of sheet name to list of updated row indices
            
        Returns:
            Bytes of the Excel file
        """
        self.logger.info("Creating output file")
        
        # Create BytesIO buffer
        output = BytesIO()
        
        # Write data to Excel
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            for sheet_name, df in data.items():
                # Clean data before writing
                df_clean = self._prepare_dataframe(df)
                
                # Write to Excel
                df_clean.to_excel(writer, sheet_name=sheet_name[:31], index=False)
        
        # Add highlighting
        output.seek(0)
        output = self._add_highlighting(output, updated_indices)
        
        # Get bytes
        output.seek(0)
        result = output.read()
        
        self.logger.info(f"Created output file with {len(data)} sheets")
        return result
    
    def _prepare_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare DataFrame for Excel output.
        
        Args:
            df: DataFrame to prepare
            
        Returns:
            Cleaned DataFrame
        """
        df_clean = df.copy()
        
        # Convert all columns to string to prevent scientific notation
        for col in df_clean.columns:
            if df_clean[col].dtype in ['float64', 'int64']:
                # Check if it's an ID column (contains large numbers)
                if 'ID' in col.upper() or 'id' in col.lower():
                    df_clean[col] = df_clean[col].astype(str).str.replace('.0', '', regex=False)
                else:
                    df_clean[col] = df_clean[col].astype(str)
            elif df_clean[col].dtype == 'object':
                # Clean string columns
                df_clean[col] = df_clean[col].fillna('').astype(str)
        
        # Remove any columns that start with underscore (internal columns)
        cols_to_remove = [col for col in df_clean.columns if col.startswith('_')]
        if cols_to_remove:
            df_clean = df_clean.drop(columns=cols_to_remove)
        
        return df_clean
    
    def _add_highlighting(
        self,
        excel_buffer: BytesIO,
        updated_indices: Dict[str, List[int]]
    ) -> BytesIO:
        """
        Add yellow highlighting to updated rows.
        
        Args:
            excel_buffer: BytesIO containing Excel file
            updated_indices: Dictionary of sheet name to list of updated row indices
            
        Returns:
            BytesIO with highlighting added
        """
        # Load workbook
        wb = load_workbook(excel_buffer)
        
        # Create yellow fill
        yellow_fill = PatternFill(
            start_color=HIGHLIGHT_COLOR,
            end_color=HIGHLIGHT_COLOR,
            fill_type="solid"
        )
        
        # Apply highlighting to each sheet
        for sheet_name, indices in updated_indices.items():
            if not indices:
                continue
            
            # Find matching worksheet (sheet names might be truncated)
            ws = None
            for ws_name in wb.sheetnames:
                if ws_name.startswith(sheet_name[:31]):
                    ws = wb[ws_name]
                    break
            
            if ws is None:
                self.logger.warning(f"Sheet {sheet_name} not found for highlighting")
                continue
            
            # Apply highlighting
            for row_idx in indices:
                # Excel rows are 1-indexed, add 1 for header
                excel_row = row_idx + 2
                
                # Highlight entire row
                for col in range(1, ws.max_column + 1):
                    cell = ws.cell(row=excel_row, column=col)
                    cell.fill = yellow_fill
            
            self.logger.info(f"Highlighted {len(indices)} rows in {sheet_name}")
        
        # Save to new buffer
        output = BytesIO()
        wb.save(output)
        return output
    
    def generate_filename(self, prefix: str = "portfolio_optimized") -> str:
        """
        Generate a filename with timestamp.
        
        Args:
            prefix: Filename prefix
            
        Returns:
            Filename with timestamp
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.xlsx"