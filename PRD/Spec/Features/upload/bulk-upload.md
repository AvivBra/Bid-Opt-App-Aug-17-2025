# איפיון העלאת Bulk Files

## 1. סקירה כללית

### מטרה
אפשר למשתמש להעלות קבצי Bulk שונים (7/30/60 ימים) עם נתוני קמפיינים.

### סוגי קבצים
- **Bulk 7 Days** - נתוני 7 ימים אחרונים
- **Bulk 30 Days** - נתוני 30 ימים אחרונים  
- **Bulk 60 Days** - נתוני 60 ימים אחרונים

### מגבלות
- גודל מקסימלי: 40MB לקובץ
- מספר שורות מקסימלי: 500,000
- פורמט: Excel (.xlsx) או CSV
- Sheet נדרש: "Sponsored Products Campaigns"

## 2. מבנה Bulk Files

### דרישות מבנה
```python
BULK_FILE_REQUIREMENTS = {
    'sheet_name': 'Sponsored Products Campaigns',
    'num_columns': 48,
    'max_rows': 500000,
    'max_size_mb': 40,
    'required_columns': [
        'Product', 'Entity', 'Operation', 'Campaign ID',
        'Ad Group ID', 'Portfolio ID', 'Ad ID', 'Keyword ID',
        'Product Targeting ID', 'Campaign Name', 'Ad Group Name',
        'Campaign Name (Informational only)', 
        'Ad Group Name (Informational only)',
        'Portfolio Name (Informational only)',
        # ... כל 48 העמודות
    ]
}
```

## 3. Upload Handlers

### מטפל כללי
```python
def handle_bulk_upload(file_type: str, uploaded_file) -> dict:
    """Handle bulk file upload for any type (7/30/60)"""
    
    result = {
        'success': False,
        'data': None,
        'errors': [],
        'stats': {}
    }
    
    try:
        # 1. Validate file size
        if uploaded_file.size > 40 * 1024 * 1024:
            result['errors'].append(f"File exceeds 40MB limit")
            return result
        
        # 2. Read file
        df = read_bulk_file(uploaded_file)
        
        # 3. Validate structure  
        validation = validate_bulk_structure(df)
        if not validation['is_valid']:
            result['errors'] = validation['errors']
            return result
        
        # 4. Store in session
        st.session_state[f'bulk_{file_type}_df'] = df
        st.session_state[f'bulk_{file_type}_file'] = uploaded_file
        
        # 5. Calculate statistics
        result['stats'] = calculate_bulk_stats(df)
        result['success'] = True
        result['data'] = df
        
    except Exception as e:
        result['errors'].append(f"Failed to read bulk file: {str(e)}")
    
    return result
```

## 4. Validation

### מבנה הקובץ
```python
def validate_bulk_structure(df: pd.DataFrame) -> dict:
    """Validate bulk file structure"""
    
    validation = {
        'is_valid': True,
        'errors': [],
        'warnings': []
    }
    
    # 1. Check column count
    if len(df.columns) != 48:
        validation['errors'].append(f"File must have exactly 48 columns, found {len(df.columns)}")
        validation['is_valid'] = False
        return validation
    
    # 2. Check column names
    expected_cols = BULK_FILE_REQUIREMENTS['required_columns']
    if list(df.columns) != expected_cols:
        missing = set(expected_cols) - set(df.columns)
        if missing:
            validation['errors'].append(f"Missing columns: {missing}")
            validation['is_valid'] = False
    
    # 3. Check row count
    if len(df) > 500000:
        validation['errors'].append(f"File has {len(df)} rows, maximum is 500,000")
        validation['is_valid'] = False
    
    # 4. Check if empty
    if len(df) == 0:
        validation['errors'].append("File has no data rows")
        validation['is_valid'] = False
    
    return validation
```

## 5. UI Components

### כפתורי העלאה
```python
def render_bulk_upload_buttons():
    """Render all bulk upload buttons in grid layout"""
    
    # First row - Template + Bulk 7
    col1, col2 = st.columns(2)
    
    with col1:
        # Template download handled separately
        pass
    
    with col2:
        if st.button("BULK 7 DAYS", key="bulk_7_btn"):
            st.session_state.show_bulk_7_uploader = True
    
    # Second row - Bulk 30 + Bulk 60
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("BULK 30 DAYS", key="bulk_30_btn"):
            st.session_state.show_bulk_30_uploader = True
    
    with col2:
        if st.button("BULK 60 DAYS", key="bulk_60_btn"):
            st.session_state.show_bulk_60_uploader = True
    
    # Show uploaders if buttons clicked
    render_bulk_uploaders()
```

### אזורי העלאה
```python
def render_bulk_uploaders():
    """Render file uploaders for each bulk type"""
    
    for bulk_type in ['7', '30', '60']:
        if st.session_state.get(f'show_bulk_{bulk_type}_uploader'):
            with st.container():
                uploaded = st.file_uploader(
                    f"Upload Bulk {bulk_type} Days",
                    type=['xlsx', 'csv'],
                    key=f"bulk_{bulk_type}_uploader"
                )
                
                if uploaded:
                    result = handle_bulk_upload(bulk_type, uploaded)
                    
                    if result['success']:
                        st.success(f"Bulk {bulk_type} uploaded successfully")
                        display_bulk_stats(result['stats'])
                    else:
                        for error in result['errors']:
                            st.error(error)
```

## 6. מצב הקבצים

### תצוגת סטטוס
```python
def render_bulk_file_status():
    """Display status of all bulk files"""
    
    status_items = []
    
    for bulk_type in ['7', '30', '60']:
        file = st.session_state.get(f'bulk_{bulk_type}_file')
        
        if file:
            df = st.session_state.get(f'bulk_{bulk_type}_df')
            size_mb = file.size / 1024 / 1024
            status_items.append(f"✓ Bulk {bulk_type}: {len(df):,} rows, {size_mb:.1f}MB")
        else:
            status_items.append(f"Bulk {bulk_type}: Not uploaded")
    
    # Display all statuses
    for status in status_items:
        if "✓" in status:
            st.success(status)
        else:
            st.info(status)
```

## 7. איזה Bulk לאיזו אופטימיזציה

### מיפוי דרישות
```python
OPTIMIZATION_BULK_REQUIREMENTS = {
    'zero_sales': {
        'bulk_7': False,
        'bulk_30': True,   # Preferred
        'bulk_60': True,   # Alternative
        'any_bulk': True   # At least one required
    },
    # TBD - אופטימיזציות עתידיות יגדירו דרישות משלהן
}
```

### בדיקת דרישות
```python
def check_bulk_requirements(optimization: str) -> tuple[bool, str]:
    """Check if required bulk files are uploaded"""
    
    requirements = OPTIMIZATION_BULK_REQUIREMENTS.get(optimization, {})
    
    if requirements.get('any_bulk'):
        # Check if any bulk file is uploaded
        has_any = any([
            st.session_state.get('bulk_7_file'),
            st.session_state.get('bulk_30_file'),
            st.session_state.get('bulk_60_file')
        ])
        
        if not has_any:
            return False, "At least one bulk file is required"
    
    # Check specific requirements
    for bulk_type in ['7', '30', '60']:
        if requirements.get(f'bulk_{bulk_type}'):
            if not st.session_state.get(f'bulk_{bulk_type}_file'):
                return False, f"Bulk {bulk_type} Days is required"
    
    return True, "All requirements met"
```

## 8. Multiple File Upload

### העלאת מספר קבצים
```python
def handle_multiple_bulk_uploads():
    """Allow uploading multiple bulk files"""
    
    uploaded_files = {}
    
    # User can upload any combination
    if st.session_state.get('bulk_7_file'):
        uploaded_files['7'] = st.session_state.bulk_7_file
    
    if st.session_state.get('bulk_30_file'):
        uploaded_files['30'] = st.session_state.bulk_30_file
    
    if st.session_state.get('bulk_60_file'):
        uploaded_files['60'] = st.session_state.bulk_60_file
    
    return uploaded_files
```

### בחירת קובץ לעיבוד
```python
def select_bulk_for_processing(optimization: str) -> pd.DataFrame:
    """Select appropriate bulk file for optimization"""
    
    # Priority order: 30 days > 60 days > 7 days
    priority_order = ['30', '60', '7']
    
    for bulk_type in priority_order:
        df = st.session_state.get(f'bulk_{bulk_type}_df')
        if df is not None:
            st.info(f"Using Bulk {bulk_type} Days for processing")
            return df
    
    return None
```

## 9. Error Messages

### הודעות שגיאה נפוצות
```python
BULK_ERROR_MESSAGES = {
    'size_exceeded': "File exceeds 40MB limit",
    'wrong_columns': "File must have exactly 48 columns",
    'missing_sheet': "Sheet 'Sponsored Products Campaigns' not found",
    'too_many_rows': "File exceeds 500,000 rows limit",
    'empty_file': "File has no data",
    'wrong_format': "File must be Excel (.xlsx) or CSV",
    'read_error': "Cannot read file - it may be corrupted"
}
```

## 10. Performance Optimization

### קריאה מהירה
```python
def read_bulk_file_optimized(uploaded_file) -> pd.DataFrame:
    """Read bulk file with optimizations"""
    
    # Determine file type
    if uploaded_file.name.endswith('.xlsx'):
        # Read only necessary sheet
        df = pd.read_excel(
            uploaded_file,
            sheet_name='Sponsored Products Campaigns',
            dtype=str,  # Read all as string initially
            engine='openpyxl'
        )
    else:  # CSV
        df = pd.read_csv(
            uploaded_file,
            dtype=str,
            low_memory=False
        )
    
    # Convert numeric columns
    numeric_cols = ['Impressions', 'Clicks', 'Spend', 'Sales', 'Orders', 'Units']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df
```

## 11. Statistics Display

### הצגת סטטיסטיקות
```python
def display_bulk_stats(stats: dict):
    """Display bulk file statistics"""
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Rows", f"{stats.get('total_rows', 0):,}")
    
    with col2:
        st.metric("Campaigns", stats.get('unique_campaigns', 0))
    
    with col3:
        st.metric("Portfolios", stats.get('unique_portfolios', 0))
    
    with col4:
        st.metric("Enabled Rows", f"{stats.get('enabled_rows', 0):,}")
```

## 12. Data Rova Integration

### Placeholder
```python
def handle_data_rova_upload():
    """Handle Data Rova file upload - TBD"""
    
    st.info("Data Rova integration will be available in future updates")
    
    # Placeholder for future implementation
    # Will handle benchmarking data
    pass
```