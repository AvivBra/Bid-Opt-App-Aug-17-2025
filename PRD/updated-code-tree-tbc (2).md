# עץ קבצי קוד מעודכן - Sidebar Architecture
## תאריך: 18 באוגוסט 2025, 12:57

## הערה חשובה
כל הקבצים שהם בסטטוס פיתוח עתידי **לא קיימים בפרויקט**. אין קבצי דמה, אין תיקיות ריקות.

```
bid-optimizer/
├── app/
│   ├── main.py
│   ├── navigation.py
│   │
│   ├── pages/
│   │   ├── __init__.py
│   │   └── bid_optimizer.py
│   │
│   ├── ui/
│   │   ├── layout.py
│   │   ├── sidebar.py
│   │   │
│   │   ├── shared/
│   │   │   ├── __init__.py
│   │   │   ├── upload_section.py
│   │   │   ├── validation_section.py
│   │   │   ├── output_section.py
│   │   │   └── page_header.py
│   │   │
│   │   └── components/
│   │       ├── __init__.py
│   │       ├── file_cards.py
│   │       ├── checklist.py
│   │       ├── buttons.py
│   │       ├── alerts.py
│   │       ├── progress_bar.py
│   │       └── download_buttons.py
│   │
│   └── state/
│       ├── __init__.py
│       ├── session_manager.py
│       ├── bid_state.py
│       └── mock_data.py
│
├── business/
│   ├── __init__.py
│   │
│   ├── common/
│   │   ├── __init__.py
│   │   ├── portfolio_filter.py
│   │   └── excluded_portfolios.py
│   │
│   ├── bid_optimizations/
│   │   ├── __init__.py
│   │   ├── base_optimization.py
│   │   └── zero_sales/
│   │       ├── __init__.py
│   │       ├── validator.py
│   │       ├── cleaner.py
│   │       ├── processor.py
│   │       └── orchestrator.py    # מנהל את תהליך Zero Sales
│   │
│   └── processors/
│       ├── __init__.py
│       └── output_formatter.py    # פורמט הפלט בלבד
│
├── data/
│   ├── __init__.py
│   ├── readers/
│   │   ├── __init__.py
│   │   ├── excel_reader.py
│   │   └── csv_reader.py
│   │
│   ├── writers/
│   │   ├── __init__.py
│   │   └── excel_writer.py        # כותב Working File (בעתיד גם Clean)
│   │
│   ├── validators/
│   │   ├── __init__.py
│   │   ├── template_validator.py
│   │   ├── bulk_validator.py
│   │   └── portfolio_validator.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── portfolio.py
│   │   └── validation_result.py
│   │
│   └── template_generator.py
│
├── config/
│   ├── __init__.py
│   ├── constants.py               # קבועים טכניים
│   ├── navigation.py              # הגדרות ניווט
│   ├── settings.py                # הגדרות כלליות
│   ├── ui_text.py                # טקסטים למשתמש
│   └── optimization_config.py    # הגדרות אופטימיזציות
│
├── utils/
│   ├── __init__.py
│   ├── file_utils.py
│   ├── filename_generator.py
│   └── page_utils.py
│
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   └── test_zero_sales.py
│   │
│   ├── integration/
│   │   └── test_bid_flow.py      # Upload→Validation→Output
│   │
│   └── fixtures/
│       ├── valid_template.xlsx
│       └── valid_bulk_60.xlsx
│
├── docs/
│   └── adr-0001-future-expansions.md  # תיעוד הרחבות עתידיות
│
├── .streamlit/
│   └── config.toml
│
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini                     # כולל -k "not tbc"
├── .gitignore
└── README.md
```

## מה קיים בפועל:
- **Bid Optimizer** עם Zero Sales בלבד
- **Working File** בלבד (לא Clean File)
- **Bulk 60** בלבד (לא 7/30)
- **Template ו-Bulk** upload (4 כפתורים מתוך 5)
- **10 Flat Portfolios** filtering
- **Sidebar** navigation (ללא Stepper)

## מה לא קיים (ומתועד ב-ADR):
- 13 אופטימיזציות נוספות
- עמוד שני בניווט
- Clean File
- Data Rova integration
- Bulk 7/30 support