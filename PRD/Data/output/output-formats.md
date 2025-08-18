# פורמטי קבצי פלט
**נתיב:** `PRD/Data/output/output-formats.md`

## סקירה כללית

המערכת מייצרת קבצי Excel מעודכנים מוכנים להעלאה חזרה ל-Amazon. כרגע המערכת מייצרת רק Working File עם עמודות עזר לניתוח.

## סוגי קבצי פלט

### 1. Working File (פעיל)
- **מטרה:** קובץ עבודה עם מידע מלא לניתוח
- **כולל:** 48 עמודות מקוריות + 7 עמודות עזר
- **סטטוס:** מיושם ופעיל

### 2. Clean File (TBC)
- **מטרה:** קובץ נקי להעלאה ישירה ל-Amazon
- **כולל:** רק 48 העמודות המקוריות
- **סטטוס:** TBC - לפיתוח עתידי

## מבנה Working File

### מוסכמות שם קובץ
```
Auto Optimized Bulk | Working | YYYY-MM-DD | HH-MM.xlsx
```

#### דוגמאות
- `Auto Optimized Bulk | Working | 2025-08-18 | 14-30.xlsx`
- `Auto Optimized Bulk | Working | 2025-12-31 | 09-15.xlsx`

### לשוניות בקובץ (Zero Sales)

#### לשונית 1: Targeting
**תוכן:** Keywords + Product Targeting שעברו אופטימיזציה

**מבנה עמודות:**
1. עמודות 1-27: המקוריות מה-Bulk
2. **עמודות עזר (28-34):**
   - Old Bid - הערך המקורי של Bid
   - calc1 - חישוב ביניים ראשון
   - calc2 - חישוב ביניים שני
   - Target CPA - מה-Template
   - Base Bid - מה-Template
   - Adj. CPA - CPA מותאם
   - Max BA - ערך Percentage מקסימלי
3. עמודה 35: Bid (המעודכן)
4. עמודות 36-55: שאר העמודות המקוריות (29-48)

#### לשונית 2: Bidding Adjustment
**תוכן:** שורות Bidding Adjustment ללא שינוי

**מבנה עמודות:**
- 48 העמודות המקוריות בלבד
- ללא עמודות עזר
- Operation נשאר כמו במקור

## עמודות העזר - פירוט

### Old Bid
- **מקור:** ערך Bid המקורי מה-Bulk
- **סוג:** Number
- **מטרה:** השוואה לפני/אחרי

### calc1
- **חישוב:** (Clicks + 1) / Units × Target CPA
- **סוג:** Number
- **מטרה:** חישוב ביניים לנוסחה

### calc2
- **חישוב:** calc1 × Adj. CPA
- **סוג:** Number
- **מטרה:** חישוב ביניים לנוסחה

### Target CPA
- **מקור:** מה-Template או ריק
- **סוג:** Number או null
- **מטרה:** פרמטר לחישוב

### Base Bid
- **מקור:** מה-Template
- **סוג:** Number
- **מטרה:** הצעת בסיס

### Adj. CPA
- **חישוב:** Target CPA × 0.5 (אם יש "up and" בשם) או Target CPA
- **סוג:** Number
- **מטרה:** CPA מותאם

### Max BA
- **חישוב:** MAX(Percentage) לפי Campaign ID
- **סוג:** Number
- **מטרה:** מגבלת Bidding Adjustment

## סימון שורות בעייתיות

### צבע ורוד (FFE4E1)
המערכת צובעת שורות בורוד במקרים הבאים:

1. **Bid < 0.02** - מתחת למינימום
2. **Bid > 1.25** - מעל למקסימום
3. **Clicks > 15** - הרבה קליקים ללא מכירות
4. **שגיאת חישוב** - NaN או null ב-Bid

### יישום הצבע
- **טכנולוגיה:** openpyxl PatternFill
- **צבע:** FFE4E1 (ורוד בהיר)
- **היקף:** כל השורה (48 עמודות + עזר)

## שדה Operation

### כלל מרכזי
**כל השורות** בפלט מקבלות Operation = "Update"

### למה?
- Amazon דורש Operation תקין
- Update מאפשר עדכון ערכים קיימים
- פשוט ואחיד לכל השורות

## סטטיסטיקות בקובץ

### מידע שנשמר בקובץ (Properties)
- תאריך יצירה
- מספר שורות מקורי
- מספר שורות מעובדות
- מספר שורות עם שגיאות
- סוג אופטימיזציה (Zero Sales)

## גודל קובץ צפוי

| שורות מקוריות | גודל משוער | זמן יצירה |
|---------------|------------|-----------|
| עד 10,000 | 2-5 MB | 1-2 שניות |
| 10,000-50,000 | 5-15 MB | 3-5 שניות |
| 50,000-200,000 | 15-30 MB | 5-10 שניות |
| 200,000-500,000 | 30-50 MB | 10-20 שניות |

## תאימות

### Excel Versions
- Excel 2016 ומעלה
- Excel 365
- Google Sheets (עם המרה)
- LibreOffice Calc

### Amazon Bulk Upload
- תואם 100% לפורמט Amazon
- ניתן להעלאה ישירה (אחרי בדיקה ידנית)

## הודעות למשתמש

### הודעת הצלחה
```
✓ File generated successfully
  - Working File: {filename}
  - Size: {size} MB
  - Processed: {rows} rows
  - Pink rows: {errors} rows
```

### הודעת שגיאה
```
❌ Failed to generate output file
  - Error: {error_message}
  - Please try again
```

## הערות חשובות

1. **Working File בלבד:** כרגע אין Clean File
2. **לשוניות נפרדות:** Targeting ו-Bidding Adjustment
3. **צבע ורוד:** לזיהוי מהיר של בעיות
4. **Operation = Update:** תמיד, לכל השורות
5. **עמודות עזר:** רק ב-Targeting, לא ב-Bidding Adjustment

---

**עדכון אחרון:** 18 באוגוסט 2025, 12:45