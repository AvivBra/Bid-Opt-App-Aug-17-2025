"""CSV file reading utilities."""

import pandas as pd
import io
from typing import Tuple, Optional
from config.constants import MAX_ROWS, BULK_REQUIRED_COLUMNS


class CSVReader:
    """Handles reading CSV files for the application."""
    
    def read_csv_file(self, file_data: bytes, filename: str = "") -> Tuple[bool, str, Optional[pd.DataFrame]]:
        """
        Read CSV file and return DataFrame.
        
        Returns:
            Tuple of (success, message, dataframe)
        """
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            
            df = None
            encoding_used = None
            
            for encoding in encodings:
                try:
                    df = pd.read_csv(io.BytesIO(file_data), encoding=encoding)
                    encoding_used = encoding
                    break
                except (UnicodeDecodeError, UnicodeError):
                    continue
            
            if df is None:
                return False, "Could not decode CSV file with any supported encoding", None
            
            # Basic validation
            if df.empty:
                return False, "CSV file is empty", None
            
            # Check row count
            row_count = len(df)
            if row_count > MAX_ROWS:
                return False, f"Too many rows: {row_count:,} (max: {MAX_ROWS:,})", None
            
            # Clean column names (remove extra spaces, etc.)
            df.columns = df.columns.str.strip()
            
            return True, f"CSV loaded: {row_count:,} rows, {len(df.columns)} columns (encoding: {encoding_used})", df
            
        except Exception as e:
            return False, f"Error reading CSV file: {str(e)}", None
    
    def validate_csv_structure(self, df: pd.DataFrame) -> Tuple[bool, str]:
        """Validate CSV structure for bulk processing."""
        
        if df is None or df.empty:
            return False, "DataFrame is empty"
        
        # Check column count (flexible for CSV)
        col_count = len(df.columns)
        if col_count < 30:  # Minimum expected columns
            return False, f"Too few columns: {col_count} (expected at least 30)"
        
        if col_count > 60:  # Maximum reasonable columns
            return False, f"Too many columns: {col_count} (expected at most 60)"
        
        # Check for critical columns that Zero Sales optimization needs
        required_columns = ['Portfolio', 'Units', 'Bid']
        missing_columns = []
        
        # Case-insensitive search for required columns
        df_cols_lower = [col.lower() for col in df.columns]
        
        for req_col in required_columns:
            if not any(req_col.lower() in col for col in df_cols_lower):
                missing_columns.append(req_col)
        
        if missing_columns:
            return False, f"Missing critical columns for Zero Sales: {', '.join(missing_columns)}"
        
        return True, f"CSV structure valid: {col_count} columns"
    
    def detect_delimiter(self, file_data: bytes, max_lines: int = 5) -> str:
        """Detect the delimiter used in CSV file."""
        
        try:
            # Read first few lines to detect delimiter
            sample = file_data[:1024].decode('utf-8', errors='ignore')
            lines = sample.split('\n')[:max_lines]
            
            # Count potential delimiters
            delimiters = [',', ';', '\t', '|']
            delimiter_counts = {}
            
            for delimiter in delimiters:
                count = sum(line.count(delimiter) for line in lines if line.strip())
                delimiter_counts[delimiter] = count
            
            # Return delimiter with highest count
            if delimiter_counts:
                return max(delimiter_counts.items(), key=lambda x: x[1])[0]
            
            return ','  # Default to comma
            
        except Exception:
            return ','  # Default to comma
    
    def preview_csv(self, file_data: bytes, lines: int = 5) -> Tuple[bool, str, Optional[pd.DataFrame]]:
        """Preview first few lines of CSV file."""
        
        try:
            # Detect delimiter
            delimiter = self.detect_delimiter(file_data)
            
            # Read with detected delimiter
            df = pd.read_csv(
                io.BytesIO(file_data), 
                delimiter=delimiter,
                nrows=lines,
                encoding='utf-8'
            )
            
            return True, f"Preview loaded ({lines} rows)", df
            
        except UnicodeDecodeError:
            try:
                # Try latin-1 encoding
                df = pd.read_csv(
                    io.BytesIO(file_data),
                    delimiter=delimiter,
                    nrows=lines,
                    encoding='latin-1'
                )
                return True, f"Preview loaded ({lines} rows, latin-1 encoding)", df
            except Exception as e:
                return False, f"Error previewing CSV: {str(e)}", None
        
        except Exception as e:
            return False, f"Error previewing CSV: {str(e)}", None