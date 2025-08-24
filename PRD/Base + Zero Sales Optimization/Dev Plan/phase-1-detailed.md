# שלב 1: תשתית והגדרות בסיסיות
**משך: 2 ימים**

## מטרת השלב
יצירת תשתית בסיסית לאפליקציה עם הגדרות Dark Mode וניהול State. בסוף השלב תהיה אפליקציה ריקה עם רקע כהה וכותרת שעובדת ב-Streamlit.

## רשימת קבצים לפיתוח (8 קבצים)

### 1. requirements.txt
**TO DO:**
- רשימת כל החבילות הנדרשות
- גרסאות מינימליות לכל חבילה
- streamlit, pandas, openpyxl, numpy, pytest

### 2. .streamlit/config.toml
**TO DO:**
- הגדרות theme עם צבעים כהים
- primaryColor בצבע ויולט
- backgroundColor שחור
- הגדרת פונט

### 3. config/constants.py
**TO DO:**
- MAX_FILE_SIZE_MB קבוע ל-40
- MAX_TEMPLATE_SIZE_MB קבוע ל-1
- MAX_ROWS קבוע ל-500000
- REQUIRED_COLUMNS קבוע ל-48
- MIN_BID ו-MAX_BID טווחים
- רשימת 10 פורטפוליוז מוחרגים

### 4. config/settings.py
**TO DO:**
- APP_TITLE שם האפליקציה
- VERSION מספר גרסה
- ENVIRONMENT סביבת הרצה
- DEBUG_MODE דגל לפיתוח
- SESSION_TIMEOUT זמן תפוגה

### 5. utils/file_utils.py
**פונקציות:**
- `get_file_size()` - מחזיר גודל קובץ במגה בייט
- `validate_file_extension()` - בודק סיומת קובץ מול רשימה מותרת
- `read_file_to_bytes()` - קורא קובץ ל-BytesIO אובייקט
- `cleanup_temp_files()` - מנקה קבצים זמניים מהמערכת

### 6. utils/filename_generator.py
**פונקציות:**
- `generate_output_filename()` - יוצר שם קובץ פלט עם תאריך ושעה
- `get_timestamp()` - מחזיר תאריך ושעה בפורמט YYYY-MM-DD HH-MM
- `sanitize_filename()` - מנקה תווים לא חוקיים משם קובץ

### 7. app/main.py
**פונקציות:**
- `main()` - נקודת כניסה ראשית להגדרת דף
- `setup_page_config()` - מגדיר את תצורת הדף ב-Streamlit
- `render_title()` - מציג כותרת ראשית

### 8. app/state/session_manager.py
**פונקציות:**
- `init_session_state()` - מאתחל את כל משתני ה-state
- `clear_session_state()` - מנקה את כל ה-state
- `get_state()` - מחזיר ערך ממשתנה state לפי מפתח
- `set_state()` - מעדכן ערך במשתנה state

## בדיקות משתמש

1. **הרצת האפליקציה**
   - הקלד בטרמינל streamlit run app/main.py
   - וודא שהדפדפן נפתח אוטומטית
   - בדוק שאין שגיאות אדומות

2. **בדיקת עיצוב**
   - רקע שחור כהה מופיע
   - כותרת BID OPTIMIZER במרכז
   - טקסט בצבע לבן

3. **בדיקת רספונסיביות**
   - שנה גודל חלון הדפדפן
   - וודא שהתוכן נשאר ממורכז

## בדיקות מתכנת

1. **בדיקת imports**
   - כל החבילות ב-requirements נטענות
   - אין התנגשויות בין גרסאות
   - pytest רץ ללא שגיאות

2. **בדיקת session_state**
   - init_session_state יוצר dictionary ריק
   - get_state מחזיר None לערך לא קיים
   - set_state שומר ערכים נכון

3. **בדיקת filename_generator**
   - generate_output_filename מחזיר פורמט נכון
   - timestamp כולל תאריך ושעה
   - אין תווים לא חוקיים

## מה המשתמש רואה

### מה עובד:
- אפליקציה נטענת בדפדפן
- רקע כהה
- כותרת ראשית
- טקסט Welcome

### מה עדיין משובש:
- אין Sidebar
- אין כפתורים
- אין Upload
- אין Validation
- אין Processing
- רק דף ריק עם כותרת

---
**תאריך: דצמבר 2024, 12:45**