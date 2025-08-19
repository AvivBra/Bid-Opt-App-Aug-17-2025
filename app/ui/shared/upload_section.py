"""Upload section UI component."""

import streamlit as st
from data.template_generator import TemplateGenerator
from data.readers.excel_reader import ExcelReader
from data.readers.csv_reader import CSVReader
from data.validators.template_validator import TemplateValidator
from data.validators.bulk_validator import BulkValidator
from app.state.bid_state import BidState
from utils.file_utils import validate_file_size, validate_file_extension
from utils.filename_generator import generate_template_filename
from app.ui.layout import create_section_header, create_status_message


class UploadSection:
    """Handles file upload UI and processing."""
    
    def __init__(self):
        self.template_gen = TemplateGenerator()
        self.excel_reader = ExcelReader()
        self.csv_reader = CSVReader()
        self.template_validator = TemplateValidator()
        self.bulk_validator = BulkValidator()
        self.bid_state = BidState()
    
    def render(self):
        """Render the upload section."""
        
        create_section_header("Upload Files", "📁")
        
        # Template section
        st.markdown("#### Template File")
        self._render_template_section()
        
        st.markdown("---")
        
        # Bulk files section
        st.markdown("#### Bulk Files")
        self._render_bulk_section()
    
    def _render_template_section(self):
        """Render template upload/download section."""
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Download Template button
            if st.button("📥 Download Template", use_container_width=True, type="secondary"):
                template_data = self.template_gen.generate_template()
                st.download_button(
                    label="⬇️ Download Template.xlsx",
                    data=template_data,
                    file_name=generate_template_filename(),
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
        
        with col2:
            # Upload Template
            template_file = st.file_uploader(
                "Upload Template File",
                type=['xlsx'],
                key="template_uploader",
                help="Excel file with Port Values and Top ASINs sheets"
            )
        
        # Process uploaded template
        if template_file is not None:
            self._process_template_upload(template_file)
        
        # Show template status
        if st.session_state.get('template_uploaded', False):
            template_info = st.session_state.get('template_info', {})
            create_status_message(
                f"✓ Template loaded: {template_info.get('portfolios', 0)} portfolios",
                "success"
            )
    
    def _render_bulk_section(self):
        """Render bulk files upload section."""
        
        # Create tabs for different bulk files
        tab1, tab2, tab3 = st.tabs(["Bulk 60 (Active)", "Bulk 7 (TBC)", "Bulk 30 (TBC)"])
        
        with tab1:
            self._render_bulk_uploader("bulk_60", "Bulk 60 Days", active=True)
        
        with tab2:
            st.info("Bulk 7 days - Coming in future phases")
            self._render_bulk_uploader("bulk_7", "Bulk 7 Days", active=False)
        
        with tab3:
            st.info("Bulk 30 days - Coming in future phases") 
            self._render_bulk_uploader("bulk_30", "Bulk 30 Days", active=False)
    
    def _render_bulk_uploader(self, file_key: str, label: str, active: bool = True):
        """Render a bulk file uploader."""
        
        if active:
            bulk_file = st.file_uploader(
                f"Upload {label}",
                type=['xlsx', 'csv'],
                key=f"{file_key}_uploader",
                help="Excel or CSV file with Sponsored Products Campaigns data"
            )
            
            if bulk_file is not None:
                self._process_bulk_upload(bulk_file, file_key)
            
            # Show status
            if st.session_state.get(f'{file_key}_uploaded', False):
                bulk_info = st.session_state.get(f'{file_key}_info', {})
                create_status_message(
                    f"✓ {label} loaded: {bulk_info.get('rows', 0):,} rows",
                    "success"
                )
        else:
            st.button(f"📤 Upload {label}", disabled=True, use_container_width=True)
    
    def _process_template_upload(self, template_file):
        """Process uploaded template file."""
        
        # Validate file size
        size_valid, size_msg = validate_file_size(template_file, is_template=True)
        if not size_valid:
            st.error(size_msg)
            return
        
        # Validate file extension
        ext_valid, ext_msg = validate_file_extension(template_file.name, ['.xlsx'])
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
            valid, validation_msg, validation_details = self.template_validator.validate_complete(data_dict)
            
            if not valid:
                st.error(f"Validation Error: {validation_msg}")
                if validation_details.get('issues'):
                    for issue in validation_details['issues'][:3]:  # Show first 3 issues
                        st.error(f"• {issue}")
                return
            
            # Store in session state
            st.session_state.template_data = data_dict
            st.session_state.template_uploaded = True
            st.session_state.template_info = {
                'filename': template_file.name,
                'size_mb': len(file_data) / (1024 * 1024),
                'portfolios': validation_details['portfolio_count'],
                'active_portfolios': validation_details['portfolio_count'] - validation_details['ignore_count'],
                'ignored_portfolios': validation_details['ignore_count']
            }
            
            st.success(validation_msg)
            
            # Show warnings if any
            if validation_details.get('warnings'):
                for warning in validation_details['warnings']:
                    st.warning(f"⚠️ {warning}")
            
            st.rerun()
            
        except Exception as e:
            st.error(f"Error processing template: {str(e)}")
    
    def _process_bulk_upload(self, bulk_file, file_key: str):
        """Process uploaded bulk file with enhanced validation."""
        
        # Validate file size
        size_valid, size_msg = validate_file_size(bulk_file, is_template=False)
        if not size_valid:
            st.error(size_msg)
            return
        
        # Validate file extension
        ext_valid, ext_msg = validate_file_extension(bulk_file.name, ['.xlsx', '.csv'])
        if not ext_valid:
            st.error(ext_msg)
            return
        
        try:
            # Read file data
            file_data = bulk_file.read()
            is_csv = bulk_file.name.lower().endswith('.csv')
            
            # Read file based on type
            if is_csv:
                success, msg, dataframe = self.csv_reader.read_csv_file(file_data, bulk_file.name)
            else:
                success, msg, dataframe = self.excel_reader.read_bulk_file(file_data, bulk_file.name)
            
            if not success:
                st.error(f"Bulk File Error: {msg}")
                return
            
            # Enhanced validation with progress indicator
            with st.spinner("Validating bulk file data..."):
                st.write(f"🔍 Starting validation of {len(dataframe):,} rows × {len(dataframe.columns)} columns...")
                
                try:
                    valid, validation_msg, validation_details = self.bulk_validator.validate_complete(
                        dataframe, bulk_file.name
                    )
                    st.write("✅ Validation completed")
                except Exception as e:
                    st.error(f"Validation failed with error: {str(e)}")
                    st.error("Please check your bulk file format and try again")
                    return
            
            if not valid:
                st.error(f"Validation Error: {validation_msg}")
                if validation_details.get('issues'):
                    for issue in validation_details['issues']:
                        # Check if this is debug info (contains emoji and newlines)
                        if "📊 NULL VALUES DEBUG ANALYSIS:" in issue:
                            # Display debug info in an expandable section
                            with st.expander("🔍 Detailed Debug Information", expanded=True):
                                st.code(issue, language="text")
                        else:
                            # Display regular issues as errors
                            st.error(f"• {issue}")
                return
            
            # Store using BidState
            file_info = {
                'filename': bulk_file.name,
                'size_mb': len(file_data) / (1024 * 1024),
                'rows': len(dataframe),
                'columns': len(dataframe.columns),
                'zero_sales_ready': validation_details.get('zero_sales_ready', False),
                'column_mapping': validation_details.get('column_mapping', {})
            }
            
            self.bid_state.store_file_data(file_key, dataframe, file_info)
            
            st.success(validation_msg)
            
            # Show warnings if any
            if validation_details.get('warnings'):
                for warning in validation_details['warnings'][:3]:
                    st.warning(f"⚠️ {warning}")
            
            # Show debug information if available (even for successful validation)
            debug_info = validation_details.get('debug_info', {})
            if debug_info.get('debug_message'):
                with st.expander("🔍 Data Analysis (High Null Values Detected)", expanded=False):
                    st.code(debug_info['debug_message'], language="text")
                    st.info("ℹ️ High null percentages are normal in Amazon bulk files due to sparse data in optional columns.")
            
            # Show zero sales readiness
            if validation_details.get('zero_sales_ready'):
                st.info("✓ File is ready for Zero Sales optimization")
            else:
                st.warning("⚠️ File may not be suitable for Zero Sales optimization")
            
            st.rerun()
            
        except Exception as e:
            st.error(f"Error processing bulk file: {str(e)}")