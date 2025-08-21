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
        page_title="Bid Optimizer", layout="centered", initial_sidebar_state="collapsed"
    )

    # Apply CSS to ensure top nav is ALWAYS visible - with animation delay
    st.markdown(
        """
        <style>
        /* FORCE top navigation to stay visible with animation */
        @keyframes keepVisible {
            from { opacity: 1; visibility: visible; }
            to { opacity: 1; visibility: visible; }
        }
        
        header[data-testid="stHeader"] {
            visibility: visible !important;
            display: block !important;
            position: sticky !important;
            top: 0 !important;
            z-index: 999999 !important;
            background-color: #0E1117 !important;
            animation: keepVisible 0s infinite !important;
        }
        
        /* Ensure navigation container is visible */
        div[data-testid="stHorizontalBlock"] {
            visibility: visible !important;
            opacity: 1 !important;
        }
        
        /* Ensure navigation buttons are visible */
        header button {
            visibility: visible !important;
            opacity: 1 !important;
            color: #FFFFFF !important;
        }
        
        /* Hide sidebar completely */
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        
        /* Remove sidebar button */
        button[kind="header"] {
            display: none !important;
        }
        
        /* Ensure main content has no left margin */
        .main {
            margin-left: 0 !important;
            padding-left: 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
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
