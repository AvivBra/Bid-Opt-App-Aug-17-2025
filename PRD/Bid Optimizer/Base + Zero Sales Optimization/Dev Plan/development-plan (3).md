# תוכנית פיתוח - Bid Optimizer for Amazon Ads

## סקירת הפרויקט
מערכת אופטימיזציה אוטומטית להצעות מחיר (Bids) בקמפיינים של Amazon Ads. המערכת בנויה בארכיטקטורת 3 שכבות עם Sidebar Navigation וממשק Dark Mode מבוסס Streamlit.

---

## שלב 1: תשתית והגדרות בסיסיות
**משך: 2 ימים | קבצים: 8**

### קבצי קוד לכתיבה:
1. **requirements.txt** - תלויות Python
2. **.streamlit/config.toml** - הגדרות Streamlit (dark theme)
3. **config/constants.py** - קבועי המערכת
4. **config/settings.py** - הגדרות כלליות
5. **utils/file_utils.py** - פונקציות עזר לקבצים
6. **utils/filename_generator.py** - יצירת שמות קבצים
7. **app/main.py** - נקודת כניסה ראשית
8. **app/state/session_manager.py** - ניהול Session State

### בדיקות למשתמש:
- האפליקציה עולה בהרצת streamlit run
- רקע כהה (#0F0F0F) נטען נכון
- כותרת BID OPTIMIZER מופיעה במרכז

### בדיקות למתכנת:
- pytest עובר על utils/filename_generator
- session_state מאותחל ללא שגיאות
- config.toml נטען עם dark theme

### מה נראה בסוף השלב:
- אפליקציה ריקה עם רקע כהה
- כותרת ראשית
- מבנה תיקיות מוכן

### קבצים לנעילה:
- requirements.txt
- .streamlit/config.toml
- config/constants.py

---

## שלב 2: Sidebar Navigation
**משך: 1 יום | קבצים: 3**

### קבצי קוד לכתיבה:
1. **app/navigation.py** - לוגיקת ניווט
2. **app/ui/sidebar.py** - רכיב Sidebar
3. **app/ui/layout.py** - מבנה כללי

### בדיקות למשתמש:
- Sidebar מופיע בצד שמאל ברוחב 200px
- כפתור Bid Optimizer פעיל וניתן ללחיצה
- כפתור Campaigns Optimizer מושבת עם Coming Soon

### בדיקות למתכנת:
- st.sidebar.selectbox מחזיר ערך נכון
- navigation.py מעדכן session_state.current_page
- CSS של sidebar נטען מ-layout.py

### מה נראה בסוף השלב:
- Sidebar עם 2 עמודים
- אזור תוכן ראשי ריק
- ניווט עובד (רק עמוד אחד פעיל)

### קבצים לנעילה:
- app/navigation.py
- app/ui/sidebar.py

---

## שלב 3: Upload Panel - Template
**משך: 2 ימים | קבצים: 7**

### קבצי קוד לכתיבה:
1. **app/pages/bid_optimizer.py** - עמוד ראשי
2. **app/ui/shared/upload_section.py** - פאנל העלאה
3. **app/ui/components/buttons.py** - רכיבי כפתורים
4. **data/template_generator.py** - יצירת Template
5. **data/readers/excel_reader.py** - קריאת Excel
6. **data/validators/template_validator.py** - בדיקת Template
7. **config/ui_text.py** - טקסטים של הממשק

### בדיקות למשתמש:
- Download Template מוריד קובץ Excel תקין
- הקובץ מכיל Port Values ו-Top ASINs
- העלאת Template מציגה הודעת הצלחה ירוקה

### בדיקות למתכנת:
- template_generator יוצר DataFrame עם 3 עמודות
- excel_reader קורא שתי לשוניות נכון
- template_validator מזהה Portfolio Names כפולים

### מה נראה בסוף השלב:
- פאנל UPLOAD FILES עם 5 כפתורים
- Download Template עובד
- Upload Template עובד
- 4 כפתורים נוספים מושבתים (Coming Soon)

### קבצים לנעילה:
- data/template_generator.py
- data/validators/template_validator.py

---

## שלב 4: Upload Panel - Bulk Files
**משך: 2 ימים | קבצים: 3**

### קבצי קוד לכתיבה:
1. **data/readers/csv_reader.py** - קריאת CSV
2. **data/validators/bulk_validator.py** - בדיקת Bulk
3. **app/state/bid_state.py** - ניהול מצב הקבצים

### בדיקות למשתמש:
- העלאת Bulk 60 מציגה הודעת הצלחה
- קובץ מעל 40MB נדחה עם שגיאה
- מספר שורות מוצג נכון בסטטוס

### בדיקות למתכנת:
- csv_reader מטפל ב-encoding UTF-8/Latin1
- bulk_validator בודק 48 עמודות בדיוק
- bid_state שומר DataFrame ב-session_state

### מה נראה בסוף השלב:
- Upload Template + Bulk 60 עובדים
- הודעות הצלחה/כישלון מדויקות
- סטטוס קבצים מוצג

### קבצים לנעילה:
- data/readers/csv_reader.py
- data/readers/excel_reader.py

---

## שלב 5: Validation Panel
**משך: 2 ימים | קבצים: 5**

### קבצי קוד לכתיבה:
1. **app/ui/shared/validation_section.py** - פאנל וולידציה
2. **app/ui/components/alerts.py** - הודעות
3. **app/ui/components/checklist.py** - רשימת בחירה
4. **data/validators/portfolio_validator.py** - בדיקת portfolios
5. **business/common/excluded_portfolios.py** - רשימת 10 הפורטפוליוז

### בדיקות למשתמש:
- פאנל Validation מופיע אחרי העלאת קבצים
- הודעה ירוקה אם portfolios תקינים
- רשימת portfolios חסרים מוצגת באדום

### בדיקות למתכנת:
- portfolio_validator משווה בין Template ל-Bulk
- excluded_portfolios מכיל 10 שמות מדויקים
- checklist מעדכן session_state.selected_optimizations

### מה נראה בסוף השלב:
- פאנל DATA VALIDATION מלא
- 14 checkboxes (רק Zero Sales פעיל)
- כפתור Process Files

### קבצים לנעילה:
- business/common/excluded_portfolios.py
- data/validators/portfolio_validator.py

---

## שלב 6: Output Panel (ללא לוגיקה)
**משך: 2 ימים | קבצים: 4**

### קבצי קוד לכתיבה:
1. **app/ui/shared/output_section.py** - פאנל פלט
2. **app/ui/components/progress_bar.py** - מד התקדמות
3. **app/ui/components/download_buttons.py** - כפתורי הורדה
4. **utils/page_utils.py** - פונקציות עזר לדף

### בדיקות למשתמש:
- לחיצה על Process Files מציגה Progress Bar
- Progress Bar מתקדם מ-0% ל-100%
- כפתורי Download מופיעים אך מושבתים

### בדיקות למתכנת:
- progress_bar מקבל ערך 0-1 ומציג אחוזים
- download_buttons מקבל BytesIO ומאפשר הורדה
- output_section מחליף את validation_section

### מה נראה בסוף השלב:
- פאנל OUTPUT FILES עם Progress Bar
- Mock processing (10 שניות סימולציה)
- כפתורי Download מושבתים

### קבצים לנעילה:
- app/ui/components/progress_bar.py

---

## שלב 7: Zero Sales - Business Logic
**משך: 3 ימים | קבצים: 5**

### קבצי קוד לכתיבה:
1. **business/bid_optimizations/base_optimization.py** - מחלקת בסיס
2. **business/bid_optimizations/zero_sales/validator.py** - וולידציה פנימית
3. **business/bid_optimizations/zero_sales/cleaner.py** - ניקוי נתונים
4. **business/bid_optimizations/zero_sales/processor.py** - חישובי Bid
5. **business/common/portfolio_filter.py** - סינון portfolios

### בדיקות למשתמש:
- יצירת קובץ דוגמה קטן (100 שורות)
- הרצה ובדיקת תוצאות ידנית
- וידוא שורות עם Units=0 מעובדות

### בדיקות למתכנת:
- test_case_a: Target CPA ריק + "up and"
- test_case_b: Target CPA ריק ללא "up and"
- test_flat_portfolios_filtered: 10 פורטפוליוז מסוננים

### מה נראה בסוף השלב:
- לוגיקת Zero Sales מוכנה
- חישובים מדויקים
- טיפול בכל 4 המקרים

### קבצים לנעילה:
- business/bid_optimizations/base_optimization.py
- business/bid_optimizations/zero_sales/* (כל 4)

---

## שלב 8: Output Generation (חיבור לוגיקה ל-UI)
**משך: 2 ימים | קבצים: 4**

### קבצי קוד לכתיבה:
1. **business/bid_optimizations/zero_sales/orchestrator.py** - תיאום התהליך
2. **business/processors/output_formatter.py** - פורמט פלט
3. **data/writers/excel_writer.py** - כתיבת Excel
4. **config/optimization_config.py** - הגדרות אופטימיזציה

### בדיקות למשתמש:
- Process Files יוצר קובץ אמיתי
- Working File נפתח ב-Excel ללא שגיאות
- צביעה ורודה לשורות עם Bid מחוץ לטווח

### בדיקות למתכנת:
- excel_writer יוצר 2 לשוניות נכונות
- output_formatter מוסיף 7 עמודות עזר
- orchestrator מחבר UI ל-Business Logic

### מה נראה בסוף השלב:
- תהליך מלא עובד מקצה לקצה
- קובץ Excel עם נתונים מעובדים
- Download Working File פעיל

### קבצים לנעילה:
- data/writers/excel_writer.py
- business/processors/output_formatter.py

---

## שלב 9: בדיקות אינטגרציה מלאות
**משך: 2 ימים | קבצים: 4**

### קבצי קוד לכתיבה:
1. **tests/unit/test_zero_sales.py** - בדיקות יחידה
2. **tests/integration/test_bid_flow.py** - בדיקות אינטגרציה
3. **tests/fixtures/valid_template.xlsx** - קובץ דוגמה
4. **tests/fixtures/valid_bulk_60.xlsx** - קובץ דוגמה

### בדיקות למשתמש:
- תהליך מלא על קובץ 10,000 שורות
- השוואת תוצאות לחישוב ידני
- בדיקת קבצים פגומים וטיפול בשגיאות

### בדיקות למתכנת:
- pytest --cov מראה 80%+ כיסוי
- test_bid_flow עובר מקצה לקצה
- test_error_handling בודק כל סוגי השגיאות

### מה נראה בסוף השלב:
- מערכת יציבה ועובדת
- כל הבדיקות עוברות
- ביצועים בטווח המוגדר

### קבצים לנעילה:
- כל קבצי הבדיקות

---

## שלב 10: תיעוד ומסירה
**משך: 1 יום | קבצים: 2**

### קבצי קוד לכתיבה:
1. **README.md** - תיעוד למפתח
2. **app/state/mock_data.py** - נתוני דוגמה לבדיקות

### בדיקות למשתמש:
- הרצה על קבצים אמיתיים מ-Amazon
- וידוא קובץ נפתח ב-Excel נכון
- בדיקת העלאה חזרה ל-Amazon

### בדיקות למתכנת:
- README מכיל הוראות התקנה מלאות
- mock_data יוצר קבצי בדיקה תקינים
- כל התלויות ב-requirements.txt

### מה נראה בסוף השלב:
- מערכת מוכנה לשימוש
- תיעוד מלא
- קבצי דוגמה

### קבצים לנעילה:
- README.md

---

## סיכום

### סה"כ קבצים: 45
- **שלב 1:** 8 קבצים
- **שלב 2:** 3 קבצים
- **שלב 3:** 7 קבצים
- **שלב 4:** 3 קבצים
- **שלב 5:** 5 קבצים
- **שלב 6:** 4 קבצים
- **שלב 7:** 5 קבצים
- **שלב 8:** 4 קבצים
- **שלב 9:** 4 קבצים
- **שלב 10:** 2 קבצים

### זמן כולל: 19 ימי עבודה

### קבצים קריטיים לנעילה מוקדמת:
1. business/common/excluded_portfolios.py (10 הפורטפוליוז)
2. config/constants.py (קבועי המערכת)
3. business/bid_optimizations/zero_sales/* (הלוגיקה העסקית)

### הערות חשובות:
- אין Stepper - רק Sidebar Navigation
- כל אופטימיזציה מבצעת validation וcleaning עצמאיים
- צביעה ורודה רק בקובץ Excel, לא ב-UI
- רק Zero Sales פעיל ב-Phase 1
- בדיקות בכל שלב מבטיחות איכות