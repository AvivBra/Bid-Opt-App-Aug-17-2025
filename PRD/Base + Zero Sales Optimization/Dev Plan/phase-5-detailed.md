# שלב 5: Validation Panel
**משך: 2 ימים**

## מטרת השלב
יצירת פאנל וולידציה שבודק התאמה בין Template ל-Bulk ומאפשר בחירת אופטימיזציות. בסוף השלב יהיה פאנל שמראה אם הקבצים תקינים ומאפשר להתחיל עיבוד.

## רשימת קבצים לפיתוח (5 קבצים)

### 1. app/ui/shared/validation_section.py
**פונקציות:**
- `render()` - מציג את כל פאנל הוולידציה
- `check_files_ready()` - בודק אם שני הקבצים הועלו
- `run_validation()` - מריץ בדיקות התאמה
- `display_validation_result()` - מציג תוצאות בצבעים
- `render_optimization_selection()` - מציג רשימת checkboxes
- `render_process_button()` - מציג כפתור Process Files

### 2. app/ui/components/alerts.py
**פונקציות:**
- `show_success()` - מציג הודעה ירוקה עם נקודה
- `show_error()` - מציג הודעה אדומה עם נקודה
- `show_warning()` - מציג הודעה כתומה עם נקודה
- `show_info()` - מציג הודעה כחולה עם נקודה
- `create_alert_html()` - יוצר HTML להודעה עם עיצוב

### 3. app/ui/components/checklist.py
**פונקציות:**
- `render_optimization_checklist()` - מציג 14 checkboxes
- `create_checkbox()` - יוצר checkbox בודד
- `mark_disabled_items()` - מוסיף Coming Soon לפריטים מושבתים
- `get_selected_optimizations()` - מחזיר רשימת נבחרים
- `update_selection_state()` - מעדכן state עם הבחירות

### 4. data/validators/portfolio_validator.py
**פונקציות:**
- `validate_portfolios()` - בדיקה ראשית של התאמה
- `get_template_portfolios()` - מחלץ רשימת פורטפוליוז מ-Template
- `get_bulk_portfolios()` - מחלץ רשימת פורטפוליוז מ-Bulk
- `find_missing_portfolios()` - מוצא פורטפוליוז חסרים
- `check_ignored_portfolios()` - בודק כמה מסומנים Ignore
- `filter_excluded_portfolios()` - מסנן 10 פורטפוליוז מוחרגים

### 5. business/common/excluded_portfolios.py
**TO DO:**
- רשימת 10 פורטפוליוז Flat קבועים
- פונקציה לבדיקה אם פורטפוליו מוחרג
- פונקציה לסינון DataFrame
- קבועים של שמות הפורטפוליוז

## בדיקות משתמש

1. **וולידציה מוצלחת**
   - העלאת 2 קבצים תקינים
   - הודעה ירוקה All portfolios valid
   - כפתור Process Files פעיל

2. **פורטפוליוז חסרים**
   - העלאת Bulk עם פורטפוליו חדש
   - הודעה אדומה עם רשימה
   - כפתור Process מושבת

3. **בחירת אופטימיזציות**
   - Zero Sales checkbox פעיל
   - 13 אחרים מושבתים
   - סימון נשמר

## בדיקות מתכנת

1. **התאמת פורטפוליוז**
   - missing portfolios מזוהים
   - excluded portfolios מסוננים
   - ignored portfolios נספרים

2. **Checkbox state**
   - רק Zero Sales enabled
   - selected_optimizations מתעדכן
   - state נשמר בין רענונים

3. **Process button**
   - מופעל רק כשוולידציה עוברת
   - מושבת אם חסרים פורטפוליוז
   - משנה state ל-processing_started

## מה המשתמש רואה

### מה עובד:
- Upload panel מלא
- Validation panel חדש
- בדיקות התאמה
- 14 checkboxes
- כפתור Process Files

### מה עדיין משובש:
- Process לא עושה כלום
- אין Progress Bar
- אין Output
- 13 אופטימיזציות מושבתות
- אין לוגיקה עסקית

---
**תאריך: דצמבר 2024, 12:45**