# איפיון עמוד Bid Optimizer

## 1. סקירה כללית

### מטרת העמוד
עמוד ראשי לביצוע אופטימיזציות על קבצי Bulk של Amazon Advertising.

### מבנה העמוד
- Select Optimizations
- Upload Files  
- Data Validation
- Output Files

## 2. Page Structure

```python
def render_bid_optimizer_page():
    """Main page for Bid Optimizer"""
    
    # Page title
    st.markdown("<h1 style='text-align: center;'>BID OPTIMIZER</h1>", 
                unsafe_allow_html=True)
    
    # Section 1: Select Optimizations
    render_optimization_section()
    
    # Section 2: Upload Files
    render_upload_section()
    
    # Section 3: Data Validation (conditional)
    if has_uploaded_files():
        render_validation_section()
    
    # Section 4: Output Files (conditional)
    if st.session_state.get('processing_status') in ['processing', 'complete']:
        render_output_section()
```

## 3. Select Optimizations Section

### Layout
```python
def render_optimization_section():
    """Render optimization selection"""
    
    with st.container():
        st.markdown(
            """
            <div class='section-container'>
                <h2 class='section-header'>SELECT OPTIMIZATIONS</h2>
            """,
            unsafe_allow_html=True
        )
        
        # Checkbox list
        optimizations = {
            'zero_sales': 'Zero Sales',
            # TBD - Future optimizations will be added here
        }
        
        selected = []
        for key, label in optimizations.items():
            if st.checkbox(label, key=f"opt_{key}"):
                selected.append(key)
        
        st.session_state.selected_optimizations = selected
        
        st.markdown("</div>", unsafe_allow_html=True)
```

### Business Rules
- לפחות אופטימיזציה אחת חייבת להיות מסומנת
- Zero Sales זמינה תמיד
- אופטימיזציות עתידיות יתווספו בשלבים 3-4

## 4. Upload Files Section

### Layout
```python
def render_upload_section():
    """Render file upload section"""
    
    with st.container():
        st.markdown(
            """
            <div class='section-container'>
                <h2 class='section-header'>UPLOAD FILES</h2>
            """,
            unsafe_allow_html=True
        )
        
        # Template download/upload
        col1, col2 = st.columns(2)
        
        with col1:
            # Download template
            template_data = generate_template()
            st.download_button(
                label="DOWNLOAD TEMPLATE",
                data=template_data,
                file_name="template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        with col2:
            # Bulk 7 Days
            if st.button("BULK 7 DAYS", key="bulk_7_btn"):
                show_file_uploader('bulk_7')
        
        # Second row
        col1, col2 = st.columns(2)
        
        with col1:
            # Bulk 30 Days
            if st.button("BULK 30 DAYS", key="bulk_30_btn"):
                show_file_uploader('bulk_30')
        
        with col2:
            # Bulk 60 Days
            if st.button("BULK 60 DAYS", key="bulk_60_btn"):
                show_file_uploader('bulk_60')
        
        # Data Rova - centered
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("DATA ROVA", key="data_rova_btn"):
                st.info("Data Rova integration - TBD")
        
        # File status
        render_file_status()
        
        st.markdown("</div>", unsafe_allow_html=True)
```

### File Upload Logic
```python
def show_file_uploader(file_type: str):
    """Show file uploader for specific type"""
    
    uploaded = st.file_uploader(
        f"Upload {file_type.replace('_', ' ').title()}",
        type=['xlsx', 'csv'],
        key=f"upload_{file_type}"
    )
    
    if uploaded:
        # Validate file
        if uploaded.size > 40 * 1024 * 1024:
            st.error("File exceeds 40MB limit")
            return
        
        # Store in session
        st.session_state[f'{file_type}_file'] = uploaded
        st.session_state[f'{file_type}_df'] = read_file(uploaded, file_type)
        st.success(f"{file_type.replace('_', ' ').title()} uploaded successfully")
```

## 5. Data Validation Section

### Layout
```python
def render_validation_section():
    """Render validation results"""
    
    with st.container():
        st.markdown(
            """
            <div class='section-container'>
                <h2 class='section-header'>DATA VALIDATION</h2>
            """,
            unsafe_allow_html=True
        )
        
        # Check which optimizations need which files
        validation_results = validate_files_for_optimizations()
        
        if validation_results['all_valid']:
            st.success("All required files are valid")
            st.info(f"{validation_results['total_rows']} rows ready for processing")
            
            # Process button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("PROCESS FILES", key="process_btn"):
                    start_processing()
        else:
            # Show errors
            for error in validation_results['errors']:
                st.error(error)
            
            # Allow re-upload
            if st.button("UPLOAD NEW FILES", key="reupload_btn"):
                reset_upload_state()
        
        st.markdown("</div>", unsafe_allow_html=True)
```

### Validation per Optimization
```python
def validate_files_for_optimizations():
    """Validate files for selected optimizations"""
    
    results = {
        'all_valid': True,
        'errors': [],
        'total_rows': 0
    }
    
    for opt in st.session_state.selected_optimizations:
        if opt == 'zero_sales':
            # Zero Sales requires template and any bulk
            if not st.session_state.get('template_file'):
                results['errors'].append("Zero Sales requires Template file")
                results['all_valid'] = False
            
            has_bulk = any([
                st.session_state.get('bulk_7_file'),
                st.session_state.get('bulk_30_file'),
                st.session_state.get('bulk_60_file')
            ])
            
            if not has_bulk:
                results['errors'].append("Zero Sales requires at least one Bulk file")
                results['all_valid'] = False
            
            # Count rows if valid
            if results['all_valid']:
                bulk_df = get_first_available_bulk()
                results['total_rows'] = len(bulk_df)
    
    return results
```

## 6. Output Files Section

### Layout
```python
def render_output_section():
    """Render output section"""
    
    with st.container():
        st.markdown(
            """
            <div class='section-container'>
                <h2 class='section-header'>OUTPUT FILES</h2>
            """,
            unsafe_allow_html=True
        )
        
        status = st.session_state.get('processing_status')
        
        if status == 'processing':
            # Show progress
            progress = st.session_state.get('processing_progress', 0)
            st.progress(progress)
            st.info(f"Processing... {int(progress * 100)}%")
        
        elif status == 'complete':
            # Show results
            st.success("Processing complete")
            
            # File info
            stats = st.session_state.get('output_stats', {})
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Working File:** {stats.get('working_size', 'N/A')}")
                st.markdown(f"Sheets: {stats.get('working_sheets', 0)}")
            
            with col2:
                st.markdown(f"**Clean File:** {stats.get('clean_size', 'N/A')}")
                st.markdown(f"Sheets: {stats.get('clean_sheets', 0)}")
            
            # Check for errors
            if stats.get('calculation_errors', 0) > 0:
                render_pink_notice(stats['calculation_errors'])
            
            # Download buttons
            col1, col2 = st.columns(2)
            
            with col1:
                working_file = st.session_state.get('output_files', {}).get('working')
                if working_file:
                    st.download_button(
                        label="DOWNLOAD WORKING",
                        data=working_file,
                        file_name=f"Working_File_{datetime.now():%Y%m%d_%H%M}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            
            with col2:
                clean_file = st.session_state.get('output_files', {}).get('clean')
                if clean_file:
                    st.download_button(
                        label="DOWNLOAD CLEAN",
                        data=clean_file,
                        file_name=f"Clean_File_{datetime.now():%Y%m%d_%H%M}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            
            # Reset button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("RESET", key="reset_btn"):
                    reset_all_state()
        
        st.markdown("</div>", unsafe_allow_html=True)
```

## 7. Processing Logic

### Start Processing
```python
def start_processing():
    """Start processing selected optimizations"""
    
    # Update status
    st.session_state.processing_status = 'processing'
    st.session_state.processing_progress = 0
    
    # Get selected optimizations
    selected = st.session_state.selected_optimizations
    
    # Process each optimization
    results = {}
    for i, opt in enumerate(selected):
        # Update progress
        progress = (i + 1) / len(selected)
        st.session_state.processing_progress = progress
        
        # Process
        if opt == 'zero_sales':
            results['zero_sales'] = process_zero_sales()
        # TBD - other optimizations
        
        # Force UI update
        st.experimental_rerun()
    
    # Generate output files
    generate_output_files(results)
    
    # Update status
    st.session_state.processing_status = 'complete'
    st.experimental_rerun()
```

## 8. State Management

### Page State
```python
def initialize_page_state():
    """Initialize page-specific state"""
    
    if 'page_initialized' not in st.session_state:
        st.session_state.page_initialized = True
        st.session_state.selected_optimizations = []
        st.session_state.processing_status = 'idle'
        st.session_state.processing_progress = 0
        st.session_state.output_files = {}
        st.session_state.output_stats = {}
```

### Reset Functions
```python
def reset_all_state():
    """Reset all page state"""
    
    # Clear files
    for key in list(st.session_state.keys()):
        if any(x in key for x in ['file', 'df', 'output', 'processing']):
            del st.session_state[key]
    
    # Reinitialize
    initialize_page_state()
    st.experimental_rerun()

def reset_upload_state():
    """Reset only upload state"""
    
    for key in list(st.session_state.keys()):
        if 'file' in key or 'df' in key:
            del st.session_state[key]
    
    st.experimental_rerun()
```

## 9. Error Handling

### Error Display
```python
def handle_processing_error(error: Exception):
    """Handle errors during processing"""
    
    st.session_state.processing_status = 'error'
    
    # Display error
    st.error(f"Processing failed: {str(error)}")
    
    # Log details
    with st.expander("Error Details"):
        st.code(traceback.format_exc())
    
    # Recovery options
    col1, col2 = st.columns(2)
    with col1:
        if st.button("RETRY", key="retry_btn"):
            start_processing()
    with col2:
        if st.button("RESET", key="error_reset_btn"):
            reset_all_state()
```

## 10. Performance Monitoring

### Processing Time
```python
def monitor_processing():
    """Monitor and display processing performance"""
    
    start_time = time.time()
    
    # ... processing ...
    
    elapsed = time.time() - start_time
    
    st.session_state.output_stats['processing_time'] = f"{elapsed:.1f}s"
    
    # Warning if too slow
    if elapsed > 60:
        st.warning(f"Processing took {elapsed:.1f} seconds. Consider using smaller files.")
```