# לוג שינוי מבנה איפיון עם סטטוס קבצים
**תאריך:** 18 באוגוסט 2025  
**שעה:** 09:00 (שעון ישראל)

## החלטה על שינוי המבנה
החלטנו לשנות את מבנה תיקיית האיפיון מהמבנה הישן שהיה מבוסס על חלוקה לפי נושאים (Core, Features, Optimizations) למבנה חדש המבוסס על ארכיטקטורת 3 שכבות (UI, Business, Data). השינוי נועד ליצור הפרדה ברורה יותר בין שכבות המערכת, למנוע כפילויות ולהקל על הפיתוח והתחזוקה. מנהל הפיתוח הקודם עזב באמצע העבודה והמבנה החדש מסדר את האיפיון בצורה נקייה ומודולרית יותר.

## מקרא סימונים
- ✅ **קיים** - קובץ קיים ונשאר במקומו
- 🔄 **להעביר** - קובץ קיים אבל צריך להעביר/לשנות שם
- ❌ **חסר** - קובץ צריך לכתוב
- 🚫 **TBC** - To Be Continued (יתווסף בעתיד)

## מבנה העץ החדש

```
PRD/
├── README.md                                   ❌
├── requirements.md                             ❌
├── architecture-overview.md                    ❌ # תיאור 3 השכבות
│
├── UI/                                         # שכבת הממשק - משותף לכל האופטימיזציות
│   ├── design/
│   │   ├── design-system.md                   ✅ # צבעים, פונטים, סגנון
│   │   ├── layout.md                          ✅ # פריסת עמודים
│   │   └── components.md                      ✅ # קומפוננטות משותפות
│   │
│   ├── pages/
│   │   ├── bid-optimizer.md                   ✅ # עמוד ראשי Bid
│   │   └── campaigns-optimizer.md             ✅ # עמוד ראשי Campaigns
│   │
│   ├── panels/                                # פאנלים משותפים
│   │   ├── upload-panel.md                    ❌ # פאנל העלאה
│   │   ├── validation-panel.md                ❌ # פאנל ולידציה
│   │   └── output-panel.md                    ❌ # פאנל פלט
│   │
│   ├── mockups/
│   │   └── desktop-view.md                    ✅
│   │
│   └── navigation/
│       ├── navigation.md                      ✅ # נביגציה וניתוב
│       └── state-management.md                ✅ # ניהול state
│
├── Business/                                   # שכבת הלוגיקה העסקית
│   ├── common/                                # לוגיקה משותפת
│   │   ├── base-optimization.md               ✅ # מחלקת בסיס לאופטימיזציות
│   │   ├── validation-flow.md                 ✅ # תהליך ולידציה כללי
│   │   ├── error-handling.md                  ✅ # טיפול בשגיאות
│   │   └── portfolio-rules.md                 ❌ # חוקי פורטפוליו (Flat וכו')
│   │
│   ├── bid-optimizations/                     # אופטימיזציות Bid
│   │   ├── zero-sales/
│   │   │   ├── overview.md                    ❌ # סקירה כללית
│   │   │   ├── validation.md                  ❌ # וולידציה ספציפית
│   │   │   ├── cleaning.md                    ❌ # ניקוי וסינון נתונים
│   │   │   ├── processing.md                  🔄 # (קיים כ-logic.md)
│   │   │   └── processing-heb.md              🔄 # (קיים כ-logic-heb.md)
│   │   │
│   │   └── TBC.md                            🚫 # 13 אופטימיזציות נוספות - יתווספו בעתיד
│   │
│   └── campaign-optimizations/                # אופטימיזציות Campaigns
│       └── TBC.md                            🚫 # Negation & Harvesting - יתווספו בעתיד
│
├── Data/                                      # שכבת הנתונים
│   ├── input/                                 # נתוני קלט
│   │   ├── template/
│   │   │   ├── upload-process.md              🔄 # (קיים כ-template-upload.md)
│   │   │   ├── structure.md                   ❌ # מבנה Template (2 לשוניות)
│   │   │   └── validation.md                  ❌ # בדיקות תקינות
│   │   │
│   │   ├── bulk/
│   │   │   ├── upload-process.md              🔄 # (קיים כ-bulk-upload.md)
│   │   │   ├── structure.md                   ❌ # מבנה 48 עמודות (זהה ל-7/30/60)
│   │   │   ├── validation.md                  ❌ # בדיקות תקינות
│   │   │   └── time-ranges.md                 ❌ # הבדלים בין 7/30/60 ימים
│   │   │
│   │   ├── data-rova/
│   │   │   └── TBC.md                         🚫 # יתווסף בעתיד
│   │   │
│   │   └── columns-definition.md              ❌ # הגדרת כל 48 העמודות
│   │
│   ├── output/                                # נתוני פלט
│   │   ├── file-generation.md                 ✅ # יצירת קבצים
│   │   ├── output-formats.md                  ❌ # פורמטי פלט
│   │   └── naming-conventions.md              ❌ # מוסכמות שמות קבצים
│   │
│   ├── processing/                            # עיבוד נתונים
│   │   ├── data-flow.md                       ✅ # זרימת נתונים
│   │   ├── file-structure.md                  ✅ # מבנה קבצים
│   │   └── architecture.md                    ✅ # ארכיטקטורת נתונים
│   │
│   └── integrations/                          # אינטגרציות
│       └── data-rova.md                       🚫 # TBC - Data Rova API
│
├── Testing/                                   # בדיקות
│   ├── test-plan.md                           ✅
│   ├── test-scenarios.md                      ❌
│   └── performance.md                         ✅
│
└── Development/                               # תוכנית פיתוח
    ├── phases.md                              ✅ # 6 שלבי פיתוח
    ├── phase-1-zero-sales.md                  ❌
    ├── phase-2-more-optimizations.md          🚫
    └── phase-3-campaigns.md                   🚫
```

## סיכום סטטוס

### קבצים קיימים שנשארים במקומם (16 קבצים):
- ✅ כל קבצי UI/design (3)
- ✅ כל קבצי UI/pages (2)
- ✅ UI/mockups/desktop-view.md
- ✅ כל קבצי UI/navigation (2)
- ✅ כל קבצי Business/common (3 מתוך 4)
- ✅ כל קבצי Data/processing (3)
- ✅ Data/output/file-generation.md
- ✅ Testing/test-plan.md, performance.md
- ✅ Development/phases.md

### קבצים להעברה/שינוי שם (4 קבצים):
- 🔄 logic.md → processing.md
- 🔄 logic-heb.md → processing-heb.md
- 🔄 template-upload.md → Data/input/template/upload-process.md
- 🔄 bulk-upload.md → Data/input/bulk/upload-process.md

### קבצים חסרים לכתיבה (19 קבצים):
- ❌ קבצים ראשיים (3)
- ❌ UI/panels (3)
- ❌ Business/zero-sales (3)
- ❌ Business/common/portfolio-rules.md
- ❌ Data/input (6)
- ❌ Data/output (2)
- ❌ Testing/test-scenarios.md
- ❌ Development/phase-1-zero-sales.md

### קבצי TBC - יתווספו בעתיד (5 קבצים):
- 🚫 Business/bid-optimizations/TBC.md
- 🚫 Business/campaign-optimizations/TBC.md
- 🚫 Data/input/data-rova/TBC.md
- 🚫 Data/integrations/data-rova.md
- 🚫 Development/phase-2&3

## הערות
- הקבצים הקיימים (צבע ירוק) כבר כתובים ומוכנים
- קבצים להעברה (כתום) קיימים אבל צריך להעביר למקום חדש או לשנות שם
- קבצים חסרים (אדום) צריך לכתוב
- קבצי TBC (אפור) יכתבו בשלב מאוחר יותר כשנגיע לאופטימיזציות נוספות