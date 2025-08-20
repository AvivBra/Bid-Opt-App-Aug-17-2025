"""Main page - displays Hello Bidder."""

import streamlit as st


class MainPage:
    """Main landing page."""

    def render(self):
        """Render the main page content."""
        st.markdown(
            "<h1 style='text-align: center;'>Hello Bidder</h1>", unsafe_allow_html=True
        )
