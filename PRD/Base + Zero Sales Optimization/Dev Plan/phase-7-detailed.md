# שלב 7: Zero Sales - Business Logic
**משך: 3 ימים**

## מטרת השלב
פיתוח הלוגיקה העסקית של Zero Sales - סינון, ניקוי וחישוב Bid חדש. בסוף השלב תהיה לוגיקה מלאה שמחשבת Bids לפי 4 מקרים אך עדיין לא מחוברת ל-UI.

## רשימת קבצים לפיתוח (5 קבצים)

### 1. business/bid_optimizations/base_optimization.py
**פונקציות:**
- `__init__()` - אתחול מחלקת בסיס לאופטימיזציות
- `get_required_files()` - מגדיר אילו קבצים נדרשים
- `validate()` - מתודה מופשטת לוולידציה
- `clean()` - מתודה מופשטת לניקוי נתונים
- `process()` - מתודה מופשטת לעיבוד
- `execute()` - מריץ את כל התהליך בסדר

### 2. business/bid_optimizations/zero_sales/validator.py
**פונקציות:**
- `validate()` - בדיקה ראשית של נתוני Zero Sales
- `check_units_column()` - בודק שעמודת Units קיימת
- `check_clicks_column()` - בודק שעמודת Clicks קיימת
- `validate_portfolio_columns()` - בודק עמודות פורטפוליו
- `check_entity_types()` - בודק סוגי Entity תקינים
- `validate_bid_column()` - בודק שעמודת Bid קיימת

### 3. business/bid_optimizations/zero_sales/cleaner.py
**פונקציות:**
- `clean()` - ניקוי ראשי של הנתונים
- `filter_zero_units()` - מסנן רק שורות עם Units=0
- `remove_flat_portfolios()` - מסיר 10 פורטפוליוז מוחרגים
- `remove_ignored_portfolios()` - מסיר פורטפוליוז עם Ignore
- `split_by_entity()` - מחלק לפי סוג Entity
- `validate_remaining_rows()` - בודק שנשארו שורות

### 4. business/bid_optimizations/zero_sales/processor.py
**פונקציות:**
- `process()` - עיבוד ראשי של Zero Sales
- `add_helper_columns()` - מוסיף 7 עמודות עזר
- `calculate_max_ba()` - מחשב Max BA לכל Campaign
- `calculate_adj_cpa()` - מחשב Adjusted CPA
- `calculate_new_bid()` - מחשב Bid חדש לפי 4 מקרים
- `apply_case_a()` - חישוב למקרה A
- `apply_case_b()` - חישוב למקרה B
- `apply_case_c()` - חישוב למקרה C
- `apply_case_d()` - חישוב למקרה D
- `mark_errors()` - מסמן שורות עם שגיאות

### 5. business/common/portfolio_filter.py
**פונקציות:**
- `filter_excluded_portfolios()` - מסנן 10 פורטפוליוז
- `is_flat_portfolio()` - בודק אם פורטפוליו הוא Flat
- `get_excluded_list()` - מחזיר רשימת מוחרגים
- `filter_dataframe()` - מסנן DataFrame לפי פורטפוליוז
- `count_filtered()` - סופר כמה שורות סוננו

## בדיקות משתמש

1. **יצירת קובץ בדיקה**
   - צור Excel עם 100 שורות
   - חלק עם Units=0
   - הרץ את הלוגיקה ידנית

2. **בדיקת חישובים**
   - Case A: Base Bid × 0.5
   - Case B: Base Bid
   - Case C+D: חישובים מורכבים

3. **בדיקת סינון**
   - Flat portfolios לא מופיעים
   - רק Units=0 נשארים
   - Ignored portfolios מסוננים

## בדיקות מתכנת

1. **Unit tests למקרים**
   - test_case_a_calculation
   - test_case_b_calculation
   - test_case_c_calculation
   - test_case_d_calculation

2. **בדיקת סינון**
   - test_filter_zero_units
   - test_remove_flat_portfolios
   - test_split_by_entity

3. **בדיקת helper columns**
   - 7 עמודות נוספות
   - Old Bid נשמר
   - Max BA מחושב נכון

## מה המשתמש רואה

### מה עובד:
- כל ה-UI (משלבים קודמים)
- לוגיקה מוכנה אך לא מחוברת

### מה עדיין משובש:
- Process Files לא מפעיל לוגיקה
- אין קובץ אמיתי להורדה
- סטטיסטיקות עדיין מדומות
- אין חיבור UI-Business

---
**תאריך: דצמבר 2024, 12:45**