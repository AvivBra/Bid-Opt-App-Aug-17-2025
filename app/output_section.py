"""Output section UI component for displaying processing results."""

import streamlit as st
import time
from typing import Optional, Dict, Any

def render() -> None:
    """Render the output section panel."""
    with st.container():
        st.markdown("### OUTPUT FILES")
        st.markdown("---")
        
        # Check current state
        if not st.session_state.get('processing_started', False):
            _render_waiting_view()
        elif st.session_state.get('processing_status') == 'processing':
            _render_processing_view()
        elif st.session_state.get('processing_status') == 'complete':
            _render_complete_view()
        elif st.session_state.get('processing_status') == 'error':
            _render_error_view()
        else:
            _render_waiting_view()

def _render_waiting_view() -> None:
    """Render view when waiting for processing to start."""
    st.info("⏳ Waiting for processing to start...")
    st.markdown("Click **Process Files** in the validation section to begin.")

def _render_processing_view() -> None:
    """Render view during processing with progress bar."""
    from app.ui.components.progress_bar import render as render_progress
    
    st.success("🔄 Processing Zero Sales optimization...")
    
    # Render progress bar
    progress_container = st.container()
    with progress_container:
        render_progress()
    
    # Display mock statistics during processing
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rows Processed", 
                 st.session_state.get('rows_processed', 0))
    with col2:
        st.metric("Optimizations Applied", 
                 st.session_state.get('optimizations_count', 0))
    with col3:
        elapsed = time.time() - st.session_state.get('processing_start_time', time.time())
        st.metric("Time Elapsed", f"{int(elapsed)}s")

def _render_complete_view() -> None:
    """Render view when processing is complete."""
    from app.ui.components.download_buttons import render_download_section
    
    st.success("✅ Processing complete!")
    
    # Display final statistics
    _display_statistics()
    
    # Render download buttons
    render_download_section()
    
    # Reset button
    if st.button("🔄 Reset and Start Over", type="secondary"):
        _reset_all_state()
        st.rerun()

def _render_error_view() -> None:
    """Render view when processing encountered an error."""
    error_msg = st.session_state.get('processing_error', 'Unknown error occurred')
    st.error(f"❌ Processing failed: {error_msg}")
    
    if st.button("🔄 Try Again", type="primary"):
        st.session_state.processing_status = None
        st.session_state.processing_started = False
        st.rerun()

def _display_statistics() -> None:
    """Display processing statistics."""
    stats = _get_mock_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Rows", f"{stats['total_rows']:,}")
    with col2:
        st.metric("Rows Modified", f"{stats['rows_modified']:,}")
    with col3:
        st.metric("Avg Bid Change", f"${stats['avg_bid_change']:.2f}")
    with col4:
        st.metric("Processing Time", f"{stats['processing_time']}s")
    
    # Show any warnings
    if stats.get('warnings'):
        st.warning(f"⚠️ {stats['warnings']}")

def _get_mock_stats() -> Dict[str, Any]:
    """Get mock statistics for display."""
    return {
        'total_rows': 12543,
        'rows_modified': 3421,
        'avg_bid_change': 0.35,
        'processing_time': 10,
        'warnings': "Please note: 127 calculation errors in Zero Sales optimization"
    }

def _reset_all_state() -> None:
    """Reset all session state."""
    keys_to_keep = ['page']  # Keep navigation state
    
    for key in list(st.session_state.keys()):
        if key not in keys_to_keep:
            del st.session_state[key]

def check_processing_started() -> bool:
    """Check if processing has been started."""
    return st.session_state.get('processing_started', False)

def render_processing_view() -> None:
    """Public method to render processing view."""
    _render_processing_view()

def render_complete_view() -> None:
    """Public method to render complete view."""
    _render_complete_view()

def render_error_view() -> None:
    """Public method to render error view."""
    _render_error_view()

def display_statistics() -> None:
    """Public method to display statistics."""
    _display_statistics()