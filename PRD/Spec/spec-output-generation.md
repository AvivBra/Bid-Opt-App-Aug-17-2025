# איפיון יצירת קבצי פלט - Bid Optimizer

## 1. סקירה כללית

### מטרה
יצירת קבצי Excel עם תוצאות האופטימיזציות.

### סוגי קבצים
- **Working File** - כולל עמודות עזר לניתוח
- **Clean File** - ללא עמודות עזר (כרגע זהה ל-Working)

### מבנה
- Sheet נפרד לכל חלק של כל אופטימיזציה
- שמות קבצים עם timestamp

## 2. File Generation Flow

```python
def generate_output_files(optimization_results: dict) -> dict:
    """Generate working and clean output files"""
    
    output = {
        'working': None,
        'clean': None,
        'stats': {}
    }
    
    try:
        # 1. Create Working File
        working_file = create_working_file(optimization_results)
        output['working'] = working_file
        
        # 2. Create Clean File (currently same as working)
        clean_file = create_clean_file(optimization_results)
        output['clean'] = clean_file
        
        # 3. Calculate statistics
        output['stats'] = calculate_output_stats(optimization_results)
        
        # 4. Store in session
        st.session_state.output_files = output
        
    except Exception as e:
        handle_output_generation_error(e)
    
    return output
```

## 3. Working File Structure

### Zero Sales Sheets
```python
def create_zero_sales_sheets(result_data: dict) -> dict:
    """Create sheets for Zero Sales optimization"""
    
    sheets = {}
    
    # 1. Main sheet - Keywords and Product Targeting with helper columns
    main_df = result_data.get('keywords_pt', pd.DataFrame())
    if not main_df.empty:
        # Ensure Operation = Update
        main_df['Operation'] = 'Update'
        sheets['Clean Zero Sales'] = main_df
    
    # 2. Bidding Adjustment sheet - without helper columns
    bidding_df = result_data.get('bidding_adjustment', pd.DataFrame())
    if not bidding_df.empty:
        bidding_df['Operation'] = 'Update'
        sheets['Bidding Adjustment Zero Sales'] = bidding_df
    
    # 3. Product Ad sheet - without helper columns
    product_ad_df = result_data.get('product_ad', pd.DataFrame())
    if not product_ad_df.empty:
        product_ad_df['Operation'] = 'Update'
        sheets['Product Ad Zero Sales'] = product_ad_df
    
    return sheets
```

### Helper Columns Order
```python
def arrange_columns_with_helpers(df: pd.DataFrame) -> pd.DataFrame:
    """Arrange columns with helper columns in correct position"""
    
    # Original 48 columns
    original_cols = BULK_FILE_REQUIREMENTS['required_columns']
    
    # Helper columns to insert before 'Bid' (column 28)
    helper_cols = [
        'Old Bid',
        'calc1', 
        'calc2',
        'Target CPA',
        'Base Bid',
        'Adj. CPA',
        'Max BA'
    ]
    
    # Find position of 'Bid' column
    bid_index = original_cols.index('Bid')
    
    # Arrange columns
    final_cols = (
        original_cols[:bid_index] +  # Columns before Bid
        helper_cols +                 # Helper columns
        original_cols[bid_index:]     # Bid and columns after
    )
    
    # Reorder dataframe
    return df[final_cols]
```

## 4. Excel Writer

### Create Excel File
```python
def create_excel_file(sheets_dict: dict, file_type: str) -> BytesIO:
    """Create Excel file with multiple sheets"""
    
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for sheet_name, df in sheets_dict.items():
            # Write dataframe
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # Apply formatting
            format_sheet(writer, sheet_name, df, file_type)
    
    output.seek(0)
    return output
```

### Formatting
```python
def format_sheet(writer, sheet_name: str, df: pd.DataFrame, file_type: str):
    """Apply formatting to Excel sheet"""
    
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]
    
    # 1. Header formatting
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#2D2D2D',
        'font_color': 'white',
        'border': 1
    })
    
    # 2. Error row formatting (pink)
    error_format = workbook.add_format({
        'bg_color': '#FFE4E1',
        'font_color': '#8B0000'
    })
    
    # 3. Apply conditional formatting for errors
    if 'has_error' in df.columns:
        error_rows = df[df['has_error'] == True].index
        for row in error_rows:
            worksheet.set_row(row + 1, None, error_format)
    
    # 4. Column widths
    set_column_widths(worksheet, df)
    
    # 5. Number formatting
    apply_number_formatting(worksheet, df)
```

## 5. File Naming

### Generate Filename
```python
def generate_output_filename(file_type: str) -> str:
    """Generate filename with timestamp"""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    
    if file_type == 'working':
        return f"Working_File_{timestamp}.xlsx"
    elif file_type == 'clean':
        return f"Clean_File_{timestamp}.xlsx"
    else:
        return f"Output_{timestamp}.xlsx"
```

## 6. Statistics Calculation

### Output Statistics
```python
def calculate_output_stats(optimization_results: dict) -> dict:
    """Calculate statistics for output files"""
    
    stats = {
        'total_rows': 0,
        'rows_modified': 0,
        'rows_with_errors': 0,
        'calculation_errors': 0,
        'low_bids': 0,
        'high_bids': 0,
        'sheets_created': 0,
        'optimizations_applied': []
    }
    
    for opt_name, result in optimization_results.items():
        if opt_name == 'zero_sales':
            # Count rows
            for df_name, df in result.items():
                stats['total_rows'] += len(df)
                
                # Count modified rows
                if 'Old Bid' in df.columns:
                    modified = df[df['Bid'] != df['Old Bid']]
                    stats['rows_modified'] += len(modified)
                
                # Count errors
                if 'Bid' in df.columns:
                    stats['low_bids'] += len(df[df['Bid'] < 0.02])
                    stats['high_bids'] += len(df[df['Bid'] > 1.25])
                    stats['calculation_errors'] += df['Bid'].isna().sum()
            
            stats['sheets_created'] += len(result)
            stats['optimizations_applied'].append('Zero Sales')
    
    return stats
```

## 7. Clean File Generation

### Current Implementation
```python
def create_clean_file(optimization_results: dict) -> BytesIO:
    """Create clean file (currently same as working)"""
    
    # Currently identical to working file
    # In future, will remove helper columns
    
    return create_working_file(optimization_results)
```

### Future Implementation
```python
def create_clean_file_future(optimization_results: dict) -> BytesIO:
    """Future: Create clean file without helper columns"""
    
    sheets = {}
    
    for opt_name, result in optimization_results.items():
        for sheet_name, df in result.items():
            # Remove helper columns
            clean_df = remove_helper_columns(df)
            sheets[sheet_name] = clean_df
    
    return create_excel_file(sheets, 'clean')

def remove_helper_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Remove helper columns from dataframe"""
    
    helper_cols = ['Old Bid', 'calc1', 'calc2', 'Target CPA', 
                   'Base Bid', 'Adj. CPA', 'Max BA', 'has_error']
    
    # Keep only original columns
    cols_to_keep = [col for col in df.columns if col not in helper_cols]
    
    return df[cols_to_keep]
```

## 8. Error Highlighting

### Mark Error Rows
```python
def highlight_error_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Mark rows with errors for highlighting"""
    
    df['has_error'] = False
    
    # Check bid range
    if 'Bid' in df.columns:
        df.loc[df['Bid'] < 0.02, 'has_error'] = True
        df.loc[df['Bid'] > 1.25, 'has_error'] = True
        df.loc[df['Bid'].isna(), 'has_error'] = True
    
    return df
```

## 9. Download Handlers

### Download Buttons
```python
def render_download_buttons():
    """Render download buttons for output files"""
    
    output_files = st.session_state.get('output_files', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        working_file = output_files.get('working')
        if working_file:
            st.download_button(
                label="DOWNLOAD WORKING",
                data=working_file,
                file_name=generate_output_filename('working'),
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_working_btn"
            )
    
    with col2:
        clean_file = output_files.get('clean')
        if clean_file:
            st.download_button(
                label="DOWNLOAD CLEAN",
                data=clean_file,
                file_name=generate_output_filename('clean'),
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_clean_btn"
            )
```

## 10. Memory Management

### Large File Handling
```python
def create_large_excel_file(sheets_dict: dict) -> BytesIO:
    """Handle large Excel file creation"""
    
    output = BytesIO()
    
    # Use constant_memory mode for large files
    with pd.ExcelWriter(
        output, 
        engine='openpyxl',
        options={'constant_memory': True}
    ) as writer:
        
        for sheet_name, df in sheets_dict.items():
            # Write in chunks if needed
            if len(df) > 100000:
                write_dataframe_in_chunks(writer, sheet_name, df)
            else:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    output.seek(0)
    return output
```

## 11. Progress Tracking

### Show Progress
```python
def generate_output_with_progress(optimization_results: dict):
    """Generate output files with progress tracking"""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_steps = len(optimization_results) * 2  # Working + Clean
    current_step = 0
    
    # Create Working File
    status_text.text("Creating Working File...")
    working_file = create_working_file(optimization_results)
    current_step += len(optimization_results)
    progress_bar.progress(current_step / total_steps)
    
    # Create Clean File
    status_text.text("Creating Clean File...")
    clean_file = create_clean_file(optimization_results)
    current_step += len(optimization_results)
    progress_bar.progress(current_step / total_steps)
    
    status_text.text("Files ready for download!")
```

## 12. Validation of Output

### Verify Output Files
```python
def validate_output_files(output_files: dict) -> bool:
    """Validate generated output files"""
    
    try:
        for file_type, file_data in output_files.items():
            if file_data:
                # Try to read the file
                test_df = pd.read_excel(file_data, sheet_name=None)
                
                # Check has sheets
                if len(test_df) == 0:
                    raise ValueError(f"{file_type} file has no sheets")
                
                # Check has data
                for sheet_name, df in test_df.items():
                    if len(df) == 0:
                        raise ValueError(f"Sheet {sheet_name} is empty")
        
        return True
        
    except Exception as e:
        st.error(f"Output validation failed: {str(e)}")
        return False
```