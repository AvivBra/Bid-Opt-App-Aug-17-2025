"""Simple sidebar for navigation - Only 2 pages."""

import streamlit as st


def render_sidebar():
    """Render sidebar with navigation buttons."""

    # Initialize current_page if not exists
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Bid Optimizer"

    with st.sidebar:
        st.markdown("### Navigation")

        # Bid Optimizer button
        if st.button("Bid Optimizer", key="btn_bid", use_container_width=True):
            st.session_state.current_page = "Bid Optimizer"
            st.rerun()

        # Campaigns Optimizer (disabled)
        st.button(
            "Campaigns Optimizer",
            key="btn_campaigns",
            use_container_width=True,
            disabled=True,
        )

        # Debug info - remove this after testing
        st.markdown("---")
        st.write("Current page:", st.session_state.current_page)


def get_current_page() -> str:
    """Get the currently selected page."""
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Bid Optimizer"
    return st.session_state.current_page
