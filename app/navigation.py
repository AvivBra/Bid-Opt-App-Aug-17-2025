"""Navigation system for the Bid Optimizer application."""

import streamlit as st
from app.ui.sidebar import render_sidebar, get_current_page
from app.ui.layout import apply_custom_css
from app.pages.bid_optimizer import BidOptimizerPage


class Navigation:
    """Handles navigation between application pages."""
    
    def __init__(self):
        self.pages = {
            'Bid Optimizer': BidOptimizerPage(),
            'Campaigns Optimizer': None  # TBC - Phase 2+
        }
    
    def render(self):
        """Render the navigation and current page."""
        
        # Apply custom CSS styling
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
        """Render coming soon message for TBC features."""
        st.title("🚧 Coming Soon")
        st.info("This feature is planned for Phase 2 development.")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("← Back to Bid Optimizer", type="primary"):
                st.session_state.current_page = 'Bid Optimizer'
                st.rerun()