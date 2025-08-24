"""Upload section UI component with fixed file handling."""

import streamlit as st
from io import BytesIO
import pandas as pd
from typing import Optional, Dict, Any
from data.template_generator import TemplateGenerator
from data.readers.excel_reader import ExcelReader
from data.validators.template_validator import TemplateValidator
from data.validators.bulk_validator import BulkValidator
from app.state.bid_state import BidState
from config.constants import MAX_FILE_SIZE_MB, MAX_TEMPLATE_SIZE_MB, REQUIRED_COLUMNS


class UploadSection:
    """Component for handling file uploads."""

    def __init__(self):
        """Initialize upload section."""
        self.template_generator = TemplateGenerator()
        self.excel_reader = ExcelReader()
        self.template_validator = TemplateValidator()
        self.bulk_validator = BulkValidator()
        self.bid_state = BidState()

    def render(self) -> None:
        """Render the upload section."""
        st.markdown("### Upload Files")
        st.markdown("---")

        # Template section
        self._render_template_section()

        # Bulk files section
        self._render_bulk_section()

        # Status display
        self._display_upload_status()

    def _render_template_section(self) -> None:
        """Render template upload section."""
        col1, col2 = st.columns(2)

        with col1:
            # Download Template button
            if st.button("Download Template", use_container_width=True):
                template_bytes = self.template_generator.create_template()
                st.download_button(
                    label="Save Template",
                    data=template_bytes,
                    file_name="template.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                )

        with col2:
            # Upload Template
            uploaded_file = st.file_uploader(
                "Upload Template",
                type=["xlsx"],
                key="template_upload",
                help="Upload your Template file with portfolio settings",
            )

            if uploaded_file is not None:
                self._process_template_upload(uploaded_file)

    def _render_bulk_section(self) -> None:
        """Render bulk files upload section with dynamic enable/disable based on selection."""

        # Get active bulk type from session state
        active_bulk_type = st.session_state.get("active_bulk_type", None)

        col1, col2, col3 = st.columns(3)

        with col1:
            # Bulk 60 - enabled only if bulk_type is "60"
            if active_bulk_type == "60":
                uploaded_file = st.file_uploader(
                    "Upload Bulk 60",
                    type=["xlsx", "csv"],
                    key="bulk_60_upload",
                    help="Upload your 60-day Bulk file from Amazon Ads",
                )

                if uploaded_file is not None:
                    self._process_bulk_upload(uploaded_file, "60")
            else:
                st.markdown("##### Bulk 60")
                st.button(
                    "Select Zero Sales first"
                    if active_bulk_type != "60"
                    else "Disabled",
                    disabled=True,
                    use_container_width=True,
                    key="bulk_60_disabled",
                )

        with col2:
            # Bulk 30 - enabled only if bulk_type is "30"
            if active_bulk_type == "30":
                uploaded_file = st.file_uploader(
                    "Upload Bulk 30",
                    type=["xlsx", "csv"],
                    key="bulk_30_upload",
                    help="Upload your 30-day Bulk file from Amazon Ads",
                )

                if uploaded_file is not None:
                    self._process_bulk_upload(uploaded_file, "30")
            else:
                st.markdown("##### Bulk 30")
                st.button(
                    "Select Bids 30 Days first"
                    if active_bulk_type != "30"
                    else "Coming Soon",
                    disabled=True,
                    use_container_width=True,
                    key="bulk_30_disabled",
                )

        with col3:
            # Bulk 7 (disabled - future feature)
            st.markdown("##### Bulk 7")
            st.button(
                "Coming Soon",
                disabled=True,
                use_container_width=True,
                key="bulk_7_disabled",
            )

        # Data Rova (disabled - future feature)
        st.markdown("##### Data Rova Integration")
        st.button(
            "Coming Soon",
            disabled=True,
            use_container_width=True,
            key="data_rova_disabled",
        )

    def _process_template_upload(self, uploaded_file) -> None:
        """Process uploaded template file."""
        try:
            # Check file size
            file_size_mb = uploaded_file.size / (1024 * 1024)
            if file_size_mb > MAX_TEMPLATE_SIZE_MB:
                st.error(f"File exceeds {MAX_TEMPLATE_SIZE_MB}MB limit")
                return

            # Read file into BytesIO
            file_bytes = BytesIO(uploaded_file.read())

            # Validate template structure
            is_valid, message, dataframes = self.template_validator.validate(file_bytes)

            if not is_valid:
                st.error(f"Validation Error: {message}")
                return

            # Save to state
            if dataframes and "Port Values" in dataframes:
                self.bid_state.save_template(file_bytes, dataframes["Port Values"])
                st.success(f"{uploaded_file.name} uploaded successfully")
            else:
                st.error("Error processing template: Invalid data structure")

        except Exception as e:
            st.error(f"Error processing template: {str(e)}")

    def _process_bulk_upload(self, uploaded_file, bulk_type: str) -> None:
        """Process uploaded bulk file."""
        try:
            # Check file size
            file_size_mb = uploaded_file.size / (1024 * 1024)
            if file_size_mb > MAX_FILE_SIZE_MB:
                st.error(f"File exceeds {MAX_FILE_SIZE_MB}MB limit")
                return

            # Read file based on type
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(
                    uploaded_file, sheet_name="Sponsored Products Campaigns"
                )

            # Validate bulk file
            is_valid, message = self.bulk_validator.validate(df)

            if not is_valid:
                st.error(f"Validation Error: {message}")
                return

            # Save to state
            file_bytes = BytesIO(uploaded_file.read())
            uploaded_file.seek(0)  # Reset file pointer
            self.bid_state.save_bulk(bulk_type, file_bytes, df)
            st.success(f"{uploaded_file.name} uploaded successfully")
            st.info(f"{len(df):,} rows loaded")

        except Exception as e:
            st.error(f"Error processing bulk file: {str(e)}")

    def _display_upload_status(self) -> None:
        """Display current upload status."""
        if (
            self.bid_state.has_template()
            or self.bid_state.has_bulk("60")
            or self.bid_state.has_bulk("30")
        ):
            st.markdown("---")
            st.markdown("#### Uploaded Files")

            if self.bid_state.has_template():
                st.success("Template file uploaded")

            if self.bid_state.has_bulk("60"):
                bulk_df = self.bid_state.get_bulk("60")
                if bulk_df is not None:
                    st.success(f"Bulk 60 file uploaded ({len(bulk_df):,} rows)")

            if self.bid_state.has_bulk("30"):
                bulk_df = self.bid_state.get_bulk("30")
                if bulk_df is not None:
                    st.success(f"Bulk 30 file uploaded ({len(bulk_df):,} rows)")


# Standalone functions for backward compatibility
def render() -> None:
    """Render the upload section."""
    section = UploadSection()
    section.render()


def process_template_upload(uploaded_file) -> bool:
    """Process template upload."""
    section = UploadSection()
    section._process_template_upload(uploaded_file)
    return True


def process_bulk_upload(uploaded_file, bulk_type: str) -> bool:
    """Process bulk upload."""
    section = UploadSection()
    section._process_bulk_upload(uploaded_file, bulk_type)
    return True
