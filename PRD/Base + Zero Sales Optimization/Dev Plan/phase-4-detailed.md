# שלב 4: Upload Panel - Bulk Files
**משך: 2 ימים**

## מטרת השלב
הוספת יכולת העלאת קובץ Bulk 60 עם תמיכה ב-Excel ו-CSV. בסוף השלב המשתמש יוכל להעלות קובץ Bulk עם 48 עמודות ועד 500,000 שורות.

## רשימת קבצים לפיתוח (3 קבצים)

### 1. data/readers/csv_reader.py
**פונקציות:**
- `read_csv_file()` - קורא קובץ CSV עם טיפול ב-encoding
- `try_utf8_encoding()` - מנסה לקרוא עם UTF-8
- `fallback_to_latin1()` - נופל ל-Latin-1 אם UTF-8 נכשל
- `read_bulk_csv()` - קורא CSV ובודק 48 עמודות
- `check_row_limit()` - בודק שאין יותר מ-500,000 שורות

### 2. data/validators/bulk_validator.py
**פונקציות:**
- `validate_bulk_file()` - בדיקה ראשית של קובץ Bulk
- `check_file_size()` - בודק שהקובץ לא עולה על 40MB
- `validate_column_count()` - בודק שיש בדיוק 48 עמודות
- `check_required_columns()` - בודק עמודות חובה כמו Entity ו-Units
- `get_bulk_stats()` - מחזיר סטטיסטיקות על הקובץ
- `validate_sheet_name()` - בודק שיש Sponsored Products Campaigns

### 3. app/state/bid_state.py
**פונקציות:**
- `init_bid_state()` - מאתחל state לקבצים
- `save_template()` - שומר Template ב-session state
- `save_bulk()` - שומר Bulk file ב-session state
- `get_uploaded_files()` - מחזיר רשימת קבצים שהועלו
- `clear_all_files()` - מנקה את כל הקבצים מה-state
- `update_file_stats()` - מעדכן סטטיסטיקות קבצים

## בדיקות משתמש

1. **העלאת Bulk 60**
   - כפתור BULK 60 DAYS פעיל
   - העלאת קובץ Excel או CSV
   - הודעת הצלחה ירוקה
   - הצגת מספר שורות

2. **בדיקת מגבלות**
   - קובץ 50MB נדחה
   - קובץ עם 30 עמודות נדחה
   - קובץ עם מיליון שורות נדחה

3. **סטטיסטיקות**
   - מספר שורות מוצג
   - מספר פורטפוליוז מוצג
   - גודל קובץ מוצג

## בדיקות מתכנת

1. **קריאת CSV**
   - UTF-8 encoding עובד
   - Latin-1 fallback עובד
   - שגיאה על קובץ פגום

2. **וולידציה**
   - 48 עמודות בדיוק
   - גודל מקסימלי 40MB
   - שורות מקסימום 500,000

3. **State management**
   - bulk_60_df נשמר ב-state
   - סטטיסטיקות מתעדכנות
   - clear_files מנקה הכל

## מה המשתמש רואה

### מה עובד:
- Upload Template (משלב קודם)
- Upload Bulk 60 חדש
- סטטיסטיקות קבצים
- הודעות שגיאה ברורות

### מה עדיין משובש:
- Bulk 7/30 מושבתים
- Data Rova מושבת
- אין Validation panel
- אין Processing
- אין Output

---
**תאריך: דצמבר 2024, 12:45**