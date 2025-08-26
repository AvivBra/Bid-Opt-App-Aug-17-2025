"""Layout utilities - FULLY CENTERED VERSION."""

import streamlit as st


def apply_custom_css():
    st.markdown(
        """
       <style>
       /* Typography */
       h1 {
           font-size: 100px !important;
           margin-bottom: -70px !important;
       }
       
       h3 {
           font-size: 20px !important;
           margin-bottom: 40px !important;
       }
       
       /* Layout - Center main content, keep navigation full width */
       .main .block-container {
           max-width: 750px !important;
           padding: 1.5rem !important;
           margin: 0 auto !important;
           text-align: center !important;
       }
       
       
       /* Center most content except navigation and radio buttons */
       p:not([data-testid*="stHeader"] *):not(nav *):not(header *):not(.stRadio *), 
       span:not([data-testid*="stHeader"] *):not(nav *):not(header *):not(.stRadio *), 
       div:not([data-testid*="stHeader"]):not(nav):not(header):not(.stRadio):not(.stRadio *) {
           text-align: center !important;
       }
       
       /* Radio buttons - Left aligned with dark accent */
       .stRadio {
           text-align: left !important;
       }
       
       .stRadio > div {
           align-items: flex-start !important;
       }
       
       .stRadio input[type="radio"] {
           accent-color: #26282c !important;
           width: 16px !important;
           height: 16px !important;
           margin-right: 8px !important;
       }
       
       /* Buttons - Left aligned with custom styling */
       .stButton {
           text-align: left !important;
       }
       
       .stButton > button {
           background-color: #DDDDDD !important;
           color: #26282c !important;
           border: none !important;
           padding: 0.5rem 2rem !important;
           border-radius: 4px !important;
           font-weight: 500 !important;
           min-width: 150px !important;
       }
       
       .stButton > button:hover {
           background-color: #CCCCCC !important;
           transform: translateY(-2px) !important;
       }
       
       .stButton > button:disabled {
           background-color: #4a4a4a !important;
           color: #888 !important;
           opacity: 0.6 !important;
       }
       
       /* Form elements accent color */
       input[type="checkbox"] {
           accent-color: #26282c !important;
       }
       
       /* Make sidebar wider for page names */
       .css-1d391kg {
           width: 300px !important;
       }
       
       [data-testid="stSidebar"] {
           width: 300px !important;
       }
       
       [data-testid="stSidebar"] > div {
           width: 300px !important;
       }
       
       /* Add very large space between radio buttons */
       [data-testid="stSidebar"] .stRadio > div > div {
           margin-bottom: 250px !important;
    
       }
       
       .stSidebar .stRadio > div {
           gap: 1px !important;
       }
       </style>
       """,
        unsafe_allow_html=True,
    )
