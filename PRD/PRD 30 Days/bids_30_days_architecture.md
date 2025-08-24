# ארכיטקטורת קבצים - הצעה ל-Bids 30 Days
**תאריך: 17/08/2025 07:10**

## עץ קבצים עם סימונים

```
├── app
│   ├── pages
│   │   └── bid_optimizer.py [לערוך]
│   ├── state
│   │   ├── bid_state.py [לערוך]
│   │   └── session_manager.py [לערוך]
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
│   │   │   └── validation_section.py [לערוך]
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
│   │   │   └── validator.py [חדש]
│   │   └── base_optimization.py
│   ├── common
│   │   ├── excluded_portfolios.py
│   │   ├── numeric_validator_py.py
│   │   ├── portfolio_filter.py
│   │   └── state_validator_py.py
│   └── processors
│       └── output_formatter.py [לערוך]
├── claude
│   └── settings.local.json
├── config
│   ├── constants.py [לערוך]
│   ├── optimization_config.py [לערוך]
│   ├── settings.py
│   └── ui_text.py [לערוך]
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
- ללא סימון - קובץ קיים שלא דורש שינוי

## סיכום השינויים

### קבצים חדשים (6):
- תיקייה חדשה: `business/bid_optimizations/bids_30_days/`
- 5 קבצים חדשים בתיקייה זו:
  - `__init__.py` - קובץ אתחול
  - `cleaner.py` - לוגיקת ניקוי נתונים
  - `orchestrator.py` - מתאם האופטימיזציה
  - `processor.py` - עיבוד הנתונים
  - `validator.py` - ולידציה

### קבצים לעריכה (10):
- **קבצי UI** (5): להוספת האופטימיזציה החדשה ברשימה ובטפסים
- **קבצי State** (2): לניהול מצב של Bulk 30
- **קבצי Config** (3): להגדרות האופטימיזציה החדשה
- **Output Formatter** (1): לטיפול בפלט החדש