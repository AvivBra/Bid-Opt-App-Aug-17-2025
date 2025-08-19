"""Layout and styling components."""

import streamlit as st
from config.constants import COLORS, MAX_CONTENT_WIDTH


def apply_custom_css():
    """Apply custom CSS styling to the application."""
    
    st.markdown(f"""
    <style>
    /* Main app styling */
    .main .block-container {{
        max-width: {MAX_CONTENT_WIDTH}px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}
    
    /* Background colors */
    .stApp {{
        background-color: {COLORS['background']};
    }}
    
    /* Sidebar styling */
    .css-1d391kg {{
        background-color: {COLORS['sidebar']};
    }}
    
    /* Button styling */
    .stButton > button {{
        background-color: {COLORS['card']};
        color: {COLORS['text']};
        border: 1px solid {COLORS['accent']}40;
        border-radius: 8px;
        width: 200px;
        height: 44px;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        border-color: {COLORS['accent']};
        background-color: {COLORS['accent']}20;
    }}
    
    .stButton > button[data-testid="baseButton-primary"] {{
        background-color: {COLORS['accent']};
        color: white;
        border-color: {COLORS['accent']};
    }}
    
    /* File uploader styling */
    .stFileUploader {{
        background-color: {COLORS['card']};
        border: 1px solid {COLORS['accent']}40;
        border-radius: 8px;
        padding: 1rem;
    }}
    
    /* Alert/message styling */
    .stAlert {{
        background-color: {COLORS['alert_bg']};
        color: {COLORS['text']};
        border-radius: 8px;
    }}
    
    /* Progress bar styling */
    .stProgress > div > div > div {{
        background-color: {COLORS['accent']};
    }}
    
    /* Card-like containers */
    .upload-card, .validation-card, .output-card {{
        background-color: {COLORS['card']};
        border: 1px solid {COLORS['accent']}40;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }}
    
    /* Section headers */
    .section-header {{
        color: {COLORS['accent']};
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        border-bottom: 2px solid {COLORS['accent']};
        padding-bottom: 0.5rem;
    }}
    
    /* Status indicators */
    .status-success {{
        color: #10B981;
    }}
    
    .status-warning {{
        color: #F59E0B;
    }}
    
    .status-error {{
        color: #EF4444;
    }}
    
    .status-info {{
        color: {COLORS['accent']};
    }}
    
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .stDeployButton {{display: none;}}
    
    </style>
    """, unsafe_allow_html=True)


def create_section_header(title: str, icon: str = "") -> None:
    """Create a styled section header."""
    icon_html = f"<span style='margin-right: 10px;'>{icon}</span>" if icon else ""
    
    st.markdown(f"""
    <div class="section-header">
        {icon_html}{title}
    </div>
    """, unsafe_allow_html=True)


def create_card_container(content_func, css_class: str = "upload-card"):
    """Create a card-like container for content."""
    
    st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
    content_func()
    st.markdown('</div>', unsafe_allow_html=True)


def create_status_message(message: str, status_type: str = "info") -> None:
    """Create a styled status message."""
    
    status_icons = {
        'success': '✅',
        'warning': '⚠️', 
        'error': '❌',
        'info': 'ℹ️'
    }
    
    icon = status_icons.get(status_type, 'ℹ️')
    css_class = f"status-{status_type}"
    
    st.markdown(f"""
    <div class="{css_class}" style="display: flex; align-items: center; margin: 10px 0;">
        <span style="margin-right: 8px; font-size: 16px;">{icon}</span>
        <span>{message}</span>
    </div>
    """, unsafe_allow_html=True)


def create_metric_display(label: str, value: str, delta: str = None) -> None:
    """Create a metric display with optional delta."""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.metric(label, value, delta)


def center_content(content_func):
    """Center content in the main area."""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        content_func()