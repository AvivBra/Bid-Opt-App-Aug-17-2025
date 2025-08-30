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

# Data handling imports
from data.readers.excel_reader import ExcelReader
from data.validators.bulk_validator import BulkValidator

# UI component imports
from app.ui.components.alerts import show_success, show_error, show_warning, show_info
from app.ui.components.download_buttons import create_download_button
from app.ui.components.file_cards import display_file_card
from app.ui.components.progress_bar import show_progress

# Utils
from utils.filename_generator import generate_filename


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
        self.excel_reader = ExcelReader()
        self.validator = BulkValidator()

        # Initialize session state
        self._init_session_state()

    def _init_session_state(self):
        """Initialize session state variables."""
        if "portfolio_selected_optimizations" not in st.session_state:
            st.session_state.portfolio_selected_optimizations = []
        if "portfolio_original_file" not in st.session_state:
            st.session_state.portfolio_original_file = None
        if "portfolio_sheets" not in st.session_state:
            st.session_state.portfolio_sheets = None
        if "portfolio_status" not in st.session_state:
            st.session_state.portfolio_status = "waiting_for_selection"
        if "portfolio_output_file" not in st.session_state:
            st.session_state.portfolio_output_file = None

    def render(self):
        """Render the Portfolio Optimizer page."""

        # Import and apply custom CSS
        from app.ui.layout import apply_custom_css

        apply_custom_css()

        # Create layout
        col1, col2, col3, col4, col5, col6 = st.columns([1, 7, 1, 1, 6, 2])

        # Title in second column
        with col2:
            st.markdown(
                "<h1 style='text-align: left;'>Portfolio<br>Optimizer</h1>",
                unsafe_allow_html=True,
            )

        # Main content in fifth column
        with col5:
            self._render_optimization_selection()
            st.markdown("<br>", unsafe_allow_html=True)
            self._render_file_upload()
            st.markdown("<br>", unsafe_allow_html=True)
            self._render_process_section()
            st.markdown("<br>", unsafe_allow_html=True)
            self._render_download_section()

    def _render_optimization_selection(self):
        """Render optimization selection section."""
        st.markdown(
            "<h3 style='text-align: left;'>1. Select Optimization</h3>",
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
                value=opt_name in st.session_state.portfolio_selected_optimizations,
                key=f"portfolio_opt_{opt_name}",
                help=description,
            )

            if is_selected:
                selected.append(opt_name)

        # Update session state
        st.session_state.portfolio_selected_optimizations = selected

        # Update status
        if selected:
            if st.session_state.portfolio_status == "waiting_for_selection":
                st.session_state.portfolio_status = "waiting_for_file"

    def _render_file_upload(self):
        """Render file upload section."""
        st.markdown(
            "<h3 style='text-align: left;'>2. Upload Files</h3>",
            unsafe_allow_html=True,
        )

        # File uploader
        uploaded_file = st.file_uploader(
            "Upload Bulk 60 File",
            type=["xlsx", "xls"],
            key="portfolio_file_upload",
            help="Upload your Amazon Ads Bulk 60 file",
        )

        if uploaded_file:
            # Process uploaded file
            if st.session_state.portfolio_original_file != uploaded_file:
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
            # Read Excel file
            sheets = self.excel_reader.read_excel(uploaded_file)

            # Validate file
            is_valid, message = self.validator.validate_bulk_file(sheets)

            if is_valid:
                # Store in session state
                st.session_state.portfolio_original_file = uploaded_file
                st.session_state.portfolio_sheets = sheets
                st.session_state.portfolio_filename = uploaded_file.name
                st.session_state.portfolio_upload_time = datetime.now()

                # Update status
                if st.session_state.portfolio_selected_optimizations:
                    st.session_state.portfolio_status = "ready_to_process"

                show_success("File uploaded successfully!")
            else:
                show_error(f"File validation failed: {message}")
                st.session_state.portfolio_status = "validation_failed"

        except Exception as e:
            self.logger.error(f"Error processing file: {str(e)}")
            show_error(f"Error processing file: {str(e)}")
            st.session_state.portfolio_status = "upload_failed"

    def _render_process_section(self):
        """Render process files section."""
        st.markdown(
            "<h3 style='text-align: left;'>3. Process Files</h3>",
            unsafe_allow_html=True,
        )

        # Check if ready to process
        can_process = (
            st.session_state.portfolio_selected_optimizations
            and st.session_state.portfolio_sheets
            and st.session_state.portfolio_status == "ready_to_process"
        )

        # Process button
        if st.button(
            "Process Files",
            disabled=not can_process,
            key="portfolio_process_button",
            use_container_width=True,
        ):
            self._process_optimizations()

        # Show status messages
        if not st.session_state.portfolio_selected_optimizations:
            show_info("Please select at least one optimization")
        elif not st.session_state.portfolio_sheets:
            show_info("Please upload a Bulk 60 file")

    def _process_optimizations(self):
        """Process the selected optimizations."""
        try:
            # Update status
            st.session_state.portfolio_status = "processing"
            st.session_state.portfolio_current_step = "starting"

            # Show progress
            progress_bar = st.progress(0, text="Starting optimization...")

            # Get selected optimizations
            selected = st.session_state.portfolio_selected_optimizations
            self.logger.info(f"Processing {len(selected)} optimizations: {selected}")

            # Update progress
            progress_bar.progress(20, text="Validating data...")
            st.session_state.portfolio_current_step = "validating"

            # Run optimizations
            progress_bar.progress(40, text="Running optimizations...")
            st.session_state.portfolio_current_step = "optimizing"

            merged_data, run_report = self.orchestrator.run_optimizations(
                st.session_state.portfolio_sheets, selected
            )

            # Store results
            st.session_state.portfolio_merged_data = merged_data
            st.session_state.portfolio_run_report = run_report
            st.session_state.portfolio_updated_indices = run_report.updated_indices

            # Create output file
            progress_bar.progress(80, text="Creating output file...")
            st.session_state.portfolio_current_step = "creating_file"

            output_bytes = self.orchestrator.create_output_file(
                merged_data, run_report.updated_indices
            )

            # Store output
            st.session_state.portfolio_output_file = output_bytes
            st.session_state.portfolio_output_filename = (
                self.service.generate_filename()
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
            "<h3 style='text-align: left;'>4. Download Results</h3>",
            unsafe_allow_html=True,
        )

        if st.session_state.portfolio_output_file:
            # Create download button
            st.download_button(
                label="📥 Download Optimized File",
                data=st.session_state.portfolio_output_file,
                file_name=st.session_state.portfolio_output_filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="portfolio_download_button",
                use_container_width=True,
            )

            # Show file info
            if st.session_state.portfolio_run_report:
                report = st.session_state.portfolio_run_report
                st.markdown(f"""
                **Optimization Summary:**
                - Optimizations run: {report.successful_optimizations}/{report.total_optimizations}
                - Rows updated: {report.total_rows_updated}
                - Processing time: {report.execution_time_seconds:.1f} seconds
                """)
        else:
            st.info("Process files to generate download")


# Create page instance
page = PortfolioOptimizerPage()
