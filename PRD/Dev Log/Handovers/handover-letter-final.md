# מכתב העברה למשלים האיפיון - Bid Optimizer

**תאריך:** 18 באוגוסט 2025, 18:00  
**אל:** משלים האיפיון  
**מאת:** מנהל האיפיון הקודם  
**נושא:** השלמת קבצי איפיון חסרים - הנחיות מדויקות

---

## חשוב - קרא לפני שאתה עושה כלום

אתה מקבל פרויקט איפיון כמעט גמור. **49 קבצים מתוך 57 כבר נכתבו**. נשארו לך 8 קבצים בלבד להשלים. אל תמציא, אל תוסיף, אל תשנה כלום בקיים. פשוט תשלים את החסר לפי ההנחיות.

---

## 1. מה המצב הנוכחי - העץ המלא

```
PRD/
├── README.md                                   ✅ קיים
├── requirements.md                             ✅ קיים
├── architecture-overview.md                    ✅ קיים
│
├── Business/
│   ├── common/
│   │   ├── base-optimization.md               ✅ קיים
│   │   ├── error-handling.md                  ✅ קיים
│   │   ├── portfolio-rules.md                 ✅ קיים - רשימת 10 Flat Portfolios
│   │   └── validation-flow.md                 ✅ קיים
│   │
│   ├── bid-optimizations/
│   │   └── zero-sales/
│   │       ├── validation.md                  ✅ קיים
│   │       ├── cleaning.md                    ✅ קיים
│   │       ├── processing.md                  ✅ קיים - הלוגיקה המלאה
│   │       └── processing-heb.md              ✅ קיים
│   │
│   └── campaign-optimizations/                🚫 TBC - אל תיגע
│
├── Data/
│   ├── input/
│   │   ├── template/
│   │   │   ├── upload-process.md              ✅ קיים
│   │   │   ├── structure.md                   ⭕ חסר - צריך לכתוב
│   │   │   └── validation.md                  ⭕ חסר - צריך לכתוב
│   │   │
│   │   ├── bulk/
│   │   │   ├── upload-process.md              ✅ קיים
│   │   │   ├── structure.md                   ⭕ חסר - צריך לכתוב
│   │   │   ├── validation.md                  ⭕ חסר - צריך לכתוב
│   │   │   └── time-ranges.md                 ⭕ חסר - צריך לכתוב
│   │   │
│   │   ├── columns-definition.md              ✅ קיים - כל 48 העמודות
│   │   └── data-rova/                         🚫 TBC - אל תיגע
│   │
│   ├── output/
│   │   ├── file-generation.md                 ✅ קיים
│   │   ├── output-formats.md                  ⭕ חסר - צריך לכתוב
│   │   └── naming-conventions.md              ⭕ חסר - צריך לכתוב
│   │
│   └── processing/
│       ├── data-flow.md                       ✅ קיים
│       ├── file-structure.md                  ✅ קיים
│       └── architecture.md                    ✅ קיים
│
├── Testing/
│   ├── test-plan.md                           ✅ קיים
│   ├── test-scenarios.md                      ✅ קיים - 22 תרחישים
│   └── performance.md                         ✅ קיים
│
├── Development/
│   ├── phases.md                              ✅ קיים - 6 שלבים
│   └── phase-1-zero-sales.md                  ⭕ חסר - צריך לכתוב
│
└── UI/
    ├── design/                                ✅ כל התיקייה קיימת
    ├── mockups/                               ✅ כל התיקייה קיימת
    ├── navigation/                            ✅ כל התיקייה קיימת
    ├── pages/                                 ✅ כל התיקייה קיימת
    └── panels/                                ✅ כל התיקייה קיימת
```

---

## 2. רשימת הקבצים שאתה צריך לכתוב (8 בלבד)

### קבצים חסרים שחובה לכתוב:

1. **`PRD/Data/input/template/structure.md`**
   - מבנה הקובץ עם 2 הלשוניות
   - Port Values: 3 עמודות (Portfolio Name, Base Bid, Target CPA)
   - Top ASINs: עמודה אחת (ASIN)

2. **`PRD/Data/input/template/validation.md`**
   - בדיקות שנעשות על Template
   - Portfolio Names ייחודיים
   - Base Bid: מספר או "Ignore"
   - Target CPA: מספר או ריק

3. **`PRD/Data/input/bulk/structure.md`**
   - Sheet: "Sponsored Products Campaigns"
   - בדיוק 48 עמודות (הרשימה המלאה ב-columns-definition.md)
   - עד 500,000 שורות

4. **`PRD/Data/input/bulk/validation.md`**
   - בדיקת 48 עמודות
   - בדיקת גודל קובץ (עד 40MB)
   - בדיקת Sheet name

5. **`PRD/Data/input/bulk/time-ranges.md`**
   - ההבדלים בין Bulk 7/30/60
   - כרגע רק Bulk 60 פעיל
   - השאר TBC

6. **`PRD/Data/output/output-formats.md`**
   - Working File: 2 לשוניות (Targeting, Bidding Adjustment)
   - 7 עמודות עזר ב-Targeting
   - Clean File: TBC

7. **`PRD/Data/output/naming-conventions.md`**
   - Working File: `Auto Optimized Bulk | Working | YYYY-MM-DD | HH-MM.xlsx`
   - Clean File: `Auto Optimized Bulk | Clean | YYYY-MM-DD | HH-MM.xlsx` (TBC)

8. **`PRD/Development/phase-1-zero-sales.md`**
   - פירוט Phase 1 בלבד
   - Zero Sales optimization
   - Working File בלבד
   - Bulk 60 בלבד

---

## 3. איפה למצוא את המידע שאתה צריך

### לקובץ structure.md של Template:
- **קרא:** `PRD/Data/input/template/upload-process.md` - יש שם את כל המידע
- **קרא:** `PRD/Business/bid-optimizations/zero-sales/validation.md` - מבנה Port Values

### לקובץ structure.md של Bulk:
- **קרא:** `PRD/Data/input/columns-definition.md` - רשימת 48 העמודות המלאה
- **קרא:** `PRD/Data/input/bulk/upload-process.md` - פרטים על המבנה

### לקובצי validation.md:
- **קרא:** `PRD/Business/common/validation-flow.md` - תהליך הוולידציה
- **קרא:** `PRD/Business/common/error-handling.md` - הודעות שגיאה

### לקובץ time-ranges.md:
- **קרא:** `PRD/Dev Log/FQA/faq-developers.md` - הסבר על Bulk 7/30/60
- **זכור:** רק Bulk 60 פעיל כרגע, השאר TBC

### לקובץ output-formats.md:
- **קרא:** `PRD/Data/output/file-generation.md` - תהליך יצירת הקבצים
- **קרא:** `PRD/Business/bid-optimizations/zero-sales/processing.md` - מבנה הפלט

### לקובץ naming-conventions.md:
- **קרא:** `PRD/UI/panels/output-panel.md` - שמות הקבצים מופיעים שם
- **קרא:** `PRD/Data/output/file-generation.md` - פורמט השמות

### לקובץ phase-1-zero-sales.md:
- **קרא:** `PRD/Development/phases.md` - תיאור כללי של Phase 1
- **קרא:** `PRD/requirements.md` - דרישות ל-Phase 1

---

## 4. כללי כתיבה שאסור לסטות מהם

### שפה וסגנון:
- **תוכן:** עברית
- **מונחים טכניים:** אנגלית (Bulk, Template, Portfolio, Sheet)
- **אורך:** 50-150 שורות לקובץ
- **מבנה:** כותרות ברורות, ללא טבלאות (רק bullet points)

### מה כן לכתוב:
- פירוט טכני ברור
- דוגמאות קונקרטיות
- מגבלות וערכים מדויקים
- הפניות לקבצים קשורים

### מה אסור לכתוב:
- קוד או פסאודו-קוד
- המצאות חדשות
- פירוט על TBC
- שינויים במה שקיים

---

## 5. נקודות קריטיות שאסור לפספס

### Portfolio Names:
- **Case Sensitive תמיד**
- **10 Flat Portfolios:** מותר שיחסרו (הרשימה ב-portfolio-rules.md)
- **Base Bid = "Ignore":** Case Sensitive

### מבנה קבצים:
- **Template:** בדיוק 2 לשוניות, בדיוק 3 עמודות ב-Port Values
- **Bulk:** בדיוק 48 עמודות, Sheet "Sponsored Products Campaigns"
- **Working File:** 48 + 7 עמודות ב-Targeting, רק 48 ב-Bidding Adjustment

### מגבלות:
- **Template:** עד 1MB
- **Bulk:** עד 40MB, עד 500,000 שורות
- **Bid:** 0.02-1.25 (מחוץ לטווח = ורוד ב-Excel, לא ב-UI)

### מה TBC (אל תפרט):
- 13 אופטימיזציות נוספות
- Campaigns Optimizer
- Clean File
- Data Rova
- Bulk 7/30

---

## 6. בדיקה עצמית לפני סיום

### לכל קובץ שכתבת:
- [ ] 50-150 שורות?
- [ ] עברית עם מונחים באנגלית?
- [ ] אין קוד?
- [ ] אין המצאות?
- [ ] מתאים למידע הקיים?

### בדיקה כללית:
- [ ] 8 קבצים נכתבו?
- [ ] לא נגעת בקבצים קיימים?
- [ ] לא הוספת קבצים חדשים?
- [ ] TBC מסומן איפה שצריך?

---

## 7. מידע טכני חשוב

### טכנולוגיות (רק לציון, לא לפירוט):
- Python 3.8+
- Streamlit
- pandas
- openpyxl

### עיצוב (כבר מאופיין במלואו):
- Dark Mode
- צבעים: #0A0A0A (רקע), #171717 (כרטיסים), #E5E5E5 (טקסט)
- Accent: #8B5CF6 (ויולט)
- ללא הודעות ורודות ב-UI (רק ב-Excel)

### ניווט:
- **Sidebar Navigation** (לא Stepper!)
- 2 עמודים: Bid Optimizer, Campaigns Optimizer (TBC)

---

## 8. אזהרות אחרונות

### אל תעשה:
- ❌ אל תמציא features חדשים
- ❌ אל תשנה קבצים קיימים
- ❌ אל תוסיף קבצים שלא ברשימה
- ❌ אל תכתוב קוד
- ❌ אל תפרט על TBC

### כן תעשה:
- ✅ קרא את הקבצים הרלוונטיים
- ✅ כתוב רק את 8 הקבצים ברשימה
- ✅ שמור על עקביות עם הקיים
- ✅ שאל רק אם יש סתירה או חוסר מידע

---

## 9. סיכום המשימה שלך

**משימה:** כתוב 8 קבצים בלבד  
**זמן משוער:** 2-3 שעות  
**מורכבות:** נמוכה (כל המידע קיים)  
**תוצאה:** איפיון מושלם ל-Phase 1

כל המידע שאתה צריך נמצא בקבצים הקיימים. אל תמציא, אל תנחש - פשוט קרא וכתוב לפי מה שכתוב.

---

**חשוב:** אל תתחיל לכתוב עד שתאשר שהבנת את המשימה. קרא את המכתב הזה פעמיים, עבור על הקבצים שצוינו, ואז אשר שאתה מוכן.

---

*מסמך זה נכתב ב-18 באוגוסט 2025, 18:00*