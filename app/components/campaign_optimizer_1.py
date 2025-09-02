"""Campaign Optimizer 1 page component."""

import streamlit as st
import pandas as pd
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from io import BytesIO

# Business logic imports
from business.campaign_optimizer_1.orchestrator import CampaignOptimizer1Orchestrator

# State management imports
from app.state.campaign_optimizer_1_state import CampaignOptimizer1State

# Data handling imports
from data.validators.campaign_optimizer_1_validators import CampaignOptimizer1Validator
from data.readers.excel_reader import ExcelReader

# UI component imports
from app.ui.components.alerts import show_validation_alert

# Create wrapper functions for alerts
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
from utils.filename_generator import generate_campaign_optimizer_1_filename

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def render_campaign_optimizer_1():
    """
    Render the Campaign Optimizer 1 page.
    
    UI Flow:
    1. Display "7 Days Budgets" checkbox
    2. When checked, show file upload section
    3. After upload and validation, show "Bulk 7" button  
    4. Process file and show download button
    """
    # Initialize state
    state = CampaignOptimizer1State()
    
    # Page header
    st.title("Campaign Optimizer 1")
    st.markdown("Optimize campaign budgets based on 7-day performance data")
    
    # Step 1: Checkbox selection
    render_checkbox_section(state)
    
    # Step 2: File upload (only if checkbox selected)
    if state.is_ready_for_upload():
        render_file_upload_section(state)
    
    # Step 3: Processing (only if file uploaded and validated)
    if state.is_ready_for_processing():
        render_processing_section(state)
    
    # Step 4: Results download (only if processing complete)
    if state.can_download_results():
        render_download_section(state)


def render_checkbox_section(state: CampaignOptimizer1State):
    """Render the checkbox selection section."""
    st.markdown("### Select Optimization Type")
    
    # 7 Days Budgets checkbox
    seven_days_selected = st.checkbox(
        "7 Days Budgets",
        value=state.is_seven_days_budgets_selected(),
        help="Optimize campaign budgets based on 7-day performance metrics (Units, ACOS, Daily Budget)"
    )
    
    # Update state
    state.set_seven_days_budgets_selected(seven_days_selected)
    
    if seven_days_selected:
        st.markdown("✅ **7 Days Budgets optimization selected**")
        st.markdown("This will apply 4-step budget optimization logic based on Units, ACOS (0.17 threshold), and Daily Budget.")
    else:
        st.markdown("Please select an optimization type to continue.")


def render_file_upload_section(state: CampaignOptimizer1State):
    """Render the file upload section."""
    st.markdown("### Upload Campaign Data")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose Excel file",
        type=['xlsx'],
        help="Upload your campaign data Excel file containing 'Sponsored Products Campaigns' sheet"
    )
    
    if uploaded_file is not None:
        try:
            # Store file data
            file_bytes = uploaded_file.read()
            state.set_input_file(file_bytes, uploaded_file.name)
            
            # Validate file
            validator = CampaignOptimizer1Validator()
            validation_result = validator.validate_input_file(file_bytes)
            
            if validation_result.is_valid:
                state.set_validation_result(True, [])
                show_success(f"✅ File '{uploaded_file.name}' uploaded and validated successfully!")
                
                # Show file info
                reader = ExcelReader()
                try:
                    success, message, bulk_df = reader.read_bulk_file(file_bytes, uploaded_file.name)
                    if success:
                        campaign_count = len(bulk_df)
                        st.info(f"📊 Found {campaign_count:,} total rows in bulk file")
                    else:
                        st.warning(f"⚠️ {message}")
                except Exception as e:
                    logger.warning(f"Could not read sheet info: {e}")
                    
            else:
                state.set_validation_result(False, validation_result.errors)
                show_error("❌ File validation failed:")
                for error in validation_result.errors:
                    st.error(f"• {error}")
                    
        except Exception as e:
            logger.error(f"Error processing uploaded file: {e}")
            show_error(f"❌ Error processing file: {str(e)}")
            state.clear_input_file()


def render_processing_section(state: CampaignOptimizer1State):
    """Render the processing section with Bulk 7 button."""
    st.markdown("### Process Optimization")
    
    # Show Bulk 7 button
    if st.button("Bulk 7", type="primary", help="Process campaign data with 7-day budget optimization"):
        try:
            state.start_processing()
            
            # Show processing status
            with st.spinner("Processing campaign optimization..."):
                # Read input file
                reader = ExcelReader()
                success, message, input_df = reader.read_bulk_file(state.get_input_file(), "input.xlsx")
                if not success:
                    raise Exception(f"Failed to read input file: {message}")
                
                # Convert DataFrame to dictionary format expected by orchestrator
                input_data = {"Sponsored Products Campaigns": input_df}
                
                # Process with orchestrator
                orchestrator = CampaignOptimizer1Orchestrator()
                output_bytes = orchestrator.process(input_data)
                
                # Get processing summary
                # Note: We need to read the processed data to get summary
                processed_reader = ExcelReader()
                success, message, processed_data = processed_reader.read_bulk_file(output_bytes, "output.xlsx")
                if not success:
                    raise Exception(f"Failed to read output file: {message}")
                summary = orchestrator.get_processing_summary(input_data, processed_data)
                
                # Mark processing complete
                state.complete_processing(output_bytes, summary)
                
                show_success("✅ Campaign optimization completed successfully!")
                
        except Exception as e:
            logger.error(f"Processing error: {e}")
            error_msg = f"Processing failed: {str(e)}"
            state.set_processing_error(error_msg)
            show_error(f"❌ {error_msg}")
    
    # Show processing status
    if state.is_processing():
        st.info("⏳ Processing in progress...")
        
    elif state.has_processing_error():
        st.error(f"❌ {state.get_processing_error()}")
        if st.button("Try Again"):
            state.clear_processing()
            st.rerun()


def render_download_section(state: CampaignOptimizer1State):
    """Render the download section."""
    st.markdown("### Download Results")
    
    # Show processing summary
    summary = state.get_processing_summary()
    if summary:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Campaigns Processed", f"{summary.get('campaigns_processed', 0):,}")
        with col2:
            st.metric("Campaigns Updated", f"{summary.get('campaigns_updated', 0):,}")
        with col3:
            st.metric("Output Sheets", summary.get('output_sheets', 0))
    
    # Download button
    output_file = state.get_output_file()
    if output_file:
        filename = generate_campaign_optimizer_1_filename()
        
        create_download_button(
            label="📥 Download Optimized Campaigns",
            data=output_file,
            file_name=filename,
            mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help_text="Download the processed Excel file with optimized campaign budgets"
        )
        
        st.success("🎉 Campaign optimization complete! Click the button above to download your results.")


if __name__ == "__main__":
    render_campaign_optimizer_1()