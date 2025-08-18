# איפיון העלאת Bulk Files

## 1. סקירה כללית

### מטרה
אפשר למשתמש להעלות קבצי Bulk שונים (7/30/60 ימים) עם נתוני קמפיינים.

### סוגי קבצים
- Bulk 7 Days - נתוני 7 ימים אחרונים
- Bulk 30 Days - נתוני 30 ימים אחרונים  
- Bulk 60 Days - נתוני 60 ימים אחרונים

### מגבלות
- גודל מקסימלי: 40MB לקובץ
- מספר שורות מקסימלי: 500,000
- פורמט: Excel (.xlsx) או CSV

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
        # ... all 48 columns
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
            result['errors'].append(f"File exceeds 40MB limit ({uploaded_file.size / 1024 / 1024:.1f}MB)")
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

### קריאת קובץ
```python
def read_bulk_file(uploaded_file) -> pd.DataFrame:
    """Read bulk file (Excel or CSV)"""
    
    file_name = uploaded_file.name.lower()
    
    if file_name.endswith('.xlsx'):
        # Read Excel with specific sheet
        df = pd.read_excel(
            uploaded_file,
            sheet_name='Sponsored Products Campaigns',
            dtype=str  # Read all as string initially
        )
    elif file_name.endswith('.csv'):
        # Read CSV
        df = pd.read_csv(uploaded_file, dtype=str)
    else:
        raise ValueError("File must be .xlsx or .csv")
    
    return df
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

### בדיקת נתונים
```python
def validate_bulk_data(df: pd.DataFrame) -> dict:
    """Validate bulk file data quality"""
    
    validation = {
        'warnings': [],
        'info': [],
        'stats': {}
    }
    
    # 1. Check Entity distribution
    entity_counts = df['Entity'].value_counts()
    validation['stats']['entity_distribution'] = entity_counts.to_dict()
    
    # 2. Check State distribution
    state_counts = df['State'].value_counts()
    if 'enabled' not in state_counts:
        validation['warnings'].append("No enabled rows found")
    
    # 3. Check for required Entity types for Zero Sales
    required_entities = ['Keyword', 'Product Targeting']
    has_required = df['Entity'].isin(required_entities).any()
    if not has_required:
        validation['warnings'].append("No Keyword or Product Targeting rows for optimization")
    
    # 4. Check Portfolio Name column
    missing_portfolios = df['Portfolio Name (Informational only)'].isna().sum()
    if missing_portfolios > 0:
        validation['warnings'].append(f"{missing_portfolios} rows have missing portfolio names")
    
    # 5. Performance metrics
    validation['stats']['total_rows'] = len(df)
    validation['stats']['enabled_rows'] = len(df[df['State'] == 'enabled'])
    validation['stats']['unique_campaigns'] = df['Campaign ID'].nunique()
    validation['stats']['unique_portfolios'] = df['Portfolio Name (Informational only)'].nunique()
    
    return validation
```

## 5. UI Components

### כפתורי העלאה
```python
def render_bulk_upload_buttons():
    """Render all bulk upload buttons"""
    
    # First row
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("BULK 7 DAYS", key="bulk_7_btn", use_container_width=False):
            st.session_state.show_bulk_7_uploader = True
    
    with col2:
        if st.button("BULK 30 DAYS", key="bulk_30_btn", use_container_width=False):
            st.session_state.show_bulk_30_uploader = True
    
    # Second row
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("BULK 60 DAYS", key="bulk_60_btn", use_container_width=False):
            st.session_state.show_bulk_60_uploader = True
    
    with col2:
        # Empty for alignment
        pass
    
    # Show uploaders if buttons clicked
    render_bulk_uploaders()
```

### אזורי העלאה
```python
def render_bulk_uploaders():
    """Render file uploaders for each bulk type"""
    
    # Bulk 7
    if st.session_state.get('show_bulk_7_uploader'):
        with st.container():
            uploaded = st.file_uploader(
                "Upload Bulk 7 Days",
                type=['xlsx', 'csv'],
                key="bulk_7_uploader"
            )
            
            if uploaded:
                handle_bulk_upload_ui('7', uploaded)
    
    # Bulk 30
    if st.session_state.get('show_bulk_30_uploader'):
        with st.container():
            uploaded = st.file_uploader(
                "Upload Bulk 30 Days",
                type=['xlsx', 'csv'],
                key="bulk_30_uploader"
            )
            
            if uploaded:
                handle_bulk_upload_ui('30', uploaded)
    
    # Bulk 60
    if st.session_state.get('show_bulk_60_uploader'):
        with st.container():
            uploaded = st.file_uploader(
                "Upload Bulk 60 Days",
                type=['xlsx', 'csv'],
                key="bulk_60_uploader"
            )
            
            if uploaded:
                handle_bulk_upload_ui('60', uploaded)
```

## 6. מצב הקבצים

### תצוגת סטטוס
```python
def render_bulk_file_status():
    """Display status of all bulk files"""
    
    bulk_types = ['7', '30', '60']
    
    for bulk_type in bulk_types:
        file = st.session_state.get(f'bulk_{bulk_type}_file')
        
        if file:
            df = st.session_state.get(f'bulk_{bulk_type}_df')
            size_mb = file.size / 1024 / 1024
            
            st.success(f"Bulk {bulk_type}: {file.name} ({size_mb:.1f}MB, {len(df):,} rows)")
        else:
            st.info(f"Bulk {bulk_type}: Not uploaded")
```

## 7. איזה Bulk לאיזו אופטימיזציה

### מיפוי דרישות
```python
OPTIMIZATION_BULK_REQUIREMENTS = {
    'zero_sales': {
        'bulk_7': False,
        'bulk_30':