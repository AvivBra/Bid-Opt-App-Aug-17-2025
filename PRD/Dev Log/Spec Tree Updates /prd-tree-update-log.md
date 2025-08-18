# עדכון עץ מסמכי האיפיון
**תאריך:** 18 באוגוסט 2025, 11:36 (שעון ישראל)

## החלטה: הסרת קובץ overview.md
**נתיב הקובץ שהוסר:** `PRD/Business/bid-optimizations/zero-sales/overview.md`  
**סיבה:** הקובץ מיותר ומבלבל, המידע מפוזר בקבצים האחרים

---

## מקרא
- ✅ = קובץ קיים ומוכן
- ⭕ = קובץ חסר שצריך לכתוב
- 🚫 = TBC לשלב עתידי
- ❌✖️ = קובץ שהוסר במכוון

---

## עץ מסמכי האיפיון המעודכן

```
PRD/
├── README.md                                   ⭕ # סקירה כללית של האיפיון
├── requirements.md                             ⭕ # דרישות עסקיות ופונקציונליות
├── architecture-overview.md                   ⭕ # תיאור 3 השכבות
│
├── UI/                                        
│   ├── design/
│   │   ├── design-system.md                   ✅ # מערכת עיצוב
│   │   ├── layout.md                          ✅ # פריסה
│   │   └── components.md                      ✅ # רכיבי UI
│   │
│   ├── pages/
│   │   ├── bid-optimizer.md                   ✅ # עמוד ראשי
│   │   └── campaigns-optimizer.md             🚫 # TBC - עתידי
│   │
│   ├── panels/
│   │   ├── upload-panel.md                    ⭕ # פאנל העלאה
│   │   ├── validation-panel.md                ⭕ # פאנל ולידציה
│   │   └── output-panel.md                    ⭕ # פאנל פלט
│   │
│   ├── navigation/
│   │   ├── navigation.md                      ✅ # ניווט
│   │   └── state-management.md                ✅ # ניהול state
│   │
│   └── mockups/
│       └── desktop-view.md                    ✅ # תצוגת דסקטופ
│
├── Business/
│   ├── common/
│   │   ├── base-optimization.md               ✅ # מבנה בסיסי
│   │   ├── validation-flow.md                 ✅ # תהליך ולידציה
│   │   ├── error-handling.md                  ✅ # טיפול בשגיאות
│   │   └── portfolio-rules.md                 ⭕ # רשימת Flat portfolios
│   │
│   ├── bid-optimizations/
│   │   ├── zero-sales/
│   │   │   ├── ~~overview.md~~                ❌✖️ # הוסר - מיותר ומבלבל
│   │   │   ├── validation.md                  ✅ # וולידציה (הושלם היום)
│   │   │   ├── cleaning.md                    ✅ # ניקוי (הושלם היום)
│   │   │   ├── processing.md                  ✅ # לוגיקה
│   │   │   └── processing-heb.md              ✅ # לוגיקה בעברית (תוקן היום)
│   │   │
│   │   └── TBC.md                            🚫 # 13 אופטימיזציות נוספות - עתידי
│   │
│   └── campaign-optimizations/
│       └── TBC.md                            🚫 # Negation & Harvesting - עתידי
│
├── Data/
│   ├── input/
│   │   ├── template/
│   │   │   ├── upload-process.md              ✅ # תהליך העלאה
│   │   │   ├── structure.md                   ⭕ # מבנה Template
│   │   │   └── validation.md                  ⭕ # בדיקות תקינות
│   │   │
│   │   ├── bulk/
│   │   │   ├── upload-process.md              ✅ # תהליך העלאה
│   │   │   ├── structure.md                   ⭕ # מבנה 48 עמודות
│   │   │   ├── validation.md                  ⭕ # בדיקות תקינות
│   │   │   └── time-ranges.md                 ⭕ # הבדלים בין 7/30/60
│   │   │
│   │   ├── data-rova/
│   │   │   └── TBC.md                         🚫 # עתידי
│   │   │
│   │   └── columns-definition.md              ⭕ # הגדרת 48 העמודות
│   │
│   ├── output/
│   │   ├── file-generation.md                 ✅ # יצירת קבצים
│   │   ├── output-formats.md                  ⭕ # פורמטי פלט
│   │   └── naming-conventions.md              ⭕ # מוסכמות שמות
│   │
│   ├── processing/
│   │   ├── data-flow.md                       ✅ # זרימת נתונים
│   │   ├── file-structure.md                  ✅ # מבנה קבצים
│   │   └── architecture.md                    ✅ # ארכיטקטורת נתונים
│   │
│   └── integrations/
│       └── data-rova.md                       🚫 # TBC - API עתידי
│
├── Testing/
│   ├── test-plan.md                           ✅ # תוכנית בדיקות
│   ├── test-scenarios.md                      ⭕ # תרחישי בדיקה
│   └── performance.md                         ✅ # ביצועים
│
└── Development/
    ├── phases.md                              ✅ # 6 שלבי פיתוח
    ├── phase-1-zero-sales.md                  ⭕ # פיתוח Zero Sales
    ├── phase-2-more-optimizations.md          🚫 # TBC - עתידי
    └── phase-3-campaigns.md                   🚫 # TBC - עתידי
```

## סיכום סטטוס

### קבצים שהושלמו היום (3)
- ✅ `Business/bid-optimizations/zero-sales/validation.md` - וולידציה מלאה
- ✅ `Business/bid-optimizations/zero-sales/cleaning.md` - ניקוי וסינון
- ✅ `Business/bid-optimizations/zero-sales/processing-heb.md` - תוקן Bulk 60

### קובץ שהוסר (1)
- ❌✖️ `Business/bid-optimizations/zero-sales/overview.md` - הוסר כמיותר

### קבצים קיימים (22)
- ✅ 22 קבצים כתובים ומוכנים

### קבצים חסרים (18)
- ⭕ 18 קבצים להשלמה

### קבצי TBC (7)
- 🚫 7 קבצים לשלב עתידי

---

**סה"כ התקדמות:** 22/40 קבצים הושלמו (55%)