"""Navigation system for the Bid Optimizer application - Without Main Page."""

import streamlit as st
from app.ui.sidebar_backup import render_sidebar, get_current_page
from app.ui.layout import apply_custom_css
from app.pages.bid_optimizer import BidOptimizerPage
from app.components.portfolio_optimizer import PortfolioOptimizerPage


class Navigation:
    """Handles navigation between application pages."""

    def __init__(self):
        self.pages = {
            "Bid Optimizer": BidOptimizerPage(),
            "Campaigns Optimizer": None,  # TBC - Phase 2+
            "Portfolio Optimizer": PortfolioOptimizerPage(),
        }

    def render(self):
        """Render the navigation and current page."""

        # Apply custom CSS styling - CENTERED
        apply_custom_css()

        # Render sidebar navigation
        render_sidebar()

        # Get current page and render content
        current_page_name = get_current_page()
        current_page = self.pages.get(current_page_name)

        if current_page:
            current_page.render()
        else:
            self._render_coming_soon()

    def _render_coming_soon(self):
        """Render coming soon message for TBC features - CENTERED."""
        st.markdown(
            "<h1 style='text-align: center;'>🚧 Coming Soon</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='text-align: center;'>This feature is planned for Phase 2 development.</p>",
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(
                "← Back to Bid Optimizer", type="primary", use_container_width=True
            ):
                st.session_state.current_page = "Bid Optimizer"
                st.rerun()
