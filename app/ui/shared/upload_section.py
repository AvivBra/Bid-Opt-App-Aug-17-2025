"""
app/ui/shared/upload_section.py
"""

"""Upload section UI component."""

import streamlit as st
from data.template_generator import TemplateGenerator
from data.readers.excel_reader import ExcelReader
from data.readers.csv_reader import CSVReader
from data.validators.template_validator import TemplateValidator
from data.validators.bulk_validator import BulkValidator
from app.state.bid_state import BidState
from app.ui.layout import create_section_header, create_status_message
from app.ui.components.buttons import create_primary_button, create_secondary_button
from utils.file_utils import validate_file_size, validate_file_extension
from config.ui_text import *


class UploadSection:
    """Handles file upload UI and processing."""

    def __init__(self):
        self.template_generator = TemplateGenerator()
        self.excel_reader = ExcelReader()
        self.csv_reader = CSVReader()
        self.template_validator = TemplateValidator()
        self.bulk_validator = BulkValidator()
        self.bid_state = BidState()

    def render(self):
        """Render the upload section."""

        create_section_header("Upload Files", "📤")

        # Create grid layout for upload buttons
        col1, col2 = st.columns(2)

        with col1:
            self._render_template_section()

        with col2:
            self._render_bulk_7_section()

        col3, col4 = st.columns(2)

        with col3:
            self._render_bulk_30_section()

        with col4:
            self._render_bulk_60_section()

        # Data Rova button (full width)
        self._render_data_rova_section()

        # File status display
        self._render_file_status()

    def _render_template_section(self):
        """Render template download and upload section."""

        # Download template button
        template_bytes = self.template_generator.generate_template()

        st.download_button(
            label=DOWNLOAD_TEMPLATE_BUTTON,
            data=template_bytes,
            file_name="bid_optimizer_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

        # Upload template
        template_file = st.file_uploader(
            "Upload Template",
            type=["xlsx"],
            key="template_uploader",
            help=TEMPLATE_UPLOAD_HELP,
        )

        if template_file:
            self._process_template_upload(template_file)

    def _render_bulk_7_section(self):
        """Render Bulk 7 Days section."""

        # Disabled button with coming soon message
        st.button(
            UPLOAD_BULK_7_BUTTON,
            disabled=True,
            use_container_width=True,
            help=BULK_7_TBC,
        )

    def _render_bulk_30_section(self):
        """Render Bulk 30 Days section."""

        # Disabled button with coming soon message
        st.button(
            UPLOAD_BULK_30_BUTTON,
            disabled=True,
            use_container_width=True,
            help=BULK_30_TBC,
        )

    def _render_bulk_60_section(self):
        """Render Bulk 60 Days section."""

        # Upload Bulk 60
        bulk_file = st.file_uploader(
            "Upload Bulk 60",
            type=["xlsx", "csv"],
            key="bulk_60_uploader",
            help=BULK_UPLOAD_HELP,
        )

        if bulk_file:
            self._process_bulk_upload(bulk_file, "bulk_60")

    def _render_data_rova_section(self):
        """Render Data Rova section."""

        st.button(
            "📊 Data Rova Integration",
            disabled=True,
            use_container_width=True,
            help="Coming in future phases",
        )

    def _render_file_status(self):
        """Display current file upload status."""

        st.markdown("---")

        # Template status - using direct session state access
        template_uploaded = st.session_state.get("template_uploaded", False)
        template_info = st.session_state.get("template_info", {})

        if template_uploaded and template_info:
            st.success(f"✓ Template: {template_info.get('filename', 'Uploaded')}")
            if template_info.get("portfolios"):
                st.caption(
                    f"Portfolios: {template_info['portfolios']} | Active: {template_info.get('active_portfolios', 0)}"
                )
        else:
            st.info("Template: Not uploaded")

        # Bulk 60 status - using direct session state access
        bulk_uploaded = st.session_state.get("bulk_60_uploaded", False)
        bulk_info = st.session_state.get("bulk_60_info", {})

        if bulk_uploaded and bulk_info:
            st.success(f"✓ Bulk 60: {bulk_info.get('filename', 'Uploaded')}")
            st.caption(
                f"Rows: {bulk_info.get('rows', 0):,} | Columns: {bulk_info.get('columns', 0)}"
            )
        else:
            st.info("Bulk 60: Not uploaded")

    def _process_template_upload(self, template_file):
        """Process uploaded template file."""

        # Validate file size
        size_valid, size_msg = validate_file_size(template_file, is_template=True)
        if not size_valid:
            st.error(size_msg)
            return

        # Validate file extension
        ext_valid, ext_msg = validate_file_extension(template_file.name, [".xlsx"])
        if not ext_valid:
            st.error(ext_msg)
            return

        try:
            # Read file data
            file_data = template_file.read()

            # Read and validate template
            success, msg, data_dict = self.excel_reader.read_template_file(file_data)

            if not success:
                st.error(f"Template Error: {msg}")
                return

            # Additional validation
            valid, validation_msg, validation_details = (
                self.template_validator.validate_complete(data_dict)
            )

            if not valid:
                st.error(f"Validation Error: {validation_msg}")
                if validation_details.get("issues"):
                    for issue in validation_details["issues"][
                        :3
                    ]:  # Show first 3 issues
                        st.error(f"• {issue}")
                return

            # Store in session state
            st.session_state.template_data = data_dict
            st.session_state.template_uploaded = True
            st.session_state.template_info = {
                "filename": template_file.name,
                "size_mb": len(file_data) / (1024 * 1024),
                "portfolios": validation_details["portfolio_count"],
                "active_portfolios": validation_details["portfolio_count"]
                - validation_details["ignore_count"],
                "ignored_portfolios": validation_details["ignore_count"],
            }

            st.success(validation_msg)

            # Show warnings if any
            if validation_details.get("warnings"):
                for warning in validation_details["warnings"]:
                    st.warning(f"⚠️ {warning}")

            st.rerun()

        except Exception as e:
            st.error(f"Error processing template: {str(e)}")

    def _process_bulk_upload(self, bulk_file, file_key: str):
        """Process uploaded bulk file."""

        # Validate file size
        size_valid, size_msg = validate_file_size(bulk_file, is_template=False)
        if not size_valid:
            st.error(size_msg)
            return

        # Validate file extension
        ext_valid, ext_msg = validate_file_extension(bulk_file.name, [".xlsx", ".csv"])
        if not ext_valid:
            st.error(ext_msg)
            return

        try:
            # Read file data
            file_data = bulk_file.read()
            is_csv = bulk_file.name.lower().endswith(".csv")

            # Read file based on type
            if is_csv:
                success, msg, dataframe = self.csv_reader.read_csv_file(
                    file_data, bulk_file.name
                )
            else:
                success, msg, dataframe = self.excel_reader.read_bulk_file(
                    file_data, bulk_file.name
                )

            if not success:
                st.error(f"Bulk File Error: {msg}")
                return

            # Simple validation without heavy analysis
            with st.spinner("Validating bulk file..."):
                valid, validation_msg, validation_details = (
                    self.bulk_validator.validate_complete(dataframe, bulk_file.name)
                )

            if not valid:
                st.error(f"Validation Error: {validation_msg}")
                if validation_details.get("issues"):
                    for issue in validation_details["issues"][:3]:
                        st.error(f"• {issue}")
                return

            # Store in session state directly (fixing the issue)
            st.session_state[f"{file_key}_data"] = dataframe
            st.session_state[f"{file_key}_uploaded"] = True
            st.session_state[f"{file_key}_info"] = {
                "filename": bulk_file.name,
                "size_mb": len(file_data) / (1024 * 1024),
                "rows": len(dataframe),
                "columns": len(dataframe.columns),
                "zero_sales_ready": validation_details.get("zero_sales_ready", False),
                "column_mapping": validation_details.get("column_mapping", {}),
            }

            st.success(validation_msg)

            # Show simple warnings if any
            if validation_details.get("warnings"):
                for warning in validation_details["warnings"][
                    :2
                ]:  # Show max 2 warnings
                    st.warning(f"⚠️ {warning}")

            st.rerun()

        except Exception as e:
            st.error(f"Error processing bulk file: {str(e)}")
