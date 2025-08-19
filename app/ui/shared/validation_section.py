"""Validation section UI component with ValidationSection class."""

import streamlit as st
from typing import List, Dict, Optional
from app.ui.components.checklist import render_optimization_checklist
from app.ui.components.alerts import show_validation_alert
from data.validators.portfolio_validator import validate_portfolios
from business.common.excluded_portfolios import EXCLUDED_PORTFOLIOS
from utils.page_utils import initialize_processing_state, switch_panel


class ValidationSection:
    """Validation section component for portfolio validation and optimization selection."""

    def __init__(self):
        """Initialize the validation section."""
        self.validation_result = None
        self.selected_optimizations = []

    def render(self) -> None:
        """Render the validation section panel."""
        with st.container():
            st.markdown("### DATA VALIDATION")
            st.markdown("---")

            # Check if files are uploaded
            if not self._check_files_uploaded():
                st.info("📤 Please upload Template and Bulk files first")
                return

            # Run validation
            self.validation_result = self._run_validation()

            # Display validation results
            self._display_validation_results(self.validation_result)

            # Show optimization selection
            st.markdown("#### Select Optimizations")
            self.selected_optimizations = render_optimization_checklist()

            # Process Files button
            self._render_process_button(self.validation_result)

    def _check_files_uploaded(self) -> bool:
        """Check if required files are uploaded."""
        return (
            st.session_state.get("template_df") is not None
            and st.session_state.get("bulk_60_df") is not None
        )

    def _run_validation(self) -> Dict:
        """Run portfolio validation."""
        try:
            template_df = st.session_state.get("template_df")
            bulk_df = st.session_state.get("bulk_60_df")

            result = validate_portfolios(template_df, bulk_df)

            # Store validation result in session state
            st.session_state.validation_result = result
            st.session_state.validation_passed = result["valid"]

            return result

        except Exception as e:
            return {"valid": False, "missing_portfolios": [], "error": str(e)}

    def _display_validation_results(self, result: Dict) -> None:
        """Display validation results with alerts."""
        if result.get("error"):
            show_validation_alert("error", f"Validation error: {result['error']}")
            return

        if result["valid"]:
            # Check for ignored portfolios
            ignored = self._check_ignored_portfolios()
            if ignored:
                show_validation_alert(
                    "info",
                    f"ℹ️ {len(ignored)} portfolios marked as 'Ignore' will be skipped",
                )
            show_validation_alert("success", "✓ All portfolios valid")
        else:
            missing = result.get("missing_portfolios", [])
            if missing:
                # Filter out excluded portfolios
                non_excluded = [p for p in missing if p not in EXCLUDED_PORTFOLIOS]
                if non_excluded:
                    show_validation_alert(
                        "error",
                        f"Missing portfolios found - Reupload Full Template: {', '.join(non_excluded[:5])}",
                    )

    def _check_ignored_portfolios(self) -> List[str]:
        """Check for portfolios marked as Ignore."""
        template_df = st.session_state.get("template_df")
        if template_df is not None and "Base Bid" in template_df.columns:
            ignored = template_df[
                template_df["Base Bid"].astype(str).str.lower() == "ignore"
            ]["Portfolio Name"].tolist()
            return ignored
        return []

    def _render_process_button(self, validation_result: Dict) -> None:
        """Render the Process Files button with proper state handling."""
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            # Check if button should be enabled
            button_enabled = (
                validation_result.get("valid", False)
                and len(st.session_state.get("selected_optimizations", [])) > 0
                and not st.session_state.get("processing_started", False)
            )

            if st.button(
                "⚡ Process Files",
                disabled=not button_enabled,
                use_container_width=True,
                type="primary",
            ):
                # Initialize processing state
                initialize_processing_state()

                # Switch to output panel
                switch_panel("output")

                # Trigger rerun to show processing
                st.rerun()

            # Show help text if disabled
            if not button_enabled:
                if st.session_state.get("processing_started"):
                    st.caption("Processing in progress...")
                elif not validation_result.get("valid", False):
                    st.caption("Fix validation errors first")
                elif len(st.session_state.get("selected_optimizations", [])) == 0:
                    st.caption("Select at least one optimization")

    def check_validation_status(self) -> bool:
        """Check if validation has passed."""
        return st.session_state.get("validation_passed", False)

    def get_validation_result(self) -> Optional[Dict]:
        """Get the stored validation result."""
        return self.validation_result

    def get_selected_optimizations(self) -> List[str]:
        """Get selected optimizations."""
        return self.selected_optimizations

    def run_portfolio_validation(self) -> Dict:
        """Public method to run validation."""
        return self._run_validation()


# Standalone function for backward compatibility
def render() -> None:
    """Render the validation section panel."""
    section = ValidationSection()
    section.render()


def check_validation_status() -> bool:
    """Check if validation has passed."""
    return st.session_state.get("validation_passed", False)


def get_validation_result() -> Optional[Dict]:
    """Get the stored validation result."""
    return st.session_state.get("validation_result")


def run_portfolio_validation() -> Dict:
    """Public method to run validation."""
    section = ValidationSection()
    return section._run_validation()
