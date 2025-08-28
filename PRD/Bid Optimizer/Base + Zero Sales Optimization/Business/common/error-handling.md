# איפיון טיפול בשגיאות - Bid Optimizer

## 1. סקירה כללית

### עקרונות
- הודעות ברורות למשתמש
- אפשרות התאוששות מכל שגיאה
- לא לקרוס את האפליקציה
- תיעוד שגיאות ללא חשיפת מידע טכני מיותר

## 2. סוגי שגיאות

### היררכיה
```python
class BidOptimizerError(Exception):
    """Base exception for all application errors"""
    pass

class FileError(BidOptimizerError):
    """File-related errors"""
    pass

class ValidationError(BidOptimizerError):
    """Validation errors"""
    pass

class ProcessingError(BidOptimizerError):
    """Processing errors"""
    pass

class OptimizationError(ProcessingError):
    """Optimization-specific errors"""
    pass
```

## 3. File Errors

### שגיאות קבצים נפוצות
```python
FILE_ERROR_HANDLERS = {
    'size_exceeded': {
        'message': "File exceeds 40MB limit",
        'recovery': "Please use a smaller file or split into multiple files"
    },
    'wrong_format': {
        'message': "File must be Excel (.xlsx) or CSV format",
        'recovery': "Please convert your file to the correct format"
    },
    'corrupted': {
        'message': "Cannot read file - it may be corrupted",
        'recovery': "Please check the file and try again"
    },
    'missing_sheet': {
        'message': "Required sheet 'Sponsored Products Campaigns' not found",
        'recovery': "Please ensure your bulk file has the correct sheet name"
    },
    'wrong_columns': {
        'message': "File has incorrect number of columns (expected 48)",
        'recovery': "Please use the correct bulk file format from Amazon"
    }
}
```

### טיפול בשגיאות קבצים
```python
def handle_file_error(error_type: str, details: str = None):
    """Handle file upload errors"""
    
    error_info = FILE_ERROR_HANDLERS.get(error_type, {})
    message = error_info.get('message', 'File error occurred')
    recovery = error_info.get('recovery', 'Please try again')
    
    # Display error
    st.error(f"❌ {message}")
    if details:
        st.error(f"Details: {details}")
    st.info(f"💡 {recovery}")
    
    # Log error
    log_error('file_error', error_type, details)
    
    # Recovery button
    if st.button("Try Again", key="file_error_retry"):
        clear_file_state()
        st.experimental_rerun()
```

## 4. Validation Errors

### שגיאות validation נפוצות
```python
VALIDATION_ERROR_HANDLERS = {
    'missing_portfolios': {
        'message': "Missing portfolios found in bulk file",
        'recovery': "Upload a new template with all required portfolios",
        'action': 'upload_new_template'
    },
    'all_ignored': {
        'message': "All portfolios are marked as 'Ignore'",
        'recovery': "At least one portfolio must be active",
        'action': 'edit_template'
    },
    'no_data_after_filter': {
        'message': "No rows left after filtering",
        'recovery': "Check that your bulk file contains rows with Units=0",
        'action': 'check_data'
    },
    'missing_required_columns': {
        'message': "Required columns are missing",
        'recovery': "Ensure your file has all required columns",
        'action': 'check_structure'
    }
}
```

### תצוגת שגיאות validation
```python
def display_validation_errors(errors: list):
    """Display validation errors with recovery options"""
    
    st.markdown(
        """
        <div class='validation-error-container'>
            <h3>Validation Failed</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    for error in errors:
        error_type = identify_error_type(error)
        handler = VALIDATION_ERROR_HANDLERS.get(error_type, {})
        
        # Error message
        st.error(f"❌ {handler.get('message', error)}")
        
        # Recovery suggestion
        st.info(f"💡 {handler.get('recovery', 'Please check your files')}")
    
    # Recovery actions
    col1, col2 = st.columns(2)
    with col1:
        if st.button("UPLOAD NEW TEMPLATE", key="validation_new_template"):
            st.session_state.show_template_uploader = True
    with col2:
        if st.button("UPLOAD NEW BULK", key="validation_new_bulk"):
            st.session_state.show_bulk_uploader = True
```

## 5. Processing Errors

### שגיאות עיבוד
```python
def handle_processing_error(error: Exception, optimization: str):
    """Handle errors during processing"""
    
    # Determine error type
    if isinstance(error, MemoryError):
        handle_memory_error()
    elif isinstance(error, TimeoutError):
        handle_timeout_error()
    elif isinstance(error, CalculationError):
        handle_calculation_error(error, optimization)
    else:
        handle_generic_error(error)
    
    # Update state
    st.session_state.processing_status = 'error'
    st.session_state.processing_error = str(error)
```

### Memory Error
```python
def handle_memory_error():
    """Handle out of memory errors"""
    
    st.error("❌ Out of memory while processing")
    st.warning("Your file is too large to process in memory")
    
    st.info(
        """
        💡 Try one of these solutions:
        1. Use a smaller date range (e.g., 7 days instead of 30)
        2. Filter unnecessary rows before uploading
        3. Split the file into smaller parts
        """
    )
    
    if st.button("RESET AND TRY AGAIN", key="memory_error_reset"):
        reset_processing_state()
        st.experimental_rerun()
```

## 6. Calculation Errors

### שגיאות חישוב ב-Zero Sales
```python
def handle_calculation_errors(df: pd.DataFrame) -> dict:
    """Handle calculation errors in optimization"""
    
    errors = {
        'low_bids': 0,
        'high_bids': 0,
        'calc_failures': 0,
        'rows_affected': []
    }
    
    # Check for bid range errors
    low_mask = df['Bid'] < 0.02
    high_mask = df['Bid'] > 1.25
    nan_mask = df['Bid'].isna()
    
    errors['low_bids'] = low_mask.sum()
    errors['high_bids'] = high_mask.sum()
    errors['calc_failures'] = nan_mask.sum()
    
    # Mark error rows
    df['has_error'] = low_mask | high_mask | nan_mask
    errors['rows_affected'] = df[df['has_error']].index.tolist()
    
    return errors
```

### Pink Notice Display
```python
def render_calculation_error_notice(errors: dict):
    """Display pink notice for calculation errors"""
    
    total_errors = errors['low_bids'] + errors['high_bids'] + errors['calc_failures']
    
    if total_errors > 0:
        st.markdown(
            f"""
            <div style='background-color: #FFE4E1; 
                        border: 1px solid #FFB6C1;
                        border-radius: 4px; 
                        padding: 20px; 
                        margin: 20px 0;
                        text-align: center;'>
                <div style='color: #8B0000; font-weight: bold;'>
                    Please note: {total_errors} calculation errors in Zero Sales optimization
                </div>
                <div style='color: #8B0000; margin-top: 10px;'>
                    {errors['low_bids']} rows below 0.02, 
                    {errors['high_bids']} rows above 1.25, 
                    {errors['calc_failures']} calculation failures
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
```

## 7. הודעות שגיאה

### רמות חומרה
```python
def display_error_by_severity(error: Exception):
    """Display error based on severity"""
    
    severity = get_error_severity(error)
    
    if severity == 'critical':
        st.error(f"❌ Critical Error: {str(error)}")
        st.stop()  # Stop execution
    
    elif severity == 'error':
        st.error(f"❌ Error: {str(error)}")
        # Allow continuation with recovery
    
    elif severity == 'warning':
        st.warning(f"⚠️ Warning: {str(error)}")
        # Continue normally
    
    elif severity == 'info':
        st.info(f"ℹ️ Note: {str(error)}")
```

### User-Friendly Messages
```python
ERROR_MESSAGE_MAPPING = {
    'KeyError': "Missing required data field",
    'ValueError': "Invalid data format",
    'TypeError': "Unexpected data type",
    'MemoryError': "Not enough memory to process",
    'TimeoutError': "Processing took too long",
    'FileNotFoundError': "File not found",
    'PermissionError': "No permission to access file"
}

def get_user_friendly_message(error: Exception) -> str:
    """Convert technical error to user-friendly message"""
    
    error_type = type(error).__name__
    return ERROR_MESSAGE_MAPPING.get(
        error_type,
        "An unexpected error occurred"
    )
```

## 8. Error Logging

### Log Structure
```python
def log_error(category: str, error: Exception, context: dict = None):
    """Log error for debugging"""
    
    error_log = {
        'timestamp': datetime.now(),
        'category': category,
        'error_type': type(error).__name__,
        'error_message': str(error),
        'context': context or {},
        'traceback': traceback.format_exc()
    }
    
    # Store in session for debugging
    if 'error_log' not in st.session_state:
        st.session_state.error_log = []
    
    st.session_state.error_log.append(error_log)
    
    # Also log to console in debug mode
    if st.session_state.get('debug_mode'):
        print(f"ERROR: {error_log}")
```

## 9. Recovery Actions

### אפשרויות התאוששות
```python
def show_recovery_options(error_type: str):
    """Show recovery options based on error type"""
    
    st.markdown("### Recovery Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("RETRY", key="recovery_retry"):
            retry_last_action()
    
    with col2:
        if st.button("RESET", key="recovery_reset"):
            reset_to_clean_state()
    
    with col3:
        if st.button("START OVER", key="recovery_start_over"):
            complete_reset()
```

## 10. Error Prevention

### Validation Before Processing
```python
def pre_process_validation() -> tuple[bool, list]:
    """Validate everything before starting processing"""
    
    errors = []
    
    # Check files exist
    if not st.session_state.get('template_file'):
        errors.append("Template file is missing")
    
    if not any([
        st.session_state.get('bulk_7_file'),
        st.session_state.get('bulk_30_file'),
        st.session_state.get('bulk_60_file')
    ]):
        errors.append("At least one bulk file is required")
    
    # Check optimizations selected
    if not st.session_state.get('selected_optimizations'):
        errors.append("No optimizations selected")
    
    # Check data integrity
    if st.session_state.get('template_df') is None:
        errors.append("Template data is not loaded properly")
    
    return len(errors) == 0, errors
```

## 11. Debug Mode

### הצגת מידע debug
```python
def render_debug_info():
    """Show debug information when enabled"""
    
    if st.checkbox("Show Debug Info", key="show_debug"):
        with st.expander("Debug Information"):
            # Error log
            if st.session_state.get('error_log'):
                st.write("### Recent Errors")
                for error in st.session_state.error_log[-5:]:
                    st.json(error)
            
            # State info
            st.write("### Current State")
            st.json({
                k: str(v)[:100] 
                for k, v in st.session_state.items()
            })
```