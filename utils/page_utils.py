"""Utility functions for page management and UI helpers."""

import streamlit as st
from typing import Dict, Any, Optional
import time

def reset_all_state() -> None:
    """Clear all session state except navigation."""
    keys_to_preserve = ['current_page', 'page']
    
    for key in list(st.session_state.keys()):
        if key not in keys_to_preserve:
            del st.session_state[key]

def format_time(seconds: float) -> str:
    """
    Format seconds into MM:SS format.
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted time string
    """
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def format_number(number: int) -> str:
    """
    Format number with comma separators.
    
    Args:
        number: Integer to format
        
    Returns:
        Formatted number string
    """
    return f"{number:,}"

def get_mock_stats() -> Dict[str, Any]:
    """
    Generate mock statistics for demo purposes.
    
    Returns:
        Dictionary with mock statistics
    """
    return {
        'total_rows': 12543,
        'rows_processed': 12543,
        'rows_modified': 3421,
        'rows_with_zero_units': 892,
        'portfolios_processed': 27,
        'portfolios_excluded': 3,
        'avg_bid_change': 0.35,
        'min_bid_applied': 0.02,
        'max_bid_applied': 4.00,
        'processing_time': 10,
        'optimizations_applied': ['Zero Sales'],
        'calculation_errors': 127,
        'warnings': []
    }

def switch_panel(panel_name: str) -> None:
    """
    Switch between UI panels.
    
    Args:
        panel_name: Name of panel to switch to
    """
    valid_panels = ['upload', 'validation', 'output']
    
    if panel_name in valid_panels:
        st.session_state.current_panel = panel_name
        st.rerun()

def initialize_processing_state() -> None:
    """Initialize state for processing simulation."""
    st.session_state.processing_started = True
    st.session_state.processing_status = 'processing'
    st.session_state.processing_start_time = time.time()
    st.session_state.rows_processed = 0
    st.session_state.optimizations_count = 0
    st.session_state.current_panel = 'output'

def complete_processing() -> None:
    """Mark processing as complete."""
    st.session_state.processing_status = 'complete'
    st.session_state.rows_processed = get_mock_stats()['total_rows']
    st.session_state.optimizations_count = 1
    
    # Generate mock output files
    st.session_state.working_file = create_mock_file()
    st.session_state.clean_file = None  # Not available in Phase 1

def create_mock_file() -> bytes:
    """
    Create mock file data for demo.
    
    Returns:
        Mock file as bytes
    """
    # Return empty bytes for now
    # In real implementation, this would be the Excel file
    return b"Mock Excel File Data"

def handle_process_files_click() -> None:
    """Handle Process Files button click."""
    # Initialize processing
    initialize_processing_state()
    
    # Start mock processing animation
    # The progress bar component will handle the animation

def get_panel_title(panel: str) -> str:
    """
    Get formatted title for panel.
    
    Args:
        panel: Panel name
        
    Returns:
        Formatted title string
    """
    titles = {
        'upload': 'UPLOAD FILES',
        'validation': 'DATA VALIDATION',
        'output': 'OUTPUT FILES'
    }
    return titles.get(panel, panel.upper())

def show_processing_metrics() -> None:
    """Display processing metrics in columns."""
    stats = get_mock_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Rows", format_number(stats['total_rows']))
    
    with col2:
        st.metric("Modified", format_number(stats['rows_modified']))
    
    with col3:
        st.metric("Excluded", stats['portfolios_excluded'])
    
    with col4:
        st.metric("Errors", stats['calculation_errors'])

def is_ready_to_process() -> bool:
    """
    Check if all conditions are met for processing.
    
    Returns:
        True if ready to process
    """
    return (
        st.session_state.get('template_uploaded', False) and
        st.session_state.get('bulk_60_uploaded', False) and
        st.session_state.get('validation_passed', False) and
        len(st.session_state.get('selected_optimizations', [])) > 0
    )