"""Layout utilities - FULLY CENTERED VERSION."""

import streamlit as st


def apply_custom_css():
    st.markdown(
        """
       <style>

       h1 {
        font-size: 50px !important;
        margin-bottom: -70px !important;
        }
        
        
        h3 {
        font-size: 20px !important;
        margin-bottom: 40px !important;
        }
        
    
           
        /* FIXED DIVIDERS - more specific selectors */
        hr, 
        .stMarkdown hr,
        [data-testid="stHorizontalBlock"] hr,
        [data-testid="column"] hr,
        div hr {
        width: 40% !important;
        border: none !important;
        border-top: 1px solid #ffffff !important;
        opacity: .6 !important;
        display: block !important;
        margin-left: auto !important;
        margin-right: auto !important;
        margin-top: 1000 !important;
        margin-bottom: 1000 !important;
}
        
        

       
       
       
       /* Centering CSS */
       
       /* Center EVERYTHING in main content - MEDIUM-WIDE */
       .main .block-container {
           max-width: 750px !important;
           padding: 1.5rem !important;
           margin: 0 auto !important;
           text-align: center !important;
       }
       
       /* Make main content area medium-wide */
       .main {
           max-width: 850px !important;
           margin: 0 auto !important;
       }

       
       /* Center all paragraphs and text */
       p, span, div, label {
           text-align: center !important;
           width: 100%;
       }
       
       /* Center all buttons */
       .stButton {
           text-align: center !important;
       }
       
       .stButton > button {
           margin: 10px auto !important;
           display: block !important;
       }
       
       /* Center file uploader */
       .stFileUploader {
           text-align: center !important;
       }
       
       .stFileUploader > div {
           margin: 0 auto !important;
           text-align: center !important;
       }
       
       .stFileUploader label {
           text-align: center !important;
           width: 100% !important;
       }
       
       /* Center checkboxes */
       .stCheckbox {
           display: flex !important;
           justify-content: center !important;
           text-align: center !important;
       }
       
       .stCheckbox > label {
           margin: 0 auto !important;
       }
       
       /* Center columns content */
       [data-testid="column"] {
           display: flex !important;
           flex-direction: column !important;
           align-items: center !important;
           text-align: center !important;
       }
       
       [data-testid="column"] > * {
           width: 100% !important;
           text-align: center !important;
       }
       
       /* Center alerts and messages */
       .stAlert, .stSuccess, .stError, .stWarning, .stInfo {
           margin: 20px auto !important;
           text-align: center !important;
           max-width: 600px !important;
       }
       
       /* Center markdown content */
       .stMarkdown {
           text-align: center !important;
       }
       
       .stMarkdown > div {
           text-align: center !important;
       }
       
      
       
       /* Center metrics */
       [data-testid="metric-container"] {
           text-align: center !important;
           margin: 0 auto !important;
       }
       
       /* Center all input fields */
       .stTextInput > div {
           text-align: center !important;
       }
       
       input {
           text-align: center !important;
       }
       
       /* Center selectbox */
       .stSelectbox > div {
           text-align: center !important;
       }
       
       /* Center multiselect */
       .stMultiSelect > div {
           text-align: center !important;
       }
       
       /* Center radio buttons */
       .stRadio > div {
           display: flex !important;
           justify-content: center !important;
       }
       
       /* Center all containers */
       .element-container {
           display: flex !important;
           justify-content: center !important;
       }
       
       /* Force center alignment for all divs */
       div[class*="css"] {
           text-align: center !important;
       }
       
       /* Streamlit dividers */
       .stMarkdown hr {
           margin: 70px auto !important;
           border-color: #ffffff !important;
       }
       
       [data-testid="stHorizontalBlock"] hr {
           margin: 50px auto !important;
           border-color: #ffffff !important;
       }
       
       /* Hide Streamlit branding BUT NOT HEADER */
       footer {
           visibility: hidden;
       }
       /* header {visibility: hidden;} - REMOVED - Need header for top navigation */
       
       /* CHECKBOX STYLES - Clean approach based on Inspector */
       /* Override accent-color for checkbox */
       input[type="checkbox"] {
           accent-color: #26282c !important;
       }
       
       /* Specific class from inspector */
       input.st-bn[type="checkbox"] {
           accent-color: #26282c !important;
       }
       
       /* When checked */
       input[type="checkbox"][aria-checked="true"] {
           accent-color: #26282c !important;
       }
       
       /* BUTTONS */
       
       /* Custom button styling */
       .stButton > button {
           background-color: #DDDDDD;
           color: #26282c;
           border: none;
           padding: 0.5rem 2rem;
           border-radius: 4px;
           font-weight: 500;
           transition: all 0.3s;
           min-width: 150px;
       }
       
       .stButton > button:hover {
           background-color: #CCCCCC;
           transform: translateY(-2px);
       }
       
       .stButton > button:disabled {
           background-color: #4a4a4a;
           cursor: not-allowed;
           transform: none;
           opacity: 0.6;
       }
       </style>
       """,
        unsafe_allow_html=True,
    )
