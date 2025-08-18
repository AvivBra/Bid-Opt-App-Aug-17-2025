# אופטימיזציית Zero Sales - לוגיקה

## סקירה כללית
אופטימיזציית Zero Sales מזהה מילות מפתח ומוצרים ללא מכירות (Units = 0) ומתאימה את הבידים שלהם כדי להפחית בזבוז תקציב תוך שמירה על נראות.

## קבצים נדרשים
- **קובץ Template:** לשונית Port Values (Portfolio Name, Base Bid, Target CPA)
- **קובץ Bulk 60:** נתוני קמפיינים מ-60 ימים עם 48 עמודות

## תהליך העיבוד

### שלב 1: חלוקה ראשונית של הנתונים
הפרדת נתוני Bulk לפי סוג Entity:
- **לשונית Targeting:** Keyword + Product Targeting (יעברו ניקוי ועיבוד)
- **לשונית Bidding Adjustment:** שורות Bidding Adjustment (נשארות כמו שהן, ללא ניקוי)

הערה: Product Ad לא נכלל באופטימיזציה זו.

### שלב 2: ניקוי נתונים (רק בלשונית Targeting)
החלת סינונים על לשונית Targeting:
1. השארת שורות עם Units = 0 בלבד
2. הסרת שורות מ-10 הפורטפוליוז המוחרגים:
   - Flat 30, Flat 25, Flat 40
   - Flat 25 | Opt, Flat 30 | Opt  
   - Flat 20, Flat 15
   - Flat 40 | Opt, Flat 20 | Opt, Flat 15 | Opt
3. הסרת שורות מפורטפוליוז המסומנים "Ignore" ב-Template

### שלב 3: הוספת עמודות עזר
הוספת 7 עמודות עזר משמאל לעמודת Bid (רק בלשונית Targeting):
1. **Max BA:** ערך Percentage מקסימלי עבור ה-Campaign ID מנתוני Bidding Adjustment
2. **Base Bid:** ערך מה-Template עבור הפורטפוליו
3. **Target CPA:** ערך מה-Template עבור הפורטפוליו  
4. **Adj. CPA:** Target CPA × (1 + Max BA/100)
5. **calc1:** חישוב ביניים (ראה שלב 4)
6. **calc2:** חישוב ביניים (ראה שלב 4)
7. **Old Bid:** ערך Bid המקורי לפני השינויים

### שלב 4: חישוב Bid חדש
החלת אחד מארבעה מקרי חישוב לפי Target CPA ושם הקמפיין:

#### Case A: Target CPA ריק + שם הקמפיין מכיל "up and"
- Bid חדש = Base Bid × 0.5

#### Case B: Target CPA ריק + שם הקמפיין לא מכיל "up and"  
- Bid חדש = Base Bid

#### Case C: Target CPA קיים + שם הקמפיין מכיל "up and"
1. calc1 = Adj. CPA × 0.5 / (Clicks + 1)
2. calc2 = calc1 - (Base Bid × 0.5)
3. אם calc1 ≤ 0: Bid חדש = calc2
4. אחרת: Bid חדש = Base Bid × 0.5

#### Case D: Target CPA קיים + שם הקמפיין לא מכיל "up and"
1. calc1 = Adj. CPA / (Clicks + 1)
2. calc2 = calc1 - (Base Bid / (1 + Max BA / 100))
3. אם calc1 ≤ 0: Bid חדש = calc2
4. אחרת: Bid חדש = Base Bid / (1 + Max BA / 100)

### שלב 5: עיבוד סופי
1. הגדרת Operation = "Update" לכל השורות בשתי הלשוניות
2. עיגול כל ערכי Bid ל-3 ספרות אחרי הנקודה
3. סימון שורות בורוד אם:
   - Bid < 0.02 (מתחת למינימום)
   - Bid > 1.25 (מעל למקסימום)
   - Clicks > 15 (קליקים רבים ללא מכירות)
   - חישוב Bid נכשל (NaN)

## מבנה הפלט

### Working File בלבד (אין Clean File בשלב הנוכחי)
**שם קובץ:** Auto Optimized Bulk | Working | YYYY-MM-DD | HH-MM.xlsx

**לשוניות:**
1. **Targeting:** Keywords + Product Targeting עם כל 48 העמודות + 7 עמודות עזר
2. **Bidding Adjustment:** שורות Bidding Adjustment עם 48 עמודות בלבד (ללא עמודות עזר)

## טיפול בשגיאות

### שגיאות ולידציה (עוצרות עיבוד)
- קבצים נדרשים חסרים
- פורטפוליוז חסרים ב-Template (שאינם ברשימת המוחרגים)
- אין שורות עם Units = 0
- כל הפורטפוליוז מסומנים כ-Ignore

### אזהרות חישוב (ממשיכות עיבוד)
- Bid מתחת למינימום (סימון ורוד)
- Bid מעל למקסימום (סימון ורוד)
- קליקים רבים ללא מכירות (סימון ורוד)
- שגיאות חישוב (סימון ורוד)

## יעדי ביצועים
- קבצים עד 40MB
- עד 500,000 שורות
- זמן עיבוד < 60 שניות לגודל קובץ מקסימלי

## חוקים עסקיים מרכזיים
1. תמיד להוסיף 1 ל-Clicks למניעת חלוקה באפס
2. אם פורטפוליו לא נמצא ב-Template במהלך העיבוד: עצירה ובקשת Template חדש
3. שורות Bidding Adjustment לעולם לא מסוננות או משתנות (מלבד Operation = "Update")
4. עמודות עזר מתווספות רק ללשונית Targeting
5. הטקסט "up and" בשם הקמפיין מפעיל אסטרטגיית הפחתת bid שונה