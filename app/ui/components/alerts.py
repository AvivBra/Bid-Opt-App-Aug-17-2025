"""Alert components for displaying messages and notifications."""

import streamlit as st
from typing import Optional, List

def show_validation_alert(alert_type: str, message: str, icon: Optional[str] = None) -> None:
    """
    Display a validation alert message.
    
    Args:
        alert_type: Type of alert ('success', 'error', 'warning', 'info')
        message: Message to display
        icon: Optional icon to prepend to message
    """
    if alert_type == 'success':
        if icon:
            st.success(f"{icon} {message}")
        else:
            st.success(message)
    elif alert_type == 'error':
        if icon:
            st.error(f"{icon} {message}")
        else:
            st.error(message)
    elif alert_type == 'warning':
        if icon:
            st.warning(f"{icon} {message}")
        else:
            st.warning(message)
    elif alert_type == 'info':
        if icon:
            st.info(f"{icon} {message}")
        else:
            st.info(message)

def show_upload_alert(success: bool, filename: str, error: Optional[str] = None) -> None:
    """
    Display an upload status alert.
    
    Args:
        success: Whether upload was successful
        filename: Name of the uploaded file
        error: Optional error message if upload failed
    """
    if success:
        st.success(f"✅ {filename} uploaded successfully")
    else:
        if error:
            st.error(f"❌ Failed to upload {filename}: {error}")
        else:
            st.error(f"❌ Failed to upload {filename}")

def show_processing_alert(status: str, message: Optional[str] = None) -> None:
    """
    Display a processing status alert.
    
    Args:
        status: Processing status ('started', 'complete', 'error')
        message: Optional custom message
    """
    if status == 'started':
        msg = message or "Processing files..."
        st.info(f"⏳ {msg}")
    elif status == 'complete':
        msg = message or "Processing complete!"
        st.success(f"✅ {msg}")
    elif status == 'error':
        msg = message or "Processing failed"
        st.error(f"❌ {msg}")

def show_portfolio_validation_results(
    valid: bool, 
    missing_portfolios: List[str] = None,
    ignored_count: int = 0
) -> None:
    """
    Display portfolio validation results.
    
    Args:
        valid: Whether validation passed
        missing_portfolios: List of missing portfolio names
        ignored_count: Number of ignored portfolios
    """
    if valid:
        if ignored_count > 0:
            st.info(f"ℹ️ {ignored_count} portfolios marked as 'Ignore' will be skipped")
        st.success("✓ All portfolios valid")
    else:
        if missing_portfolios:
            # Show first 5 missing portfolios
            display_list = missing_portfolios[:5]
            if len(missing_portfolios) > 5:
                display_list.append(f"... and {len(missing_portfolios) - 5} more")
            
            st.error(f"Missing portfolios found - Reupload Full Template: {', '.join(display_list)}")

def show_optimization_results(
    total_rows: int,
    modified_rows: int,
    errors: int = 0,
    warnings: List[str] = None
) -> None:
    """
    Display optimization results summary.
    
    Args:
        total_rows: Total number of rows processed
        modified_rows: Number of rows modified
        errors: Number of errors encountered
        warnings: List of warning messages
    """
    # Success message
    st.success(f"✅ Processed {total_rows:,} rows, modified {modified_rows:,} rows")
    
    # Show errors if any
    if errors > 0:
        st.warning(f"⚠️ Please note: {errors} calculation errors in Zero Sales optimization")
    
    # Show warnings if any
    if warnings:
        for warning in warnings:
            st.warning(f"⚠️ {warning}")

def show_file_size_error(max_size_mb: int, actual_size_mb: float) -> None:
    """
    Display file size error message.
    
    Args:
        max_size_mb: Maximum allowed file size in MB
        actual_size_mb: Actual file size in MB
    """
    st.error(f"File exceeds {max_size_mb}MB limit (actual: {actual_size_mb:.1f}MB)")

def show_file_format_error(expected_formats: List[str]) -> None:
    """
    Display file format error message.
    
    Args:
        expected_formats: List of expected file formats
    """
    formats_str = ", ".join(expected_formats)
    st.error(f"File must be one of: {formats_str}")

def show_column_mismatch_error(expected: int, actual: int) -> None:
    """
    Display column count mismatch error.
    
    Args:
        expected: Expected number of columns
        actual: Actual number of columns
    """
    st.error(f"Column count mismatch. Expected: {expected}, Found: {actual}")

def show_download_ready(file_type: str = "Working File") -> None:
    """
    Display download ready notification.
    
    Args:
        file_type: Type of file ready for download
    """
    st.success(f"📥 {file_type} is ready for download")

def clear_alerts() -> None:
    """Clear all alerts from the current container."""
    # This is handled by Streamlit's rerun mechanism
    pass

class AlertManager:
    """Manager class for handling multiple alerts."""
    
    def __init__(self):
        """Initialize alert manager."""
        self.alerts = []
    
    def add_alert(self, alert_type: str, message: str):
        """Add an alert to the queue."""
        self.alerts.append({"type": alert_type, "message": message})
    
    def display_all(self):
        """Display all queued alerts."""
        for alert in self.alerts:
            show_validation_alert(alert["type"], alert["message"])
    
    def clear(self):
        """Clear all alerts."""
        self.alerts = []
    
    def has_errors(self) -> bool:
        """Check if there are any error alerts."""
        return any(alert["type"] == "error" for alert in self.alerts)
    
    def has_warnings(self) -> bool:
        """Check if there are any warning alerts."""
        return any(alert["type"] == "warning" for alert in self.alerts)