# מפרט אופטימיזציית Zero Sales

## 1. סקירה כללית

### מטרה
אופטימיזציית Zero Sales מזהה מוצרים/מילות מפתח שלא הניבו מכירות ומפחיתה את הבידים שלהם כדי לחסוך בעלויות.

### קבצים נדרשים
- Template (חובה)
- Bulk 60 (חובה)

### תוצאה
עדכון ערכי Bid עבור פריטים עם 0 מכירות ב-60 הימים האחרונים.

## 2. תהליך האופטימיזציה

### שלב 1: ולידציה
1. בדיקת קיום הקבצים הנדרשים
2. בדיקת מבנה Template (3 עמודות, לשונית Port Values)
3. בדיקת מבנה Bulk 60 (48 עמודות)
4. בדיקת עמודות קריטיות: Units, Clicks, Portfolio Name
5. השוואת פורטפוליוז בין Template ל-Bulk

### שלב 2: ניקוי נתונים
```
סינון שורות שעונות על כל התנאים:
- Units = 0 (אין מכירות)
- Entity IN ('Keyword', 'Product Targeting', 'Product Ad', 'Bidding Adjustment')
- State = 'enabled'
- Portfolio Name NOT IN (רשימת Flat portfolios)
```

### רשימת Flat Portfolios להתעלמות
```
Flat 30, Flat 25, Flat 40, Flat 25 | Opt,
Flat 30 | Opt, Flat 20, Flat 15,
Flat 40 | Opt, Flat 20 | Opt, Flat 15 | Opt
```

### שלב 3: חלוקה ללשוניות
1. **Targets**: Keyword + Product Targeting
2. **Product Ads**: Product Ad בלבד
3. **Bidding Adjustments**: Bidding Adjustment בלבד

### שלב 4: הוספת עמודות עזר
עמודות נוספות **לפני עמודת Bid** (רק בלשונית Targets):

| עמודה | חישוב |
|-------|--------|
| Old Bid | = Bid (שמירת ערך מקורי) |
| calc1 | ראה נוסחאות למטה |
| calc2 | ראה נוסחאות למטה |
| Target CPA | מ-Template לפי Portfolio Name |
| Base Bid | מ-Template לפי Portfolio Name |
| Adj. CPA | = Target CPA × (1 + Max BA/100) |
| Max BA | ערך מקסימלי מ-Percentage עבור Campaign |

### שלב 5: חישוב Bid חדש

#### מקרה א: ללא Target CPA + יש "up and" בשם
```python
if pd.isna(target_cpa) and "up and" in campaign_name:
    new_bid = base_bid * 0.5
```

#### מקרה ב: ללא Target CPA + אין "up and" בשם
```python
if pd.isna(target_cpa) and "up and" not in campaign_name:
    new_bid = base_bid
```

#### מקרה ג: עם Target CPA + יש "up and" בשם
```python
if not pd.isna(target_cpa) and "up and" in campaign_name:
    calc1 = adj_cpa * 0.5 / (clicks + 1)
    calc2 = calc1 - base_bid * 0.5
    
    if calc1 <= 0:
        new_bid = calc2
    else:
        new_bid = base_bid * 0.5
```

#### מקרה ד: עם Target CPA + אין "up and" בשם
```python
if not pd.isna(target_cpa) and "up and" not in campaign_name:
    calc1 = adj_cpa / (clicks + 1)
    calc2 = calc1 - base_bid
    
    if calc1 <= 0:
        new_bid = calc2
    else:
        new_bid = base_bid
```

### שלב 6: עיגול ותיקון ערכים
```python
# עיגול ל-3 ספרות אחרי הנקודה
new_bid = round(new_bid, 3)

# מינימום 0.02
if new_bid < 0.02:
    new_bid = 0.02
    mark_pink = True  # סימון בורוד

# מקסימום 1.25
if new_bid > 1.25:
    new_bid = 1.25
    mark_pink = True  # סימון בורוד
```

## 3. תוצאות ופלט

### Working File
```
לשונית: "Working Zero Sales"
כולל:
- כל 48 העמודות המקוריות
- 7 עמודות עזר (Old Bid, calc1, calc2, Target CPA, Base Bid, Adj. CPA, Max BA)
- Operation = "Update" לכל השורות
- סימון ורוד לשורות עם בעיות
```

### Clean File
```
לשונית: "Clean Zero Sales"
כולל:
- רק 48 העמודות המקוריות
- Operation = "Update" לכל השורות
- ערכי Bid מעודכנים
```

## 4. הודעות למשתמש

### הודעות ולידציה
```
✅ "All portfolios valid"
❌ "Missing portfolios: {names}"
❌ "Template file is required"
❌ "Bulk 60 file is required"
⚠️ "No Bidding Adjustment rows found"
```

### הודעות עיבוד
```
ℹ️ "Processing {n} rows with zero sales"
⚠️ "{n} rows have Bid below $0.02"
⚠️ "{n} rows have Bid above $1.25"
⚠️ "{n} calculation errors occurred"
✅ "Zero Sales optimization complete"
```

### Pink Notice Box
```
"Please note: {n} rows highlighted due to:
- {x} bids below minimum ($0.02)
- {y} bids above maximum ($1.25)
- {z} calculation errors"
```

## 5. דוגמאות

### דוגמה 1: מוצר ללא מכירות
```
לפני:
Portfolio: Kids-Brand-US
Units: 0, Clicks: 10, Bid: 2.00
Base Bid: 1.25, Target CPA: 5.00

חישוב:
adj_cpa = 5.00 × 1.01 = 5.05
calc1 = 5.05 / (10 + 1) = 0.459
calc2 = 0.459 - 1.25 = -0.791
new_bid = 1.25 (כי calc1 > 0)

אחרי:
Bid: 1.25, Operation: Update
```

### דוגמה 2: מוצר עם "up and" בשם
```
לפני:
Campaign: "Brand up and coming"
Units: 0, Clicks: 5, Bid: 1.50
Base Bid: 1.00, Target CPA: None

חישוב:
new_bid = 1.00 × 0.5 = 0.50

אחרי:
Bid: 0.50, Operation: Update
```

## 6. שיקולי ביצועים

### נפחים צפויים
- 10K-100K שורות ב-Bulk 60
- 10-100 פורטפוליוז
- 10-50% שורות עם Units=0

### זמני עיבוד יעד
- ולידציה: < 2 שניות
- ניקוי: < 3 שניות
- עיבוד: < 5 שניות ל-100K שורות
- סה"כ: < 10 שניות

## 7. בדיקות נדרשות

### בדיקות ולידציה
- קבצים חסרים
- עמודות חסרות
- פורטפוליוז לא תואמים
- ערכי Base Bid לא תקינים

### בדיקות עיבוד
- חישוב נכון לכל 4 המקרים
- עיגול נכון
- טיפול בערכי קצה
- סימון שורות בעייתיות

### בדיקות End-to-End
- העלאת קבצים → ולידציה → עיבוד → הורדה
- בדיקת קובץ הפלט ב-Excel
- בדיקה שניתן לטעון חזרה ל-Amazon