"""Checklist component for optimization selection."""

import streamlit as st
from typing import List, Dict, Any


def create_optimization_checklist(
    optimizations: List[Dict[str, Any]], 
    key_prefix: str = "opt"
) -> List[str]:
    """
    Create a checklist for optimization selection.
    
    Args:
        optimizations: List of optimization dictionaries with keys:
            - name: Display name
            - key: Unique key for the optimization
            - enabled: Whether checkbox is enabled
            - default: Default checked state
            - help: Help text
        key_prefix: Prefix for Streamlit keys
    
    Returns:
        List of selected optimization keys
    """
    
    selected_optimizations = []
    
    for opt in optimizations:
        opt_name = opt['name']
        opt_key = opt['key']
        opt_enabled = opt.get('enabled', True)
        opt_default = opt.get('default', False)
        opt_help = opt.get('help', '')
        
        checkbox_key = f"{key_prefix}_{opt_key}"
        
        # Get current state from session if exists
        current_value = st.session_state.get(checkbox_key, opt_default)
        
        is_checked = st.checkbox(
            opt_name,
            value=current_value,
            disabled=not opt_enabled,
            help=opt_help,
            key=checkbox_key
        )
        
        if is_checked and opt_enabled:
            selected_optimizations.append(opt_key)
    
    return selected_optimizations


def create_validation_checklist(validation_items: List[Dict[str, Any]]) -> Dict[str, bool]:
    """
    Create a validation status checklist.
    
    Args:
        validation_items: List of validation items with keys:
            - name: Display name
            - status: 'pass', 'fail', 'warning', 'pending'
            - message: Status message
    
    Returns:
        Dictionary mapping item names to pass/fail status
    """
    
    results = {}
    
    for item in validation_items:
        name = item['name']
        status = item.get('status', 'pending')
        message = item.get('message', '')
        
        # Status icon and color
        if status == 'pass':
            icon = "✅"
            color = "success"
        elif status == 'fail':
            icon = "❌"
            color = "error"
        elif status == 'warning':
            icon = "⚠️"
            color = "warning"
        else:  # pending
            icon = "⏳"
            color = "info"
        
        # Display item
        col1, col2 = st.columns([1, 4])
        
        with col1:
            st.markdown(f"<span style='font-size: 20px;'>{icon}</span>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"**{name}**")
            if message:
                if color == "success":
                    st.success(message)
                elif color == "error":
                    st.error(message)
                elif color == "warning":
                    st.warning(message)
                else:
                    st.info(message)
        
        results[name] = status == 'pass'
    
    return results


def create_file_status_checklist(file_statuses: Dict[str, Dict[str, Any]]) -> None:
    """
    Create a checklist showing file upload status.
    
    Args:
        file_statuses: Dictionary mapping file types to status info
    """
    
    st.markdown("#### 📁 File Upload Status")
    
    for file_type, status_info in file_statuses.items():
        uploaded = status_info.get('uploaded', False)
        filename = status_info.get('filename', 'Not uploaded')
        data_available = status_info.get('data_available', False)
        
        col1, col2, col3 = st.columns([1, 3, 2])
        
        with col1:
            if uploaded and data_available:
                st.markdown("✅")
            elif uploaded:
                st.markdown("⚠️")
            else:
                st.markdown("❌")
        
        with col2:
            st.markdown(f"**{file_type.replace('_', ' ').title()}**")
            st.caption(filename if uploaded else "Not uploaded")
        
        with col3:
            if uploaded and data_available:
                st.success("Ready")
            elif uploaded:
                st.warning("Issues")
            else:
                st.error("Missing")


def create_processing_steps_checklist(steps: List[Dict[str, Any]]) -> None:
    """
    Create a checklist showing processing steps.
    
    Args:
        steps: List of processing steps with keys:
            - name: Step name
            - status: 'complete', 'in_progress', 'pending', 'failed'
            - message: Optional status message
    """
    
    st.markdown("#### ⚙️ Processing Steps")
    
    for i, step in enumerate(steps, 1):
        name = step['name']
        status = step.get('status', 'pending')
        message = step.get('message', '')
        
        col1, col2 = st.columns([1, 4])
        
        with col1:
            if status == 'complete':
                st.markdown(f"✅ {i}")
            elif status == 'in_progress':
                st.markdown(f"⏳ {i}")
            elif status == 'failed':
                st.markdown(f"❌ {i}")
            else:  # pending
                st.markdown(f"⭕ {i}")
        
        with col2:
            st.markdown(f"**{name}**")
            if message:
                if status == 'complete':
                    st.success(message)
                elif status == 'failed':
                    st.error(message)
                elif status == 'in_progress':
                    st.info(message)
                else:
                    st.caption(message)