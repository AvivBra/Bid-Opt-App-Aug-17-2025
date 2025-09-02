"""Campaign Optimizer 1 state management."""

import streamlit as st
import pandas as pd
from typing import Dict, List, Optional, Any
from io import BytesIO
import time


class CampaignOptimizer1State:
    """Manages Campaign Optimizer 1 state in session."""

    def __init__(self):
        """Initialize Campaign Optimizer 1 state manager."""
        self.init()

    def init(self) -> None:
        """Initialize Campaign Optimizer 1 specific state variables."""
        if "campaign_optimizer_1_state_initialized" not in st.session_state:
            # File storage
            st.session_state.campaign_optimizer_1_file = None
            st.session_state.campaign_optimizer_1_df = None

            # Upload status
            st.session_state.campaign_optimizer_1_uploaded = False

            # Validation state
            st.session_state.campaign_optimizer_1_validation_passed = False
            st.session_state.campaign_optimizer_1_validation_result = None
            st.session_state.campaign_optimizer_1_validation_errors = []

            # Processing state
            st.session_state.campaign_optimizer_1_processing_started = False
            st.session_state.campaign_optimizer_1_processing_status = None  # None, 'processing', 'complete', 'error'
            st.session_state.campaign_optimizer_1_processing_start_time = None
            st.session_state.campaign_optimizer_1_processing_error = None

            # Progress tracking
            st.session_state.campaign_optimizer_1_rows_processed = 0
            st.session_state.campaign_optimizer_1_campaigns_updated = 0
            st.session_state.campaign_optimizer_1_progress_value = 0.0

            # Checkbox state
            st.session_state.seven_days_budgets_selected = False

            # Results storage
            st.session_state.campaign_optimizer_1_output_file = None
            st.session_state.campaign_optimizer_1_processing_summary = None
            
            # Mark as initialized
            st.session_state.campaign_optimizer_1_state_initialized = True

    # File management methods
    def set_input_file(self, file_data: bytes, filename: str = None):
        """Store uploaded file data."""
        st.session_state.campaign_optimizer_1_file = file_data
        st.session_state.campaign_optimizer_1_uploaded = True

    def get_input_file(self) -> Optional[bytes]:
        """Get stored file data."""
        return st.session_state.campaign_optimizer_1_file

    def clear_input_file(self):
        """Clear stored file data."""
        st.session_state.campaign_optimizer_1_file = None
        st.session_state.campaign_optimizer_1_df = None
        st.session_state.campaign_optimizer_1_uploaded = False
        self.clear_validation()
        self.clear_processing()

    # Checkbox state methods
    def set_seven_days_budgets_selected(self, selected: bool):
        """Set 7 Days Budgets checkbox state."""
        st.session_state.seven_days_budgets_selected = selected

    def is_seven_days_budgets_selected(self) -> bool:
        """Check if 7 Days Budgets checkbox is selected."""
        return st.session_state.seven_days_budgets_selected

    # Validation methods
    def set_validation_result(self, passed: bool, errors: List[str] = None):
        """Set validation results."""
        st.session_state.campaign_optimizer_1_validation_passed = passed
        st.session_state.campaign_optimizer_1_validation_errors = errors or []

    def is_validation_passed(self) -> bool:
        """Check if validation passed."""
        return st.session_state.campaign_optimizer_1_validation_passed

    def get_validation_errors(self) -> List[str]:
        """Get validation errors."""
        return st.session_state.campaign_optimizer_1_validation_errors

    def clear_validation(self):
        """Clear validation state."""
        st.session_state.campaign_optimizer_1_validation_passed = False
        st.session_state.campaign_optimizer_1_validation_errors = []

    # Processing methods
    def start_processing(self):
        """Mark processing as started."""
        st.session_state.campaign_optimizer_1_processing_started = True
        st.session_state.campaign_optimizer_1_processing_status = 'processing'
        st.session_state.campaign_optimizer_1_processing_start_time = time.time()
        st.session_state.campaign_optimizer_1_processing_error = None

    def complete_processing(self, output_file: bytes, summary: Dict[str, Any]):
        """Mark processing as complete."""
        st.session_state.campaign_optimizer_1_processing_status = 'complete'
        st.session_state.campaign_optimizer_1_output_file = output_file
        st.session_state.campaign_optimizer_1_processing_summary = summary

    def set_processing_error(self, error_message: str):
        """Set processing error."""
        st.session_state.campaign_optimizer_1_processing_status = 'error'
        st.session_state.campaign_optimizer_1_processing_error = error_message

    def is_processing(self) -> bool:
        """Check if processing is in progress."""
        return st.session_state.campaign_optimizer_1_processing_status == 'processing'

    def is_processing_complete(self) -> bool:
        """Check if processing is complete."""
        return st.session_state.campaign_optimizer_1_processing_status == 'complete'

    def has_processing_error(self) -> bool:
        """Check if processing has error."""
        return st.session_state.campaign_optimizer_1_processing_status == 'error'

    def get_processing_error(self) -> Optional[str]:
        """Get processing error message."""
        return st.session_state.campaign_optimizer_1_processing_error

    def clear_processing(self):
        """Clear processing state."""
        st.session_state.campaign_optimizer_1_processing_started = False
        st.session_state.campaign_optimizer_1_processing_status = None
        st.session_state.campaign_optimizer_1_processing_start_time = None
        st.session_state.campaign_optimizer_1_processing_error = None
        st.session_state.campaign_optimizer_1_output_file = None
        st.session_state.campaign_optimizer_1_processing_summary = None

    # Results methods
    def get_output_file(self) -> Optional[bytes]:
        """Get processed output file."""
        return st.session_state.campaign_optimizer_1_output_file

    def get_processing_summary(self) -> Optional[Dict[str, Any]]:
        """Get processing summary."""
        return st.session_state.campaign_optimizer_1_processing_summary

    # Ready state checks
    def is_ready_for_upload(self) -> bool:
        """Check if ready for file upload (checkbox selected)."""
        return self.is_seven_days_budgets_selected()

    def is_ready_for_processing(self) -> bool:
        """Check if ready for processing (file uploaded and validated)."""
        return (
            self.is_seven_days_budgets_selected() and
            st.session_state.campaign_optimizer_1_uploaded and
            self.is_validation_passed()
        )

    def can_download_results(self) -> bool:
        """Check if results can be downloaded."""
        return self.is_processing_complete() and st.session_state.campaign_optimizer_1_output_file is not None