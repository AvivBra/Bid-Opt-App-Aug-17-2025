# זרימת נתונים - Bid Optimizer

## 1. תרשים זרימה ראשי

```
┌────────────────────────────────────────┐
│            USER INTERFACE              │
│  [Template] [Bulk30] [Bulk60] [Bulk7]  │
│           [Data Rova]                  │
└────────────┬───────────────────────────┘
             │ Upload Files
             ▼
┌────────────────────────────────────────┐
│           SESSION STATE                │
│    Store: Files + DataFrames           │
└────────────┬───────────────────────────┘
             │ Select Optimizations
             ▼
┌────────────────────────────────────────┐
│          ORCHESTRATOR                  │
│   Coordinate validation & processing   │
└────────────┬───────────────────────────┘
             │ For each optimization
             ▼
┌────────────────────────────────────────┐
│      OPTIMIZATION MODULE               │
│  ┌──────────┐                         │
│  │ Validate │ Check required files    │
│  └────┬─────┘                         │
│       ▼                               │
│  ┌──────────┐                         │
│  │  Clean   │ Filter & prepare data   │
│  └────┬─────┘                         │
│       ▼                               │
│  ┌──────────┐                         │
│  │ Process  │ Apply optimization      │
│  └────┬─────┘                         │
└────────────┬───────────────────────────┘
             │ Return results
             ▼
┌────────────────────────────────────────┐
│         FILE GENERATOR                 │
│   Create Working & Clean files         │
└────────────┬───────────────────────────┘
             │ Download
             ▼
         [Output Files]
```

## 2. שלב העלאת קבצים

### זרימה
```
User clicks upload → File selected → FileReader.read() 
→ DataFrame created → Stored in Session State
```

### נתונים נשמרים
```python
session_state = {
    'template_file': BytesIO,      # קובץ גולמי
    'template_df': DataFrame,      # נתונים מעובדים
    'bulk_30_file': BytesIO,
    'bulk_30_df': DataFrame,
    'bulk_60_file': BytesIO,
    'bulk_60_df': DataFrame,
    'bulk_7_file': BytesIO,
    'bulk_7_df': DataFrame,
    'data_rova_file': BytesIO,
    'data_rova_df': DataFrame
}
```

## 3. שלב בחירת אופטימיזציות

### זרימה
```
User selects checkboxes → List of selected optimizations 
→ Stored in Session State
```

### נתונים
```python
session_state['selected_optimizations'] = [
    'zero_sales',
    'portfolio_bid',
    # ...
]
```

## 4. שלב הולידציה

### זרימה לכל אופטימיזציה
```
Orchestrator.validate_all()
    ↓
For each selected optimization:
    1. Get required_files from optimization
    2. Check files exist in session_state
    3. Call optimization.validate(files)
    4. Store validation result
    ↓
Return all validation results
```

### נתונים
```python
session_state['validation_results'] = {
    'zero_sales': {
        'is_valid': True,
        'errors': [],
        'warnings': ['5 rows with high bids']
    },
    'portfolio_bid': {
        'is_valid': False,
        'errors': ['Missing Bulk 30 file'],
        'warnings': []
    }
}
```

## 5. שלב העיבוד

### זרימה לכל אופטימיזציה תקינה
```
Orchestrator.process_all()
    ↓
For each valid optimization:
    1. Get required files from session_state
    2. Call optimization.process(files)
        a. Clean data internally
        b. Apply optimization logic
        c. Return processed DataFrames
    3. Store results
    ↓
FileGenerator.create_output_files(all_results)
```

### נתונים מעובדים
```python
processing_results = {
    'zero_sales': {
        'working': DataFrame,  # עם עמודות עזר
        'clean': DataFrame     # רק 48 עמודות
    },
    'portfolio_bid': {
        'working': DataFrame,
        'clean': DataFrame
    }
}
```

## 6. שלב יצירת קבצי פלט

### זרימה
```
FileGenerator receives all results
    ↓
Create Working File:
    - Add sheet for each optimization
    - Include helper columns
    ↓
Create Clean File:
    - Add sheet for each optimization
    - Only original columns
    ↓
Generate filenames with timestamp
    ↓
Return BytesIO objects
```

### פורמט שמות
```
Auto Optimized Bulk | Working | 2024-01-15 | 14-30.xlsx
Auto Optimized Bulk | Clean | 2024-01-15 | 14-30.xlsx
```

## 7. זרימת שגיאות

### טיפול בשגיאות
```
Error occurs → Exception raised → Caught by Orchestrator
→ User-friendly message → Display in UI
```

### סוגי שגיאות
- קובץ חסר
- מבנה לא תקין
- נתונים חסרים
- כשל בעיבוד

## 8. ניקוי נתונים (בתוך כל אופטימיזציה)

### זרימה
```
Raw DataFrame from session_state
    ↓
Optimization.clean():
    - Filter by Entity
    - Filter by State
    - Remove invalid rows
    - Handle missing values
    ↓
Cleaned DataFrame for processing
```

### כל אופטימיזציה מנקה אחרת
- **Zero Sales**: Entity in [Keyword, Product Targeting], Units=0
- **Portfolio Bid**: [יוגדר בהמשך]
- **אחרות**: לפי הצורך

## 9. State Management

### מחזור חיים
```
1. INITIAL: No files uploaded
2. UPLOADING: Files being uploaded
3. UPLOADED: Files ready
4. VALIDATING: Checking files
5. READY: Can process
6. PROCESSING: Running optimizations
7. COMPLETE: Results ready
8. RESET: Clear everything
```

### Reset Flow
```
User clicks "New Processing" → Clear session_state 
→ Return to INITIAL state → Ready for new files
```

## 10. ביצועים וזיכרון

### עקרונות
- DataFrames נשמרים בזיכרון
- עיבוד סדרתי (לא מקבילי)
- ניקוי זיכרון אחרי כל אופטימיזציה
- מקסימום 2GB RAM

### אופטימיזציה
```python
# עיבוד יעיל
for optimization in selected:
    result = optimization.process(files)
    save_result(result)
    del result  # Free memory
    gc.collect()
```