"""Main entry point for the Bid Optimizer application."""

import streamlit as st
import sys
import os
from pathlib import Path

# Add parent directory to path to fix imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.state.session_manager import SessionManager
from app.pages.bid_optimizer import BidOptimizerPage


def main():
    """Main application entry point."""

    # Setup page configuration - MUST BE FIRST AND ONLY ONCE
    st.set_page_config(
        page_title="Bid Optimizer",
        layout="wide",  # CHANGED FROM "centered" TO "wide"
        initial_sidebar_state="collapsed",
    )

    # Initialize session state
    session_manager = SessionManager()
    session_manager.initialize()

    # Define bid optimizer page function
    def bid_optimizer_page():
        """Bid Optimizer page"""
        page = BidOptimizerPage()
        page.render()

    # Define a simple second page
    def campaigns_page():
        """Campaigns Optimizer page"""
        st.title("Campaigns Optimizer")
        st.info("🚧 Coming Soon - This feature is planned for Phase 2 development.")

    # Create pages with two options
    pages = [
        st.Page(bid_optimizer_page, title="Bid Optimizer"),
        st.Page(campaigns_page, title="Campaigns Optimizer"),
    ]

    # Create top navigation menu
    pg = st.navigation(pages, position="top")

    # Run the selected page
    pg.run()


if __name__ == "__main__":
    main()
