# מבנה תיקיית מסמכי איפיון - PRD/Spec

## הערות חשובות
- **שפה:** כל המסמכים בעברית, שמות ומונחים טכניים באנגלית
- **ממשק:** כל הממשק באנגלית בלבד
- **פוקוס נוכחי:** איפיון מלא רק ל-Zero Sales
- **אופטימיזציות עתידיות:** מסומנות ב-"TBD - יתווסף בעתיד"
- **Campaigns Optimizer:** מסומן ב-"TBD - איפיון הטאב השני יתווסף בעתיד"

```
PRD/
├── README.md                           # סקירה כללית של האיפיון
├── requirements.md                     # דרישות עסקיות ופונקציונליות
├── change-log.md                       # תיעוד שינויים ועדכונים
│
├── Spec/
│   ├── Core/                          # איפיונים ליבה
│   │   ├── architecture.md            # ארכיטקטורה כללית
│   │   ├── file-structure.md          # מבנה קבצים ותיקיות
│   │   ├── data-flow.md               # זרימת נתונים
│   │   ├── state-management.md        # ניהול state
│   │   └── navigation.md              # נביגציה וניתוב
│   │
│   ├── UI/                            # איפיוני ממשק משתמש
│   │   ├── design-system.md           # מערכת עיצוב (צבעים, פונטים)
│   │   ├── layout.md                  # פריסת עמודים
│   │   ├── components.md              # קומפוננטות UI
│   │   ├── pages/
│   │   │   ├── bid-optimizer.md       # עמוד Bid Optimizer
│   │   │   └── campaigns-optimizer.md # עמוד Campaigns
│   │   └── mockups/
│   │       ├── desktop-view.md        # סימולציות desktop
│   │       └── states.md              # מצבי תצוגה
│   │
│   ├── Features/                      # איפיוני פיצ'רים
│   │   ├── upload/
│   │   │   ├── template-upload.md     # העלאת template עם 2 לשוניות
│   │   │   ├── bulk-upload.md         # העלאת bulk files (7/30/60 ימים)
│   │   │   └── data-rova.md          # TBD - אינטגרציית Data Rova (benchmarking)
│   │   │
│   │   ├── validation/
│   │   │   ├── validation-flow.md     # תהליך וולידציה
│   │   │   ├── error-handling.md      # טיפול בשגיאות
│   │   │   └── messages.md            # הודעות למשתמש
│   │   │
│   │   └── output/
│   │       ├── file-generation.md     # יצירת קבצי פלט
│   │       ├── download.md            # הורדת קבצים
│   │       └── formats.md             # פורמטים של קבצים
│   │
│   ├── Optimizations/                 # איפיוני אופטימיזציות
│   │   ├── base-optimization.md       # מבנה בסיסי לכל אופטימיזציה
│   │   │
│   │   ├── bid-optimizations/
│   │   │   ├── zero-sales/
│   │   │   │   ├── logic.md          # לוגיקת עיבוד
│   │   │   │   ├── validation.md     # וולידציות ספציפיות
│   │   │   │   ├── calculations.md   # חישובים
│   │   │   │   └── output.md         # מבנה פלט
│   │   │   │
│   │   │   └── future-optimizations.md # TBD - יתווספו 13 אופטימיזציות נוספות
│   │   │
│   │   └── campaign-optimizations/
│   │       └── TBD.md                 # TBD - איפיון Negation ו-Harvesting יתווסף בעתיד
│   │
│   ├── Data/                          # איפיוני נתונים
│   │   ├── input-formats.md           # פורמטי קלט
│   │   ├── output-formats.md          # פורמטי פלט
│   │   ├── template-structure.md      # מבנה template - Port Values + Top ASINs
│   │   ├── bulk-structure.md          # מבנה bulk files (48 עמודות, עד 500K שורות)
│   │   ├── columns-definition.md      # הגדרת עמודות
│   │   ├── mock-data.md              # נתוני דמה לבדיקות
│   │   └── performance.md            # ביצועים - עד 40MB, זמני עיבוד
│   │
│   ├── API/                           # איפיוני API
│   │   ├── internal-api.md           # API פנימי
│   │   └── integrations/
│   │       └── data-rova-api.md      # API של Data Rova
│   │
│   └── Testing/                       # איפיוני בדיקות
│       ├── test-plan.md              # תוכנית בדיקות
│       ├── test-scenarios.md         # תרחישי בדיקה
│       ├── edge-cases.md             # מקרי קצה
│       └── performance.md            # דרישות ביצועים
│
├── Dev-Plan/                          # תוכנית פיתוח
│   ├── phases.md                     # 6 שלבי פיתוח
│   ├── phase-1-bid-zero-sales.md     # שלב 1: Bid Optimizer עם Zero Sales בלבד
│   ├── phase-2-more-optimizations.md # שלב 2: TBD - 13 אופטימיזציות נוספות
│   ├── phase-3-campaigns.md          # שלב 3: TBD - Campaigns Optimizer
│   ├── milestones.md                 # אבני דרך
│   └── dependencies.md               # תלויות
│
├── Business/                          # לוגיקה עסקית
│   ├── calculations/                 # נוסחאות וחישובים
│   │   ├── bid-calculations.md       # חישובי bid
│   │   ├── cpa-calculations.md       # חישובי CPA
│   │   └── formulas.md              # נוסחאות כלליות
│   │
│   └── rules/                        # חוקים עסקיים
│       ├── portfolio-rules.md        # חוקי פורטפוליו
│       ├── optimization-rules.md     # חוקי אופטימיזציה
│       └── validation-rules.md       # חוקי וולידציה
│
└── Assets/                           # נכסים
    ├── diagrams/                     # דיאגרמות
    │   ├── architecture.svg          # דיאגרמת ארכיטקטורה
    │   ├── data-flow.svg             # דיאגרמת זרימה
    │   └── state-machine.svg         # מכונת מצבים
    │
    ├── examples/                     # דוגמאות
    │   ├── template-example.xlsx     # דוגמת template
    │   ├── bulk-example.xlsx         # דוגמת bulk
    │   └── output-example.xlsx       # דוגמת פלט
    │
    └── references/                   # חומרי עזר
        ├── amazon-api-docs.md        # תיעוד Amazon API
        ├── excel-formats.md          # פורמטי Excel
        └── glossary.md               # מילון מונחים
```

## עקרונות ארגון

### 1. הפרדה לפי נושא
- **Core** - איפיונים בסיסיים שמשפיעים על כל המערכת
- **UI** - כל מה שקשור לממשק משתמש
- **Features** - פיצ'רים ספציפיים
- **Optimizations** - כל אופטימיזציה בתיקייה נפרדת
- **Data** - מבני נתונים ופורמטים

### 2. היררכיה ברורה
- תיקיות ראשיות לנושאים גדולים
- תת-תיקיות לפירוט
- קבצים אטומיים לכל נושא ספציפי

### 3. מוסכמות שמות
- שמות באנגלית בלבד
- kebab-case לשמות קבצים
- שמות תיאוריים וברורים

### 4. תיעוד מקושר
- כל קובץ מפנה לקבצים רלוונטיים
- README בכל תיקייה ראשית
- קישורים צולבים בין מסמכים

### 5. גרסאות ושינויים
- change-log.md לתיעוד שינויים
- תאריכים בראש כל מסמך
- היסטוריית שינויים בכל קובץ קריטי

## יתרונות המבנה

1. **קל לניווט** - מציאת מידע מהירה
2. **מודולרי** - קל להוסיף אופטימיזציות חדשות
3. **מתועד היטב** - כל נושא במקום אחד
4. **ניתן להרחבה** - קל להוסיף עמודים ופיצ'רים
5. **ברור למפתחים** - התאמה למבנה הקוד
6. **מוכן לעתיד** - מקומות מסומנים ל-TBD

## הערות לפיתוח

### זמני עיבוד צפויים
- **קובץ 10MB:** עד 30 שניות
- **קובץ 20MB:** עד 60 שניות  
- **קובץ 40MB:** עד 120 שניות
- **500K שורות:** עד 180 שניות

### קבצי Bulk
- **Bulk 7:** נתונים מ-7 ימים אחרונים
- **Bulk 30:** נתונים מ-30 ימים אחרונים
- **Bulk 60:** נתונים מ-60 ימים אחרונים
- **מבנה זהה:** כל הקבצים עם אותן 48 עמודות

### Template
- **לשונית Port Values:** Portfolio Name, Base Bid, Target CPA
- **לשונית Top ASINs:** עמודת ASIN בלבד (לשימוש עתידי)