page = BidOptimizerPage()
page.render()
"""Main entry point for the Bid Optimizer application - Complete version."""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path to fix imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.navigation import Navigation
from app.ui.layout import setup_page_config
from app.state.session_manager import SessionManager


def main():
    """Main application entry point."""

    # Setup page configuration
    setup_page_config()

    # Initialize session state
    session_manager = SessionManager()
    session_manager.initialize()

    # Create and render navigation
    nav = Navigation()
    nav.render()


if __name__ == "__main__":
    main()
