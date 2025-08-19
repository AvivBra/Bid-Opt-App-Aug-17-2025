"""Main entry point for Bid Optimizer application."""

import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config.settings import settings
from app.state.session_manager import SessionManager
from app.navigation import Navigation


def main():
    """Main application entry point."""
    
    # Configure Streamlit page
    st.set_page_config(
        page_title=settings.app_title,
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session manager
    session_manager = SessionManager()
    session_manager.initialize()
    
    # Create navigation
    nav = Navigation()
    
    # Display application
    nav.render()


if __name__ == "__main__":
    main()