# מפרט קבצי פלט - Bid Optimizer

## 1. סקירה כללית

### 2 סוגי קבצים
1. **Working File** - כולל עמודות עזר לבדיקה
2. **Clean File** - נתונים נקיים לטעינה ב-Amazon

### מאפיינים משותפים
- פורמט: Excel (.xlsx)
- קידוד: UTF-8
- לשונית לכל אופטימיזציה
- Operation="Update" בכל השורות

## 2. מבנה שמות קבצים

### פורמט
```
Auto Optimized Bulk | {Type} | {Date} | {Time}.xlsx
```

### פרמטרים
- **Type**: "Working" או "Clean"
- **Date**: YYYY-MM-DD
- **Time**: HH-MM (24 שעות)

### דוגמאות
```
Auto Optimized Bulk | Working | 2024-01-15 | 14-30.xlsx
Auto Optimized Bulk | Clean | 2024-01-15 | 14-30.xlsx
```

## 3. Working File

### מטרה
קובץ לבדיקה וניתוח עם כל המידע

### מבנה לשוניות
```
Working Zero Sales
Working Portfolio Bid  
Working Budget Optimization
[לשונית לכל אופטימיזציה שרצה]
```

### תוכן לשונית
- 48 העמודות המקוריות
- עמודות עזר משמאל לעמודת Bid
- כל השורות שעובדו
- סימון שורות בעייתיות

### עמודות עזר (Zero Sales)
| עמודה | תיאור |
|-------|--------|
| Old Bid | ערך Bid מקורי |
| calc1 | חישוב ביניים 1 |
| calc2 | חישוב ביניים 2 |
| Target CPA | מהTemplate |
| Base Bid | מהTemplate |
| Adj. CPA | CPA מתואם |
| Max BA | Bidding Adjustment מקסימלי |

## 4. Clean File

### מטרה
קובץ נקי לטעינה חזרה ב-Amazon

### מבנה לשוניות
```
Clean Zero Sales
Clean Portfolio Bid
Clean Budget Optimization
[לשונית לכל אופטימיזציה שרצה]
```

### תוכן לשונית
- רק 48 העמודות המקוריות
- ללא עמודות עזר
- Operation="Update" בכל השורות
- ערכי Bid מעודכנים

## 5. סדר עמודות

### 48 עמודות (זהה למקור)
```
1. Product
2. Entity
3. Operation (תמיד "Update")
4. Campaign ID
5. Ad Group ID
...
28. Bid (ערך מעודכן)
...
48. ROAS
```

## 6. לשוניות נוספות

### העתקה מהמקור
אם קיימות לשוניות נוספות בקבצי המקור:
- "Portfolios" 
- לשוניות אחרות

הן יועתקו כמו שהן לשני קבצי הפלט.

## 7. סימון שורות בעייתיות

### Working File בלבד
שורות עם בעיות מסומנות בצבע:
- **ורוד**: Bid < 0.02 או > 1.25
- **אדום**: שגיאת חישוב
- **כתום**: אזהרה

### מידע נוסף
הודעה מסכמת על מספר השורות הבעייתיות

## 8. פורמט נתונים

### מספרים
- **IDs**: טקסט (למניעת scientific notation)
- **Bid**: 3 ספרות אחרי הנקודה (0.000)
- **Budget**: 2 ספרות אחרי הנקודה (0.00)

### תאריכים
- פורמט: MM/DD/YYYY
- דוגמה: 01/15/2024

### טקסט
- UTF-8
- שמירת תווים מיוחדים

## 9. גודל קבצים

### יחס לקובץ מקור
- Working: ~1.5x (עמודות נוספות)
- Clean: ~1x (אותו גודל)

### ביצועים
- יצירה: < 5 שניות ל-100K שורות
- הורדה: תלוי בחיבור

## 10. ולידציות פלט

### בדיקות Working File
1. כל העמודות קיימות
2. עמודות עזר במקום הנכון
3. Operation="Update"
4. ערכי Bid בטווח

### בדיקות Clean File
1. רק 48 עמודות
2. סדר עמודות נכון
3. Operation="Update"
4. ניתן לטעינה ב-Amazon

## 11. מקרי קצה

### אין שורות לעיבוד
- לשונית עם headers בלבד
- הודעה: "No rows to process"

### כל השורות עם שגיאות
- הקובץ נוצר עם הערכים המקוריים
- הודעה על השגיאות

### אופטימיזציה נכשלה
- לא נוצרת לשונית
- הודעה על הכישלון

## 12. דוגמה - Zero Sales Output

### Working File
```
[48 columns] | Old Bid | calc1 | calc2 | Target CPA | Base Bid | Adj. CPA | Max BA
...          | 2.00    | 0.45  | -0.55 | 5.00       | 1.00     | 5.05     | 1
Operation="Update", Bid=1.00
```

### Clean File
```
[48 columns only]
Operation="Update", Bid=1.00
```