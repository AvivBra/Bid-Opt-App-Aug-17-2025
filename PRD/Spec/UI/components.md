# איפיון קומפוננטות UI - Bid Optimizer

## 1. Button Component

### Primary Button
```python
def render_primary_button(label: str, key: str, disabled: bool = False):
    """Render primary action button"""
    
    return st.button(
        label=label.upper(),
        key=key,
        disabled=disabled,
        use_container_width=False,
        type="primary"
    )
```

### Style
```css
.button-primary {
    width: 200px;
    height: 44px;
    background: #8B5CF6;
    color: #FFFFFF;
    border: none;
    border-radius: 4px;
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    font-weight: 400;
    text-transform: uppercase;
    cursor: pointer;
    transition: all 0.2s;
}

.button-primary:hover {
    background: #7C3AED;
}

.button-primary:disabled {
    background: #2D2D2D;
    color: #666666;
    cursor: not-allowed;
}
```

### Usage Examples
```python
# Process button
render_primary_button("Process Files", "process_btn")

# Download button
render_primary_button("Download Working", "download_working")

# Reset button
render_primary_button("Reset", "reset_btn")
```

## 2. File Upload Component

### Upload Button
```python
def render_upload_button(file_type: str, label: str):
    """Render file upload button"""
    
    uploaded = st.file_uploader(
        label="",
        type=['xlsx', 'csv'],
        key=f"upload_{file_type}",
        label_visibility="collapsed"
    )
    
    if uploaded:
        # Store in session state
        st.session_state[f'{file_type}_file'] = uploaded
        st.success(f"{label} uploaded successfully")
    
    return uploaded
```

### Multi-Upload Grid
```python
def render_bulk_upload_buttons():
    """Render all bulk upload buttons"""
    
    # First row
    col1, col2 = st.columns(2)
    with col1:
        render_primary_button("Download Template", "template_download")
    with col2:
        render_primary_button("Bulk 7 Days", "bulk_7_upload")
    
    # Second row
    col1, col2 = st.columns(2)
    with col1:
        render_primary_button("Bulk 30 Days", "bulk_30_upload")
    with col2:
        render_primary_button("Bulk 60 Days", "bulk_60_upload")
    
    # Data Rova - centered
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        render_primary_button("Data Rova", "data_rova_upload")
```

## 3. Checkbox List Component

### Optimization Checklist
```python
def render_optimization_checklist():
    """Render list of optimization checkboxes"""
    
    optimizations = [
        "Zero Sales",
        # TBD - Future optimizations
    ]
    
    selected = []
    
    st.markdown(
        """
        <div class="checkbox-container">
        """,
        unsafe_allow_html=True
    )
    
    for opt in optimizations:
        if st.checkbox(opt, key=f"opt_{opt.replace(' ', '_').lower()}"):
            selected.append(opt)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Store in session state
    st.session_state.selected_optimizations = selected
    
    return selected
```

### Checkbox Style
```css
.checkbox-container {
    background: #0F0F0F;
    border: 1px solid #2D2D2D;
    border-radius: 4px;
    padding: 16px;
}

.stCheckbox {
    margin-bottom: 12px;
}

.stCheckbox > label {
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    color: #FFFFFF;
}

.stCheckbox > div[data-baseweb="checkbox"] {
    width: 16px;
    height: 16px;
}
```

## 4. Progress Bar Component

### Processing Progress
```python
def render_progress_bar(progress: float, text: str = ""):
    """Render progress bar with text"""
    
    # Streamlit native progress
    progress_bar = st.progress(progress)
    
    if text:
        st.markdown(
            f"""
            <div class="progress-text">
                {text}
            </div>
            """,
            unsafe_allow_html=True
        )
    
    return progress_bar
```

### Animated Progress
```python
def animate_progress(duration: int = 3):
    """Animate progress from 0 to 100%"""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(101):
        progress_bar.progress(i)
        status_text.text(f"Processing... {i}%")
        time.sleep(duration / 100)
    
    status_text.text("Complete!")
```

## 5. Alert Component

### Alert Messages
```python
def render_alert(message: str, alert_type: str = "info"):
    """Render alert message"""
    
    icons = {
        "success": "✓",
        "error": "✗",
        "warning": "⚠",
        "info": "ℹ"
    }
    
    colors = {
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B",
        "info": "#3B82F6"
    }
    
    st.markdown(
        f"""
        <div class="alert alert-{alert_type}">
            <span class="alert-icon">{icons.get(alert_type, '')}</span>
            <span class="alert-message">{message}</span>
        </div>
        """,
        unsafe_allow_html=True
    )
```

### Pink Notice
```python
def render_pink_notice(error_count: int):
    """Render pink notice for calculation errors"""
    
    st.markdown(
        f"""
        <div class="pink-notice">
            Please note: {error_count} calculation errors in Zero Sales optimization
        </div>
        """,
        unsafe_allow_html=True
    )
```

## 6. Status Display Component

### File Status
```python
def render_file_status():
    """Display status of uploaded files"""
    
    files = {
        "Template": st.session_state.get('template_file'),
        "Bulk 7": st.session_state.get('bulk_7_file'),
        "Bulk 30": st.session_state.get('bulk_30_file'),
        "Bulk 60": st.session_state.get('bulk_60_file'),
        "Data Rova": st.session_state.get('data_rova_file')
    }
    
    status_html = "<div class='file-status'>"
    
    for name, file in files.items():
        if file:
            status = f"✓ {name}: {file.name}"
            color = "#10B981"
        else:
            status = f"{name}: Not uploaded"
            color = "#666666"
        
        status_html += f'<span style="color: {color}">{status}</span><br>'
    
    status_html += "</div>"
    
    st.markdown(status_html, unsafe_allow_html=True)
```

## 7. Section Header Component

### Section Title
```python
def render_section_header(title: str):
    """Render section header"""
    
    st.markdown(
        f"""
        <h2 class="section-header">{title.upper()}</h2>
        """,
        unsafe_allow_html=True
    )
```

### Style
```css
.section-header {
    font-family: 'Inter', sans-serif;
    font-size: 18px;
    font-weight: 400;
    text-transform: uppercase;
    color: #FFFFFF;
    margin-bottom: 24px;
    padding-bottom: 12px;
    border-bottom: 1px solid #2D2D2D;
}
```

## 8. Validation Results Component

### Results Display
```python
def render_validation_results(results: dict):
    """Display validation results"""
    
    if results['is_valid']:
        render_alert("All portfolios valid", "success")
        st.markdown(f"{results['row_count']} rows ready for processing")
        
        # Enable process button
        render_primary_button("Process Files", "process_btn", disabled=False)
    
    else:
        render_alert("Validation failed", "error")
        
        # Show specific errors
        for error in results['errors']:
            st.markdown(f"• {error}")
        
        # Upload new template button
        render_primary_button("Upload New Template", "new_template_btn")
```

## 9. Statistics Component

### Processing Stats
```python
def render_statistics(stats: dict):
    """Render processing statistics"""
    
    st.markdown(
        """
        <div class="stats-container">
            <h3>Processing Statistics</h3>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Rows Processed", stats.get('rows_processed', 0))
    
    with col2:
        st.metric("Rows Modified", stats.get('rows_modified', 0))
    
    with col3:
        st.metric("Errors", stats.get('errors', 0))
    
    with col4:
        st.metric("Time", stats.get('processing_time', '0s'))
    
    st.markdown("</div>", unsafe_allow_html=True)
```

## 10. Download Component

### Download Buttons
```python
def render_download_buttons():
    """Render file download buttons"""
    
    working_file = st.session_state.get('output_files', {}).get('working')
    clean_file = st.session_state.get('output_files', {}).get('clean')
    
    col1, col2 = st.columns(2)
    
    with col1:
        if working_file:
            st.download_button(
                label="DOWNLOAD WORKING",
                data=working_file,
                file_name=f"Working_File_{datetime.now():%Y%m%d_%H%M}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_working"
            )
    
    with col2:
        if clean_file:
            st.download_button(
                label="DOWNLOAD CLEAN",
                data=clean_file,
                file_name=f"Clean_File_{datetime.now():%Y%m%d_%H%M}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_clean"
            )
```

## 11. Modal Component (Future)

### Confirmation Modal
```python
def render_confirmation_modal(title: str, message: str):
    """Render confirmation modal"""
    
    # Streamlit doesn't have native modals yet
    # Using expander as alternative
    
    with st.expander(title, expanded=True):
        st.write(message)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("CONFIRM", key="modal_confirm"):
                return True
        with col2:
            if st.button("CANCEL", key="modal_cancel"):
                return False
    
    return None
```

## 12. Loading Component

### Loading Spinner
```python
def render_loading(message: str = "Loading..."):
    """Render loading spinner"""
    
    with st.spinner(message):
        # Content to load
        yield
```

### Usage
```python
with render_loading("Processing files..."):
    # Heavy processing here
    process_files()
```

## 13. Empty State Component

### No Data Display
```python
def render_empty_state(message: str, action_label: str = None):
    """Render empty state message"""
    
    st.markdown(
        f"""
        <div class="empty-state">
            <p class="empty-message">{message}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if action_label:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            render_primary_button(action_label, "empty_action")
```

### Style
```css
.empty-state {
    text-align: center;
    padding: 40px;
    color: #666666;
}

.empty-message {
    font-size: 16px;
    margin-bottom: 20px;
}
```