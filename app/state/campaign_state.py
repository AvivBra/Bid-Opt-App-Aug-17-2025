"""Campaign optimizer state management."""

import streamlit as st
import pandas as pd
from typing import Dict, List, Optional, Any
from io import BytesIO
import time


class CampaignState:
    """Manages campaign optimizer state in session."""

    def __init__(self):
        """Initialize campaign state manager."""
        self.init()

    def init(self) -> None:
        """Initialize campaign optimizer specific state variables."""
        if "campaign_state_initialized" not in st.session_state:
            # File storage
            st.session_state.campaign_template_file = None
            st.session_state.campaign_template_df = None
            st.session_state.data_rova_file = None
            st.session_state.data_rova_df = None
            st.session_state.data_dive_file = None
            st.session_state.data_dive_df = None

            # Upload status
            st.session_state.campaign_template_uploaded = False
            st.session_state.data_rova_uploaded = False
            st.session_state.data_dive_uploaded = False

            # Validation state
            st.session_state.campaign_validation_passed = False
            st.session_state.campaign_validation_result = None

            # Processing state
            st.session_state.campaign_processing_started = False
            st.session_state.campaign_processing_status = None
            st.session_state.campaign_processing_complete = False
            st.session_state.campaign_processing_error = None

            # Progress tracking
            st.session_state.campaign_rows_processed = 0
            st.session_state.campaign_progress_value = 0.0

            # Optimization selection
            st.session_state.selected_campaign_optimization = "Campaign Creator"

            # Output files
            st.session_state.campaign_bulk_file = None
            st.session_state.campaign_output_generated = False

            st.session_state.campaign_state_initialized = True

    def save_template(self, file: BytesIO, df: pd.DataFrame) -> None:
        """Save template file and dataframe to state."""
        st.session_state.campaign_template_file = file
        st.session_state.campaign_template_df = df
        st.session_state.campaign_template_uploaded = True

        # Reset validation when new template uploaded
        self.reset_validation()

    def save_data_rova(self, file: BytesIO, df: pd.DataFrame) -> None:
        """Save Data Rova file and dataframe to state."""
        st.session_state.data_rova_file = file
        st.session_state.data_rova_df = df
        st.session_state.data_rova_uploaded = True

    def save_data_dive(self, file: BytesIO, df: pd.DataFrame) -> None:
        """Save Data Dive file and dataframe to state."""
        st.session_state.data_dive_file = file
        st.session_state.data_dive_df = df
        st.session_state.data_dive_uploaded = True

    def reset_validation(self) -> None:
        """Reset validation-related state."""
        st.session_state.campaign_validation_passed = False
        st.session_state.campaign_validation_result = None

    def reset_processing(self) -> None:
        """Reset processing-related state."""
        st.session_state.campaign_processing_started = False
        st.session_state.campaign_processing_status = None
        st.session_state.campaign_processing_complete = False
        st.session_state.campaign_processing_error = None
        st.session_state.campaign_rows_processed = 0
        st.session_state.campaign_progress_value = 0.0
        st.session_state.campaign_bulk_file = None
        st.session_state.campaign_output_generated = False

    def get_template(self) -> Optional[pd.DataFrame]:
        """Get template DataFrame from state."""
        return st.session_state.get("campaign_template_df")

    def get_data_rova(self) -> Optional[pd.DataFrame]:
        """Get Data Rova DataFrame from state."""
        return st.session_state.get("data_rova_df")

    def get_data_dive(self) -> Optional[pd.DataFrame]:
        """Get Data Dive DataFrame from state."""
        return st.session_state.get("data_dive_df")

    def is_ready_for_processing(self) -> bool:
        """Check if all conditions are met for processing."""
        return (
            st.session_state.get("campaign_template_uploaded", False)
            and st.session_state.get("campaign_validation_passed", False)
            and st.session_state.get("selected_campaign_optimization") == "Campaign Creator"
        )

    def start_processing(self) -> None:
        """Initialize processing state."""
        st.session_state.campaign_processing_started = True
        st.session_state.campaign_processing_status = "processing"
        st.session_state.campaign_processing_start_time = time.time()
        st.session_state.campaign_rows_processed = 0
        st.session_state.campaign_progress_value = 0.0

    def complete_processing(self, output_data: Dict[str, Any]) -> None:
        """Mark processing as complete and save results."""
        st.session_state.campaign_processing_status = "complete"
        st.session_state.campaign_processing_complete = True
        st.session_state.campaign_output_generated = True

        if "bulk_file" in output_data:
            st.session_state.campaign_bulk_file = output_data["bulk_file"]

    def set_error(self, error_msg: str) -> None:
        """Set processing error state."""
        st.session_state.campaign_processing_status = "error"
        st.session_state.campaign_processing_error = error_msg

    def reset_all(self) -> None:
        """Reset all campaign optimizer state."""
        keys_to_preserve = ["current_page", "page", "campaign_state_initialized"]

        campaign_keys = [k for k in st.session_state.keys() if k.startswith("campaign_") or k.startswith("data_")]
        
        for key in campaign_keys:
            if key not in keys_to_preserve:
                del st.session_state[key]

        # Re-initialize
        self.init()

    @staticmethod
    def has_template() -> bool:
        """Check if template is uploaded."""
        return st.session_state.get("campaign_template_uploaded", False)

    @staticmethod
    def has_data_rova() -> bool:
        """Check if Data Rova is uploaded."""
        return st.session_state.get("data_rova_uploaded", False)

    @staticmethod
    def has_data_dive() -> bool:
        """Check if Data Dive is uploaded."""
        return st.session_state.get("data_dive_uploaded", False)

    @staticmethod
    def is_processing() -> bool:
        """Check if currently processing."""
        return st.session_state.get("campaign_processing_status") == "processing"

    @staticmethod
    def is_complete() -> bool:
        """Check if processing is complete."""
        return st.session_state.get("campaign_processing_complete", False)

    @staticmethod
    def has_error() -> bool:
        """Check if processing encountered an error."""
        return st.session_state.get("campaign_processing_status") == "error"

    @staticmethod
    def get_error_message() -> Optional[str]:
        """Get error message if any."""
        return st.session_state.get("campaign_processing_error")

    @staticmethod
    def get_bulk_file() -> Optional[BytesIO]:
        """Get campaign bulk file if generated."""
        return st.session_state.get("campaign_bulk_file")