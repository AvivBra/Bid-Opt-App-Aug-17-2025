"""Validation section UI component - SIMPLIFIED."""

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
        """Render the validation section - SIMPLIFIED."""

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

            # Show basic stats
            if details.get("processing_ready"):
                st.info(f"📊 {details['processing_ready']:,} rows ready for processing")

            if details.get("zero_sales_candidates"):
                st.info(
                    f"🎯 {details['zero_sales_candidates']:,} zero sales candidates found"
                )

        else:
            st.error(f"✗ {msg}")

            # Show missing portfolios if any
            if details.get("missing_in_template"):
                st.error("Missing portfolios in template:")
                for portfolio in details["missing_in_template"][:5]:  # Show max 5
                    st.caption(f"• {portfolio}")
                if len(details["missing_in_template"]) > 5:
                    st.caption(f"...and {len(details['missing_in_template']) - 5} more")

        st.markdown("---")

        # Optimization selection (simplified)
        self._render_optimization_selection()

        st.markdown("---")

        # Process button
        if valid:
            self._render_process_button()

    def _render_optimization_selection(self):
        """Render optimization checkboxes - SIMPLIFIED."""

        st.subheader("Select Optimizations")

        # Only Zero Sales is active in Phase 1
        col1, col2 = st.columns(2)

        with col1:
            zero_sales = st.checkbox(
                "Zero Sales Optimization", value=True, key="opt_zero_sales"
            )

            # Future optimizations (disabled)
            st.checkbox(
                "Portfolio Bid Optimization", disabled=True, key="opt_portfolio"
            )
            st.checkbox("Budget Optimization", disabled=True, key="opt_budget")
            st.checkbox("Keyword Optimization", disabled=True, key="opt_keyword")
            st.checkbox("ASIN Targeting", disabled=True, key="opt_asin")
            st.checkbox("Placement Optimization", disabled=True, key="opt_placement")
            st.checkbox("Negative Keyword Mining", disabled=True, key="opt_negative")

        with col2:
            st.checkbox("Dayparting Optimization", disabled=True, key="opt_daypart")
            st.checkbox("Search Term Harvesting", disabled=True, key="opt_search")
            st.checkbox("Bid Modifier Optimization", disabled=True, key="opt_modifier")
            st.checkbox("Campaign Structure", disabled=True, key="opt_structure")
            st.checkbox("Product Targeting", disabled=True, key="opt_product")
            st.checkbox("Auto to Manual", disabled=True, key="opt_auto")
            st.checkbox("Performance Cleanup", disabled=True, key="opt_cleanup")

        # Store selected optimizations
        if zero_sales:
            st.session_state.selected_optimizations = ["zero_sales"]
        else:
            st.session_state.selected_optimizations = []

    def _render_process_button(self):
        """Render the process files button."""

        if st.session_state.get("selected_optimizations"):
            if create_primary_button("⚡ Process Files", "process_files_btn"):
                st.session_state.processing_started = True
                st.session_state.current_view = "processing"
                st.rerun()
        else:
            st.warning("Please select at least one optimization")
