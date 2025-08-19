"""Bulk file validation utilities."""

import pandas as pd
from typing import Tuple, Dict, Any, List
from config.constants import BULK_REQUIRED_COLUMNS, BULK_SHEET_NAME, MAX_ROWS


class BulkValidator:
    """Validates bulk files and their data for optimization processing."""
    
    def __init__(self):
        self.required_columns = BULK_REQUIRED_COLUMNS
        self.required_sheet = BULK_SHEET_NAME
        
        # Critical columns for Zero Sales optimization
        self.zero_sales_columns = [
            'portfolio', 'units', 'bid', 'clicks', 'campaign',
            'ad group', 'targeting', 'match type'
        ]
    
    def validate_complete(self, df: pd.DataFrame, filename: str = "") -> Tuple[bool, str, Dict[str, Any]]:
        """
        Complete validation of bulk file data.
        
        Returns:
            Tuple of (is_valid, message, validation_details)
        """
        
        validation_results = {
            'structure_valid': False,
            'data_valid': False,
            'row_count': 0,
            'column_count': 0,
            'zero_sales_ready': False,
            'issues': [],
            'warnings': [],
            'column_mapping': {}
        }
        
        if df is None or df.empty:
            validation_results['issues'].append("DataFrame is empty")
            return False, "Bulk file is empty", validation_results
        
        # Basic structure validation
        validation_results['row_count'] = len(df)
        validation_results['column_count'] = len(df.columns)
        
        structure_valid, structure_msg = self._validate_structure(df, filename)
        validation_results['structure_valid'] = structure_valid
        
        if not structure_valid:
            validation_results['issues'].append(structure_msg)
            return False, structure_msg, validation_results
        
        # Data content validation
        data_valid, data_msg, data_details = self._validate_data_content(df)
        validation_results['data_valid'] = data_valid
        validation_results.update(data_details)
        
        if not data_valid:
            validation_results['issues'].append(data_msg)
            return False, data_msg, validation_results
        
        # Zero Sales specific validation
        zero_sales_ready, zero_msg, column_mapping = self._validate_zero_sales_requirements(df)
        validation_results['zero_sales_ready'] = zero_sales_ready
        validation_results['column_mapping'] = column_mapping
        
        if not zero_sales_ready:
            validation_results['warnings'].append(f"Zero Sales optimization may not work: {zero_msg}")
        
        # Success message
        success_msg = f"Bulk file valid: {validation_results['row_count']:,} rows, {validation_results['column_count']} columns"
        
        return True, success_msg, validation_results
    
    def _validate_structure(self, df: pd.DataFrame, filename: str) -> Tuple[bool, str]:
        """Validate basic file structure."""
        
        # Check row count
        if len(df) > MAX_ROWS:
            return False, f"Too many rows: {len(df):,} (max: {MAX_ROWS:,})"
        
        if len(df) == 0:
            return False, "File contains no data rows"
        
        # Check column count (flexible based on file type)
        col_count = len(df.columns)
        
        if filename.lower().endswith('.xlsx'):
            # Excel files should have exactly 48 columns
            if col_count != BULK_REQUIRED_COLUMNS:
                return False, f"Excel bulk file must have exactly {BULK_REQUIRED_COLUMNS} columns (found: {col_count})"
        else:
            # CSV files are more flexible
            if col_count < 20:
                return False, f"Too few columns: {col_count} (expected at least 20)"
            if col_count > 100:
                return False, f"Too many columns: {col_count} (expected at most 100)"
        
        return True, "File structure is valid"
    
    def _validate_data_content(self, df: pd.DataFrame) -> Tuple[bool, str, Dict[str, Any]]:
        """Validate data content quality."""
        
        details = {
            'empty_rows': 0,
            'duplicate_rows': 0,
            'null_percentage': 0.0,
            'issues': [],
            'warnings': []
        }
        
        # Check for completely empty rows
        empty_rows = df.isnull().all(axis=1).sum()
        details['empty_rows'] = empty_rows
        
        if empty_rows > len(df) * 0.1:  # More than 10% empty
            details['warnings'].append(f"Many empty rows: {empty_rows}")
        
        # Check for duplicate rows
        duplicate_rows = df.duplicated().sum()
        details['duplicate_rows'] = duplicate_rows
        
        if duplicate_rows > 0:
            details['warnings'].append(f"Duplicate rows found: {duplicate_rows}")
        
        # Check null percentage
        total_cells = df.size
        null_cells = df.isnull().sum().sum()
        null_percentage = (null_cells / total_cells) * 100 if total_cells > 0 else 0
        details['null_percentage'] = null_percentage
        
        if null_percentage > 50:
            details['issues'].append(f"Too many null values: {null_percentage:.1f}%")
            return False, f"File has too many missing values ({null_percentage:.1f}%)", details
        
        if null_percentage > 20:
            details['warnings'].append(f"High null percentage: {null_percentage:.1f}%")
        
        return True, "Data content is acceptable", details
    
    def _validate_zero_sales_requirements(self, df: pd.DataFrame) -> Tuple[bool, str, Dict[str, str]]:
        """Validate requirements for Zero Sales optimization."""
        
        column_mapping = {}
        missing_columns = []
        
        # Map critical columns (case-insensitive search)
        df_cols_lower = {col.lower(): col for col in df.columns}
        
        for required_col in self.zero_sales_columns:
            mapped_col = None
            
            # Direct match
            if required_col in df_cols_lower:
                mapped_col = df_cols_lower[required_col]
            else:
                # Partial match
                for col_lower, col_original in df_cols_lower.items():
                    if required_col in col_lower or col_lower.startswith(required_col):
                        mapped_col = col_original
                        break
            
            if mapped_col:
                column_mapping[required_col] = mapped_col
            else:
                missing_columns.append(required_col)
        
        # Check critical columns
        critical_missing = []
        for critical_col in ['portfolio', 'units', 'bid']:
            if critical_col not in column_mapping:
                critical_missing.append(critical_col)
        
        if critical_missing:
            return False, f"Missing critical columns: {', '.join(critical_missing)}", column_mapping
        
        # Validate data in critical columns
        if 'portfolio' in column_mapping:
            portfolio_col = column_mapping['portfolio']
            empty_portfolios = df[portfolio_col].isnull().sum()
            if empty_portfolios > len(df) * 0.5:
                return False, f"Too many empty portfolio values: {empty_portfolios}", column_mapping
        
        if 'units' in column_mapping:
            units_col = column_mapping['units']
            try:
                # Try to convert to numeric
                pd.to_numeric(df[units_col], errors='coerce')
            except Exception:
                return False, f"Units column contains non-numeric data", column_mapping
        
        return True, f"Zero Sales requirements met (mapped {len(column_mapping)} columns)", column_mapping
    
    def get_data_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get comprehensive summary of bulk file data."""
        
        if df is None or df.empty:
            return {'empty': True}
        
        summary = {
            'empty': False,
            'rows': len(df),
            'columns': len(df.columns),
            'memory_mb': df.memory_usage(deep=True).sum() / (1024 * 1024),
            'null_percentage': (df.isnull().sum().sum() / df.size) * 100,
            'duplicates': df.duplicated().sum(),
            'column_names': list(df.columns)[:10],  # First 10 columns
            'data_types': df.dtypes.value_counts().to_dict()
        }
        
        # Sample data preview
        try:
            summary['preview'] = df.head(3).to_dict('records')
        except Exception:
            summary['preview'] = []
        
        return summary
    
    def suggest_column_fixes(self, df: pd.DataFrame) -> List[str]:
        """Suggest fixes for common column issues."""
        
        suggestions = []
        
        if df is None or df.empty:
            return suggestions
        
        # Check for columns with all null values
        null_columns = df.columns[df.isnull().all()].tolist()
        if null_columns:
            suggestions.append(f"Remove empty columns: {', '.join(null_columns[:3])}")
        
        # Check for columns with mostly null values
        mostly_null = []
        for col in df.columns:
            null_pct = (df[col].isnull().sum() / len(df)) * 100
            if null_pct > 80:
                mostly_null.append(col)
        
        if mostly_null:
            suggestions.append(f"Consider removing mostly empty columns: {', '.join(mostly_null[:3])}")
        
        # Check for duplicate columns
        duplicate_cols = df.columns[df.columns.duplicated()].tolist()
        if duplicate_cols:
            suggestions.append(f"Remove duplicate column names: {', '.join(duplicate_cols)}")
        
        return suggestions