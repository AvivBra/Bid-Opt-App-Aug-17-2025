"""Download buttons component for output files."""

import streamlit as st
from typing import Optional
from io import BytesIO

def create_download_button(
    label: str,
    data: Optional[BytesIO] = None,
    file_name: str = "",
    mime_type: str = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    disabled: bool = False,
    help_text: Optional[str] = None
) -> None:
    """
    Create a styled download button.
    
    Args:
        label: Button label text
        data: File data as BytesIO
        file_name: Name for downloaded file
        mime_type: MIME type of file
        disabled: Whether button is disabled
        help_text: Help tooltip text
    """
    if disabled:
        # Show disabled button with Coming Soon
        st.button(
            label=f"{label} (Coming Soon)",
            disabled=True,
            help=help_text or "This feature will be available in a future update",
            use_container_width=True
        )
    else:
        # Mock download button for now (since no real data in phase 6)
        st.button(
            label=label,
            disabled=True,  # Always disabled in phase 6
            help="File generation in progress...",
            use_container_width=True
        )

def render_download_section() -> None:
    """Render the download buttons section."""
    st.markdown("### 📥 Download Files")
    
    col1, col2 = st.columns(2)
    
    with col1:
        create_working_button()
    
    with col2:
        create_clean_button()
    
    # Apply custom styles
    apply_download_styles()

def create_working_button() -> None:
    """Create Working File download button."""
    # In phase 6, this is just a mock disabled button
    working_file = st.session_state.get('working_file')
    
    if st.session_state.get('processing_status') == 'complete':
        # Show as "ready" but still disabled (no real file yet)
        st.button(
            "📄 Download Working File",
            disabled=True,
            help="Working file with helper columns (Feature coming soon)",
            use_container_width=True,
            type="primary"
        )
    else:
        create_download_button(
            label="📄 Download Working File",
            disabled=True,
            help_text="Process files first to generate output"
        )

def create_clean_button() -> None:
    """Create Clean File download button (always disabled)."""
    create_download_button(
        label="📄 Download Clean File",
        disabled=True,
        help_text="Clean file without helper columns"
    )

def apply_download_styles() -> None:
    """Apply custom CSS styles to download buttons."""
    st.markdown("""
        <style>
        /* Download button styles */
        .stButton > button:disabled {
            background-color: #2b2b2b !important;
            color: #666666 !important;
            border: 1px solid #444444 !important;
            cursor: not-allowed !important;
        }
        
        .stButton > button:not(:disabled) {
            background: linear-gradient(90deg, #CCCCCC 0%, #EEEEEE 100%) !important;
            color: white !important;
            border: none !important;
            font-weight: 600 !important;
            padding: 0.5rem 1rem !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:not(:disabled):hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 5px 15px rgba(124, 58, 237, 0.3) !important;
        }
        </style>
    """, unsafe_allow_html=True)