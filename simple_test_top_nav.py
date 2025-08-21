"""Simple test for top navigation - save and run this file directly"""

import streamlit as st

# MUST be first
st.set_page_config(
    page_title="Navigation Test",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Simple CSS to ensure visibility
st.markdown("""
    <style>
    /* Force header to be visible */
    header[data-testid="stHeader"] {
        background-color: #262730 !important;
        height: 55px !important;
    }
    
    /* Hide sidebar completely */
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Define pages
def page_home():
    st.title("🏠 Home Page")
    st.write("Welcome to the home page!")

def page_about():
    st.title("📖 About Page")
    st.write("This is the about page!")

def page_contact():
    st.title("📧 Contact Page")
    st.write("This is the contact page!")

# Create navigation with position="top"
pages = [
    st.Page(page_home, title="Home", icon="🏠"),
    st.Page(page_about, title="About", icon="📖"),
    st.Page(page_contact, title="Contact", icon="📧"),
]

# This should create a top navigation menu
pg = st.navigation(pages, position="top")

# Display what page we're on for debugging
st.sidebar.write(f"Current page object: {pg}")

# Run the selected page
pg.run()