"""Sidebar component for navigation - CLEAN version without any text."""

import streamlit as st


def render_sidebar():
    """Render the navigation sidebar - MINIMAL."""

    with st.sidebar:
        # Apply custom CSS for sidebar styling
        st.markdown(
            """
       <style>
       /* Hide all sidebar text elements */
       section[data-testid="stSidebar"] .element-container {
           display: none !important;
       }
       
       /* Show only buttons */
       section[data-testid="stSidebar"] .stButton {
           display: block !important;
       }
       
       /* Center buttons */
       section[data-testid="stSidebar"] button {
           margin: 20px auto;
           display: block;
           width: 180px;
       }
       
       /* Sidebar background */
       section[data-testid="stSidebar"] {
           background-color: #1a1a1a;
           width: 200px;
           padding-top: 50px;
       }
       
       /* Hide all markdown text */
       section[data-testid="stSidebar"] .stMarkdown {
           display: none !important;
       }
       </style>
       """,
            unsafe_allow_html=True,
        )

        # Navigation buttons ONLY - no text
        if st.button(
            "Bid Optimizer", type="primary", use_container_width=True, key="nav_bid"
        ):
            st.session_state.current_page = "Bid Optimizer"
            st.rerun()

        # Disabled button - no text
        st.button(
            "Campaigns Optimizer",
            disabled=True,
            use_container_width=True,
            key="nav_campaigns",
        )


def get_current_page() -> str:
    """Get the currently selected page."""
    return st.session_state.get("current_page", "Bid Optimizer")
