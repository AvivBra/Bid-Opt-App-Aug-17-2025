"""Validation section UI component - WITHOUT STATISTICS."""

import streamlit as st
from data.validators.portfolio_validator import PortfolioValidator
from app.state.bid_state import BidState
from app.ui.layout import create_section_header, create_status_message
from app.ui.components.buttons import create_primary_button


class ValidationSection:
    """Handles data validation UI and processing."""

    def __init__(self):
        self.portfolio_validator = PortfolioValidator()
        self.bid_state = BidState()

    def render(self):
        """Render the validation section."""

        create_section_header("Data Validation", "✓")

        # Check if files are ready for validation
        if not self.bid_state.has_required_files():
            create_status_message(
                "Upload Template and Bulk files to begin validation", "info"
            )
            return

        # Get file data
        template_uploaded, template_data, template_info = self.bid_state.get_file_data(
            "template"
        )
        bulk_uploaded, bulk_data, bulk_info = self.bid_state.get_file_data("bulk_60")

        if not template_data or bulk_data is None:
            create_status_message(
                "File data not available - please re-upload files", "error"
            )
            return

        # Perform validation
        valid, msg, details = self.portfolio_validator.validate_portfolio_matching(
            template_data, bulk_data
        )

        # Display validation results
        if valid:
            st.success(f"✓ {msg}")

            # REMOVED: Statistics display
            # No longer showing "rows ready for processing" or "zero sales candidates"

        else:
            st.error(f"✗ {msg}")

            # Show ALL missing portfolios
            if details.get("missing_in_template"):
                st.error(
                    "The following portfolios are in the Bulk file but not in Template:"
                )

                # Display ALL missing portfolios, each on its own line
                for portfolio in details["missing_in_template"]:
                    st.caption(f"• {portfolio}")

                # Add upload new template button
                st.info("(Bulk file will be kept in memory)")
                if st.button("Upload New Template", key="upload_new_template_btn"):
                    st.session_state.show_template_uploader = True

        st.markdown("---")

        # Optimization selection (simplified for Phase 1)
        self._render_optimization_selection()

        st.markdown("---")

        # Process button - only show if validation passed
        if valid:
            self._render_process_button()

    def _render_optimization_selection(self):
        """Render optimization checkboxes - Phase 1 only Zero Sales."""

        st.subheader("Select Optimizations")

        # Only Zero Sales is enabled in Phase 1
        col1, col2 = st.columns(2)

        with col1:
            zero_sales = st.checkbox("Zero Sales", value=True, key="opt_zero_sales")
            if zero_sales:
                st.session_state.selected_optimizations = ["zero_sales"]

        with col2:
            # Future optimizations - all disabled in Phase 1
            st.checkbox(
                "Portfolio Bid Optimization", disabled=True, key="opt_portfolio_bid"
            )
            st.caption("Coming Soon")

        # Additional rows for future optimizations
        col3, col4 = st.columns(2)

        with col3:
            st.checkbox("Budget Optimization", disabled=True, key="opt_budget")
            st.caption("Coming Soon")

        with col4:
            st.checkbox("Keyword Optimization", disabled=True, key="opt_keyword")
            st.caption("Coming Soon")

    def _render_process_button(self):
        """Render the process files button."""

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            if st.button(
                "⚡ PROCESS FILES",
                key="process_files_btn",
                use_container_width=True,
                type="primary",
            ):
                st.session_state.processing_status = "started"
                st.session_state.current_view = "output"
                st.rerun()
