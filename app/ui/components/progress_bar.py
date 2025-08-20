"""Progress bar component for showing processing status."""

import streamlit as st
import time
from typing import Optional

def render(progress_value: Optional[float] = None) -> None:
    """
    Render progress bar with percentage display.
    
    Args:
        progress_value: Value between 0 and 1, or None for auto-animation
    """
    if progress_value is None:
        # Auto-animate for mock processing
        animate_mock_progress()
    else:
        # Display specific progress value
        _display_progress(progress_value)

def create_progress_html(percent: int) -> str:
    """
    Create custom HTML for styled progress bar.
    
    Args:
        percent: Percentage value (0-100)
        
    Returns:
        HTML string for progress bar
    """
    html = f"""
    <div style="
        width: 100%;
        height: 30px;
        background-color: #2b2b2b;
        border-radius: 15px;
        overflow: hidden;
        position: relative;
        margin: 10px 0;
    ">
        <div style="
            width: {percent}%;
            height: 100%;
            background: linear-gradient(90deg, #CCCCCC 0%, #EEEEEE 100%);
            border-radius: 15px;
            transition: width 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
        ">
            <span style="
                color: white;
                font-weight: 400;
                font-size: 14px;
                position: absolute;
                left: 50%;
                transform: translateX(-50%);
            ">{percent}%</span>
        </div>
    </div>
    """
    return html

def update_progress(value: float) -> None:
    """
    Update progress value in session state.
    
    Args:
        value: Progress value between 0 and 1
    """
    st.session_state.progress_value = max(0, min(1, value))

def animate_mock_progress() -> None:
    """Animate progress bar for mock processing (10 seconds)."""
    if 'progress_placeholder' not in st.session_state:
        st.session_state.progress_placeholder = st.empty()
    
    if 'mock_progress_start' not in st.session_state:
        st.session_state.mock_progress_start = time.time()
    
    # Calculate elapsed time
    elapsed = time.time() - st.session_state.mock_progress_start
    duration = 10  # 10 seconds total
    
    # Calculate progress
    progress = min(elapsed / duration, 1.0)
    
    # Display progress
    with st.session_state.progress_placeholder.container():
        percent = int(progress * 100)
        st.markdown(create_progress_html(percent), unsafe_allow_html=True)
        
        # Show time elapsed
        time_elapsed = min(elapsed, duration)
        st.caption(f"Time elapsed: {format_time(time_elapsed)}")
    
    # Update session state when complete
    if progress >= 1.0:
        st.session_state.processing_status = 'complete'
        st.session_state.rows_processed = 12543
        st.session_state.optimizations_count = 1
        # Clean up
        if 'mock_progress_start' in st.session_state:
            del st.session_state.mock_progress_start
        if 'progress_placeholder' in st.session_state:
            del st.session_state.progress_placeholder
        st.rerun()
    else:
        # Continue animation
        time.sleep(0.1)
        st.rerun()

def show_time_elapsed() -> None:
    """Display time elapsed since processing started."""
    if 'processing_start_time' in st.session_state:
        elapsed = time.time() - st.session_state.processing_start_time
        st.caption(f"Time elapsed: {format_time(elapsed)}")

def format_time(seconds: float) -> str:
    """
    Format time in MM:SS format.
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted time string
    """
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def _display_progress(value: float) -> None:
    """
    Display progress bar with specific value.
    
    Args:
        value: Progress value between 0 and 1
    """
    percent = int(value * 100)
    st.markdown(create_progress_html(percent), unsafe_allow_html=True)