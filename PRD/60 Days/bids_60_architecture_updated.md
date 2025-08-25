# ארכיטקטורת קבצים - הוספת Bids 60 Days Optimization
**תאריך: 17/08/2025 20:30**

## עץ קבצים מעודכן עם סימונים

```
├── app
│   ├── pages
│   │   └── bid_optimizer.py [לעדכון]
│   ├── state
│   │   ├── bid_state.py [לעדכון]
│   │   └── session_manager.py
│   ├── ui
│   │   ├── components
│   │   │   ├── alerts.py
│   │   │   ├── buttons.py
│   │   │   ├── checklist.py [לעדכון]
│   │   │   ├── download_buttons.py
│   │   │   ├── file_cards.py
│   │   │   └── progress_bar.py
│   │   ├── shared
│   │   │   ├── output_section.py [לעדכון]
│   │   │   ├── page_header.py
│   │   │   ├── upload_section.py [לעדכון]
│   │   │   └── validation_section.py
│   │   ├── layout.py
│   │   └── sidebar_backup.py
│   ├── main.py
│   └── navigation.py
├── business
│   ├── bid_optimizations
│   │   ├── bids_30_days
│   │   │   ├── __init__.py
│   │   │   ├── cleaner.py
│   │   │   ├── constants.py
│   │   │   ├── orchestrator.py
│   │   │   ├── output_formatter_30_days.py
│   │   │   ├── processor.py
│   │   │   └── validator.py
│   │   ├── bids_60_days [חדש - תיקייה]
│   │   │   ├── __init__.py [חדש]
│   │   │   ├── cleaner.py [חדש]
│   │   │   ├── constants.py [חדש]
│   │   │   ├── orchestrator.py [חדש]
│   │   │   ├── output_formatter_60_days.py [חדש]
│   │   │   └── processor.py [חדש]
│   │   ├── zero_sales
│   │   │   ├── cleaner.py
│   │   │   ├── orchestrator.py
│   │   │   ├── processor.py
│   │   │   └── validator.py
│   │   └── base_optimization.py
│   ├── common
│   │   ├── excluded_portfolios.py
│   │   ├── numeric_validator_py.py
│   │   ├── portfolio_filter.py
│   │   └── state_validator_py.py
│   └── processors
│       ├── excel_base_formatter.py
│       └── output_formatter.py
├── claude
│   └── settings.local.json
├── config
│   ├── constants.py
│   ├── optimization_config.py [לעדכון]
│   ├── settings.py
│   └── ui_text.py [לעדכון]
├── data
│   ├── readers
│   │   ├── csv_reader.py
│   │   └── excel_reader.py
│   ├── validators
│   │   ├── bulk_validator.py
│   │   ├── portfolio_validator.py
│   │   └── template_validator.py
│   ├── writers
│   │   └── excel_writer.py
│   └── template_generator.py
├── utils
│   ├── file_utils.py
│   ├── filename_generator.py
│   └── page_utils.py
├── readme-file.md
├── requirements.txt
└── simple_test_top_nav.py
```

## מקרא סימונים

- **[חדש]** - קובץ חדש שיש להוסיף
- **[חדש - תיקייה]** - תיקייה חדשה שיש ליצור
- **[לעדכון]** - קובץ קיים שדורש עדכון

## סיכום השינויים

### קבצים חדשים (7):
מודול חדש לאופטימיזציית Bids 60 Days:
- `business/bid_optimizations/bids_60_days/` - תיקייה חדשה
- `__init__.py` - קובץ אתחול למודול
- `cleaner.py` - לוגיקת ניקוי לנתוני 60 יום
- `constants.py` - קבועים ספציפיים ל-60 יום
- `orchestrator.py` - מתאם האופטימיזציה
- `output_formatter_60_days.py` - פורמט פלט ייחודי
- `processor.py` - לוגיקת עיבוד ל-60 יום

### קבצים לעדכון (6):
- **app/pages/bid_optimizer.py** - הוספת תמיכה באופטימיזציה החדשה
- **app/state/bid_state.py** - ניהול מצב עבור Bulk 60 (מקביל ל-Bulk 30)
- **app/ui/components/checklist.py** - הוספת checkbox ל-"Bids 60 Days"
- **app/ui/shared/upload_section.py** - הפעלת כפתור "Upload Bulk 60" עבור Bids 60
- **app/ui/shared/output_section.py** - הצגת סטטיסטיקות ספציפיות ל-60 יום
- **config/optimization_config.py** - הגדרות קונפיגורציה ל-Bids 60 Days
- **config/ui_text.py** - טקסטים למשתמש עבור האופטימיזציה החדשה

## הערות ארכיטקטוניות

### 1. הפרדה מודולרית
- כל אופטימיזציה (Zero Sales, Bids 30, Bids 60) בתיקייה נפרדת
- ירושה מ-`base_optimization.py` לקוד משותף
- שימוש חוזר בקומפוננטות משותפות מ-`business/common/`
- **וולידציה משתמשת בקבצי הוולידציה הגלובליים ב-`data/validators/`**

### 2. ניהול מצב סשן
- Template משותף לכל האופטימיזציות
- Bulk data נפרד לכל אופטימיזציה:
  - `bulk_60` עבור Zero Sales
  - `bulk_30` עבור Bids 30 Days  
  - `bulk_60_bids` עבור Bids 60 Days (להבדיל מ-Zero Sales)
- ניקוי אוטומטי בעת החלפת אופטימיזציה

### 3. ממשק משתמש
- רק אופטימיזציה אחת פעילה בכל רגע
- כפתורי Upload מותאמים לאופטימיזציה שנבחרה:
  - Zero Sales → Bulk 60
  - Bids 30 Days → Bulk 30
  - Bids 60 Days → Bulk 60 (Bids)

### 4. זרימת נתונים
```
Template (משותף) + Bulk (ספציפי) 
    ↓
Validation (קבצים גלובליים)
    ↓
Cleaning (ספציפי לאופטימיזציה)
    ↓
Processing (ספציפי לאופטימיזציה)
    ↓
Output Formatting (ספציפי לאופטימיזציה)
    ↓
Excel File
```

## המלצות ליישום

1. **שלב ראשון:** יצירת תשתית המודול החדש (תיקייה + orchestrator + constants)
2. **שלב שני:** מימוש cleaner (ירושה/שימוש חוזר במידת האפשר)
3. **שלב שלישי:** מימוש processor עם הלוגיקה הספציפית ל-60 יום
4. **שלב רביעי:** עדכון ממשק המשתמש (checklist + upload section)
5. **שלב חמישי:** עדכון ניהול מצב וקונפיגורציה
6. **שלב שישי:** בדיקות אינטגרציה מקצה לקצה

## הבדלים צפויים בין Bids 30 ל-Bids 60

- **תקופת נתונים:** 60 יום במקום 30
- **קריטריונים לסינון:** סף שונה ל-units/clicks
- **חישובי Bid:** נוסחאות מותאמות לתקופה ארוכה
- **Target CPA:** אולי חישוב שונה של Adj. CPA
- **Max BA:** אולי לוגיקה שונה לחישוב Maximum Bid Adjustment
- **גיליונות פלט:** מבנה דומה אך עם התאמות ספציפיות