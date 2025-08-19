"""Session state management for Streamlit application."""

import streamlit as st
from typing import Any, Optional
import pandas as pd


class SessionManager:
    """Manages Streamlit session state and data persistence."""
    
    def initialize(self):
        """Initialize session state with default values."""
        
        # Navigation state
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'Bid Optimizer'
        
        # File upload state
        if 'template_uploaded' not in st.session_state:
            st.session_state.template_uploaded = False
        if 'bulk_60_uploaded' not in st.session_state:
            st.session_state.bulk_60_uploaded = False
        if 'bulk_7_uploaded' not in st.session_state:
            st.session_state.bulk_7_uploaded = False
        if 'bulk_30_uploaded' not in st.session_state:
            st.session_state.bulk_30_uploaded = False
        
        # File data storage (in memory only)
        if 'template_data' not in st.session_state:
            st.session_state.template_data = None
        if 'bulk_60_data' not in st.session_state:
            st.session_state.bulk_60_data = None
        if 'bulk_7_data' not in st.session_state:
            st.session_state.bulk_7_data = None
        if 'bulk_30_data' not in st.session_state:
            st.session_state.bulk_30_data = None
            
        # File metadata
        if 'template_info' not in st.session_state:
            st.session_state.template_info = {}
        if 'bulk_60_info' not in st.session_state:
            st.session_state.bulk_60_info = {}
        if 'bulk_7_info' not in st.session_state:
            st.session_state.bulk_7_info = {}
        if 'bulk_30_info' not in st.session_state:
            st.session_state.bulk_30_info = {}
        
        # Validation state
        if 'validation_complete' not in st.session_state:
            st.session_state.validation_complete = False
        if 'validation_results' not in st.session_state:
            st.session_state.validation_results = {}
        
        # Optimization selection
        if 'selected_optimizations' not in st.session_state:
            st.session_state.selected_optimizations = ['zero_sales']  # Only Zero Sales active
        
        # Processing state
        if 'processing_active' not in st.session_state:
            st.session_state.processing_active = False
        if 'processing_progress' not in st.session_state:
            st.session_state.processing_progress = 0.0
        if 'processing_message' not in st.session_state:
            st.session_state.processing_message = ""
        
        # Output state
        if 'output_ready' not in st.session_state:
            st.session_state.output_ready = False
        if 'working_file_data' not in st.session_state:
            st.session_state.working_file_data = None
        if 'clean_file_data' not in st.session_state:
            st.session_state.clean_file_data = None
    
    def clear_session(self):
        """Clear all session data (reset functionality)."""
        keys_to_keep = ['current_page']  # Keep navigation state
        
        for key in list(st.session_state.keys()):
            if key not in keys_to_keep:
                del st.session_state[key]
        
        # Reinitialize
        self.initialize()
    
    def get_value(self, key: str, default: Any = None) -> Any:
        """Get value from session state."""
        return st.session_state.get(key, default)
    
    def set_value(self, key: str, value: Any):
        """Set value in session state."""
        st.session_state[key] = value
    
    def has_required_files(self) -> bool:
        """Check if required files are uploaded."""
        return (st.session_state.template_uploaded and 
                st.session_state.bulk_60_uploaded)
    
    def get_file_status(self) -> dict:
        """Get status of all uploaded files."""
        return {
            'template': {
                'uploaded': st.session_state.template_uploaded,
                'info': st.session_state.template_info
            },
            'bulk_60': {
                'uploaded': st.session_state.bulk_60_uploaded,
                'info': st.session_state.bulk_60_info
            },
            'bulk_7': {
                'uploaded': st.session_state.bulk_7_uploaded,
                'info': st.session_state.bulk_7_info
            },
            'bulk_30': {
                'uploaded': st.session_state.bulk_30_uploaded,
                'info': st.session_state.bulk_30_info
            }
        }
    
    def get_processing_state(self) -> dict:
        """Get current processing state."""
        return {
            'active': st.session_state.processing_active,
            'progress': st.session_state.processing_progress,
            'message': st.session_state.processing_message,
            'output_ready': st.session_state.output_ready
        }