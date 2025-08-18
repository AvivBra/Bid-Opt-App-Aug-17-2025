# FAQ למפתחים - Bid Optimizer

**תאריך:** 18 באוגוסט 2025, 12:45 (שעון ישראל)  
**אל:** צוות הפיתוח  
**מאת:** מנהל האיפיון  

---

## 1. איך לצבוע שורות בורוד ב-Excel עם openpyxl?

### תשובה: שתי אפשרויות

#### אפשרות א' - צביעה ישירה (מומלץ)
השתמשו ב-PatternFill עם הצבע FFE4E1 (ורוד בהיר) והחילו על התאים הרלוונטיים.

#### אפשרות ב' - Conditional Formatting
השתמשו ב-CellIsRule עם תנאים lessThan/greaterThan והחילו את אותו PatternFill.

**המלצה:** השתמשו באפשרות א' (צביעה ישירה) כי:
- פשוט יותר למימוש
- ביצועים טובים יותר
- תומך בתנאים מורכבים (NaN, שגיאות חישוב)

---

## 2. מה ההבדל בין Working File ל-Clean File?

### בשלב הנוכחי (Zero Sales בלבד)
- **Working File:** כולל 7 עמודות עזר (Old Bid, calc1, calc2, Target CPA, Base Bid, Adj. CPA, Max BA)
- **Clean File:** TBC - לא מיושם כרגע, יתווסף בעתיד

### בעתיד (TBC)
- **Working File:** יכלול עמודות עזר לניתוח
- **Clean File:** רק 48 העמודות המקוריות להעלאה ל-Amazon

---

## 3. איפה להוסיף את 7 עמודות העזר?

**מיקום:** משמאל לעמודת Bid (עמודה 28)

**סדר העמודות אחרי הוספה:**
- עמודות 1-27: המקוריות
- עמודות 28-34: עמודות עזר (Old Bid, calc1, calc2, Target CPA, Base Bid, Adj. CPA, Max BA)
- עמודה 35: Bid (המקורית עמודה 28)
- עמודות 36-55: שאר העמודות המקוריות (29-48)

---

## 4. איך מטפלים ב-Bidding Adjustment?

### העיקרון
שורות עם `Entity = "Bidding Adjustment"` **לא עוברות אופטימיזציה**

### מה כן קורה להן
1. מופרדות בתחילת התהליך
2. Operation נשאר כמו בקובץ המקורי (לא משתנה)
3. עוברות ללשונית נפרדת בפלט
4. **לא מקבלות** עמודות עזר

---

## 5. מה קורה כשאין עמודת Percentage?

### לחישוב Max BA
- **הודעת שגיאה:** "Percentage column missing - cannot calculate Max BA"
- **התנהגות:** המערכת עוצרת את העיבוד
- **פתרון:** המשתמש צריך להעלות קובץ Bulk חדש עם כל 48 העמודות הנדרשות

---

## 6. איך בוחרים איזה Bulk להשתמש?

### כרגע (Zero Sales)
**תמיד Bulk 60**

### בעתיד (TBC)
יוגדר לפי סוג האופטימיזציה

---

## 7. מה הסטטוס של עמודות Informational?

### עמודות 12, 13, 14, 19, 20, 24, 25, 27, 37
- **לא משתתפות בחישובים**
- **כן נשמרות בפלט**
- **אסור למחוק אותן**

### רשימת העמודות
- Campaign Name (Informational only) - עמודה 12
- Ad Group Name (Informational only) - עמודה 13
- Portfolio Name (Informational only) - עמודה 14
- Campaign State (Informational only) - עמודה 19
- Ad Group State (Informational only) - עמודה 20
- Eligibility Status (Informational only) - עמודה 24
- Reason for Ineligibility (Informational only) - עמודה 25
- Ad Group Default Bid (Informational only) - עמודה 27
- Resolved Product Targeting Expression (Informational only) - עמודה 37

---

## 8. מהי רשימת 10 ה-Flat Portfolios?

### הרשימה המלאה (Case Sensitive!)
```python
EXCLUDED_PORTFOLIOS = [
    "Flat 30",
    "Flat 25", 
    "Flat 40",
    "Flat 25 | Opt",
    "Flat 30 | Opt",
    "Flat 20",
    "Flat 15",
    "Flat 40 | Opt",
    "Flat 20 | Opt",
    "Flat 15 | Opt"
]
```

### איך לסנן
```python
# סינון פורטפוליוז מוחרגים
filtered_df = df[~df['Portfolio Name (Informational only)'].isin(EXCLUDED_PORTFOLIOS)]
```

---

## 9. מה המבנה של קובץ הפלט?

### שם הקובץ
```
Auto Optimized Bulk | Working | YYYY-MM-DD | HH-MM.xlsx
```

### לשוניות ב-Working File (Zero Sales)
1. **"Targeting"** - Keywords + Product Targeting עם עמודות עזר
2. **"Bidding Adjustment"** - שורות Bidding Adjustment בלי עמודות עזר

---

## 10. איך מטפלים בשגיאות חישוב?

### זיהוי וסימון
```python
import numpy as np
import pandas as pd

# בדיקת שגיאות חישוב
if pd.isna(bid_value) or np.isnan(bid_value) or bid_value < 0:
    # סמן בורוד
    for col in range(1, 49):
        ws.cell(row=row_num, column=col).fill = pink_fill
    
    # רשום בלוג
    error_count += 1
    
# הודעה מסכמת
print(f"Pink Notice: {error_count} calculation errors marked")
```

---

## טיפים חשובים

### 1. ביצועים
- קבצים עד 500K שורות
- זמן עיבוד מקסימלי: 60 שניות
- השתמשו ב-chunking לקבצים גדולים

### 2. Operation Field
- **תמיד** הגדירו ל-"Update" בכל השורות בפלט
- גם ב-Bidding Adjustment שלא השתנה

### 3. Target CPA
- יכול להיות ריק (None/NaN)
- אם ריק, השתמשו רק ב-Base Bid

### 4. Python ו-Streamlit
- Python 3.8+
- Streamlit לממשק
- pandas לעיבוד נתונים
- openpyxl לקבצי Excel

---

**בהצלחה בפיתוח!**