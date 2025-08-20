"""Main layout configuration for the application."""

import streamlit as st
from typing import Any, Optional


def apply_custom_layout():
    """Apply custom layout and styling to the Streamlit app."""

    # Load Google Inter font
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400&display=swap" rel="stylesheet">
        """,
        unsafe_allow_html=True,
    )

    # Apply custom CSS
    st.markdown(
        """
        <style>
        /* Main app styling */
        .stApp {
            background-color: #0F0F0F;
            font-family: 'Inter', sans-serif;
            font-weight: 400;
        }
        
        /* Remove Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Container styling */
        .main .block-container {
            max-width: 800px;
            padding: 40px 24px;
            margin: 0 auto;
        }
        
        /* Section containers */
        .section-container {
            background: #1A1A1A;
            border: 1px solid #2D2D2D;
            border-radius: 4px;
            padding: 32px;
            margin-bottom: 48px;
        }
        
        /* Card container */
        .card-container {
            background: #1A1A1A;
            border: 1px solid #2D2D2D;
            border-radius: 4px;
            padding: 32px;
            margin-bottom: 48px;
        }
        
        /* Button styling */
        .stButton > button {
            background-color: #8B5CF6;
            color: white;
            border: none;
            padding: 0 24px;
            height: 44px;
            font-size: 14px;
            font-weight: 400;
            text-transform: uppercase;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.2s;
            font-family: 'Inter', sans-serif;
        }
        
        .stButton > button:hover {
            background-color: #7C3AED;
        }
        
        .stButton > button:disabled {
            background-color: #2D2D2D;
            color: #666666;
            cursor: not-allowed;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #1A1A1A;
            border-right: 1px solid #2D2D2D;
        }
        
        /* File uploader styling */
        .stFileUploader {
            background-color: #1A1A1A;
            border: 1px solid #2D2D2D;
            border-radius: 4px;
            padding: 16px;
        }
        
        /* Success/Error/Warning/Info messages */
        .stAlert {
            background-color: #1A1A1A;
            border: 1px solid #2D2D2D;
            border-radius: 4px;
            padding: 16px;
        }
        
        /* Checkbox styling */
        .stCheckbox {
            color: white;
            font-family: 'Inter', sans-serif;
        }
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            color: white;
            font-family: 'Inter', sans-serif;
            font-weight: 400;
        }
        
        /* Text */
        p, span, div {
            color: #E5E5E5;
            font-family: 'Inter', sans-serif;
        }
        
        /* Progress bar container */
        .stProgress {
            background-color: #2D2D2D;
            border-radius: 4px;
            height: 8px;
        }
        
        /* Progress bar fill */
        .stProgress > div > div {
            background-color: #8B5CF6;
        }
        
        /* Metric styling */
        .metric-container {
            background-color: #1A1A1A;
            border: 1px solid #2D2D2D;
            border-radius: 4px;
            padding: 16px;
            text-align: center;
        }
        
        /* Input fields */
        .stTextInput > div > div > input {
            background-color: #1A1A1A;
            color: white;
            border: 1px solid #2D2D2D;
            font-family: 'Inter', sans-serif;
        }
        
        /* Select boxes */
        .stSelectbox > div > div {
            background-color: #1A1A1A;
            color: white;
            border: 1px solid #2D2D2D;
            font-family: 'Inter', sans-serif;
        }
        
        /* Custom classes */
        .section-header {
            font-size: 18px;
            text-transform: uppercase;
            color: white;
            margin-bottom: 24px;
            font-family: 'Inter', sans-serif;
            font-weight: 400;
        }
        
        .status-text {
            color: #A1A1A1;
            font-size: 12px;
            font-family: 'Inter', sans-serif;
        }
        
        .error-text {
            color: #EF4444;
            font-family: 'Inter', sans-serif;
        }
        
        .success-text {
            color: #10B981;
            font-family: 'Inter', sans-serif;
        }
        
        .warning-text {
            color: #F59E0B;
            font-family: 'Inter', sans-serif;
        }
        
        /* Status messages */
        .status-success {
            background-color: rgba(16, 185, 129, 0.1);
            border: 1px solid #10B981;
            color: #10B981;
            padding: 16px;
            border-radius: 4px;
            margin-bottom: 16px;
        }
        
        .status-error {
            background-color: rgba(239, 68, 68, 0.1);
            border: 1px solid #EF4444;
            color: #EF4444;
            padding: 16px;
            border-radius: 4px;
            margin-bottom: 16px;
        }
        
        .status-warning {
            background-color: rgba(245, 158, 11, 0.1);
            border: 1px solid #F59E0B;
            color: #F59E0B;
            padding: 16px;
            border-radius: 4px;
            margin-bottom: 16px;
        }
        
        .status-info {
            background-color: rgba(59, 130, 246, 0.1);
            border: 1px solid #3B82F6;
            color: #3B82F6;
            padding: 16px;
            border-radius: 4px;
            margin-bottom: 16px;
        }
        
        /* Card styles for upload, validation, output */
        .upload-card, .validation-card, .output-card {
            background: #1A1A1A;
            border: 1px solid #2D2D2D;
            border-radius: 4px;
            padding: 32px;
            margin-bottom: 48px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def apply_custom_css():
    """Legacy function name for backwards compatibility."""
    apply_custom_layout()


def set_page_config():
    """Set Streamlit page configuration."""
    st.set_page_config(
        page_title="Bid Optimizer",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={"Get Help": None, "Report a bug": None, "About": None},
    )


def initialize_layout():
    """Initialize the layout (call this once in main.py)."""
    set_page_config()
    apply_custom_layout()


def create_card_container(content_func: Any, css_class: str = "card-container") -> None:
    """
    Create a card container and render content function inside it.

    Args:
        content_func: Function that renders the card content
        css_class: CSS class name for styling (e.g., "upload-card", "validation-card")
    """
    # Apply the CSS class via markdown
    st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)

    # Execute the content function
    content_func()

    # Close the div
    st.markdown("</div>", unsafe_allow_html=True)


def center_content(content_func: Any) -> None:
    """
    Center content in the main area.

    Args:
        content_func: Function that renders the content
    """
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        content_func()


def create_status_message(message: str, status: str = "info") -> None:
    """
    Create a status message with appropriate styling.

    Args:
        message: Message to display
        status: Status type ('success', 'error', 'warning', 'info')
    """
    status_class = f"status-{status}"

    st.markdown(
        f"""
        <div class="{status_class}">
            {message}
        </div>
        """,
        unsafe_allow_html=True,
    )


def create_section(title: str) -> Any:
    """
    Create a section with consistent styling.

    Args:
        title: Section title

    Returns:
        Streamlit container for the section content
    """
    st.markdown(
        f"""
        <div class="section-container">
            <h2 class="section-header">{title.upper()}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    return st.container()


def add_vertical_space(height: int = 1) -> None:
    """
    Add vertical spacing.

    Args:
        height: Number of line breaks to add
    """
    for _ in range(height):
        st.write("")


def create_columns_layout(ratios: list) -> list:
    """
    Create columns with specific ratios.

    Args:
        ratios: List of column width ratios

    Returns:
        List of column objects
    """
    return st.columns(ratios)


def render_divider() -> None:
    """Render a horizontal divider."""
    st.markdown(
        """
        <hr style="
            border: none;
            border-top: 1px solid #2D2D2D;
            margin: 32px 0;
        ">
        """,
        unsafe_allow_html=True,
    )


def create_section_header(title: str, icon: str = None) -> None:
    """
    Create a section header.

    Args:
        title: Header title
        icon: Optional icon/emoji
    """
    icon_html = f"<span style='margin-right: 10px;'>{icon}</span>" if icon else ""

    st.markdown(
        f"""
        <div class="section-header">
            {icon_html}{title.upper()}
        </div>
        """,
        unsafe_allow_html=True,
    )
