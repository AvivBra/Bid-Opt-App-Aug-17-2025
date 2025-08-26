# איפיון תהליך וולידציה
**תאריך:** 26.08.2025  
**שעה:** 18:20

## Session State - טבלת נתונים

המערכת בונה טבלה ב-session state עם העמודות הבאות:

| עמודה | מקור הנתונים | תיאור |
|-------|---------------|--------|
| **target** | Data Dive | כל ה-Keywords וכל ה-ASINs מ-Data Dive, כל אחד בשורה נפרדת |
| **ASIN** | Template | מהטמפלט |
| **Product Type** | Template | מהטמפלט |
| **Niche** | Template | מהטמפלט |
| **Campaign type** | Checkboxes | מה-checkboxes שהמשתמש סימן |
| **Bid** | Template | לפי סוג הקמפיין מהטמפלט |
| **kw cvr** | Data Rova | ערך מעמודת "Keyword Conversion" ב-Data Rova עבור המילה המתאימה |
| **kw sales** | Data Rova | ערך מעמודת "Keyword Monthly Sales" ב-Data Rova עבור המילה המתאימה |

### מבנה השורות
כל שורה בטבלה מייצגת צירוף ייחודי של:
- **Target** - Keyword או ASIN
- **ASIN** 
- **Campaign Type**

## תהליך הוולידציה

### זרימת התהליך
1. המשתמש מעלה קבצים
2. לוחץ Process
3. המערכת יוצרת את ה-Session State

### שלבי עיבוד

#### 1. מחיקת כפילויות
מחיקת שורות כפולות אם קיימות

#### 2. בדיקת Keywords חסרים
אם יש Keywords שמופיעים ב-Data Dive ולא ב-Data Rova, או אם לא הועלה Data Rova כלל:

**הודעה למשתמש:**
```
The following keywords are missing DR info:
[keywords list]
```

**תצוגת המילים החסרות:**
- כל מילת מפתח בשורה נפרדת
- עד 500 מילים
- תצוגה בתיבה קומפקטית ואסתטית
- אפשרות קלה להעתיק את כל המילים לקליפבורד

**אפשרויות המשך:**
- המשתמש יכול להעלות מחדש קובץ Data Rova
- המערכת משלימה את הנתונים החסרים
- מציגה שוב אם עדיין חסרים נתונים
- התהליך חוזר בלולאה עד שהמשתמש לוחץ Process שוב

#### 3. עיבוד סופי
כשהמשתמש לוחץ Process שוב, המערכת מעבדת:
- רק את ה-Keywords שיש עליהם מידע מ-Data Rova
- **פלוס** כל ה-Targets שהם ASINs של מתחרים מקבצי Data Dive

## וולידציה של התאמה בין Checkboxes למידע ב-Session State

### קמפיינים הדורשים מידע על Keywords

הקמפיינים הבאים **חייבים** מידע על מילות מפתח מ-Data Rova:
- Testing
- Phrase
- Broad
- Halloween Testing
- Halloween Phrase
- Halloween Broad

**תנאי שגיאה:**
- אם מסומן אחד מהקמפיינים הללו
- ואף מילת מפתח מ-Data Dive לא כוללת מידע מ-Data Rova
- והמשתמש לוחץ לעיבוד בפעם השנייה בלי להעלות Data Rova

**הודעת שגיאה:**
```
Can't create [campaign names by the relevant checkboxes] with no DR keywords info
```

### קמפיינים של Product Targeting בלבד

הקמפיינים הבאים צריכים **רק** Product Targeting:
- Testing PT
- Expanded
- Halloween Testing PT
- Halloween Expanded

**תנאי עיבוד:**
- אם רק אלו מסומנים - מספיק קובץ Data Dive בלבד
- לא צריך להציג רשימת מילים חסרות מ-Data Rova
- ניתן לבצע עיבוד ללא קובץ Data Rova