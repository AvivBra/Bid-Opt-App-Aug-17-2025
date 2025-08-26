"""Main entry point for the Bid Optimizer application."""

import streamlit as st
import sys
import os
from pathlib import Path

# Add parent directory to path to fix imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.state.session_manager import SessionManager
from app.components.bid_optimizer import BidOptimizerPage
from app.components.campaign_optimizer import CampaignOptimizerPage


def main():
    """Main application entry point."""

    # Setup page configuration - MUST BE FIRST AND ONLY ONCE
    st.set_page_config(
        page_title="Bid Optimizer",
        layout="wide",  # CHANGED FROM "centered" TO "wide"
        initial_sidebar_state="expanded",
    )

    # Initialize session state
    session_manager = SessionManager()
    session_manager.initialize()

    # Sidebar navigation
    page_selection = st.sidebar.radio(
        "",
        ["Bid Optimizer", "Campaign Optimizer"],
        index=0
    )

    # Render selected page
    if page_selection == "Bid Optimizer":
        page = BidOptimizerPage()
        page.render()
    elif page_selection == "Campaign Optimizer":
        page = CampaignOptimizerPage()
        page.render()


if __name__ == "__main__":
    main()
