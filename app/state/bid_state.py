"""Bid optimizer state management with BidState class."""

import streamlit as st
import pandas as pd
from typing import Dict, List, Optional, Any
from io import BytesIO
import time


class BidState:
    """Manages bid optimizer state in session."""

    def __init__(self):
        """Initialize bid state manager."""
        self.init()

    def init(self) -> None:
        """Initialize bid optimizer specific state variables."""
        if "bid_state_initialized" not in st.session_state:
            # File storage
            st.session_state.template_file = None
            st.session_state.template_df = None
            st.session_state.bulk_60_file = None
            st.session_state.bulk_60_df = None
            st.session_state.bulk_30_file = None  # For future use
            st.session_state.bulk_7_file = None  # For future use
            st.session_state.data_rova_file = None  # For future use

            # Upload status
            st.session_state.template_uploaded = False
            st.session_state.bulk_60_uploaded = False
            st.session_state.bulk_30_uploaded = False
            st.session_state.bulk_7_uploaded = False

            # Validation state
            st.session_state.validation_passed = False
            st.session_state.validation_result = None
            st.session_state.missing_portfolios = []

            # Processing state
            st.session_state.processing_started = False
            st.session_state.processing_status = (
                None  # None, 'processing', 'complete', 'error'
            )
            st.session_state.processing_start_time = None
            st.session_state.processing_error = None

            # Progress tracking
            st.session_state.rows_processed = 0
            st.session_state.optimizations_count = 0
            st.session_state.progress_value = 0.0

            # Optimization selection
            st.session_state.selected_optimizations = []

            # Output files
            st.session_state.working_file = None
            st.session_state.clean_file = None
            st.session_state.output_generated = False

            # UI state
            st.session_state.current_panel = "upload"

            st.session_state.bid_state_initialized = True

    def save_template(self, file: BytesIO, df: pd.DataFrame) -> None:
        """Save template file and dataframe to state."""
        st.session_state.template_file = file
        st.session_state.template_df = df
        st.session_state.template_uploaded = True

        # Reset validation when new template uploaded
        self.reset_validation()

    def save_bulk(self, bulk_type: str, file: BytesIO, df: pd.DataFrame) -> None:
        """
        Save bulk file and dataframe to state.

        UPDATED: Clear other bulk types when saving new one (mutual exclusion)

        Args:
            bulk_type: Type of bulk file ('60', '30', '7')
            file: File BytesIO object
            df: Parsed DataFrame
        """
        # Clear all bulk data first (mutual exclusion)
        self._clear_all_bulk_data()

        if bulk_type == "60":
            st.session_state.bulk_60_file = file
            st.session_state.bulk_60_df = df
            st.session_state.bulk_60_uploaded = True
            st.session_state.active_bulk = "60"
        elif bulk_type == "30":
            st.session_state.bulk_30_file = file
            st.session_state.bulk_30_df = df
            st.session_state.bulk_30_uploaded = True
            st.session_state.active_bulk = "30"
        elif bulk_type == "7":
            st.session_state.bulk_7_file = file
            st.session_state.bulk_7_df = df
            st.session_state.bulk_7_uploaded = True
            st.session_state.active_bulk = "7"

        # Reset validation when new bulk uploaded
        self.reset_validation()

    def _clear_all_bulk_data(self) -> None:
        """Clear all bulk data from session (private method)."""
        # Clear Bulk 60
        if "bulk_60_file" in st.session_state:
            del st.session_state.bulk_60_file
        if "bulk_60_df" in st.session_state:
            del st.session_state.bulk_60_df
        st.session_state.bulk_60_uploaded = False

        # Clear Bulk 30
        if "bulk_30_file" in st.session_state:
            del st.session_state.bulk_30_file
        if "bulk_30_df" in st.session_state:
            del st.session_state.bulk_30_df
        st.session_state.bulk_30_uploaded = False

        # Clear Bulk 7
        if "bulk_7_file" in st.session_state:
            del st.session_state.bulk_7_file
        if "bulk_7_df" in st.session_state:
            del st.session_state.bulk_7_df
        st.session_state.bulk_7_uploaded = False

        # Clear active bulk indicator
        if "active_bulk" in st.session_state:
            del st.session_state.active_bulk

    def reset_validation(self) -> None:
        """
        Reset validation-related state.

        UPDATED: Also clear bulk data when validation is reset
        """
        st.session_state.validation_passed = False
        st.session_state.validation_result = None
        st.session_state.missing_portfolios = []

        # Clear bulk data when validation is reset (optimization changed)
        if st.session_state.get("optimization_changed", False):
            self._clear_all_bulk_data()
            st.session_state.optimization_changed = False

        # Also reset processing if it was started
        if st.session_state.get("processing_started"):
            self.reset_processing()

    def reset_processing(self) -> None:
        """Reset processing-related state."""
        st.session_state.processing_started = False
        st.session_state.processing_status = None
        st.session_state.processing_start_time = None
        st.session_state.processing_error = None
        st.session_state.rows_processed = 0
        st.session_state.optimizations_count = 0
        st.session_state.progress_value = 0.0
        st.session_state.output_generated = False
        st.session_state.working_file = None
        st.session_state.clean_file = None

    def get_template(self) -> Optional[pd.DataFrame]:
        """Get template DataFrame from state."""
        return st.session_state.get("template_df")

    def get_bulk(self, bulk_type: str = "60") -> Optional[pd.DataFrame]:
        """Get bulk DataFrame from state."""
        if bulk_type == "60":
            return st.session_state.get("bulk_60_df")
        elif bulk_type == "30":
            return st.session_state.get("bulk_30_df")
        elif bulk_type == "7":
            return st.session_state.get("bulk_7_df")
        return None

    def get_active_bulk(self) -> Optional[pd.DataFrame]:
        """
        Get the currently active bulk DataFrame.

        NEW METHOD: Returns whichever bulk is currently active

        Returns:
            Active bulk DataFrame or None
        """
        active_type = st.session_state.get("active_bulk", None)

        if active_type == "60":
            return st.session_state.get("bulk_60_df")
        elif active_type == "30":
            return st.session_state.get("bulk_30_df")
        elif active_type == "7":
            return st.session_state.get("bulk_7_df")

        return None

    def get_active_bulk_type(self) -> Optional[str]:
        """
        Get the type of currently active bulk.

        NEW METHOD

        Returns:
            '60', '30', '7', or None
        """
        return st.session_state.get("active_bulk", None)

    def get_selected_optimizations(self) -> List[str]:
        """Get list of selected optimizations."""
        return st.session_state.get("selected_optimizations", [])

    def set_selected_optimizations(self, optimizations: List[str]) -> None:
        """Set selected optimizations."""
        st.session_state.selected_optimizations = optimizations

    def is_ready_for_processing(self) -> bool:
        """
        Check if all conditions are met for processing.

        UPDATED: Check for any bulk file, not just bulk 60

        Returns:
            True if ready to process
        """
        return (
            st.session_state.get("template_uploaded", False)
            and self.has_any_bulk()  # Changed from bulk_60_uploaded
            and st.session_state.get("validation_passed", False)
            and len(st.session_state.get("selected_optimizations", [])) > 0
        )

    def has_any_bulk(self) -> bool:
        """
        Check if any bulk file is uploaded.

        NEW METHOD

        Returns:
            True if any bulk file is uploaded
        """
        return (
            st.session_state.get("bulk_60_uploaded", False)
            or st.session_state.get("bulk_30_uploaded", False)
            or st.session_state.get("bulk_7_uploaded", False)
        )

    def handle_optimization_change(self, new_optimization: str) -> None:
        """
        Handle optimization change.

        NEW METHOD

        Args:
            new_optimization: Name of the newly selected optimization
        """
        current_optimization = st.session_state.get("current_optimization", None)

        if current_optimization != new_optimization:
            # Mark that optimization changed
            st.session_state.optimization_changed = True
            st.session_state.current_optimization = new_optimization

            # Clear bulk data and validation
            self._clear_all_bulk_data()
            self.reset_validation()

            # Update bulk type based on optimization
            if new_optimization == "Zero Sales":
                st.session_state.active_bulk_type = "60"
            elif new_optimization == "Bids 30 Days":
                st.session_state.active_bulk_type = "30"
            else:
                st.session_state.active_bulk_type = None

    def start_processing(self) -> None:
        """Initialize processing state."""
        st.session_state.processing_started = True
        st.session_state.processing_status = "processing"
        st.session_state.processing_start_time = time.time()
        st.session_state.rows_processed = 0
        st.session_state.optimizations_count = 0
        st.session_state.progress_value = 0.0

    def complete_processing(self, output_data: Dict[str, Any]) -> None:
        """
        Mark processing as complete and save results.

        Args:
            output_data: Dictionary with output file data
        """
        st.session_state.processing_status = "complete"
        st.session_state.output_generated = True

        if "working_file" in output_data:
            st.session_state.working_file = output_data["working_file"]

        if "clean_file" in output_data:
            st.session_state.clean_file = output_data["clean_file"]

        if "statistics" in output_data:
            st.session_state.processing_stats = output_data["statistics"]

    def set_error(self, error_msg: str) -> None:
        """Set processing error state."""
        st.session_state.processing_status = "error"
        st.session_state.processing_error = error_msg

    def reset_all(self) -> None:
        """Reset all bid optimizer state."""
        keys_to_preserve = ["current_page", "page", "bid_state_initialized"]

        for key in list(st.session_state.keys()):
            if key not in keys_to_preserve:
                del st.session_state[key]

        # Re-initialize
        self.init()

    @staticmethod
    def has_template() -> bool:
        """Check if template is uploaded."""
        return st.session_state.get("template_uploaded", False)

    @staticmethod
    def has_bulk(bulk_type: str = "60") -> bool:
        """Check if bulk file is uploaded."""
        if bulk_type == "60":
            return st.session_state.get("bulk_60_uploaded", False)
        elif bulk_type == "30":
            return st.session_state.get("bulk_30_uploaded", False)
        elif bulk_type == "7":
            return st.session_state.get("bulk_7_uploaded", False)
        return False

    @staticmethod
    def is_processing() -> bool:
        """Check if currently processing."""
        return st.session_state.get("processing_status") == "processing"

    @staticmethod
    def is_complete() -> bool:
        """Check if processing is complete."""
        return st.session_state.get("processing_status") == "complete"

    @staticmethod
    def has_error() -> bool:
        """Check if processing encountered an error."""
        return st.session_state.get("processing_status") == "error"

    @staticmethod
    def get_error_message() -> Optional[str]:
        """Get error message if any."""
        return st.session_state.get("processing_error")

    @staticmethod
    def get_working_file() -> Optional[BytesIO]:
        """Get working file if generated."""
        return st.session_state.get("working_file")

    @staticmethod
    def get_clean_file() -> Optional[BytesIO]:
        """Get clean file if generated."""
        return st.session_state.get("clean_file")

    def has_required_files(self) -> bool:
        """Check if required files (template and bulk) are uploaded."""
        return (
            st.session_state.get("template_uploaded", False) and self.has_any_bulk()
        )  # Changed to has_any_bulk


# Backward compatibility - keep the standalone functions as well
def init_bid_state() -> None:
    """Initialize bid optimizer specific state variables."""
    state = BidState()
    state.init()


def save_template_data(file: BytesIO, df: pd.DataFrame) -> None:
    """Save template file and dataframe to state."""
    state = BidState()
    state.save_template(file, df)


def save_bulk_data(bulk_type: str, file: BytesIO, df: pd.DataFrame) -> None:
    """Save bulk file and dataframe to state."""
    state = BidState()
    state.save_bulk(bulk_type, file, df)


def reset_validation_state() -> None:
    """Reset validation-related state."""
    state = BidState()
    state.reset_validation()


def reset_processing_state() -> None:
    """Reset processing-related state."""
    state = BidState()
    state.reset_processing()


def get_template_data() -> Optional[pd.DataFrame]:
    """Get template DataFrame from state."""
    state = BidState()
    return state.get_template()


def get_bulk_data(bulk_type: str = "60") -> Optional[pd.DataFrame]:
    """Get bulk DataFrame from state."""
    state = BidState()
    return state.get_bulk(bulk_type)


def get_selected_optimizations() -> List[str]:
    """Get list of selected optimizations."""
    return st.session_state.get("selected_optimizations", [])


def set_selected_optimizations(optimizations: List[str]) -> None:
    """Set selected optimizations."""
    st.session_state.selected_optimizations = optimizations


def is_ready_for_processing() -> bool:
    """Check if all conditions are met for processing."""
    state = BidState()
    return state.is_ready_for_processing()


def start_processing() -> None:
    """Initialize processing state."""
    state = BidState()
    state.start_processing()


def complete_processing(output_data: Dict[str, Any]) -> None:
    """Mark processing as complete and save results."""
    state = BidState()
    state.complete_processing(output_data)


def set_processing_error(error_msg: str) -> None:
    """Set processing error state."""
    state = BidState()
    state.set_error(error_msg)


def reset_all() -> None:
    """Reset all bid optimizer state."""
    state = BidState()
    state.reset_all()
