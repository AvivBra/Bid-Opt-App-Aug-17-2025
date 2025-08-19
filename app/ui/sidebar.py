"""Sidebar component for navigation."""

import streamlit as st
from config.constants import COLORS


def render_sidebar():
    """Render the navigation sidebar."""
    
    with st.sidebar:
        # Apply custom CSS for sidebar styling
        st.markdown(f"""
        <style>
        .sidebar .sidebar-content {{
            background-color: {COLORS['sidebar']};
            width: 200px;
        }}
        .nav-button {{
            width: 100%;
            margin-bottom: 8px;
        }}
        </style>
        """, unsafe_allow_html=True)
        
        # Application logo/title
        st.markdown(f"""
        <div style="text-align: center; padding: 20px 0; border-bottom: 1px solid {COLORS['accent']}30; margin-bottom: 20px;">
            <h2 style="color: {COLORS['accent']}; margin: 0;">BID OPTIMIZER</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation section
        st.markdown("### Navigation")
        
        # Navigation buttons
        pages = {
            'Bid Optimizer': {
                'active': True,
                'icon': '📊',
                'description': 'Optimize bids for Amazon campaigns'
            },
            'Campaigns Optimizer': {
                'active': False,
                'icon': '🎯', 
                'description': 'Coming Soon - Phase 2+'
            }
        }
        
        for page_name, page_config in pages.items():
            if page_config['active']:
                # Active page button
                button_type = "primary" if st.session_state.get('current_page') == page_name else "secondary"
                
                if st.button(
                    f"{page_config['icon']} {page_name}",
                    type=button_type,
                    use_container_width=True,
                    help=page_config['description'],
                    key=f"nav_{page_name.lower().replace(' ', '_')}"
                ):
                    st.session_state.current_page = page_name
                    st.rerun()
            else:
                # Disabled page button  
                st.button(
                    f"{page_config['icon']} {page_name}",
                    disabled=True,
                    use_container_width=True,
                    help=page_config['description'],
                    key=f"nav_{page_name.lower().replace(' ', '_')}_disabled"
                )
        
        # Footer section
        st.markdown("---")
        st.markdown(
            f"""
            <div style="text-align: center; color: {COLORS['text']}70; font-size: 12px;">
                <p>Phase 1: Zero Sales<br>
                Version 1.0.0</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Reset button
        if st.button("🔄 Reset Session", use_container_width=True, type="secondary"):
            # Clear session state except navigation
            keys_to_keep = ['current_page']
            for key in list(st.session_state.keys()):
                if key not in keys_to_keep:
                    del st.session_state[key]
            st.rerun()


def get_current_page() -> str:
    """Get the currently selected page."""
    return st.session_state.get('current_page', 'Bid Optimizer')