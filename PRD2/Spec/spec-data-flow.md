# איפיון זרימת נתונים - Bid Optimizer

## 1. סקירה כללית

### זרימה ראשית
```
User Input → File Upload → Optimization Processing → Output Generation → File Download
```

### עקרונות
- זרימה חד-כיוונית (Unidirectional)
- ללא State גלובלי בין אופטימיזציות
- כל אופטימיזציה עצמאית
- עיבוד בזיכרון בלבד

## 2. זרימת Upload

### תהליך העלאת קבצים
```
User Action: Click Upload Button
    ↓
File Selection (Template / Bulk 7 / Bulk 30 / Bulk 60 / Data Rova)
    ↓
File Validation (Size, Format)
    ↓
Read to DataFrame
    ↓
Store in Session State
    ↓
Update UI Status
```

### קוד דוגמה
```python
def handle_file_upload(file_type: str, uploaded_file):
    # 1. Validate file
    if uploaded_file.size > 40 * 1024 * 1024:
        raise FileError("File exceeds 40MB limit")
    
    # 2. Read file
    if file_type == 'template':
        df = pd.read_excel(uploaded_file, sheet_name=None)
        # Returns dict with 'Port Values' and 'Top ASINs'
    else:
        df = pd.read_excel(uploaded_file, sheet_name='Sponsored Products Campaigns')
    
    # 3. Store in session
    st.session_state[f'{file_type}_df'] = df
    
    # 4. Update UI
    st.success(f"{file_type} uploaded successfully")
```

## 3. זרימת Optimization Selection

### בחירת אופטימיזציות
```
User Selection (Checkboxes)
    ↓
Store Selected Optimizations List
    ↓
Enable/Disable Process Button
    ↓
Display Required Files for Selected Optimizations
```

### מיפוי דרישות קבצים
```python
OPTIMIZATION_REQUIREMENTS = {
    'Zero Sales': {
        'template': True,
        'bulk_30': True,
        'bulk_7': False,
        'bulk_60': False,
        'data_rova': False
    },
    # TBD - אופטימיזציות עתידיות
}
```

## 4. זרימת Processing

### תהליך עיבוד ראשי
```
User Click: Process Files
    ↓
For Each Selected Optimization:
    ↓
    Load Optimization Module
    ↓
    Internal Validation
    ↓
    Internal Cleaning
    ↓
    Process Data
    ↓
    Generate Output Sheets
    ↓
Combine All Sheets
    ↓
Create Working & Clean Files
```

### קוד דוגמה
```python
def process_optimizations(selected_optimizations: List[str]):
    all_results = {}
    
    for opt_name in selected_optimizations:
        # 1. Load module
        optimization = load_optimization(opt_name)
        
        # 2. Get required data
        bulk_df = get_required_bulk(optimization)
        template_df = st.session_state['template_df']['Port Values']
        
        # 3. Process (includes validation & cleaning)
        try:
            result = optimization.process(bulk_df, template_df)
            all_results[opt_name] = result
        except ValidationError as e:
            st.error(f"{opt_name}: {e}")
            continue
    
    return all_results
```

## 5. זרימת Data בתוך אופטימיזציה

### Zero Sales Data Flow
```
Input: Bulk DataFrame + Template DataFrame
    ↓
Validate Required Columns
    ↓
Filter Rows (Units = 0, Not Flat Portfolios)
    ↓
Split by Entity Type
    ├── Keywords & Product Targeting
    │       ↓
    │   Add Helper Columns
    │       ↓
    │   Calculate New Bids
    │       ↓
    │   Mark Errors
    │
    ├── Bidding Adjustment (No changes)
    │
    └── Product Ad (No changes)
        ↓
    Combine Results
        ↓
    Return Dict of DataFrames
```

## 6. זרימת Output Generation

### יצירת קבצי פלט
```
All Optimization Results
    ↓
Create Excel Writer Objects
    ↓
For Each Optimization Result:
    ↓
    Write Sheets to Working File
    ↓
    Write Sheets to Clean File
    ↓
Generate Filenames with Timestamp
    ↓
Store in Session State
    ↓
Enable Download Buttons
```

### מבנה Output
```python
output_structure = {
    'working_file': {
        'Clean Zero Sales': df_with_helpers,
        'Bidding Adjustment Zero Sales': df_bidding,
        'Product Ad Zero Sales': df_product_ad,
        # TBD - sheets מאופטימיזציות נוספות
    },
    'clean_file': {
        # כרגע זהה ל-working
        # בעתיד ללא עמודות עזר
    }
}
```

## 7. זרימת Error Handling

### טיפול בשגיאות
```
Error Occurs
    ↓
Catch Exception
    ↓
Determine Error Type:
    ├── File Error → Show upload error message
    ├── Validation Error → Show validation message
    ├── Processing Error → Show processing error
    └── System Error → Show generic error
        ↓
    Log Error Details
        ↓
    Allow User Recovery
```

### סוגי שגיאות
```python
class ErrorFlow:
    FILE_ERRORS = [
        "File exceeds 40MB",
        "Invalid file format",
        "Corrupted file"
    ]
    
    VALIDATION_ERRORS = [
        "Missing portfolios",
        "Invalid column structure",
        "No data after filtering"
    ]
    
    PROCESSING_ERRORS = [
        "Calculation failed",
        "Memory exceeded",
        "Timeout"
    ]
```

## 8. זרימת State Management

### Session State Updates
```
User Action
    ↓
Update Session State
    ↓
Trigger UI Re-render
    ↓
Check State Dependencies
    ↓
Enable/Disable UI Elements
```

### State Dependencies
```python
STATE_DEPENDENCIES = {
    'show_validation': ['template_file', 'bulk_file'],
    'enable_process': ['validation_passed', 'optimizations_selected'],
    'show_output': ['processing_complete'],
    'enable_download': ['output_files_ready']
}
```

## 9. זרימת Navigation

### מעבר בין עמודים
```
Sidebar Click
    ↓
Check Current State
    ↓
Save Current Page State
    ↓
Load New Page
    ↓
Restore Page State
    ↓
Render Page Content
```

## 10. זרימת Performance

### אופטימיזציה לקבצים גדולים
```
Large File Detected (>20MB)
    ↓
Show Warning Message
    ↓
Process in Chunks:
    ├── Read chunk (10,000 rows)
    ├── Process chunk
    ├── Update progress bar
    └── Combine results
        ↓
    Generate output
```

### Chunking Strategy
```python
def process_large_file(df, chunk_size=10000):
    total_rows = len(df)
    results = []
    
    for i in range(0, total_rows, chunk_size):
        chunk = df.iloc[i:i+chunk_size]
        result = process_chunk(chunk)
        results.append(result)
        
        # Update progress
        progress = (i + chunk_size) / total_rows
        st.progress(progress)
    
    return pd.concat(results)
```

## 11. Data Formats בזרימה

### Input Formats
```yaml
Template:
  format: Excel
  sheets:
    - Port Values: [Portfolio Name, Base Bid, Target CPA]
    - Top ASINs: [ASIN]

Bulk:
  format: Excel
  sheet: Sponsored Products Campaigns
  columns: 48
  rows: max 500,000
```

### Processing Formats
```yaml
DataFrame:
  index: RangeIndex
  columns: Original + Helper columns
  dtypes: Mixed (numeric, string)
```

### Output Formats
```yaml
Working File:
  format: Excel
  sheets: Multiple (per optimization)
  includes: Helper columns

Clean File:
  format: Excel
  sheets: Multiple (per optimization)
  includes: No helper columns (future)
```

## 12. זרימת Data Rova (TBD)

```python
# TBD - יתווסף בעתיד
def data_rova_flow():
    """
    אינטגרציה עם Data Rova לנתוני benchmarking
    """
    pass
```

## 13. זרימת Campaigns Optimizer (TBD)

```python
# TBD - יתווסף בשלב 5-6
def campaigns_optimizer_flow():
    """
    זרימה ל-Negation ו-Harvesting
    """
    pass
```