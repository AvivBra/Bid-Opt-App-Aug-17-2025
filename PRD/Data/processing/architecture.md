# איפיון ארכיטקטורה - Bid Optimizer

## 1. סקירה כללית

### מטרת המערכת
מערכת לאופטימיזציה של Bids בקמפיינים של Amazon Advertising. המערכת מעבדת קבצי Bulk גדולים (עד 40MB, 500K שורות) ומחילה אופטימיזציות שונות על הנתונים.

### עקרונות ארכיטקטוניים
- **הפרדת אחריות** - UI, Business Logic, Data Access
- **מודולריות** - כל אופטימיזציה במודול נפרד
- **ללא State** - כל פונקציה מקבלת את כל הנתונים שהיא צריכה
- **ניתן להרחבה** - קל להוסיף אופטימיזציות ועמודים חדשים

## 2. ארכיטקטורת 3 שכבות

### שכבת UI (app/ui/)
**תפקיד:** ממשק משתמש וויזואליזציה

**רכיבים:**
- `sidebar.py` - ניווט בין עמודים
- `pages/` - עמודי האפליקציה
- `shared/` - קומפוננטות משותפות
- `components/` - רכיבי UI לשימוש חוזר
- `layout.py` - עיצוב ופריסה

**כללים:**
- קריאה מ-Session State בלבד
- קריאה לפונקציות Orchestrator בלבד
- אין לוגיקת עיבוד נתונים
- כל הטקסטים באנגלית

### שכבת Business Logic (business/)
**תפקיד:** לוגיקה עסקית וחישובים

**רכיבים:**
- `bid_optimizations/` - אופטימיזציות Bid
- `campaign_optimizations/` - אופטימיזציות Campaign (TBD)
- `processors/` - עיבוד נתונים
- `services/` - תיאום בין רכיבים

**כללים:**
- מקבל DataFrames, מחזיר DataFrames
- אין תלות ב-Streamlit
- כל אופטימיזציה מבצעת validation וcleaning עצמאיים
- ניתן לבדיקה בנפרד מה-UI

### שכבת Data Access (data/)
**תפקיד:** קריאה וכתיבה של קבצים

**רכיבים:**
- `readers/` - קריאת Excel/CSV
- `writers/` - כתיבת קבצי פלט
- `models/` - מבני נתונים
- `templates/` - יצירת templates

**כללים:**
- אין לוגיקה עסקית
- רק I/O operations
- מחזיר DataFrames או Exceptions

## 3. זרימת נתונים

### תהליך העלאה
```
User → UI (upload buttons) → Session State → Orchestrator → 
→ Excel/CSV Reader → DataFrame → Session State
```

### תהליך אופטימיזציה
```
Session State → Orchestrator → Optimization Module →
→ Internal Validation → Internal Cleaning → Processing →
→ FileGenerator → OutputWriter → Excel Files
```

### תהליך ניווט
```
Sidebar Selection → Page Router → Load Page → 
→ Render Components → Access Session State
```

## 4. Session State Structure

```python
{
    # קבצים שהועלו
    'template_file': BytesIO,
    'bulk_7_file': BytesIO,
    'bulk_30_file': BytesIO,
    'bulk_60_file': BytesIO,
    'data_rova_file': BytesIO,  # TBD
    
    # DataFrames
    'template_df': pd.DataFrame,
    'bulk_dfs': Dict[str, pd.DataFrame],
    
    # בחירות משתמש
    'selected_optimizations': List[str],
    'current_page': str,  # 'bid_optimizer' או 'campaigns_optimizer'
    
    # קבצי פלט
    'output_files': {
        'working': BytesIO,
        'clean': BytesIO
    },
    
    # מצב אפליקציה
    'current_state': 'upload' | 'process' | 'complete'
}
```

## 5. תקשורת בין שכבות

### UI → Business
- תמיד דרך Orchestrator
- פרמטרים: DataFrames או primitives
- החזרה: DataFrames או ValidationResult

### Business → Data
- ישירות לקוראים/כותבים
- פרמטרים: file paths או BytesIO
- החזרה: DataFrames או Exceptions

### אסור
- UI → Data (ישירות)
- Data → Business (callback)
- Business → UI (ישירות)

## 6. ניהול שגיאות

### היררכיית Exceptions
```
ApplicationError
├── ValidationError
│   ├── FileValidationError
│   ├── DataValidationError
│   └── PortfolioValidationError
├── ProcessingError
│   ├── OptimizationError
│   └── CalculationError
└── IOError
    ├── FileReadError
    └── FileWriteError
```

### Error Propagation
- Exceptions עולים מ-Data → Business → UI
- UI מציג הודעות ידידותיות למשתמש
- Business לא תופס Exceptions מ-Data
- Logging בכל שכבה

## 7. ביצועים

### מגבלות
- גודל קובץ מקסימלי: 40MB
- מספר שורות מקסימלי: 500,000
- זיכרון מקסימלי: 4GB

### זמני עיבוד צפויים
| גודל קובץ | זמן עיבוד |
|-----------|-----------|
| < 5MB | < 15 שניות |
| 5-10MB | 15-30 שניות |
| 10-20MB | 30-60 שניות |
| 20-40MB | 60-120 שניות |
| 500K שורות | עד 180 שניות |

### אופטימיזציות
- קריאה בחלקים (chunks) לקבצים גדולים
- עיבוד מקבילי כאשר אפשר
- Cache לנתונים שלא משתנים
- Progress bar לתהליכים ארוכים

## 8. אבטחה

### הגנות
- בדיקת גודל קובץ לפני קריאה
- Sanitization לשמות קבצים
- Validation לכל input
- אין הרצת קוד דינמי

### מגבלות
- אין שמירת נתונים רגישים ב-Session State
- אין העלאת קבצים לשרת
- כל העיבוד מתבצע בזיכרון

## 9. הרחבה עתידית

### הוספת אופטימיזציה חדשה
1. יצירת מודול ב-`bid_optimizations/`
2. ירושה מ-`BaseOptimization`
3. מימוש `validate()`, `clean()`, `process()`
4. הוספה ל-checklist ב-UI

### הוספת עמוד חדש
1. יצירת קובץ ב-`pages/`
2. הוספה ל-sidebar
3. שימוש ב-shared components
4. חיבור ל-orchestrator

### Campaigns Optimizer (TBD)
- ארכיטקטורה זהה ל-Bid Optimizer
- Orchestrator נפרד
- State management נפרד
- אותן קומפוננטות UI