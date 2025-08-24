# שלב 3: Upload Panel - Template
**משך: 2 ימים**

## מטרת השלב
יצירת פאנל העלאה עם יכולת להוריד Template ולהעלות אותו חזרה. בסוף השלב המשתמש יוכל להוריד קובץ Template של Excel ולהעלות אותו בחזרה עם בדיקות תקינות.

## רשימת קבצים לפיתוח (7 קבצים)

### 1. app/pages/bid_optimizer.py
**פונקציות:**
- `render_bid_optimizer_page()` - מציג את כל עמוד Bid Optimizer
- `show_page_title()` - מציג כותרת העמוד
- `render_upload_panel()` - קורא לפאנל ההעלאה
- `check_files_uploaded()` - בודק אילו קבצים הועלו

### 2. app/ui/shared/upload_section.py
**פונקציות:**
- `render()` - מציג את כל פאנל ההעלאה
- `render_template_section()` - מציג כפתורי Template
- `render_bulk_section()` - מציג כפתורי Bulk מושבתים
- `handle_template_upload()` - מטפל בהעלאת Template
- `show_upload_status()` - מציג סטטוס קבצים שהועלו

### 3. app/ui/components/buttons.py
**פונקציות:**
- `create_upload_button()` - יוצר כפתור העלאה עם עיצוב
- `create_download_button()` - יוצר כפתור הורדה עם עיצוב
- `create_disabled_button()` - יוצר כפתור מושבת עם Coming Soon
- `apply_button_styles()` - מחיל עיצוב על כפתורים

### 4. data/template_generator.py
**פונקציות:**
- `create_template()` - יוצר קובץ Template עם 2 לשוניות
- `create_port_values_sheet()` - יוצר לשונית Port Values עם 3 עמודות
- `create_top_asins_sheet()` - יוצר לשונית Top ASINs עם עמודה אחת
- `write_to_excel()` - כותב DataFrames לקובץ Excel
- `add_example_data()` - מוסיף נתוני דוגמה לקובץ

### 5. data/readers/excel_reader.py
**פונקציות:**
- `read_excel_file()` - קורא קובץ Excel לפי שם לשונית
- `read_template()` - קורא Template עם 2 לשוניות ספציפיות
- `validate_excel_format()` - בודק שהקובץ הוא Excel תקין
- `get_sheet_names()` - מחזיר רשימת שמות לשוניות
- `read_all_sheets()` - קורא את כל הלשוניות לדיקשנרי

### 6. data/validators/template_validator.py
**פונקציות:**
- `validate_template_structure()` - בודק מבנה כללי של Template
- `check_required_sheets()` - בודק קיום לשוניות Port Values ו-Top ASINs
- `validate_port_values_columns()` - בודק 3 עמודות נדרשות
- `check_duplicate_portfolios()` - מחפש שמות פורטפוליו כפולים
- `validate_base_bid_values()` - בודק ערכי Base Bid בטווח או Ignore
- `validate_target_cpa_values()` - בודק ערכי Target CPA תקינים

### 7. config/ui_text.py
**TO DO:**
- מילון עם כל הטקסטים של הממשק
- כותרות לפאנלים
- הודעות הצלחה וכישלון
- תוויות לכפתורים
- טקסטים ל-Coming Soon

## בדיקות משתמש

1. **הורדת Template**
   - לחיצה על DOWNLOAD TEMPLATE
   - קובץ Excel נשמר למחשב
   - הקובץ נפתח ב-Excel
   - 2 לשוניות קיימות

2. **העלאת Template**
   - גרירת קובץ לאזור העלאה
   - הודעה ירוקה מופיעה
   - סטטוס מתעדכן

3. **בדיקת שגיאות**
   - העלאת קובץ לא תקין
   - הודעת שגיאה ברורה
   - אפשרות לנסות שוב

## בדיקות מתכנת

1. **יצירת Template**
   - create_template מחזיר BytesIO
   - 2 לשוניות נוצרות
   - 3 עמודות ב-Port Values
   - נתוני דוגמה תקינים

2. **קריאת Template**
   - read_template מזהה לשוניות
   - שגיאה אם חסרה לשונית
   - DataFrames נוצרים נכון

3. **וולידציה**
   - duplicate portfolios מזוהים
   - Base Bid מחוץ לטווח נתפס
   - Ignore מזוהה כערך תקין

## מה המשתמש רואה

### מה עובד:
- פאנל UPLOAD FILES
- Download Template פעיל
- Upload Template פעיל
- הודעות סטטוס
- 4 כפתורים מושבתים

### מה עדיין משובש:
- Bulk files לא עובדים
- אין Validation panel
- אין Processing
- אין Output
- רוב הכפתורים מושבתים

---
**תאריך: דצמבר 2024, 12:45**