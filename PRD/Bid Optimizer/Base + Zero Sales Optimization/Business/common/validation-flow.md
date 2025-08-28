# איפיון תהליך Validation - Bid Optimizer

## 1. עקרון מרכזי - אין Validation גלובלי

### השינוי המרכזי
- **לפני:** Validation וcleaning גלובליים לכל האופטימיזציות
- **אחרי:** כל אופטימיזציה מבצעת validation וcleaning עצמאיים

### היתרונות
- כל אופטימיזציה יכולה לדרוש נתונים שונים
- אין תלות בין אופטימיזציות
- קל להוסיף אופטימיזציות חדשות
- אין כשל כללי אם אופטימיזציה אחת נכשלת

## 2. תהליך ה-Validation בכל אופטימיזציה

### שלב 1: בדיקת קבצים נדרשים
```python
def check_required_files(self):
    """כל אופטימיזציה מגדירה אילו קבצים היא צריכה"""
    
    # דוגמה ל-Zero Sales
    required_files = {
        'template': True,
        'bulk_30': True,  # או כל bulk אחר
        'data_rova': False  # לא נדרש
    }
    
    for file_type, is_required in required_files.items():
        if is_required and not self.has_file(file_type):
            raise ValidationError(f"Missing required file: {file_type}")
```

### שלב 2: בדיקת מבנה הקבצים
```python
def validate_file_structure(self, df, file_type):
    """בדיקה שהקובץ מכיל את העמודות הנדרשות"""
    
    if file_type == 'template':
        required_columns = ['Portfolio Name (Informational only)', 'Base Bid', 'Target CPA']
        if list(df.columns) != required_columns:
            raise ValidationError("Template structure invalid")
    
    elif file_type == 'bulk':
        if len(df.columns) != 48:
            raise ValidationError("Bulk file must have exactly 48 columns")
```

### שלב 3: בדיקת נתונים ספציפיים לאופטימיזציה
```python
def validate_optimization_specific(self, df):
    """כל אופטימיזציה בודקת את מה שהיא צריכה"""
    
    # Zero Sales בודק:
    if 'Units' not in df.columns:
        raise ValidationError("Units column required for Zero Sales")
    
    if 'Clicks' not in df.columns:
        raise ValidationError("Clicks column required for Zero Sales")
```

## 3. תהליך ה-Cleaning בכל אופטימיזציה

### ניקוי ספציפי לאופטימיזציה
```python
def clean_data(self, df):
    """כל אופטימיזציה מנקה לפי הצרכים שלה"""
    
    # Zero Sales מסנן:
    cleaned = df[
        (df['Units'] == 0) &
        (~df['Portfolio Name (Informational only)'].isin(FLAT_PORTFOLIOS)) &
        (df['Entity'].isin(['Keyword', 'Product Targeting', 'Product Ad', 'Bidding Adjustment']))
    ]
    
    return cleaned
```

## 4. דוגמה מלאה - Zero Sales Validation

### הקוד המלא
```python
class ZeroSalesOptimization(BaseOptimization):
    
    def validate_and_clean(self, bulk_df, template_df):
        """Validation וcleaning משולבים"""
        
        # 1. בדיקת עמודות Template
        self._validate_template(template_df)
        
        # 2. בדיקת עמודות Bulk
        self._validate_bulk(bulk_df)
        
        # 3. בדיקת portfolios
        self._validate_portfolios(bulk_df, template_df)
        
        # 4. ניקוי הנתונים
        cleaned_df = self._clean_data(bulk_df)
        
        # 5. בדיקה שנשארו שורות
        if len(cleaned_df) == 0:
            raise ValidationError("No rows left after filtering")
        
        return cleaned_df
    
    def _validate_portfolios(self, bulk_df, template_df):
        """בדיקת התאמה בין portfolios"""
        
        bulk_portfolios = set(bulk_df['Portfolio Name (Informational only)'].unique())
        template_portfolios = set(template_df['Portfolio Name (Informational only)'].unique())
        
        # Portfolios שמותר שיחסרו
        allowed_missing = {
            'Flat 30', 'Flat 25', 'Flat 40', 
            'Flat 25 | Opt', 'Flat 30 | Opt', 
            'Flat 20', 'Flat 15', 'Flat 40 | Opt',
            'Flat 20 | Opt', 'Flat 15 | Opt'
        }
        
        missing = bulk_portfolios - template_portfolios - allowed_missing
        
        if missing:
            raise ValidationError(f"Missing portfolios in template: {missing}")
```

## 5. הודעות Validation

### סוגי הודעות
```python
# Error - חוסם המשך
"Missing required file: Bulk 30"
"Template structure invalid"
"Missing portfolios in template: {names}"
"No rows left after filtering"

# Warning - לא חוסם
"Note: No Bidding Adjustment rows found"
"Large file detected - processing may take longer"
"{n} portfolios marked as Ignore"

# Info - מידע בלבד
"Processing Zero Sales optimization..."
"Found {n} rows with Units = 0"
"Optimization complete"
```

## 6. UI Integration

### הצגת הודעות ב-UI
```python
def display_validation_results(results):
    """הצגת תוצאות validation ב-UI"""
    
    if results['status'] == 'error':
        st.error(results['message'])
        st.button("Upload New Files")
        
    elif results['status'] == 'warning':
        st.warning(results['message'])
        st.button("Process Anyway")
        
    elif results['status'] == 'success':
        st.success("Validation passed")
        st.button("Process Files")
```

## 7. מקרי קצה

### קובץ ריק אחרי ניקוי
```python
if len(cleaned_df) == 0:
    # הודעה ידידותית למשתמש
    message = "No rows match the criteria for this optimization. "
    message += "Please check that you have rows with Units = 0."
    raise ValidationError(message)
```

### כל ה-portfolios מסומנים Ignore
```python
active_portfolios = template_df[template_df['Base Bid'] != 'Ignore']
if len(active_portfolios) == 0:
    raise ValidationError("All portfolios marked as Ignore - cannot proceed")
```

### חסרות עמודות קריטיות
```python
critical_columns = ['Units', 'Clicks', 'Bid']
missing = set(critical_columns) - set(df.columns)
if missing:
    raise ValidationError(f"Critical columns missing: {missing}")
```

## 8. Performance Considerations

### עיבוד בחלקים
```python
def validate_large_file(df, chunk_size=10000):
    """Validation לקבצים גדולים"""
    
    total_rows = len(df)
    if total_rows > 100000:
        st.info(f"Validating {total_rows:,} rows...")
        
    # עיבוד בחלקים עם progress bar
    for i in range(0, total_rows, chunk_size):
        chunk = df.iloc[i:i+chunk_size]
        validate_chunk(chunk)
        update_progress(i / total_rows)
```

## 9. אופטימיזציות עתידיות

### Template למה שיבוא
```python
class FutureOptimization(BaseOptimization):
    
    def get_required_files(self):
        """TBD - כל אופטימיזציה תגדיר מה היא צריכה"""
        return {
            'template': True,
            'bulk_7': False,
            'bulk_30': True,
            'bulk_60': False,
            'data_rova': True  # אולי תצטרך benchmarking
        }
    
    def validate_specific(self, df):
        """TBD - validation ספציפי לאופטימיזציה"""
        pass
```

## 10. Campaigns Optimizer

```python
# TBD - איפיון Validation ל-Negation ו-Harvesting יתווסף בעתיד
class NegationOptimization(BaseOptimization):
    """יתווסף בשלב 5"""
    pass

class HarvestingOptimization(BaseOptimization):
    """יתווסף בשלב 6"""
    pass
```