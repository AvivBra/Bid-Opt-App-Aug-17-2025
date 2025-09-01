"""Portfolio Optimizer page component."""

import streamlit as st
import pandas as pd
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from io import BytesIO

# Business logic imports
from business.portfolio_optimizations.factory import get_portfolio_optimization_factory
from business.portfolio_optimizations.orchestrator import (
    PortfolioOptimizationOrchestrator,
)
from business.portfolio_optimizations.service import PortfolioOptimizationService

# State management imports
from app.state.portfolio_state import PortfolioState

# Data handling imports - removed ExcelReader as it doesn't have the methods we need
from data.validators.bulk_validator import BulkValidator
from data.template_generator import TemplateGenerator
from data.readers.excel_reader import ExcelReader

# UI component imports - FIXED: Creating wrapper functions for alerts
from app.ui.components.alerts import show_validation_alert


# Create wrapper functions for backward compatibility
def show_success(message: str):
    """Wrapper for success alert."""
    show_validation_alert("success", message)


def show_error(message: str):
    """Wrapper for error alert."""
    show_validation_alert("error", message)


def show_warning(message: str):
    """Wrapper for warning alert."""
    show_validation_alert("warning", message)


def show_info(message: str):
    """Wrapper for info alert."""
    show_validation_alert("info", message)


from app.ui.components.download_buttons import create_download_button
from app.ui.components.file_cards import render_file_card


# Create wrapper function for display_file_card
def display_file_card(filename: str, size_or_sheets: Any, details: Any = None):
    """Wrapper for render_file_card to match expected interface."""
    if isinstance(size_or_sheets, int):
        # It's number of sheets
        render_file_card(
            title="BULK 60",
            file_name=filename,
            status="uploaded",
            details={"Sheets": size_or_sheets},
        )
    else:
        # It's file size
        size_mb = size_or_sheets / (1024 * 1024) if size_or_sheets else 0
        render_file_card(
            title="BULK 60",
            file_name=filename,
            status="uploaded",
            details={
                "Size": f"{size_mb:.1f} MB",
                "Sheets": details if details else "N/A",
            },
        )


# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s [PortfolioOptimizer] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class PortfolioOptimizerPage:
    """Portfolio Optimizer page component."""

    def __init__(self):
        self.logger = logging.getLogger("PortfolioOptimizer")
        self.factory = get_portfolio_optimization_factory()
        self.orchestrator = PortfolioOptimizationOrchestrator()
        self.service = PortfolioOptimizationService()
        self.validator = BulkValidator()
        
        # Initialize proper state management
        self.state = PortfolioState()
        self.state.init()
        
        # Template generation
        self.template_generator = TemplateGenerator()
        self.excel_reader = ExcelReader()

    def _init_session_state(self):
        """Initialize session state variables using proper state management."""
        # State is now managed by PortfolioState class
        # This method maintained for backward compatibility but delegates to state manager
        self.state.init()

    def render(self):
        """Render the Portfolio Optimizer page."""
        # Import and apply custom CSS
        from app.ui.layout import apply_custom_css

        apply_custom_css()

        # Create 6 columns layout: [col1 | col2 | col3 | col4 | col5 | col6]
        # Same layout as other pages
        col1, col2, col3, col4, col5, col6 = st.columns([1, 7, 1, 1, 6, 2])

        # TITLE IN SECOND COLUMN FROM LEFT (same as other pages)
        with col2:
            st.markdown(
                "<h1 style='text-align: left;'>Portfolio<br>Optimizer</h1>",
                unsafe_allow_html=True,
            )

        # ALL CONTENT IN FIFTH COLUMN (SECOND FROM RIGHT) - same as other pages
        with col5:
            self._render_optimization_selection()
            # Remove extra line break - spacing is handled inside _render_optimization_selection
            self._render_file_upload()
            st.markdown("<br>", unsafe_allow_html=True)
            self._render_process_section()
            st.markdown("<br>", unsafe_allow_html=True)
            self._render_download_section()

    def _render_optimization_selection(self):
        """Render optimization selection section."""
        st.markdown(
            "<h3 style='text-align: left;'>1.Select Optimization</h3>",
            unsafe_allow_html=True,
        )

        # Get available optimizations
        available_optimizations = self.factory.get_enabled_optimizations()

        # Track selected optimizations
        selected = []

        # Generate checkboxes
        for opt_name, opt_info in available_optimizations.items():
            display_name = opt_info.get("display_name", opt_name)
            description = opt_info.get("description", "")

            is_selected = st.checkbox(
                display_name,
                value=opt_name in st.session_state.get("portfolio_selected_optimizations", []),
                key=f"portfolio_opt_{opt_name}",
                help=description,
            )

            if is_selected:
                selected.append(opt_name)

        # Update session state
        st.session_state.portfolio_selected_optimizations = selected

        # Update status
        if selected:
            if st.session_state.get("portfolio_status") == "waiting_for_selection":
                st.session_state.portfolio_status = "waiting_for_file"

        # Add spacing like in other pages
        st.markdown(
            """
            <div style='height: 150px;'></div>
            """,
            unsafe_allow_html=True,
        )

    def _render_file_upload(self):
        """Render file upload section."""
        st.markdown(
            "<h3 style='text-align: left;'>2.Upload Files</h3>",
            unsafe_allow_html=True,
        )

        # Check if Organize Top Campaigns is selected
        selected_optimizations = st.session_state.get("portfolio_selected_optimizations", [])
        organize_top_campaigns_selected = "organize_top_campaigns" in selected_optimizations

        # Template section for Organize Top Campaigns
        if organize_top_campaigns_selected:
            self._render_template_section()

        # File uploader
        uploaded_file = st.file_uploader(
            "Upload Bulk 60 File",
            type=["xlsx", "xls"],
            key="portfolio_file_upload",
            help="Upload your Amazon Ads Bulk 60 file",
        )

        if uploaded_file:
            # Process uploaded file
            # Check if this is a different file than what's already processed
            current_file = st.session_state.get("portfolio_original_file")
            if current_file != uploaded_file:
                with st.spinner("Reading file..."):
                    self._process_uploaded_file(uploaded_file)

            # Display file info
            if st.session_state.portfolio_sheets:
                display_file_card(
                    uploaded_file.name,
                    uploaded_file.size,
                    len(st.session_state.portfolio_sheets),
                )

    def _process_uploaded_file(self, uploaded_file):
        """Process the uploaded file."""
        try:
            # Read Excel file - Portfolio Optimizer needs all sheets
            # Using pandas directly as ExcelReader doesn't have read_all_sheets
            sheets = pd.read_excel(uploaded_file, sheet_name=None)

            # Validate file structure
            required_sheets = ["Sponsored Products Campaigns", "Portfolios"]
            missing_sheets = [s for s in required_sheets if s not in sheets]

            if missing_sheets:
                show_error(f"Missing required sheets: {', '.join(missing_sheets)}")
                st.session_state.portfolio_status = "validation_failed"
                return

            # Store in session state
            st.session_state.portfolio_original_file = uploaded_file
            st.session_state.portfolio_sheets = sheets
            st.session_state.portfolio_filename = uploaded_file.name
            st.session_state.portfolio_upload_time = datetime.now()

            # Update status
            if st.session_state.portfolio_selected_optimizations:
                st.session_state.portfolio_status = "ready_to_process"

            show_success(f"File uploaded successfully! Found {len(sheets)} sheets")

            # Display file info
            display_file_card(uploaded_file.name, uploaded_file.size, len(sheets))

        except Exception as e:
            self.logger.error(f"Error processing file: {str(e)}")
            show_error(f"Error processing file: {str(e)}")
            st.session_state.portfolio_status = "upload_failed"
    
    def _render_template_section(self):
        """Render template download and upload section for Organize Top Campaigns."""
        st.markdown("#### Template for Top ASINs")
        
        # Template download button
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("Download Template", type="secondary", use_container_width=True):
                try:
                    template_bytes = self.template_generator.generate_top_asins_template()
                    st.download_button(
                        label="Click to download template",
                        data=template_bytes,
                        file_name="Top_ASINs_Template.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    show_success("Template generated successfully! Click the download link above.")
                except Exception as e:
                    show_error(f"Error generating template: {str(e)}")
        
        # Template upload
        template_file = st.file_uploader(
            "Upload Filled Template",
            type=["xlsx", "xls"],
            key="portfolio_template_upload",
            help="Upload your filled Top ASINs template",
        )
        
        if template_file:
            try:
                success, message, template_df = self.excel_reader.read_top_asins_template(
                    template_file.getvalue(), template_file.name
                )
                
                if success:
                    # Save to state
                    from app.state.portfolio_state import save_portfolio_template_data
                    save_portfolio_template_data(BytesIO(template_file.getvalue()), template_df)
                    show_success(message)
                    
                    # Display template info
                    st.info(f"✅ Template uploaded: {len(template_df)} ASINs")
                else:
                    show_error(message)
                    
            except Exception as e:
                show_error(f"Error processing template: {str(e)}")
        
        st.markdown("---")

    def _render_process_section(self):
        """Render process files section."""
        st.markdown(
            "<h3 style='text-align: left;'>3.Process Files</h3>",
            unsafe_allow_html=True,
        )

        # Check if ready to process
        selected_optimizations = st.session_state.get("portfolio_selected_optimizations", [])
        has_bulk_file = st.session_state.get("portfolio_sheets")
        has_template = st.session_state.get("portfolio_template_uploaded", False)
        
        # For Organize Top Campaigns, we need both bulk file and template
        organize_top_campaigns_selected = "organize_top_campaigns" in selected_optimizations
        template_required = organize_top_campaigns_selected and not has_template
        
        can_process = (
            selected_optimizations
            and has_bulk_file
            and not template_required
            and st.session_state.get("portfolio_status") == "ready_to_process"
        )

        # Process button
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            if st.button(
                "Process Optimizations",
                type="primary",
                use_container_width=True,
                disabled=st.session_state.get("portfolio_status") == "processing",
            ):
                self._process_optimizations()

        # Show status messages
        if not selected_optimizations:
            show_info("Please select at least one optimization")
        elif not has_bulk_file:
            show_info("Please upload a Bulk 60 file")
        elif template_required:
            show_info("Please upload a template file for Organize Top Campaigns")

    def _process_optimizations(self):
        """Process selected optimizations."""
        try:
            # Update status
            st.session_state.portfolio_status = "processing"
            st.session_state.portfolio_current_step = "starting"

            # Show progress
            progress_bar = st.progress(0, text="Starting optimization...")

            # Get selected optimizations
            selected = st.session_state.get("portfolio_selected_optimizations", [])
            self.logger.info(f"Processing {len(selected)} optimizations: {selected}")

            # Update progress
            progress_bar.progress(20, text="Validating data...")
            st.session_state.portfolio_current_step = "validating"

            # Handle template data for Organize Top Campaigns
            if "organize_top_campaigns" in selected:
                from app.state.portfolio_state import get_portfolio_template_data
                template_data = get_portfolio_template_data()
                if template_data is not None:
                    # Set template data on the strategy before running
                    strategy = self.factory.create_strategy("organize_top_campaigns")
                    if strategy and hasattr(strategy, 'set_template_data'):
                        strategy.set_template_data(template_data)

            # Run optimizations
            progress_bar.progress(40, text="Running optimizations...")
            st.session_state.portfolio_current_step = "optimizing"

            merged_data, run_report = self.orchestrator.run_optimizations(
                st.session_state.get("portfolio_sheets", {}), selected
            )

            # Store results
            st.session_state.portfolio_merged_data = merged_data
            st.session_state.portfolio_run_report = run_report

            # According to the architecture, updated_indices comes from results_manager
            # and should be stored separately or accessed through merge_report
            # For now, we'll create an empty dict if not available
            updated_indices = getattr(run_report, "updated_indices", {})
            if not updated_indices:
                # Try to get from optimization_details if available
                if hasattr(run_report, "optimization_details"):
                    # Extract updated indices from optimization details if possible
                    updated_indices = {}
                    for sheet in merged_data.keys():
                        updated_indices[sheet] = []

            st.session_state.portfolio_updated_indices = updated_indices

            # Create output file
            progress_bar.progress(80, text="Creating output file...")
            st.session_state.portfolio_current_step = "creating_file"

            output_bytes = self.orchestrator.create_output_file(
                merged_data, updated_indices
            )

            # Store output
            st.session_state.portfolio_output_file = output_bytes
            st.session_state.portfolio_output_filename = (
                self.service.generate_filename()  # Using service's method
            )
            st.session_state.portfolio_output_created_at = datetime.now()

            # Update status
            progress_bar.progress(100, text="Complete!")
            st.session_state.portfolio_status = "ready_for_download"

            # Show success message
            show_success(
                f"Successfully processed {run_report.successful_optimizations} optimizations. "
                f"Updated {run_report.total_rows_updated} rows."
            )

            # Show any conflicts
            if run_report.conflicts:
                show_warning(
                    f"Found {len(run_report.conflicts)} conflicts (last value was used)"
                )

            # Rerun to update UI
            st.rerun()

        except Exception as e:
            self.logger.error(f"Error processing optimizations: {str(e)}")
            show_error(f"Processing failed: {str(e)}")
            st.session_state.portfolio_status = "processing_failed"

    def _render_download_section(self):
        """Render download section."""
        st.markdown(
            "<h3 style='text-align: left;'>4.Download Results</h3>",
            unsafe_allow_html=True,
        )

        # Show statistics
        if "portfolio_run_report" in st.session_state and st.session_state.get("portfolio_run_report"):
            report = st.session_state.portfolio_run_report

            col1, col2, col3 = st.columns(3)
            with col1:
                # Handle missing total_rows attribute gracefully
                total_rows = getattr(report, 'total_rows', report.total_rows_updated)
                st.metric("Total Rows", f"{total_rows:,}")
            with col2:
                st.metric("Rows Updated", f"{report.total_rows_updated:,}")
            with col3:
                st.metric("Optimizations Applied", report.successful_optimizations)

        # Download button
        if st.session_state.get("portfolio_output_file"):
            create_download_button(
                label="Download Optimized File",
                data=st.session_state.portfolio_output_file,
                file_name=st.session_state.get("portfolio_output_filename", "portfolio_optimized.xlsx"),
            )

            # Show success message
            show_validation_alert(
                "success", "Your optimized file is ready for download!"
            )

        # Reset button
        st.markdown("---")
        if st.button("Start New Optimization"):
            self._reset_state()
            st.rerun()

    def _reset_state(self):
        """Reset all portfolio optimizer state."""
        keys_to_reset = [
            "portfolio_selected_optimizations",
            "portfolio_original_file",
            "portfolio_sheets",
            "portfolio_status",
            "portfolio_output_file",
            "portfolio_merged_data",
            "portfolio_run_report",
            "portfolio_updated_indices",
            "portfolio_output_filename",
            "portfolio_output_created_at",
            "portfolio_current_step",
            "portfolio_filename",
            "portfolio_upload_time",
        ]

        for key in keys_to_reset:
            if key in st.session_state:
                del st.session_state[key]

        # Re-initialize
        self._init_session_state()
