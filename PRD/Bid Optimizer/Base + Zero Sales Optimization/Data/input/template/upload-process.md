# איפיון העלאת Template

## 1. סקירה כללית

### מטרה
אפשר למשתמש להוריד template ריק או להעלות template ממולא עם הגדרות portfolios.

### מבנה Template
- 2 לשוניות: Port Values ו-Top ASINs
- קובץ Excel בלבד (.xlsx)
- גודל מקסימלי: 1MB

## 2. Download Template

### יצירת Template ריק
```python
def generate_empty_template() -> BytesIO:
    """Generate empty template with both sheets"""
    
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Port Values sheet
        port_values_df = pd.DataFrame({
            'Portfolio Name': [],
            'Base Bid': [],
            'Target CPA': []
        })
        port_values_df.to_excel(writer, sheet_name='Port Values', index=False)
        
        # Top ASINs sheet
        top_asins_df = pd.DataFrame({
            'ASIN': []
        })
        top_asins_df.to_excel(writer, sheet_name='Top ASINs', index=False)
        
        # Add formatting
        format_template_sheets(writer)
    
    output.seek(0)
    return output
```

### Formatting
```python
def format_template_sheets(writer):
    """Add formatting to template sheets"""
    
    workbook = writer.book
    
    # Header format
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#8B5CF6',
        'font_color': 'white',
        'border': 1
    })
    
    # Format Port Values sheet
    worksheet = writer.sheets['Port Values']
    worksheet.set_column('A:A', 30)  # Portfolio Name
    worksheet.set_column('B:B', 15)  # Base Bid
    worksheet.set_column('C:C', 15)  # Target CPA
    
    # Format Top ASINs sheet
    worksheet = writer.sheets['Top ASINs']
    worksheet.set_column('A:A', 20)  # ASIN
```

## 3. Upload Template

### File Upload Handler
```python
def handle_template_upload(uploaded_file) -> dict:
    """Handle template file upload"""
    
    result = {
        'success': False,
        'data': None,
        'errors': []
    }
    
    try:
        # 1. Validate file size
        if uploaded_file.size > 1024 * 1024:  # 1MB
            result['errors'].append("Template file exceeds 1MB limit")
            return result
        
        # 2. Read Excel file
        sheets = pd.read_excel(uploaded_file, sheet_name=None)
        
        # 3. Validate structure
        validation = validate_template_structure(sheets)
        if validation['errors']:
            result['errors'] = validation['errors']
            return result
        
        # 4. Store in session
        st.session_state.template_df = sheets
        st.session_state.template_file = uploaded_file
        
        result['success'] = True
        result['data'] = sheets
        
    except Exception as e:
        result['errors'].append(f"Failed to read template: {str(e)}")
    
    return result
```

## 4. Template Validation

### Structure Validation
```python
def validate_template_structure(sheets: dict) -> dict:
    """Validate template structure"""
    
    validation = {
        'is_valid': True,
        'errors': [],
        'warnings': []
    }
    
    # 1. Check required sheets
    if 'Port Values' not in sheets:
        validation['errors'].append("Missing 'Port Values' sheet")
        validation['is_valid'] = False
    
    if 'Top ASINs' not in sheets:
        validation['warnings'].append("Missing 'Top ASINs' sheet (optional)")
    
    # 2. Validate Port Values columns
    if 'Port Values' in sheets:
        port_df = sheets['Port Values']
        required_cols = ['Portfolio Name', 'Base Bid', 'Target CPA']
        
        if list(port_df.columns) != required_cols:
            validation['errors'].append(f"Port Values must have columns: {required_cols}")
            validation['is_valid'] = False
    
    # 3. Validate Top ASINs columns
    if 'Top ASINs' in sheets:
        asin_df = sheets['Top ASINs']
        if list(asin_df.columns) != ['ASIN']:
            validation['warnings'].append("Top ASINs should have only 'ASIN' column")
    
    return validation
```

### Data Validation
```python
def validate_template_data(sheets: dict) -> dict:
    """Validate template data"""
    
    validation = {
        'is_valid': True,
        'errors': [],
        'warnings': [],
        'stats': {}
    }
    
    port_df = sheets.get('Port Values', pd.DataFrame())
    
    # 1. Check for empty template
    if len(port_df) == 0:
        validation['warnings'].append("Template is empty")
        return validation
    
    # 2. Check for duplicate portfolios
    duplicates = port_df['Portfolio Name'].duplicated()
    if duplicates.any():
        dup_names = port_df[duplicates]['Portfolio Name'].unique()
        validation['errors'].append(f"Duplicate portfolios: {', '.join(dup_names)}")
        validation['is_valid'] = False
    
    # 3. Validate Base Bid values
    for idx, row in port_df.iterrows():
        base_bid = row['Base Bid']
        
        if pd.isna(base_bid):
            validation['errors'].append(f"Row {idx+2}: Base Bid is required")
            validation['is_valid'] = False
        elif base_bid != 'Ignore':
            try:
                bid_value = float(base_bid)
                if bid_value < 0 or bid_value > 4:
                    validation['errors'].append(f"Row {idx+2}: Base Bid must be 0-4")
                    validation['is_valid'] = False
            except:
                validation['errors'].append(f"Row {idx+2}: Invalid Base Bid value")
                validation['is_valid'] = False
    
    # 4. Check Target CPA (optional)
    invalid_cpa = port_df[
        ~port_df['Target CPA'].isna() & 
        ((port_df['Target CPA'] < 0) | (port_df['Target CPA'] > 4))
    ]
    if len(invalid_cpa) > 0:
        validation['warnings'].append(f"{len(invalid_cpa)} rows have invalid Target CPA")
    
    # 5. Statistics
    validation['stats'] = {
        'total_portfolios': len(port_df),
        'ignored_portfolios': len(port_df[port_df['Base Bid'] == 'Ignore']),
        'active_portfolios': len(port_df[port_df['Base Bid'] != 'Ignore']),
        'portfolios_with_cpa': len(port_df[~port_df['Target CPA'].isna()])
    }
    
    return validation
```

## 5. UI Components

### Download Button
```python
def render_template_download():
    """Render template download button"""
    
    template_data = generate_empty_template()
    
    st.download_button(
        label="DOWNLOAD TEMPLATE",
        data=template_data,
        file_name=f"template_{datetime.now():%Y%m%d}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="download_template",
        use_container_width=False
    )
```

### Upload Area
```python
def render_template_upload():
    """Render template upload area"""
    
    uploaded = st.file_uploader(
        "Upload Template File",
        type=['xlsx'],
        key="template_uploader",
        help="Upload Excel file with Port Values and Top ASINs sheets"
    )
    
    if uploaded:
        result = handle_template_upload(uploaded)
        
        if result['success']:
            st.success("Template uploaded successfully")
            
            # Show statistics
            if 'Port Values' in result['data']:
                stats = validate_template_data(result['data'])['stats']
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Portfolios", stats['total_portfolios'])
                with col2:
                    st.metric("Active", stats['active_portfolios'])
                with col3:
                    st.metric("Ignored", stats['ignored_portfolios'])
        else:
            for error in result['errors']:
                st.error(error)
```

## 6. Template Examples

### Sample Port Values Data
```python
SAMPLE_PORT_VALUES = pd.DataFrame({
    'Portfolio Name': [
        'Kids-Brand-US',
        'Kids-Brand-EU',
        'Supplements-US',
        'Supplements-EU',
        'Electronics-US'
    ],
    'Base Bid': [1.25, 0.95, 2.10, 'Ignore', 1.85],
    'Target CPA': [5.00, 4.50, 8.00, None, 7.50]
})
```

### Sample Top ASINs Data
```python
SAMPLE_TOP_ASINS = pd.DataFrame({
    'ASIN': [
        'B001234567',
        'B002345678',
        'B003456789',
        'B004567890',
        'B005678901'
    ]
})
```

## 7. Error Messages

### Common Errors
```python
TEMPLATE_ERROR_MESSAGES = {
    'file_too_large': "Template file exceeds 1MB limit",
    'wrong_format': "Template must be Excel (.xlsx) format",
    'missing_sheet': "Missing required 'Port Values' sheet",
    'wrong_columns': "Port Values sheet has incorrect columns",
    'duplicate_portfolios': "Duplicate portfolio names found",
    'invalid_base_bid': "Base Bid must be a number (0-4) or 'Ignore'",
    'all_ignored': "All portfolios are marked as 'Ignore'",
    'empty_template': "Template has no data"
}
```

## 8. Integration with Optimizations

### Zero Sales Integration
```python
def get_portfolio_settings(portfolio_name: str) -> dict:
    """Get settings for a specific portfolio"""
    
    template_df = st.session_state.get('template_df', {})
    port_values = template_df.get('Port Values', pd.DataFrame())
    
    portfolio_row = port_values[
        port_values['Portfolio Name'] == portfolio_name
    ]
    
    if portfolio_row.empty:
        return None
    
    return {
        'base_bid': portfolio_row.iloc[0]['Base Bid'],
        'target_cpa': portfolio_row.iloc[0]['Target CPA']
    }
```

## 9. Top ASINs Usage (Future)

### Placeholder for Future Use
```python
def get_top_asins() -> list:
    """Get list of top ASINs - TBD usage in future optimizations"""
    
    template_df = st.session_state.get('template_df', {})
    top_asins = template_df.get('Top ASINs', pd.DataFrame())
    
    if top_asins.empty:
        return []
    
    return top_asins['ASIN'].tolist()
```

## 10. Performance Considerations

### Caching Template
```python
@st.cache_data
def cache_template_data(file_hash):
    """Cache template data for performance"""
    
    return st.session_state.template_df
```

### Large Portfolio Lists
```python
def handle_large_portfolio_list(port_df):
    """Handle templates with many portfolios"""
    
    if len(port_df) > 1000:
        st.warning(f"Template has {len(port_df)} portfolios. Processing may be slower.")
        
        # Process in chunks if needed
        return process_in_chunks(port_df)
```