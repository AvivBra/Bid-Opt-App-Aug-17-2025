"""Excel file reading utilities."""

import pandas as pd
import io
from typing import Dict, Tuple, Optional
from config.constants import TEMPLATE_REQUIRED_SHEETS, BULK_SHEET_NAME


class ExcelReader:
    """Handles reading Excel files for the application."""
    
    def read_template_file(self, file_data: bytes) -> Tuple[bool, str, Optional[Dict[str, pd.DataFrame]]]:
        """
        Read template Excel file and return DataFrames.
        
        Returns:
            Tuple of (success, message, data_dict)
        """
        try:
            # Read all sheets
            excel_data = pd.read_excel(io.BytesIO(file_data), sheet_name=None)
            
            # Validate required sheets
            missing_sheets = []
            for sheet in TEMPLATE_REQUIRED_SHEETS:
                if sheet not in excel_data:
                    missing_sheets.append(sheet)
            
            if missing_sheets:
                return False, f"Missing required sheets: {', '.join(missing_sheets)}", None
            
            # Clean and validate Port Values data
            port_values_df = excel_data['Port Values']
            cleaned_port_values, validation_msg = self._clean_port_values(port_values_df)
            
            if not validation_msg.startswith("Success"):
                return False, validation_msg, None
            
            # Return cleaned data
            cleaned_data = {
                'Port Values': cleaned_port_values,
                'Top ASINs': excel_data.get('Top ASINs', pd.DataFrame())
            }
            
            return True, f"Template loaded: {len(cleaned_port_values)} portfolios", cleaned_data
            
        except Exception as e:
            return False, f"Error reading template file: {str(e)}", None
    
    def read_bulk_file(self, file_data: bytes, filename: str = "") -> Tuple[bool, str, Optional[pd.DataFrame]]:
        """
        Read bulk Excel file and return DataFrame.
        
        Returns:
            Tuple of (success, message, dataframe)
        """
        try:
            # Determine file type
            is_csv = filename.lower().endswith('.csv')
            
            if is_csv:
                # Handle CSV files
                try:
                    df = pd.read_csv(io.BytesIO(file_data))
                except UnicodeDecodeError:
                    # Try different encoding
                    df = pd.read_csv(io.BytesIO(file_data), encoding='latin-1')
            else:
                # Handle Excel files - try to find the correct sheet
                excel_data = pd.read_excel(io.BytesIO(file_data), sheet_name=None)
                
                if BULK_SHEET_NAME in excel_data:
                    df = excel_data[BULK_SHEET_NAME]
                else:
                    # Look for similar sheet names
                    available_sheets = list(excel_data.keys())
                    possible_sheets = [s for s in available_sheets if 'campaign' in s.lower()]
                    
                    if possible_sheets:
                        df = excel_data[possible_sheets[0]]
                        sheet_msg = f"Using sheet '{possible_sheets[0]}' (expected '{BULK_SHEET_NAME}')"
                    else:
                        return False, f"Sheet '{BULK_SHEET_NAME}' not found. Available: {available_sheets}", None
            
            # Basic validation
            if df.empty:
                return False, "Bulk file is empty", None
            
            # Check row count
            row_count = len(df)
            if row_count > 500_000:
                return False, f"Too many rows: {row_count:,} (max: 500,000)", None
            
            return True, f"Bulk file loaded: {row_count:,} rows, {len(df.columns)} columns", df
            
        except Exception as e:
            return False, f"Error reading bulk file: {str(e)}", None
    
    def _clean_port_values(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, str]:
        """Clean and validate Port Values DataFrame."""
        
        try:
            # Remove completely empty rows
            df = df.dropna(how='all')
            
            # Remove instruction/example rows (containing brackets)
            df = df[~df.astype(str).apply(lambda x: x.str.contains(r'\[.*\]', na=False)).any(axis=1)]
            
            # Required columns
            required_cols = ['Portfolio Name', 'Base Bid', 'Target CPA']
            
            # Check if required columns exist
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                return df, f"Missing columns: {', '.join(missing_cols)}"
            
            # Clean Portfolio Name column
            df['Portfolio Name'] = df['Portfolio Name'].astype(str).str.strip()
            df = df[df['Portfolio Name'] != '']  # Remove empty portfolio names
            df = df[df['Portfolio Name'] != 'nan']  # Remove NaN values converted to string
            
            # Check for duplicates
            duplicates = df[df['Portfolio Name'].duplicated()]
            if not duplicates.empty:
                dup_names = duplicates['Portfolio Name'].tolist()
                return df, f"Duplicate portfolio names found: {', '.join(dup_names)}"
            
            # Clean Base Bid column
            df['Base Bid'] = df['Base Bid'].astype(str).str.strip()
            
            # Clean Target CPA column (can be empty)
            df['Target CPA'] = df['Target CPA'].astype(str).str.strip()
            df['Target CPA'] = df['Target CPA'].replace(['nan', ''], '')
            
            # Validate Base Bid values
            for idx, base_bid in df['Base Bid'].items():
                if base_bid.lower() == 'ignore':
                    continue  # 'Ignore' is valid
                
                try:
                    bid_value = float(base_bid)
                    if not (0.02 <= bid_value <= 4.0):
                        return df, f"Base Bid out of range (0.02-4.0): {bid_value} in row {idx+1}"
                except ValueError:
                    return df, f"Invalid Base Bid value: '{base_bid}' in row {idx+1}"
            
            # Validate Target CPA values (optional)
            for idx, target_cpa in df['Target CPA'].items():
                if target_cpa == '' or pd.isna(target_cpa):
                    continue  # Empty is valid
                
                try:
                    cpa_value = float(target_cpa)
                    if not (0.01 <= cpa_value <= 4.0):
                        return df, f"Target CPA out of range (0.01-4.0): {cpa_value} in row {idx+1}"
                except ValueError:
                    return df, f"Invalid Target CPA value: '{target_cpa}' in row {idx+1}"
            
            return df, f"Success: {len(df)} valid portfolios loaded"
            
        except Exception as e:
            return df, f"Error cleaning Port Values: {str(e)}"