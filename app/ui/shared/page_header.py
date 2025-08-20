# Path: app/ui/shared/page_header.py
"""Page header component for displaying page titles and descriptions."""

import streamlit as st
from typing import Optional, Dict, Any

def render_page_header(
    title: str,
    subtitle: Optional[str] = None,
    show_separator: bool = True,
    centered: bool = True
) -> None:
    """
    Render the main page header with title and optional subtitle.
    
    Args:
        title: Main page title
        subtitle: Optional subtitle or description
        show_separator: Whether to show separator line below
        centered: Whether to center the header text
    """
    # Text alignment
    alignment = "center" if centered else "left"
    
    # Main title
    st.markdown(
        f"""
        <h1 style="
            text-align: {alignment};
            color: #FFFFFF;
            font-family: 'Inter', sans-serif;
            font-size: 28px;
            font-weight: 400;
            margin: 0 0 8px 0;
            padding: 0;
        ">{title}</h1>
        """,
        unsafe_allow_html=True
    )
    
    # Optional subtitle
    if subtitle:
        st.markdown(
            f"""
            <p style="
                text-align: {alignment};
                color: #A1A1A1;
                font-family: 'Inter', sans-serif;
                font-size: 14px;
                font-weight: 400;
                margin: 0 0 24px 0;
            ">{subtitle}</p>
            """,
            unsafe_allow_html=True
        )
    
    # Separator line
    if show_separator:
        st.markdown(
            """
            <div style="
                width: 100%;
                height: 1px;
                background-color: #2D2D2D;
                margin: 24px 0 48px 0;
            "></div>
            """,
            unsafe_allow_html=True
        )

def render_section_header(
    title: str,
    uppercase: bool = True,
    icon: Optional[str] = None
) -> None:
    """
    Render a section header within the page.
    
    Args:
        title: Section title text
        uppercase: Whether to display in uppercase
        icon: Optional emoji/icon (though generally not used in this minimalist design)
    """
    display_title = title.upper() if uppercase else title
    
    # Add icon if provided (though the design prefers no icons)
    if icon:
        display_title = f"{icon} {display_title}"
    
    st.markdown(
        f"""
        <h2 style="
            color: #E5E5E5;
            font-family: 'Inter', sans-serif;
            font-size: 18px;
            font-weight: 400;
            text-transform: {'uppercase' if uppercase else 'none'};
            margin: 0 0 24px 0;
            padding: 0;
        ">{display_title}</h2>
        """,
        unsafe_allow_html=True
    )

def render_subsection_header(
    title: str,
    description: Optional[str] = None
) -> None:
    """
    Render a subsection header for nested content.
    
    Args:
        title: Subsection title
        description: Optional description text
    """
    st.markdown(
        f"""
        <h3 style="
            color: #E5E5E5;
            font-family: 'Inter', sans-serif;
            font-size: 16px;
            font-weight: 400;
            margin: 0 0 12px 0;
        ">{title}</h3>
        """,
        unsafe_allow_html=True
    )
    
    if description:
        st.markdown(
            f"""
            <p style="
                color: #A1A1A1;
                font-family: 'Inter', sans-serif;
                font-size: 12px;
                margin: 0 0 16px 0;
            ">{description}</p>
            """,
            unsafe_allow_html=True
        )

def render_status_header(
    status: str,
    status_type: str = "info"
) -> None:
    """
    Render a status header with appropriate color coding.
    
    Args:
        status: Status message to display
        status_type: Type of status ('success', 'error', 'warning', 'info')
    """
    # Color mapping for different status types
    colors = {
        'success': '#10B981',
        'error': '#EF4444',
        'warning': '#F59E0B',
        'info': '#3B82F6',
        'default': '#A1A1A1'
    }
    
    color = colors.get(status_type, colors['default'])
    
    st.markdown(
        f"""
        <div style="
            background-color: #1A1A1A;
            border: 1px solid {color};
            border-radius: 4px;
            padding: 16px;
            margin-bottom: 24px;
        ">
            <p style="
                color: {color};
                font-family: 'Inter', sans-serif;
                font-size: 14px;
                font-weight: 400;
                margin: 0;
                text-align: center;
            ">{status}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_breadcrumb(
    path: list,
    separator: str = "/"
) -> None:
    """
    Render a breadcrumb navigation path.
    
    Args:
        path: List of path items ['Home', 'Bid Optimizer', 'Zero Sales']
        separator: Separator character between items
    """
    breadcrumb_html = ""
    
    for i, item in enumerate(path):
        # Make the last item active (not a link)
        if i == len(path) - 1:
            breadcrumb_html += f"""
                <span style="color: #FFFFFF;">{item}</span>
            """
        else:
            breadcrumb_html += f"""
                <span style="color: #A1A1A1;">{item}</span>
                <span style="color: #666666; margin: 0 8px;">{separator}</span>
            """
    
    st.markdown(
        f"""
        <div style="
            font-family: 'Inter', sans-serif;
            font-size: 12px;
            margin-bottom: 16px;
        ">
            {breadcrumb_html}
        </div>
        """,
        unsafe_allow_html=True
    )

def render_page_info(info: Dict[str, Any]) -> None:
    """
    Render page information/metadata.
    
    Args:
        info: Dictionary containing page information
              e.g., {'version': '1.0', 'last_updated': '2025-08-17'}
    """
    info_items = []
    
    for key, value in info.items():
        formatted_key = key.replace('_', ' ').title()
        info_items.append(f"{formatted_key}: {value}")
    
    info_text = " | ".join(info_items)
    
    st.markdown(
        f"""
        <div style="
            color: #666666;
            font-family: 'Inter', sans-serif;
            font-size: 11px;
            text-align: right;
            margin-bottom: 24px;
        ">{info_text}</div>
        """,
        unsafe_allow_html=True
    )

def render_help_text(
    text: str,
    style: str = "inline"
) -> None:
    """
    Render help or informational text.
    
    Args:
        text: Help text to display
        style: Display style ('inline', 'block', 'tooltip')
    """
    if style == "inline":
        st.markdown(
            f"""
            <span style="
                color: #666666;
                font-family: 'Inter', sans-serif;
                font-size: 12px;
                font-style: italic;
            ">{text}</span>
            """,
            unsafe_allow_html=True
        )
    elif style == "block":
        st.markdown(
            f"""
            <div style="
                background-color: #0F0F0F;
                border-left: 3px solid #DDDDDD;
                padding: 12px 16px;
                margin: 16px 0;
            ">
                <p style="
                    color: #A1A1A1;
                    font-family: 'Inter', sans-serif;
                    font-size: 12px;
                    margin: 0;
                ">{text}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

def clear_header_space() -> None:
    """Add consistent spacing after header sections."""
    st.markdown(
        """
        <div style="margin-bottom: 48px;"></div>
        """,
        unsafe_allow_html=True
    )

def render_page_title_with_actions(
    title: str,
    actions: Optional[list] = None
) -> None:
    """
    Render page title with action buttons on the same line.
    
    Args:
        title: Page title
        actions: List of action buttons to display
                 e.g., [{'label': 'Export', 'key': 'export_btn'}]
    """
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(
            f"""
            <h1 style="
                color: #FFFFFF;
                font-family: 'Inter', sans-serif;
                font-size: 28px;
                font-weight: 400;
                margin: 0;
            ">{title}</h1>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        if actions:
            for action in actions:
                st.button(
                    action.get('label', 'Action'),
                    key=action.get('key', f'action_{title}'),
                    use_container_width=True
                )