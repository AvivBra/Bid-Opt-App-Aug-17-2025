# עץ פרויקט מעודכן - Bid Optimizer

```
bid-optimizer/
├── app/
│   ├── main.py
│   ├── ui/
│   │   ├── page_single.py
│   │   ├── panels/
│   │   │   ├── __init__.py
│   │   │   ├── upload_panel.py
│   │   │   ├── validate_panel.py
│   │   │   └── output_panel.py
│   │   ├── components/
│   │   │   ├── __init__.py
│   │   │   ├── checklist.py
│   │   │   ├── file_cards.py
│   │   │   ├── alerts.py
│   │   │   └── buttons.py
│   │   └── layout.py
│   └── state/
│       ├── __init__.py
│       ├── session.py
│       └── mock_data.py
├── business/
│   ├── __init__.py
│   ├── processors/
│   │   ├── __init__.py
│   │   └── file_generator.py
│   ├── optimizations/
│   │   ├── __init__.py
│   │   ├── base_optimization.py
│   │   ├── zero_sales/
│   │   │   ├── __init__.py
│   │   │   ├── validator.py
│   │   │   ├── cleaner.py
│   │   │   └── processor.py
│   │   ├── portfolio_bid/
│   │   │   ├── __init__.py
│   │   │   ├── validator.py
│   │   │   ├── cleaner.py
│   │   │   └── processor.py
│   │   ├── budget_optimization/
│   │   │   ├── __init__.py
│   │   │   ├── validator.py
│   │   │   ├── cleaner.py
│   │   │   └── processor.py
│   │   └── [11 תיקיות אופטימיזציות נוספות עם אותו מבנה]
│   └── services/
│       ├── __init__.py
│       └── orchestrator.py
├── data/
│   ├── __init__.py
│   ├── readers/
│   │   ├── __init__.py
│   │   ├── excel_reader.py
│   │   └── csv_reader.py
│   ├── writers/
│   │   ├── __init__.py
│   │   └── output_writer.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── portfolio.py
│   │   └── validation_result.py
│   └── template_generator.py
├── config/
│   ├── __init__.py
│   ├── constants.py
│   ├── settings.py
│   └── ui_text.py
├── utils/
│   ├── __init__.py
│   ├── file_utils.py
│   └── filename_generator.py
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_readers.py
│   │   ├── test_writers.py
│   │   ├── test_optimizations.py
│   │   ├── test_file_generator.py
│   │   └── test_orchestrator.py
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_upload_flow.py
│   │   ├── test_processing_flow.py
│   │   └── test_end_to_end.py
│   ├── fixtures/
│   │   ├── valid_template.xlsx
│   │   ├── valid_bulk_30.xlsx
│   │   ├── valid_bulk_60.xlsx
│   │   ├── valid_bulk_7.xlsx
│   │   ├── valid_data_rova.xlsx
│   │   └── mock_scenarios.py
│   └── conftest.py
├── .streamlit/
│   └── config.toml
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── .gitignore
└── README.md
```