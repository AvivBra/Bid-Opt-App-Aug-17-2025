# מפרט ארכיטקטורה - Bid Optimizer

## 1. סקירה כללית

### ארכיטקטורת 4 שכבות
```
┌─────────────────────────────────┐
│         UI Layer                │
├─────────────────────────────────┤
│      Business Layer             │
├─────────────────────────────────┤
│    Optimizations Layer          │
├─────────────────────────────────┤
│        Data Layer               │
└─────────────────────────────────┘
```

### עקרונות מנחים
- הפרדת אחריות מלאה
- תקשורת חד-כיוונית מלמעלה למטה
- כל שכבה חושפת ממשק ברור
- אין תלויות צולבות

## 2. שכבת UI (app/ui/)

### אחריות
- הצגת ממשק למשתמש
- קבלת קבצים ובחירות
- הצגת תוצאות ומשוב
- ניהול מצב הסשן

### רכיבים
```
ui/
├── page_single.py          # עמוד ראשי
├── panels/
│   ├── upload_panel.py     # אזור העלאת קבצים
│   ├── validate_panel.py   # תצוגת ולידציה
│   └── output_panel.py     # אזור הורדות
└── components/
    ├── file_cards.py       # כרטיסי קבצים
    ├── checklist.py        # רשימת אופטימיזציות
    └── buttons.py          # כפתורים
```

### כללים
- לא מבצעת חישובים
- לא ניגשת ישירות לקבצים
- תקשורת רק דרך Orchestrator

## 3. שכבת Business (business/)

### אחריות
- תיאום בין רכיבים
- ניהול זרימת עבודה
- יצירת קבצי פלט
- החזרת תוצאות ל-UI

### רכיבים
```
business/
├── services/
│   └── orchestrator.py     # מתאם ראשי
└── processors/
    └── file_generator.py   # יוצר קבצי פלט
```

### Orchestrator API
```python
class Orchestrator:
    def validate_files(files: Dict) -> Dict
    def get_required_files(optimization: str) -> List
    def run_optimizations(files: Dict, selected: List) -> Dict
    def generate_output_files(results: Dict) -> Tuple[BytesIO, BytesIO]
```

## 4. שכבת Optimizations (business/optimizations/)

### אחריות
- ביצוע אופטימיזציות ספציפיות
- ולידציה עצמאית
- ניקוי נתונים ספציפי
- עיבוד והחזרת תוצאות

### מבנה אופטימיזציה
```
zero_sales/
├── __init__.py
├── validator.py    # ולידציות ספציפיות
├── cleaner.py     # ניקוי נתונים
└── processor.py   # לוגיקת עיבוד
```

### BaseOptimization Interface
```python
class BaseOptimization:
    @property
    def required_files(self) -> List[str]
    
    def validate(self, files: Dict) -> ValidationResult
    def clean(self, df: DataFrame) -> DataFrame
    def process(self, files: Dict) -> Dict[str, DataFrame]
```

## 5. שכבת Data (data/)

### אחריות
- קריאת קבצים
- כתיבת קבצים
- מודלים של נתונים
- יצירת טמפלייטים

### רכיבים
```
data/
├── readers/
│   ├── excel_reader.py
│   └── csv_reader.py
├── writers/
│   └── output_writer.py
├── models/
│   ├── portfolio.py
│   └── validation_result.py
└── template_generator.py
```

### Reader API
```python
class FileReader:
    def read_file(file: BytesIO) -> DataFrame
    def validate_structure(df: DataFrame) -> bool
```

## 6. זרימת נתונים

### Upload Flow
```
User → UI → Session State → Orchestrator → FileReader → DataFrame
```

### Validation Flow
```
Orchestrator → Optimization.validate() → ValidationResult → UI
```

### Processing Flow
```
Orchestrator → Optimization.process() → DataFrames → FileGenerator → Excel
```

## 7. Session State Structure

```python
{
    # קבצים שהועלו
    'template_file': BytesIO,
    'bulk_30_file': BytesIO,
    'bulk_60_file': BytesIO,
    'bulk_7_file': BytesIO,
    'data_rova_file': BytesIO,
    
    # DataFrames
    'template_df': DataFrame,
    'bulk_30_df': DataFrame,
    'bulk_60_df': DataFrame,
    'bulk_7_df': DataFrame,
    'data_rova_df': DataFrame,
    
    # בחירות משתמש
    'selected_optimizations': List[str],
    
    # תוצאות ולידציה (לכל אופטימיזציה)
    'validation_results': {
        'zero_sales': ValidationResult,
        'portfolio_bid': ValidationResult,
        ...
    },
    
    # תוצאות עיבוד
    'processing_results': {
        'zero_sales': Dict[str, DataFrame],
        ...
    },
    
    # קבצי פלט
    'output_files': {
        'working': BytesIO,
        'clean': BytesIO
    }
}
```

## 8. תקשורת בין שכבות

### חוקי תקשורת
- UI ← Orchestrator בלבד
- Orchestrator ← Optimizations
- Optimizations ← Data Layer
- אין תקשורת ישירה UI ← Data

### טיפול בשגיאות
```
Data Layer → Exception → Optimization → Result → Orchestrator → UI Message
```

## 9. הרחבה עתידית

### הוספת אופטימיזציה חדשה
1. יצירת תיקייה תחת optimizations/
2. יישום BaseOptimization
3. הגדרת required_files
4. כתיבת validator, cleaner, processor
5. רישום ב-Orchestrator

### הוספת סוג קובץ חדש
1. הוספת כפתור ב-UI
2. עדכון Session State
3. עדכון Orchestrator
4. עדכון אופטימיזציות רלוונטיות

## 10. אילוצים טכניים

### מגבלות
- קובץ עד 40MB
- עד 500,000 שורות
- עד 14 אופטימיזציות במקביל
- זמן עיבוד מקסימלי 120 שניות

### ביצועים
- קריאת קובץ: < 5 שניות
- ולידציה: < 2 שניות לאופטימיזציה
- עיבוד: < 10 שניות ל-100K שורות
- יצירת פלט: < 5 שניות