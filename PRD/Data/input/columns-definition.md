# הגדרת 48 העמודות - Bulk Files

## סקירה כללית

קבצי Bulk מ-Amazon מכילים בדיוק 48 עמודות בסדר קבוע. כל עמודה מייצגת מידע ספציפי על קמפיינים, קבוצות מודעות, מילות מפתח ומטריקות ביצועים.

## רשימת העמודות המלאה

### עמודות 1-10: מזהים בסיסיים

| # | שם עמודה | סוג | תיאור | ערכים אפשריים |
|---|----------|-----|--------|----------------|
| 1 | Product | String | סוג המוצר | "Sponsored Products" |
| 2 | Entity | String | סוג הישות | Keyword, Product Targeting, Product Ad, Bidding Adjustment, Campaign, Ad Group |
| 3 | Operation | String | פעולה לביצוע | Create, Update, Delete |
| 4 | Campaign ID | Number | מזהה קמפיין | מספר ייחודי |
| 5 | Ad Group ID | Number | מזהה קבוצת מודעות | מספר ייחודי |
| 6 | Portfolio ID | Number | מזהה פורטפוליו | מספר ייחודי או ריק |
| 7 | Ad ID | Number | מזהה מודעה | מספר ייחודי או ריק |
| 8 | Keyword ID | Number | מזהה מילת מפתח | מספר ייחודי או ריק |
| 9 | Product Targeting ID | Number | מזהה מיקוד מוצר | מספר ייחודי או ריק |
| 10 | Campaign Name | String | שם הקמפיין | טקסט חופשי |

### עמודות 11-20: שמות ומצבים

| # | שם עמודה | סוג | תיאור | Informational? |
|---|----------|-----|--------|---------------|
| 11 | Ad Group Name | String | שם קבוצת המודעות | לא |
| 12 | Campaign Name (Informational only) | String | שם קמפיין למידע | **כן** |
| 13 | Ad Group Name (Informational only) | String | שם קבוצה למידע | **כן** |
| 14 | Portfolio Name (Informational only) | String | שם פורטפוליו למידע | **כן** |
| 15 | Start Date | Date | תאריך התחלה | לא |
| 16 | End Date | Date | תאריך סיום | לא |
| 17 | Targeting Type | String | סוג מיקוד | לא |
| 18 | State | String | מצב פעיל | לא |
| 19 | Campaign State (Informational only) | String | מצב קמפיין למידע | **כן** |
| 20 | Ad Group State (Informational only) | String | מצב קבוצה למידע | **כן** |

### עמודות 21-30: הגדרות והצעות

| # | שם עמודה | סוג | תיאור | Informational? |
|---|----------|-----|--------|---------------|
| 21 | Daily Budget | Number | תקציב יומי | לא |
| 22 | SKU | String | מק"ט | לא |
| 23 | ASIN | String | מזהה מוצר אמזון | לא |
| 24 | Eligibility Status (Informational only) | String | סטטוס זכאות | **כן** |
| 25 | Reason for Ineligibility (Informational only) | String | סיבת אי-זכאות | **כן** |
| 26 | Ad Group Default Bid | Number | הצעת ברירת מחדל | לא |
| 27 | Ad Group Default Bid (Informational only) | Number | הצעת ברירת מחדל למידע | **כן** |
| 28 | Bid | Number | הצעה נוכחית | לא |
| 29 | Keyword Text | String | טקסט מילת מפתח | לא |
| 30 | Native Language Keyword | String | מילת מפתח בשפת מקור | לא |

### עמודות 31-40: הגדרות מתקדמות ומטריקות

| # | שם עמודה | סוג | תיאור | Informational? |
|---|----------|-----|--------|---------------|
| 31 | Native Language Locale | String | קוד שפה | לא |
| 32 | Match Type | String | סוג התאמה | לא |
| 33 | Bidding Strategy | String | אסטרטגיית הצעות | לא |
| 34 | Placement | String | מיקום מודעה | לא |
| 35 | Percentage | Number | אחוז התאמה | לא |
| 36 | Product Targeting Expression | String | ביטוי מיקוד מוצר | לא |
| 37 | Resolved Product Targeting Expression (Informational only) | String | ביטוי מיקוד מפורש | **כן** |
| 38 | Impressions | Number | חשיפות | לא |
| 39 | Clicks | Number | קליקים | לא |
| 40 | Click-through Rate | Number | שיעור הקלקה | לא |

### עמודות 41-48: מטריקות ביצועים

| # | שם עמודה | סוג | תיאור | חישובים |
|---|----------|-----|--------|----------|
| 41 | Spend | Number | הוצאה | לא |
| 42 | Sales | Number | מכירות | לא |
| 43 | Orders | Number | הזמנות | לא |
| 44 | Units | Number | יחידות | **מפתח ל-Zero Sales** |
| 45 | Conversion Rate | Number | שיעור המרה | לא |
| 46 | ACOS | Number | עלות פרסום/מכירות | לא |
| 47 | CPC | Number | עלות לקליק | לא |
| 48 | ROAS | Number | החזר על השקעה | לא |

## עמודות Informational

### רשימת 9 העמודות שלא משתתפות בחישובים

1. **עמודה 12:** Campaign Name (Informational only)
2. **עמודה 13:** Ad Group Name (Informational only)
3. **עמודה 14:** Portfolio Name (Informational only)
4. **עמודה 19:** Campaign State (Informational only)
5. **עמודה 20:** Ad Group State (Informational only)
6. **עמודה 24:** Eligibility Status (Informational only)
7. **עמודה 25:** Reason for Ineligibility (Informational only)
8. **עמודה 27:** Ad Group Default Bid (Informational only)
9. **עמודה 37:** Resolved Product Targeting Expression (Informational only)

### כללים לעמודות Informational
- **אסור למחוק** - נשמרות בפלט כמו שהן
- **לא משתתפות בחישובים** - לא משפיעות על האופטימיזציה
- **לקריאה בלבד** - לא משנים את הערכים שלהן

## עמודות קריטיות לאופטימיזציות

### Zero Sales
- **Units (44):** לזיהוי מוצרים ללא מכירות
- **Clicks (39):** לחישוב CPC מותאם
- **Bid (28):** הערך שמעדכנים
- **Percentage (35):** לחישוב Max BA
- **Entity (2):** לסינון סוגי ישויות
- **Portfolio Name (14):** לסינון Flat Portfolios

## ערכי Entity Types

| ערך | תיאור | Zero Sales |
|-----|-------|------------|
| Keyword | מילות מפתח | ✓ מעבד |
| Product Targeting | מיקוד מוצרים | ✓ מעבד |
| Product Ad | מודעות מוצר | ✓ מעביר כמו שהוא |
| Bidding Adjustment | התאמות הצעות | ✓ מעביר כמו שהוא |
| Campaign | קמפיינים | ✗ מסנן |
| Ad Group | קבוצות מודעות | ✗ מסנן |

## ערכי State

| ערך | משמעות | טיפול |
|-----|---------|-------|
| enabled | פעיל | מעבד |
| paused | מושהה | מסנן |
| archived | מאורכב | מסנן |

## דגשים חשובים

1. **סדר קבוע:** אסור לשנות את סדר העמודות
2. **48 בדיוק:** חייב להיות מספר מדויק של עמודות
3. **Case Sensitive:** ערכים כמו Entity ו-State רגישים לאותיות
4. **ערכים ריקים:** עמודות מספריות יכולות להיות ריקות או 0
5. **דיוק:** מספרים עשרוניים עד 3 ספרות אחרי הנקודה

---

**עדכון אחרון:** 18 באוגוסט 2025, 12:45