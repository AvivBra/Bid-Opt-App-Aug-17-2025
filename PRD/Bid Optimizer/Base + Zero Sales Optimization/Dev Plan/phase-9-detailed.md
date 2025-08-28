# שלב 9: בדיקות אינטגרציה מלאות
**משך: 2 ימים**

## מטרת השלב
כתיבת בדיקות מקיפות לכל המערכת ותיקון באגים שנמצאו. בסוף השלב המערכת תהיה יציבה ומבוקרת עם כיסוי בדיקות גבוה.

## רשימת קבצים לפיתוח (4 קבצים)

### 1. tests/unit/test_zero_sales.py
**פונקציות בדיקה:**
- `test_case_a_calculation()` - בודק חישוב מקרה A
- `test_case_b_calculation()` - בודק חישוב מקרה B
- `test_case_c_calculation()` - בודק חישוב מקרה C
- `test_case_d_calculation()` - בודק חישוב מקרה D
- `test_filter_zero_units()` - בודק סינון Units=0
- `test_exclude_flat_portfolios()` - בודק סינון 10 פורטפוליוז
- `test_add_helper_columns()` - בודק הוספת 7 עמודות
- `test_bid_range_validation()` - בודק טווח 0.02-4.00

### 2. tests/integration/test_bid_flow.py
**פונקציות בדיקה:**
- `test_full_flow()` - בודק תהליך מקצה לקצה
- `test_upload_template()` - בודק העלאת Template
- `test_upload_bulk()` - בודק העלאת Bulk
- `test_validation_pass()` - בודק וולידציה מוצלחת
- `test_validation_fail()` - בודק וולידציה נכשלת
- `test_processing()` - בודק עיבוד
- `test_download_file()` - בודק הורדת קובץ
- `test_reset_state()` - בודק ניקוי state

### 3. tests/fixtures/valid_template.xlsx
**תוכן הקובץ:**
- לשונית Port Values עם 5 פורטפוליוז
- לשונית Top ASINs עם 10 מוצרים
- ערכי Base Bid מגוונים
- פורטפוליו אחד עם Ignore
- Target CPA חלקי

### 4. tests/fixtures/valid_bulk_60.xlsx
**תוכן הקובץ:**
- 10,000 שורות לבדיקה
- 48 עמודות בדיוק
- מגוון Entity types
- חלק עם Units=0
- כולל Flat portfolios

## בדיקות משתמש

1. **תרחיש Happy Path**
   - העלאת קבצים תקינים
   - בחירת Zero Sales
   - Process Files
   - הורדת תוצאה

2. **תרחיש שגיאות**
   - קובץ גדול מדי
   - חסרות עמודות
   - פורטפוליוז חסרים
   - התאוששות משגיאות

3. **ביצועים**
   - 10,000 שורות < 10 שניות
   - 100,000 שורות < 30 שניות
   - זיכרון < 2GB

## בדיקות מתכנת

1. **Unit tests**
   - כל החישובים מדויקים
   - סינונים עובדים
   - וולידציות תקינות
   - 80%+ code coverage

2. **Integration tests**
   - תהליך מלא עובר
   - טיפול בשגיאות
   - State management
   - File I/O

3. **Performance tests**
   - זמני עיבוד בטווח
   - זיכרון לא דולף
   - קבצים גדולים נטענים

## מה המשתמש רואה

### מה עובד:
- מערכת יציבה לחלוטין
- כל התכונות של Phase 1
- טיפול בשגיאות מלא
- ביצועים טובים

### מה עדיין משובש:
- תכונות TBC (כמתוכנן)
- Clean File מושבת
- 13 אופטימיזציות מושבתות

---
**תאריך: דצמבר 2024, 12:45**