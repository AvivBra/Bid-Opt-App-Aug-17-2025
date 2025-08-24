# סקירת ארכיטקטורת Bid Optimizer

## עקרונות ארכיטקטוניים

### ארכיטקטורת 3 שכבות
המערכת בנויה על ארכיטקטורת 3 שכבות מופרדות לחלוטין, כאשר כל שכבה אחראית לתחום ספציפי ואין תלות ישירה בין שכבות לא סמוכות.

### הפרדת אחריות
• **UI Layer:** ממשק משתמש בלבד, ללא לוגיקה עסקית
• **Business Layer:** לוגיקה עסקית וחישובים, ללא תלות ב-UI
• **Data Layer:** קריאה וכתיבת קבצים, ללא לוגיקה עסקית

### אופטימיזציות עצמאיות
כל אופטימיזציה היא מודול עצמאי שמבצע וולידציה וניקוי פנימיים. אין וולידציה גלובלית או ניקוי גלובלי. זה מאפשר הוספת אופטימיזציות חדשות בקלות.

## שכבת UI - ממשק משתמש

### רכיבים עיקריים

**Sidebar Navigation:**
• רוחב קבוע 200px
• 2 עמודים: Bid Optimizer (פעיל), Campaigns Optimizer (TBC)
• צבע רקע: #171717
• ללא Stepper - ניווט ישיר בין עמודים

**Main Content Area:**
• רוחב מקסימלי 800px, ממורכז
• רקע: #0A0A0A
• מכיל את הפאנלים: Upload, Validation, Output

**Shared Components:**
• Buttons - רוחב 200px, גובה 44px
• Checkboxes - רק Zero Sales מוצג
• Progress bars - צבע ויולט #8B5CF6
• Alerts - רקע #404040, נקודות צבעוניות

### מבנה קבצים
```
app/
├── main.py - נקודת כניסה
├── navigation.py - ניהול Sidebar
├── pages/
│   └── bid_optimizer.py - עמוד ראשי
└── ui/
    ├── shared/ - פאנלים משותפים
    └── components/ - רכיבי UI
```

### State Management
• שימוש ב-Streamlit Session State
• שמירת קבצים שהועלו בזיכרון
• מעבר בין מצבים: Upload → Validation → Processing → Output

## שכבת Business - לוגיקה עסקית

### מבנה האופטימיזציות

**Base Optimization Class:**
• מחלקת אב לכל האופטימיזציות
• מתודות חובה: validate(), clean(), process()
• כל אופטימיזציה יורשת וממשת

**Zero Sales Optimization:**
• וולידציה: בדיקת Units, Clicks, Portfolio columns
• ניקוי: סינון Units=0, הסרת Flat portfolios, הסרת Ignore
• עיבוד: חישוב Bid לפי 4 מקרים
• פלט: 3 DataFrames (Targeting, Bidding Adjustment, Product Ad)

### מבנה קבצים
```
business/
├── common/
│   ├── portfolio_filter.py - סינון Flat portfolios
│   └── excluded_portfolios.py - רשימת 10 הפורטפוליוז
├── bid_optimizations/
│   ├── base_optimization.py - מחלקת בסיס
│   └── zero_sales/
│       ├── validator.py - וולידציה ספציפית
│       ├── cleaner.py - ניקוי וסינון
│       └── processor.py - חישובי Bid
└── processors/
    └── output_formatter.py - פורמט פלט
```

### עקרון העצמאות
• כל אופטימיזציה מקבלת DataFrames גולמיים
• מבצעת וולידציה וניקוי עצמאיים
• לא תלויה באופטימיזציות אחרות
• מחזירה תוצאות מוכנות לכתיבה

## שכבת Data - ניהול נתונים

### קריאת קבצים

**Template Reader:**
• קורא 2 לשוניות: Port Values, Top ASINs
• מאמת מבנה 3 עמודות
• בודק Portfolio Names כפולים

**Bulk Reader:**
• קורא Sheet "Sponsored Products Campaigns"
• מאמת 48 עמודות בדיוק
• תומך ב-CSV ו-Excel
• מטפל בקבצים עד 40MB

### כתיבת קבצים

**Working File Writer:**
• יוצר Excel עם 2 לשוניות
• מוסיף 7 עמודות עזר ל-Targeting
• צובע שורות בעייתיות בורוד (#FFE4E1)
• שומר עם timestamp בשם

### מבנה קבצים
```
data/
├── readers/
│   ├── excel_reader.py - קריאת Excel
│   └── csv_reader.py - קריאת CSV
├── writers/
│   └── excel_writer.py - כתיבת Working File
├── validators/
│   ├── template_validator.py - בדיקת Template
│   └── bulk_validator.py - בדיקת Bulk
└── template_generator.py - יצירת Template ריק
```

## זרימת נתונים

### תהליך מלא
1. **Upload:** משתמש מעלה Template + Bulk 60
2. **Storage:** קבצים נשמרים ב-Session State
3. **Validation Display:** הצגת תוצאות בדיקת התאמה
4. **User Action:** לחיצה על Process Files
5. **Optimization:** Zero Sales מקבל את ה-DataFrames
6. **Internal Validation:** בדיקות בתוך האופטימיזציה
7. **Internal Cleaning:** סינון וניקוי נתונים
8. **Processing:** חישוב Bid חדש
9. **Output Generation:** יצירת Working File
10. **Download:** משתמש מוריד את הקובץ

### תקשורת בין שכבות
• UI → Business: דרך Orchestrator בלבד
• Business → Data: קריאות ישירות ל-readers/writers
• Data → Business: החזרת DataFrames או Exceptions
• אסור: UI → Data ישירות

## ניהול שגיאות

### היררכיית Exceptions
• **FileError:** בעיות קריאה/כתיבה
• **ValidationError:** נתונים לא תקינים
• **ProcessingError:** כשל בחישובים
• **TimeoutError:** חריגה מזמן מקסימלי

### טיפול בשגיאות
• כל שכבה תופסת את השגיאות שלה
• מעבירה למעלה עם הקשר
• UI מציג הודעות ידידותיות למשתמש
• אפשרות Retry או Reset

## ביצועים

### אופטימיזציות
• קריאת קבצים בחלקים (chunks) מעל 20MB
• שימוש ב-vectorized operations ב-pandas
• מניעת העתקות מיותרות של DataFrames
• ניקוי זיכרון אחרי כל אופטימיזציה

### מגבלות
• זיכרון מקסימלי: 4GB
• זמן עיבוד מקסימלי: 5 דקות
• גודל קובץ מקסימלי: 40MB
• מספר שורות מקסימלי: 500,000

## הרחבות עתידיות

### Phase 2-3: אופטימיזציות נוספות
• 13 אופטימיזציות חדשות
• כל אחת תירש מ-BaseOptimization
• תוסיף validate(), clean(), process() משלה
• ללא שינוי בארכיטקטורה

### Phase 4-6: Campaigns Optimizer
• עמוד חדש ב-Sidebar
• Negation ו-Harvesting
• אותה ארכיטקטורת 3 שכבות
• שימוש חוזר ברכיבי UI

### אינטגרציות
• Data Rova API - benchmarking data
• Cloud storage - שמירת תוצאות
• Scheduling - הרצות אוטומטיות

## סביבת פיתוח

### טכנולוגיות
• **Python 3.8+** - שפת תכנות
• **Streamlit** - ממשק משתמש
• **pandas** - עיבוד נתונים
• **openpyxl** - קבצי Excel
• **pytest** - בדיקות

### מבנה פרויקט
```
bid-optimizer/
├── app/ - קוד UI
├── business/ - לוגיקה עסקית
├── data/ - ניהול נתונים
├── config/ - הגדרות
├── utils/ - פונקציות עזר
└── tests/ - בדיקות
```

## נקודות מפתח

• **Sidebar במקום Stepper** - ניווט ישיר בין עמודים
• **אופטימיזציות עצמאיות** - כל אחת מנהלת את עצמה
• **אין וולידציה גלובלית** - כל אופטימיזציה בודקת מה שהיא צריכה
• **10 Flat Portfolios** - תמיד מסוננים
• **צביעה ורודה רק ב-Excel** - לא ב-UI
• **Working File בלבד** - Clean File הוא TBC