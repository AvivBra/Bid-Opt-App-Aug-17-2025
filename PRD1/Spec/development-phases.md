# תוכנית פיתוח - Bid Optimizer

## סקירה כללית

### גישת הפיתוח
- **בניית אפליקציה חדשה מאפס** (לא תיקון הקיימת)
- **שימוש בקוד קיים** רק לחלקים ספציפיים (ראה טבלת Reuse)
- **UI נשאר זהה** פרט לשינויים הנדרשים (5 כפתורים)
- **לוגיקת Zero Sales** נשארת זהה לחלוטין

### לוח זמנים
- **Phase A**: UI מלא (2 ימים)
- **Phase B**: לוגיקה עסקית (3 ימים)
- **סה"כ**: 5 ימי עבודה

## Phase A: UI עם Mock Data (2 ימים)

### A1: שלד בסיסי (2 שעות)

**מה לבנות:**
```
app/
├── main.py              # נקודת כניסה
├── ui/
│   ├── page.py         # עמוד ראשי
│   └── layout.py       # עיצוב
└── .streamlit/
    └── config.toml     # הגדרות
```

**לקחת מהקיים:**
- config.toml - העתקה מלאה
- layout.py - הסטייל והצבעים

**קריטריונים:**
- [ ] האפליקציה עולה
- [ ] כותרת "BID OPTIMIZER"
- [ ] רקע לבן, כפתורים אדומים

### A2: Upload Section (3 שעות)

**מה לבנות:**
```
ui/
├── panels/
│   └── upload_panel.py
└── components/
    ├── file_cards.py    # כרטיסי 5 קבצים
    ├── checklist.py
    └── buttons.py
```

**לקחת מהקיים:**
- checklist.py - רשימת 14 אופטימיזציות
- buttons.py - סטייל כפתורים

**שינויים נדרשים:**
- 5 כפתורי העלאה במקום 1
- סטטוס נפרד לכל קובץ

**קריטריונים:**
- [ ] 5 כפתורי העלאה נפרדים
- [ ] Download Template עובד
- [ ] 14 אופטימיזציות בצ'קליסט

### A3: Validation Section (2 שעות)

**מה לבנות:**
```
ui/
├── panels/
│   └── validate_panel.py
└── components/
    ├── alerts.py
    └── validation_messages.py
```

**לקחת מהקיים:**
- alerts.py - מבנה ההודעות
- צבעים וסטייל

**קריטריונים:**
- [ ] הודעות לכל אופטימיזציה
- [ ] תצוגת Missing Portfolios
- [ ] כפתור Process Files

### A4: Output Section (2 שעות)

**מה לבנות:**
```
ui/
├── panels/
│   └── output_panel.py
└── components/
    ├── progress_bar.py
    └── download_buttons.py
```

**לקחת מהקיים:**
- progress_bar.py - אנימציה
- סטייל כפתורי הורדה

**קריטריונים:**
- [ ] Progress bar עובד
- [ ] 2 כפתורי הורדה
- [ ] Pink notice box
- [ ] New Processing button

### A5: Mock Data & State (3 שעות)

**מה לבנות:**
```
app/
└── state/
    ├── session.py
    └── mock_data.py
tests/
└── fixtures/
    ├── mock_template.py
    ├── mock_bulk.py
    └── mock_scenarios.py
```

**תרחישי Mock:**
1. Valid - הכל תקין
2. Missing - פורטפוליוז חסרים
3. Large - קובץ גדול
4. Invalid - שגיאות

**קריטריונים:**
- [ ] 4 תרחישי בדיקה עובדים
- [ ] State management תקין
- [ ] מעברים בין מצבים

## Phase B: החלפת Mock בלוגיקה אמיתית (3 ימים)

### B1: File Readers (3 שעות)

**מה לבנות:**
```
data/
└── readers/
    ├── excel_reader.py
    └── csv_reader.py
```

**לקחת מהקיים:**
- excel_reader.py - קוד קריאה
- csv_reader.py - קוד קריאה
- ולידציות בסיסיות

**קריטריונים:**
- [ ] קריאת Excel עובדת
- [ ] קריאת CSV עובדת
- [ ] בדיקת 48 עמודות

### B2: Optimization Framework (4 שעות)

**מה לבנות:**
```
business/
└── optimizations/
    └── base_optimization.py
```

**לבנות מאפס:**
- BaseOptimization class
- ValidationResult model
- ממשק לאופטימיזציות

**קריטריונים:**
- [ ] מחלקת בסיס מוגדרת
- [ ] ממשק ברור
- [ ] תמיכה בירושה

### B3: Zero Sales Implementation (4 שעות)

**מה לבנות:**
```
business/
└── optimizations/
    └── zero_sales/
        ├── __init__.py
        ├── validator.py
        ├── cleaner.py
        └── processor.py
```

**לקחת מהקיים:**
- **כל הנוסחאות והחישובים** - העתקה מדויקת
- לוגיקת 4 המקרים
- חישובי calc1, calc2
- לוגיקת Max BA

**לבנות מאפס:**
- מבנה המודול
- הפרדה לקבצים
- ולידציה ספציפית

**קריטריונים:**
- [ ] ולידציה עובדת
- [ ] ניקוי נתונים נכון
- [ ] חישובים זהים לקיים
- [ ] תוצאות נכונות

### B4: File Generation (3 שעות)

**מה לבנות:**
```
business/
└── processors/
    └── file_generator.py
data/
└── writers/
    └── output_writer.py
utils/
└── filename_generator.py
```

**לקחת מהקיים:**
- output_writer.py - כתיבת Excel
- filename_generator.py - פורמט שמות

**קריטריונים:**
- [ ] Working file נוצר
- [ ] Clean file נוצר
- [ ] שמות דינמיים
- [ ] לשוניות נכונות

### B5: Integration & Orchestrator (4 שעות)

**מה לבנות:**
```
business/
└── services/
    └── orchestrator.py
```

**לבנות מאפס:**
- תיאום בין רכיבים
- ניהול זרימה
- טיפול בשגיאות

**קריטריונים:**
- [ ] זרימה מלאה עובדת
- [ ] ולידציות רצות
- [ ] עיבוד מצליח
- [ ] קבצים נוצרים

## טבלת Reuse - מה לקחת מהקוד הקיים

| רכיב | לקחת ✅ | לבנות מחדש ❌ | הערות |
|------|---------|----------------|--------|
| **UI Layout** | ✅ | | סטייל וצבעים זהים |
| **Session State Structure** | | ❌ | מבנה חדש ל-5 קבצים |
| **File Readers** | ✅ | | קוד קריאת קבצים |
| **Template Generator** | ✅ | | + לשונית Top ASINs |
| **Zero Sales Formulas** | ✅ | | העתקה מדויקת |
| **Zero Sales Structure** | | ❌ | מבנה תיקיות חדש |
| **Validation Logic** | | ❌ | ולידציה בתוך כל אופטימיזציה |
| **Orchestrator** | | ❌ | לוגיקה חדשה |
| **Output Writer** | ✅ | | כתיבת Excel |
| **Filename Generator** | ✅ | | פורמט שמות |
| **Progress Bar** | ✅ | | אנימציה |
| **Constants** | ✅ | | + עדכון ל-5 קבצים |

## קריטריונים כלליים להצלחה

### UI (סוף Phase A)
- [ ] כל ה-UI עובד עם Mock Data
- [ ] ניתן לבדוק כל תרחיש
- [ ] מעברים חלקים בין מצבים
- [ ] עיצוב זהה לקיים

### Backend (סוף Phase B)
- [ ] קבצים אמיתיים נקראים
- [ ] Zero Sales מחשב נכון
- [ ] קבצי פלט תקינים
- [ ] ביצועים סבירים (<10 שניות)

### End-to-End
- [ ] העלאה → ולידציה → עיבוד → הורדה
- [ ] קבצים נפתחים ב-Excel
- [ ] ניתן לטעון חזרה ל-Amazon
- [ ] Reset מנקה הכל

## הערות חשובות

1. **לא לשנות את לוגיקת Zero Sales** - העתקה מדויקת של החישובים
2. **לשמור על העיצוב הקיים** - רק שינויים הכרחיים
3. **Mock Data קודם** - בדיקה מלאה לפני לוגיקה
4. **בדיקות בכל שלב** - לא להמשיך עם באגים

## סיכום

- **5 ימי עבודה** לאפליקציה מלאה
- **UI ננעל** אחרי יומיים
- **Zero Sales** בלבד בשלב ראשון
- **קוד נקי** ומודולרי מההתחלה