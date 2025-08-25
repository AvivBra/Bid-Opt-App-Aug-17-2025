# ארכיטקטורת קבצים - הצעה ל-Bids 30 Days
**תאריך: 17/08/2025 13:00**

## עץ קבצים עם סימונים

```
├── app
│   ├── pages
│   │   └── bid_optimizer.py [לערוך]
│   ├── state
│   │   ├── bid_state.py [לערוך - ניהול סשן משותף]
│   │   └── session_manager.py
│   ├── ui
│   │   ├── components
│   │   │   ├── alerts.py
│   │   │   ├── buttons.py
│   │   │   ├── checklist.py [לערוך]
│   │   │   ├── download_buttons.py
│   │   │   ├── file_cards.py
│   │   │   └── progress_bar.py
│   │   ├── shared
│   │   │   ├── output_section.py
│   │   │   ├── page_header.py
│   │   │   ├── upload_section.py [לערוך]
│   │   │   └── validation_section.py
│   │   ├── layout.py
│   │   └── sidebar_backup.py
│   ├── main.py
│   └── navigation.py
├── business
│   ├── bid_optimizations
│   │   ├── zero_sales
│   │   │   ├── cleaner.py
│   │   │   ├── orchestrator.py
│   │   │   ├── processor.py
│   │   │   └── validator.py
│   │   ├── bids_30_days [חדש]
│   │   │   ├── __init__.py [חדש]
│   │   │   ├── cleaner.py [חדש]
│   │   │   ├── orchestrator.py [חדש]
│   │   │   ├── processor.py [חדש]
│   │   │   ├── validator.py [חדש]
│   │   │   ├── output_formatter_30_days.py [חדש]
│   │   │   └── constants.py [חדש]
│   │   └── base_optimization.py
│   ├── common
│   │   ├── excluded_portfolios.py
│   │   ├── numeric_validator_py.py
│   │   ├── portfolio_filter.py
│   │   └── state_validator_py.py
│   └── processors
│       └── output_formatter.py
├── claude
│   └── settings.local.json
├── config
│   ├── constants.py
│   ├── optimization_config.py [לערוך]
│   ├── settings.py
│   └── ui_text.py
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

## מקרא

- **[חדש]** - קובץ חדש שיש להוסיף
- **[לערוך]** - קובץ קיים שדורש עריכה
- **[לערוך - ניהול סשן משותף]** - דגש מיוחד על ניהול נתוני סשן משותפים
- ללא סימון - קובץ קיים שלא דורש שינוי

## סיכום השינויים

### קבצים חדשים (8):
- תיקייה חדשה: `business/bid_optimizations/bids_30_days/`
- 7 קבצים חדשים בתיקייה זו:
  - `__init__.py` - קובץ אתחול
  - `cleaner.py` - לוגיקת ניקוי נתונים
  - `orchestrator.py` - מתאם האופטימיזציה
  - `processor.py` - עיבוד הנתונים
  - `validator.py` - ולידציה
  - `output_formatter_30_days.py` - פורמט פלט ספציפי (כולל צביעת עמודות)
  - `constants.py` - קבועים ספציפיים לאופטימיזציה

### קבצים לעריכה (5):
- **קבצי UI** (2): 
  - `checklist.py` - להוספת האופטימיזציה החדשה ברשימה
  - `upload_section.py` - להפעלת כפתור Bulk 30
- **קבצי State** (1): 
  - `bid_state.py` - **לניהול מצב משותף של Bulk data עם ניקוי בעת החלפת אופטימיזציה**
- **קבצי Config** (1): 
  - `optimization_config.py` - להגדרות האופטימיזציה החדשה
- **קובץ ראשי** (1):
  - `bid_optimizer.py` - לחיבור האופטימיזציה החדשה

## הערות ניהול סשן

### נתוני Template
- נשמרים במפתח: `template_df`
- משותפים לשתי האופטימיזציות
- לא נמחקים בעת החלפת אופטימיזציה

### נתוני Bulk
- נשמרים במפתח משותף: `bulk_data`
- מוחלפים בעת החלפת אופטימיזציה (60 או 30 ימים)
- נמחקים אוטומטית בעת בחירת אופטימיזציה שונה

### זרימת ניקוי סשן
1. משתמש בוחר אופטימיזציה חדשה
2. המערכת מנקה את `bulk_data` הקיים
3. כפתורי Upload מתעדכנים בהתאם לבחירה
4. משתמש מעלה קובץ Bulk חדש המתאים לאופטימיזציה