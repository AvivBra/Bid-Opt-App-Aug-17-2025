"""File utility functions."""

import os
import pandas as pd
from typing import Optional, Tuple
from config.constants import MAX_TEMPLATE_SIZE_MB, MAX_BULK_SIZE_MB


def get_file_size_mb(file) -> float:
    """Get file size in MB from uploaded file object."""
    if hasattr(file, 'size'):
        return file.size / (1024 * 1024)
    return 0.0


def validate_file_size(file, is_template: bool = True) -> Tuple[bool, str]:
    """Validate uploaded file size against limits."""
    size_mb = get_file_size_mb(file)
    max_size = MAX_TEMPLATE_SIZE_MB if is_template else MAX_BULK_SIZE_MB
    file_type = "Template" if is_template else "Bulk"
    
    if size_mb > max_size:
        return False, f"{file_type} file too large: {size_mb:.1f}MB (max: {max_size}MB)"
    
    return True, f"{file_type} file size: {size_mb:.1f}MB"


def validate_file_extension(filename: str, allowed_extensions: list) -> Tuple[bool, str]:
    """Validate file has allowed extension."""
    if not filename:
        return False, "No filename provided"
    
    file_ext = os.path.splitext(filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        allowed_str = ", ".join(allowed_extensions)
        return False, f"Invalid file type: {file_ext}. Allowed: {allowed_str}"
    
    return True, f"Valid file type: {file_ext}"


def safe_filename(filename: str) -> str:
    """Create safe filename by removing/replacing problematic characters."""
    if not filename:
        return "unnamed_file"
    
    # Remove path components
    filename = os.path.basename(filename)
    
    # Replace problematic characters
    problematic_chars = ['<', '>', ':', '"', '|', '?', '*', '/', '\\']
    for char in problematic_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    
    # Ensure not empty
    if not filename:
        return "unnamed_file"
    
    return filename


def get_dataframe_info(df: pd.DataFrame) -> dict:
    """Get basic information about a DataFrame."""
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "memory_mb": df.memory_usage(deep=True).sum() / (1024 * 1024),
        "has_nulls": df.isnull().any().any(),
        "column_names": list(df.columns)
    }


def estimate_processing_time(num_rows: int) -> int:
    """Estimate processing time in seconds based on row count."""
    if num_rows <= 10_000:
        return min(120, max(5, num_rows // 100))
    elif num_rows <= 100_000:
        return min(120, max(30, num_rows // 1000))
    else:
        return min(300, max(60, num_rows // 2000))