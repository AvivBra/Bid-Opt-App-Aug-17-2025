"""Portfolio optimizer state management."""

import streamlit as st
import pandas as pd
from typing import Dict, List, Optional, Any
from io import BytesIO
import time


class PortfolioState:
    """Manages portfolio optimizer state in session."""

    def __init__(self):
        """Initialize portfolio state manager."""
        self.init()

    def init(self) -> None:
        """Initialize portfolio optimizer specific state variables."""
        if "portfolio_state_initialized" not in st.session_state:
            # File storage - Empty Portfolios doesn't need template
            st.session_state.portfolio_bulk_60_file = None
            st.session_state.portfolio_bulk_60_df = None
            st.session_state.portfolio_bulk_30_file = None  # For future use
            st.session_state.portfolio_bulk_7_file = None  # For future use

            # Upload status
            st.session_state.portfolio_bulk_60_uploaded = False
            st.session_state.portfolio_bulk_30_uploaded = False
            st.session_state.portfolio_bulk_7_uploaded = False

            # Validation state
            st.session_state.portfolio_validation_passed = False
            st.session_state.portfolio_validation_result = None
            st.session_state.portfolio_validation_errors = []

            # Processing state
            st.session_state.portfolio_processing_started = False
            st.session_state.portfolio_processing_status = None  # None, 'processing', 'complete', 'error'
            st.session_state.portfolio_processing_start_time = None
            st.session_state.portfolio_processing_error = None

            # Progress tracking
            st.session_state.portfolio_rows_processed = 0
            st.session_state.portfolio_optimizations_count = 0
            st.session_state.portfolio_progress_value = 0.0

            # Optimization selection
            st.session_state.portfolio_selected_optimizations = []
            st.session_state.empty_portfolios_selected = False
            st.session_state.campaigns_without_portfolios_selected = False

            # Empty Portfolios specific state
            st.session_state.empty_portfolios_found = 0
            st.session_state.empty_portfolios_renamed = 0
            st.session_state.empty_portfolios_results = None
            
            # Campaigns without Portfolios specific state
            st.session_state.campaigns_without_portfolios_found = 0
            st.session_state.campaigns_without_portfolios_updated = 0
            st.session_state.campaigns_without_portfolios_results = None

            # Output files
            st.session_state.portfolio_working_file = None
            st.session_state.portfolio_clean_file = None
            st.session_state.portfolio_output_generated = False

            # UI state
            st.session_state.portfolio_current_panel = "upload"

            st.session_state.portfolio_state_initialized = True

    def save_bulk(self, bulk_type: str, file: BytesIO, df: pd.DataFrame) -> None:
        """
        Save bulk file and dataframe to state.
        
        Args:
            bulk_type: Type of bulk file ('60', '30', or '7')
            file: File object
            df: Parsed DataFrame
        """
        if bulk_type == "60":
            st.session_state.portfolio_bulk_60_file = file
            st.session_state.portfolio_bulk_60_df = df
            st.session_state.portfolio_bulk_60_uploaded = True
        elif bulk_type == "30":
            st.session_state.portfolio_bulk_30_file = file
            st.session_state.portfolio_bulk_30_df = df
            st.session_state.portfolio_bulk_30_uploaded = True
        elif bulk_type == "7":
            st.session_state.portfolio_bulk_7_file = file
            st.session_state.portfolio_bulk_7_df = df
            st.session_state.portfolio_bulk_7_uploaded = True

        # Reset validation when new file uploaded
        self.reset_validation()

    def get_bulk(self, bulk_type: str = "60") -> Optional[pd.DataFrame]:
        """Get bulk DataFrame from state."""
        if bulk_type == "60":
            return st.session_state.get("portfolio_bulk_60_df")
        elif bulk_type == "30":
            return st.session_state.get("portfolio_bulk_30_df")
        elif bulk_type == "7":
            return st.session_state.get("portfolio_bulk_7_df")
        return None

    def reset_validation(self) -> None:
        """Reset validation state."""
        st.session_state.portfolio_validation_passed = False
        st.session_state.portfolio_validation_result = None
        st.session_state.portfolio_validation_errors = []

    def reset_processing(self) -> None:
        """Reset processing state."""
        st.session_state.portfolio_processing_started = False
        st.session_state.portfolio_processing_status = None
        st.session_state.portfolio_processing_start_time = None
        st.session_state.portfolio_processing_error = None
        st.session_state.portfolio_rows_processed = 0
        st.session_state.portfolio_optimizations_count = 0
        st.session_state.portfolio_progress_value = 0.0

    def set_validation_result(self, passed: bool, result: Dict[str, Any]) -> None:
        """Set validation result."""
        st.session_state.portfolio_validation_passed = passed
        st.session_state.portfolio_validation_result = result
        if not passed and "errors" in result:
            st.session_state.portfolio_validation_errors = result["errors"]

    def has_any_bulk(self) -> bool:
        """Check if any bulk file is uploaded."""
        return (
            st.session_state.get("portfolio_bulk_60_uploaded", False)
            or st.session_state.get("portfolio_bulk_30_uploaded", False)
            or st.session_state.get("portfolio_bulk_7_uploaded", False)
        )

    def is_ready_for_processing(self) -> bool:
        """Check if ready for processing."""
        # For Empty Portfolios, only need bulk file
        if st.session_state.get("empty_portfolios_selected", False):
            return self.has_any_bulk()
        
        # For Campaigns without Portfolios, only need bulk file
        if st.session_state.get("campaigns_without_portfolios_selected", False):
            return self.has_any_bulk()
        
        # For future optimizations, might need different requirements
        return self.has_any_bulk()

    def start_processing(self) -> None:
        """Initialize processing state."""
        st.session_state.portfolio_processing_started = True
        st.session_state.portfolio_processing_status = "processing"
        st.session_state.portfolio_processing_start_time = time.time()
        st.session_state.portfolio_rows_processed = 0
        st.session_state.portfolio_optimizations_count = 0
        st.session_state.portfolio_progress_value = 0.0

    def complete_processing(self, output_data: Dict[str, Any]) -> None:
        """
        Mark processing as complete and save results.
        
        Args:
            output_data: Dictionary with output file data
        """
        st.session_state.portfolio_processing_status = "complete"
        st.session_state.portfolio_output_generated = True

        if "working_file" in output_data:
            st.session_state.portfolio_working_file = output_data["working_file"]

        if "clean_file" in output_data:
            st.session_state.portfolio_clean_file = output_data["clean_file"]

        if "statistics" in output_data:
            st.session_state.portfolio_processing_stats = output_data["statistics"]

        # Save Empty Portfolios specific results
        if st.session_state.get("empty_portfolios_selected", False):
            if "empty_portfolios_found" in output_data:
                st.session_state.empty_portfolios_found = output_data["empty_portfolios_found"]
            if "empty_portfolios_renamed" in output_data:
                st.session_state.empty_portfolios_renamed = output_data["empty_portfolios_renamed"]
            if "empty_portfolios_results" in output_data:
                st.session_state.empty_portfolios_results = output_data["empty_portfolios_results"]
        
        # Save Campaigns without Portfolios specific results
        if st.session_state.get("campaigns_without_portfolios_selected", False):
            if "campaigns_without_portfolios_found" in output_data:
                st.session_state.campaigns_without_portfolios_found = output_data["campaigns_without_portfolios_found"]
            if "campaigns_without_portfolios_updated" in output_data:
                st.session_state.campaigns_without_portfolios_updated = output_data["campaigns_without_portfolios_updated"]
            if "campaigns_without_portfolios_results" in output_data:
                st.session_state.campaigns_without_portfolios_results = output_data["campaigns_without_portfolios_results"]

    def set_error(self, error_msg: str) -> None:
        """Set processing error state."""
        st.session_state.portfolio_processing_status = "error"
        st.session_state.portfolio_processing_error = error_msg

    def reset_all(self) -> None:
        """Reset all portfolio optimizer state."""
        keys_to_preserve = ["current_page", "page", "portfolio_state_initialized"]

        # Clear all portfolio-specific keys
        portfolio_keys = [k for k in st.session_state.keys() if k.startswith("portfolio_") or k.startswith("empty_portfolios_") or k.startswith("campaigns_without_portfolios_")]
        
        for key in portfolio_keys:
            if key not in keys_to_preserve:
                del st.session_state[key]

        # Re-initialize
        self.init()

    @staticmethod
    def has_bulk(bulk_type: str = "60") -> bool:
        """Check if bulk file is uploaded."""
        if bulk_type == "60":
            return st.session_state.get("portfolio_bulk_60_uploaded", False)
        elif bulk_type == "30":
            return st.session_state.get("portfolio_bulk_30_uploaded", False)
        elif bulk_type == "7":
            return st.session_state.get("portfolio_bulk_7_uploaded", False)
        return False

    @staticmethod
    def is_processing() -> bool:
        """Check if currently processing."""
        return st.session_state.get("portfolio_processing_status") == "processing"

    @staticmethod
    def is_complete() -> bool:
        """Check if processing is complete."""
        return st.session_state.get("portfolio_processing_status") == "complete"

    @staticmethod
    def has_error() -> bool:
        """Check if processing encountered an error."""
        return st.session_state.get("portfolio_processing_status") == "error"

    @staticmethod
    def get_error_message() -> Optional[str]:
        """Get error message if any."""
        return st.session_state.get("portfolio_processing_error")

    @staticmethod
    def get_working_file() -> Optional[BytesIO]:
        """Get working file if generated."""
        return st.session_state.get("portfolio_working_file")

    @staticmethod
    def get_clean_file() -> Optional[BytesIO]:
        """Get clean file if generated."""
        return st.session_state.get("portfolio_clean_file")


# Backward compatibility - standalone functions
def init_portfolio_state() -> None:
    """Initialize portfolio optimizer specific state variables."""
    state = PortfolioState()
    state.init()


def save_portfolio_bulk_data(bulk_type: str, file: BytesIO, df: pd.DataFrame) -> None:
    """Save bulk file and dataframe to state."""
    state = PortfolioState()
    state.save_bulk(bulk_type, file, df)


def reset_portfolio_validation_state() -> None:
    """Reset validation-related state."""
    state = PortfolioState()
    state.reset_validation()


def reset_portfolio_processing_state() -> None:
    """Reset processing-related state."""
    state = PortfolioState()
    state.reset_processing()


def get_portfolio_bulk_data(bulk_type: str = "60") -> Optional[pd.DataFrame]:
    """Get bulk DataFrame from state."""
    state = PortfolioState()
    return state.get_bulk(bulk_type)


def get_portfolio_selected_optimizations() -> List[str]:
    """Get list of selected optimizations."""
    return st.session_state.get("portfolio_selected_optimizations", [])


def set_portfolio_selected_optimizations(optimizations: List[str]) -> None:
    """Set selected optimizations."""
    st.session_state.portfolio_selected_optimizations = optimizations


def is_portfolio_ready_for_processing() -> bool:
    """Check if all conditions are met for processing."""
    state = PortfolioState()
    return state.is_ready_for_processing()


def start_portfolio_processing() -> None:
    """Initialize processing state."""
    state = PortfolioState()
    state.start_processing()


def complete_portfolio_processing(output_data: Dict[str, Any]) -> None:
    """Mark processing as complete and save results."""
    state = PortfolioState()
    state.complete_processing(output_data)


def set_portfolio_processing_error(error_msg: str) -> None:
    """Set processing error state."""
    state = PortfolioState()
    state.set_error(error_msg)


def reset_portfolio_all() -> None:
    """Reset all portfolio optimizer state."""
    state = PortfolioState()
    state.reset_all()
