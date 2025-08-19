"""Bid Optimizer main page."""

import streamlit as st
from app.ui.layout import create_card_container, center_content, create_status_message
from app.ui.shared.upload_section import UploadSection
from app.ui.shared.validation_section import ValidationSection
from app.ui.components.buttons import create_action_buttons
from app.state.bid_state import BidState
from config.settings import settings
from config.ui_text import WELCOME_MESSAGE, WELCOME_SUBTITLE


class BidOptimizerPage:
    """Main page for Bid Optimization functionality."""
    
    def __init__(self):
        self.upload_section = UploadSection()
        self.validation_section = ValidationSection()
        self.bid_state = BidState()
    
    def render(self):
        """Render the Bid Optimizer page."""
        
        # Page title
        st.title(settings.app_title)
        
        # Center the main content
        center_content(self._render_content)
    
    def _render_content(self):
        """Render the main page content."""
        
        # Welcome message
        st.markdown(f"### {WELCOME_MESSAGE}")
        create_status_message(WELCOME_SUBTITLE, "info")
        
        # Upload Files Section
        st.markdown("<br>", unsafe_allow_html=True)
        create_card_container(self.upload_section.render, "upload-card")
        
        # Show action buttons if files are uploaded
        if self._has_files():
            st.markdown("---")
            actions = create_action_buttons()
            
            # Handle button actions
            if actions.get('reset'):
                self._handle_reset()
            
            if actions.get('process'):
                self._handle_process()
            
            if actions.get('help'):
                self._show_help()
        
        # Data Validation Section
        if self.bid_state.has_required_files():
            st.markdown("<br>", unsafe_allow_html=True)
            create_card_container(self.validation_section.render, "validation-card")
        
        # Output Files Section (placeholder)
        def output_section():
            st.markdown("#### 📊 Output Files")
            st.info("Output generation coming in Phase 7...")
            
            col1, col2 = st.columns(2)
            with col1:
                st.button("📥 Download Working File", disabled=True, use_container_width=True)
            with col2:
                st.button("📥 Download Clean File", disabled=True, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        create_card_container(output_section, "output-card")
    
    def _has_files(self) -> bool:
        """Check if any files are uploaded."""
        return (st.session_state.get('template_uploaded', False) or 
                st.session_state.get('bulk_60_uploaded', False))
    
    def _handle_reset(self):
        """Handle reset button click."""
        # Clear file-related session state
        file_keys = [
            'template_uploaded', 'template_data', 'template_info',
            'bulk_60_uploaded', 'bulk_60_data', 'bulk_60_info',
            'bulk_7_uploaded', 'bulk_7_data', 'bulk_7_info',
            'bulk_30_uploaded', 'bulk_30_data', 'bulk_30_info'
        ]
        
        for key in file_keys:
            if key in st.session_state:
                del st.session_state[key]
        
        st.success("Session reset successfully")
        st.rerun()
    
    def _handle_process(self):
        """Handle process files button click."""
        st.info("File processing coming in Phase 6...")
    
    def _show_help(self):
        """Show help information."""
        with st.expander("📖 Help & Instructions", expanded=True):
            st.markdown("""
            **Getting Started:**
            1. Download the template file and fill in your portfolio data
            2. Upload your completed template file
            3. Upload your Bulk 60 days file from Amazon Ads
            4. Click 'Process Files' to run Zero Sales optimization
            
            **Template Requirements:**
            - Portfolio Name: Must match names in Bulk file
            - Base Bid: 0.02-4.00 or 'Ignore' to skip
            - Target CPA: 0.01-4.00 or leave empty
            
            **Bulk File Requirements:**
            - Excel file with 'Sponsored Products Campaigns' sheet
            - Maximum 500,000 rows
            - Must contain Units and Portfolio columns
            """)
            
            st.info("For more detailed help, refer to the documentation.")