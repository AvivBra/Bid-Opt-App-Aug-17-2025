# עץ קבצי קוד מתוקן - Bid Optimizer
## תאריך: דצמבר 2024, 11:40

```
bid-optimizer/
├── app/
│   ├── main.py
│   ├── navigation.py
│   ├── pages/
│   │   └── bid_optimizer.py
│   ├── ui/
│   │   ├── layout.py
│   │   ├── sidebar.py
│   │   ├── shared/
│   │   │   ├── upload_section.py
│   │   │   ├── validation_section.py
│   │   │   ├── output_section.py
│   │   │   └── page_header.py
│   │   └── components/
│   │       ├── file_cards.py
│   │       ├── checklist.py
│   │       ├── buttons.py
│   │       ├── alerts.py
│   │       ├── progress_bar.py
│   │       └── download_buttons.py
│   └── state/
│       ├── session_manager.py
│       ├── bid_state.py
│       └── mock_data.py
│
├── business/
│   ├── common/
│   │   ├── portfolio_filter.py
│   │   └── excluded_portfolios.py
│   ├── bid_optimizations/
│   │   ├── base_optimization.py
│   │   └── zero_sales/
│   │       ├── validator.py
│   │       ├── cleaner.py
│   │       ├── processor.py
│   │       └── orchestrator.py
│   └── processors/
│       └── output_formatter.py
│
├── data/
│   ├── readers/
│   │   ├── excel_reader.py
│   │   └── csv_reader.py
│   ├── writers/
│   │   └── excel_writer.py
│   ├── validators/
│   │   ├── template_validator.py
│   │   ├── bulk_validator.py
│   │   └── portfolio_validator.py
│   └── template_generator.py
│
├── config/
│   ├── constants.py
│   ├── settings.py
│   ├── ui_text.py
│   └── optimization_config.py
│
├── utils/
│   ├── file_utils.py
│   ├── filename_generator.py
│   └── page_utils.py
│
├── tests/
│   ├── unit/
│   │   └── test_zero_sales.py
│   ├── integration/
│   │   └── test_bid_flow.py
│   └── fixtures/
│       ├── valid_template.xlsx
│       └── valid_bulk_60.xlsx
│
├── requirements.txt
├── README.md
└── .streamlit/
    └── config.toml
```

## הערות

### קבצים שהוסרו:
- `config/navigation.py` - כפילות עם `app/navigation.py`
- `data/models/` - תיקייה מיותרת

### קבצים שנוספו:
- `requirements.txt` - רשימת תלויות Python
- `README.md` - תיעוד למפתח
- `.streamlit/config.toml` - הגדרות Streamlit

### מבנה התיקיות:
- **app/** - ממשק משתמש וניווט
- **business/** - לוגיקה עסקית
- **data/** - קריאה וכתיבת קבצים
- **config/** - הגדרות וקבועים
- **utils/** - פונקציות עזר
- **tests/** - בדיקות

## Phase 1 - Zero Sales Only
כל הקבצים לעיל נדרשים לפיתוח Phase 1.
אין קבצי TBC או תיקיות ריקות.