"""Bid optimizer application state management - WITHOUT STATISTICS."""

import streamlit as st
import pandas as pd
from typing import Dict, Tuple, Any, Optional
import logging


class BidState:
    """Manages application state for bid optimizer."""

    def __init__(self):
        self.logger = logging.getLogger("bid_state")
        self._initialize_state()

    def _initialize_state(self):
        """Initialize session state variables if not present."""

        # File storage
        if "template_file" not in st.session_state:
            st.session_state.template_file = None
        if "template_data" not in st.session_state:
            st.session_state.template_data = None

        if "bulk_60_file" not in st.session_state:
            st.session_state.bulk_60_file = None
        if "bulk_60_data" not in st.session_state:
            st.session_state.bulk_60_data = None

        # Processing state
        if "processing_status" not in st.session_state:
            st.session_state.processing_status = "idle"
        if "processing_error" not in st.session_state:
            st.session_state.processing_error = None

        # Results
        if "output_data" not in st.session_state:
            st.session_state.output_data = None
        if "output_file" not in st.session_state:
            st.session_state.output_file = None

        # UI state
        if "current_view" not in st.session_state:
            st.session_state.current_view = "upload"
        if "selected_optimizations" not in st.session_state:
            st.session_state.selected_optimizations = []

    def has_required_files(self) -> bool:
        """Check if required files are uploaded."""
        return (
            st.session_state.template_data is not None
            and st.session_state.bulk_60_data is not None
        )

    def get_file_data(self, file_type: str) -> Tuple[bool, Any, Dict]:
        """
        Get file data and info.

        Args:
            file_type: 'template' or 'bulk_60'

        Returns:
            Tuple of (is_uploaded, data, info)
        """

        if file_type == "template":
            data = st.session_state.template_data
            file = st.session_state.template_file
        elif file_type == "bulk_60":
            data = st.session_state.bulk_60_data
            file = st.session_state.bulk_60_file
        else:
            return False, None, {}

        if data is None:
            return False, None, {}

        info = {
            "filename": file.name if file else "Unknown",
            "size": file.size if file else 0,
        }

        # Add row count for bulk data
        if file_type == "bulk_60" and isinstance(data, pd.DataFrame):
            info["row_count"] = len(data)

        return True, data, info

    def set_file_data(self, file_type: str, file_obj, data):
        """Store file data in session state."""

        if file_type == "template":
            st.session_state.template_file = file_obj
            st.session_state.template_data = data
        elif file_type == "bulk_60":
            st.session_state.bulk_60_file = file_obj
            st.session_state.bulk_60_data = data

    def clear_file_data(self, file_type: str = None):
        """Clear file data from session state."""

        if file_type == "template" or file_type is None:
            st.session_state.template_file = None
            st.session_state.template_data = None

        if file_type == "bulk_60" or file_type is None:
            st.session_state.bulk_60_file = None
            st.session_state.bulk_60_data = None

    def set_processing_status(self, status: str, error: str = None):
        """Update processing status."""

        st.session_state.processing_status = status
        st.session_state.processing_error = error

    def get_processing_status(self) -> Tuple[str, Optional[str]]:
        """Get current processing status."""

        return (st.session_state.processing_status, st.session_state.processing_error)

    def set_output_data(self, data, file_bytes=None):
        """Store processing output."""

        st.session_state.output_data = data
        st.session_state.output_file = file_bytes

    def get_output_data(self) -> Tuple[Any, Any]:
        """Get processing output."""

        return (st.session_state.output_data, st.session_state.output_file)

    def reset_state(self):
        """Reset all state to initial values."""

        # Clear files
        self.clear_file_data()

        # Reset processing
        st.session_state.processing_status = "idle"
        st.session_state.processing_error = None

        # Clear results
        st.session_state.output_data = None
        st.session_state.output_file = None

        # Reset UI
        st.session_state.current_view = "upload"
        st.session_state.selected_optimizations = []

    def validate_data_compatibility(
        self, template_data: Dict[str, pd.DataFrame], bulk_data: pd.DataFrame
    ) -> Tuple[bool, str, Dict]:
        """
        Basic validation of data compatibility.

        REMOVED: Statistics calculations that were causing confusion
        """

        details = {
            "template_portfolios": [],
            "bulk_portfolios": [],
            "portfolio_matches": [],
            "portfolio_mismatches": [],
            "issues": [],
            "warnings": [],
        }

        try:
            # Get template portfolios
            if "Port Values" not in template_data:
                details["issues"].append("Missing 'Port Values' sheet in template")
                return False, "Invalid template structure", details

            port_values = template_data["Port Values"]

            if "Portfolio Name" not in port_values.columns:
                details["issues"].append("Missing 'Portfolio Name' column in template")
                return False, "Invalid template structure", details

            template_portfolios = set(
                port_values["Portfolio Name"].astype(str).str.strip()
            )
            details["template_portfolios"] = list(template_portfolios)

            # Get bulk portfolios
            portfolio_col = None
            for col in bulk_data.columns:
                if "portfolio" in col.lower():
                    portfolio_col = col
                    break

            if portfolio_col is None:
                details["issues"].append("No portfolio column found in bulk file")
                return False, "Portfolio column not found in bulk file", details

            bulk_portfolios = set(bulk_data[portfolio_col].astype(str).str.strip())

            # Find matches and mismatches
            details["portfolio_matches"] = list(template_portfolios & bulk_portfolios)
            details["portfolio_mismatches"] = list(
                template_portfolios - bulk_portfolios
            )

            # REMOVED: Zero sales candidates calculation
            # This was causing confusion with incorrect counts

            # Validation results
            if len(details["portfolio_matches"]) == 0:
                return (
                    False,
                    "No matching portfolios found between template and bulk file",
                    details,
                )

            if len(details["portfolio_mismatches"]) > len(details["portfolio_matches"]):
                details["warnings"].append(
                    f"Many template portfolios not found in bulk: {len(details['portfolio_mismatches'])}"
                )

            success_msg = f"Data compatible: {len(details['portfolio_matches'])} matching portfolios"

            return True, success_msg, details

        except Exception as e:
            return False, f"Error validating compatibility: {str(e)}", details

    def get_optimization_config(self) -> Dict[str, Any]:
        """Get configuration for optimization processing."""

        config = {
            "selected_optimizations": st.session_state.get(
                "selected_optimizations", ["zero_sales"]
            ),
            "zero_sales_enabled": "zero_sales"
            in st.session_state.get("selected_optimizations", []),
            "processing_mode": "standard",  # or 'fast', 'thorough'
            "output_format": "working_file",  # or 'clean_file', 'both'
        }

        return config
