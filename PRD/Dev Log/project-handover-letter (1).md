# מכתב העברת פרויקט - Bid Optimizer for Amazon Ads

**תאריך:** 18 באוגוסט 2025  
**אל:** מנהל האיפיון החדש  
**מאת:** מנהל הפרויקט  
**נושא:** הנחיות מלאות להמשך איפיון המערכת

---

## שלום,

אתה מקבל לידיך פרויקט איפיון באמצע הדרך. המפתח הקודם עזב והשאיר עבודה חלקית. מסמך זה מכיל את כל מה שאתה צריך לדעת כדי להמשיך ללא תקלות.

---

## 1. תיאור הפרויקט

### מה זה?
מערכת אופטימיזציה אוטומטית להצעות מחיר (Bids) בקמפיינים של Amazon Ads. המערכת מקבלת קבצי Excel מ-Amazon, מריצה אופטימיזציות שונות ומחזירה קבצי Excel מעודכנים להעלאה חזרה ל-Amazon.

### למי זה?
חברת PPC שמנהלת קמפיינים של לקוחות רבים ב-Amazon. כרגע עושים את האופטימיזציות ידנית ב-Excel וזה לוקח שעות. המערכת תחסוך 90% מהזמן.

### איך זה עובד?
1. המשתמש מעלה 2 קבצים: Template (הגדרות) ו-Bulk (נתונים מ-Amazon)
2. בוחר אילו אופטימיזציות להריץ (מתוך 14 אפשרויות)
3. המערכת מעבדת ומחזירה קבצי Excel מוכנים להעלאה ל-Amazon

---

## 2. מה השתנה לאחרונה?

### גרסה ישנה (15 באוגוסט)
- ממשק Stepper (3 שלבים: Upload → Validate → Output)
- וולידציה גלובלית על כל הקובץ
- ניקוי גלובלי של הנתונים
- אופטימיזציות רצות על נתונים מנוקים

### גרסה חדשה (17 באוגוסט) - **זה מה שממשיכים!**
- ממשק Sidebar עם 2 עמודים (Bid Optimizer, Campaigns Optimizer)
- **כל אופטימיזציה מבצעת וולידציה וניקוי עצמאיים**
- אין וולידציה גלובלית
- מבנה מודולרי יותר

---

## 3. מבנה הקבצים הנוכחי

### ארכיטקטורת 3 שכבות:
```
PRD/
├── UI/           # ממשק משתמש - משותף לכל האופטימיזציות
├── Business/     # לוגיקה עסקית - נפרד לכל אופטימיזציה
└── Data/         # ניהול נתונים - קלט/פלט/עיבוד
```

### קבצים קיימים (22 קבצים):
✅ **UI מלא:** design-system, layout, components, pages, navigation, state-management  
✅ **Business חלקי:** base-optimization, validation-flow, error-handling, zero-sales/processing  
✅ **Data חלקי:** upload processes, file-generation, data-flow, architecture  
✅ **Testing:** test-plan, performance  
✅ **Development:** phases

### קבצים חסרים (19 קבצים להשלים):
❌ **ראשיים:** README.md, requirements.md, architecture-overview.md  
❌ **UI/panels:** upload-panel.md, validation-panel.md, output-panel.md  
❌ **Business/zero-sales:** overview.md, validation.md, cleaning.md  
❌ **Business/common:** portfolio-rules.md  
❌ **Data/input:** structure.md files (לכל סוג קלט)  
❌ **Data:** columns-definition.md, output-formats.md, naming-conventions.md  

---

## 4. מה שאתה צריך לדעת - המידע הקריטי

### קבצי הקלט:

#### Template File (2 לשוניות):
**לשונית 1: Port Values**
| Portfolio Name | Base Bid | Target CPA |
|---------------|----------|------------|
| Kids-Brand-US | 1.25 | 5.00 |
| Supplements-EU | 2.10 | 8.50 |

**לשונית 2: Top ASINs** (לשימוש עתידי)
| ASIN |
|------|
| B001234567 |

#### Bulk Files (48 עמודות, עד 500K שורות):
- **Bulk 7:** נתוני 7 ימים אחרונים
- **Bulk 30:** נתוני 30 ימים אחרונים (בשימוש ב-Zero Sales)
- **Bulk 60:** נתוני 60 ימים אחרונים

**48 העמודות (בסדר מדויק):**
1. Product
2. Entity (Keyword/Product Targeting/Product Ad/Bidding Adjustment)
3. Operation
4. Campaign ID
5-14. IDs ושמות
15-37. הגדרות וסטטוסים
38-48. מטריקות (Impressions, Clicks, Sales, Orders, Units, ACOS, CPC, ROAS)

### 10 הפורטפוליוז המוחרגים (תמיד לדלג עליהם):
```
Flat 30, Flat 25, Flat 40, Flat 25 | Opt, Flat 30 | Opt,
Flat 20, Flat 15, Flat 40 | Opt, Flat 20 | Opt, Flat 15 | Opt
```

### 14 האופטימיזציות:
**מאופיינות:** Zero Sales בלבד  
**ממתינות לאיפיון:** Portfolio Bid, Budget Optimization, Keyword Optimization, ASIN Targeting ועוד 9

---

## 5. איך לכתוב איפיון - המתודולוגיה

### כל אופטימיזציה צריכה 4 קבצים:

1. **overview.md** - סקירה כללית
   - מה האופטימיזציה עושה
   - מתי להשתמש בה
   - אילו Entity Types רלוונטיים

2. **validation.md** - בדיקות תקינות
   - אילו עמודות נדרשות
   - אילו ערכים תקינים
   - מה לעשות עם שגיאות

3. **cleaning.md** - ניקוי וסינון
   - אילו שורות לסנן (לפי Entity, State, Portfolio)
   - אילו ערכים לנרמל
   - איך לטפל בערכים חסרים

4. **processing.md** - הלוגיקה העסקית
   - החישובים שצריך לבצע
   - איך לעדכן את ה-Bid
   - מבנה הפלט

### כללי כתיבה:
- **שפה:** עברית לתוכן, אנגלית לממשק ומונחים טכניים
- **דוגמאות:** תמיד לכלול דוגמאות מספריות
- **טבלאות:** להשתמש בטבלאות למבני נתונים
- **זרימה:** לתאר את התהליך צעד-צעד

---

## 6. משימות לביצוע - סדר עבודה מומלץ

### שלב א' - השלמת Zero Sales (3 קבצים):
1. `Business/bid-optimizations/zero-sales/overview.md`
2. `Business/bid-optimizations/zero-sales/validation.md`
3. `Business/bid-optimizations/zero-sales/cleaning.md`

**טיפ:** קרא את `processing.md` ו-`processing-heb.md` הקיימים - כל המידע שם!

### שלב ב' - קבצי תשתית (10 קבצים):
1. `PRD/README.md` - סקירה כללית של האיפיון
2. `PRD/requirements.md` - דרישות עסקיות ופונקציונליות
3. `PRD/architecture-overview.md` - תיאור 3 השכבות
4. `Business/common/portfolio-rules.md` - רשימת ה-10 Flat portfolios
5. `Data/input/template/structure.md` - מבנה 2 הלשוניות
6. `Data/input/bulk/structure.md` - מבנה 48 העמודות
7. `Data/input/columns-definition.md` - הגדרה מפורטת לכל עמודה
8. `Data/output/output-formats.md` - מבנה קבצי הפלט
9. `Data/output/naming-conventions.md` - מוסכמות שמות קבצים
10. `Testing/test-scenarios.md` - תרחישי בדיקה

### שלב ג' - UI Panels (3 קבצים):
1. `UI/panels/upload-panel.md`
2. `UI/panels/validation-panel.md`
3. `UI/panels/output-panel.md`

### שלב ד' - תיעוד פיתוח (3 קבצים):
1. `Development/phase-1-zero-sales.md`
2. `Development/phase-2-more-optimizations.md` (TBC)
3. `Development/phase-3-campaigns.md` (TBC)

---

## 7. דוגמה: איך Zero Sales עובד (כדי שתבין את הסגנון)

### תהליך:
1. **סינון:** שורות עם Units = 0
2. **ניקוי:** הסרת Flat portfolios, הסרת Ignore portfolios
3. **חלוקה:** Keywords/Product Targeting לטיפול, Bidding Adjustment נשאר כמו שהוא
4. **חישוב:** 4 מקרים לפי Target CPA ושם הקמפיין ("up and")
5. **פלט:** 2 sheets - Targeting עם 7 עמודות עזר, Bidding Adjustment ללא שינוי

### החישוב המרכזי:
```
אם Target CPA ריק ויש "up and" בשם → Bid = Base Bid × 0.5
אם Target CPA ריק ואין "up and" → Bid = Base Bid
אם Target CPA קיים ויש "up and" → חישוב מורכב עם Adj. CPA × 0.5
אם Target CPA קיים ואין "up and" → חישוב מורכב עם Adj. CPA
```

---

## 8. היכן למצוא מידע נוסף

### בפרויקט:
- `PRD/Business/bid-optimizations/zero-sales/processing.md` - הלוגיקה המלאה
- `PRD/Business/bid-optimizations/zero-sales/processing-heb.md` - הסבר בעברית
- `PRD/Dev Log/` - היסטוריית השינויים

### מקורות חיצוניים:
- פרויקט "Bid Opt App Aug 15, 2025" - הגרסה הישנה
- פרויקט "Bid Opt App Aug 17, 2025" - הגרסה החדשה

---

## 9. כללי ברזל - חובה לזכור!

1. **אל תמחק קבצים קיימים** - גם אם נראים לא רלוונטיים
2. **כל אופטימיזציה עצמאית** - וולידציה וניקוי פנימיים
3. **Entity Types חשובים** - כל אופטימיזציה מטפלת בסוגים שונים
4. **10 Flat Portfolios** - תמיד לסנן אותם
5. **Base Bid = "Ignore"** - לא לטפל בפורטפוליו הזה
6. **Operation = "Update"** - תמיד בפלט
7. **48 עמודות בדיוק** - לא להוסיף או להוריד
8. **עמודות עזר** - רק ב-Working File, לא ב-Clean File

---

## 10. איך לבקש עזרה

אם משהו לא ברור, חפש קודם ב:
1. קבצי processing.md הקיימים
2. הלוג ב-Dev Log
3. הקבצים הקיימים ב-UI ו-Business

אם עדיין לא ברור, תכין שאלה ספציפית עם:
- באיזה קובץ אתה עובד
- מה ניסית לעשות
- איפה נתקעת
- דוגמה קונקרטית

---

## 11. צ'קליסט לסיום

- [ ] קראת את כל הקבצים הקיימים
- [ ] הבנת את ההבדל בין הגרסה הישנה לחדשה
- [ ] הבנת את מבנה 3 השכבות
- [ ] הבנת איך Zero Sales עובד
- [ ] יודע מה ה-10 Flat Portfolios
- [ ] יודע מה ה-48 עמודות
- [ ] מכיר את 4 הקבצים שכל אופטימיזציה צריכה

---

**בהצלחה!**  
אתה מקבל פרויקט מאורגן עם בסיס טוב. המטרה: להשלים את 19 הקבצים החסרים ולהכין תשתית ל-13 האופטימיזציות הנוספות.

**זכור:** Zero Sales הוא התבנית שלך. אם משהו עובד שם, כנראה שככה צריך לעבוד בכל האופטימיזציות.

---

*מסמך זה נכתב ב-18 באוגוסט 2025, 09:00 (שעון ישראל)*