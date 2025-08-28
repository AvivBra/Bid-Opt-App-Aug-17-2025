# איפיון עץ קבצים מלא - Empty Portfolios Optimization
## תאריך: 28/08/2025 | שעה: 19:30

```
├── app
│   ├── components
│   │   ├── bid_optimizer.py [לערוך - הוספת Empty Portfolios לרשימת האופטימיזציות]
│   │   └── campaign_optimizer.py
│   ├── state
│   │   ├── bid_state.py [לערוך - הוספת state עבור Empty Portfolios]
│   │   ├── campaign_state.py
│   │   └── session_manager.py
│   ├── ui
│   │   ├── components
│   │   │   ├── alerts.py
│   │   │   ├── buttons.py
│   │   │   ├── checklist.py
│   │   │   ├── download_buttons.py
│   │   │   ├── file_cards.py
│   │   │   └── progress_bar.py
│   │   ├── shared
│   │   │   ├── output_section.py
│   │   │   ├── page_header.py
│   │   │   ├── upload_section.py
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
│   │   ├── bids_60_days
│   │   │   ├── __init__.py
│   │   │   ├── cleaner.py
│   │   │   ├── constants.py
│   │   │   ├── orchestrator.py
│   │   │   ├── output_formatter.py
│   │   │   └── processor.py
│   │   ├── zero_sales
│   │   │   ├── cleaner.py
│   │   │   ├── orchestrator.py
│   │   │   ├── processor.py
│   │   │   └── validator.py
│   │   ├── empty_portfolios [תיקייה חדשה]
│   │   │   ├── __init__.py [קובץ חדש]
│   │   │   ├── cleaner.py [קובץ חדש]
│   │   │   ├── constants.py [קובץ חדש]
│   │   │   ├── orchestrator.py [קובץ חדש]
│   │   │   ├── processor.py [קובץ חדש]
│   │   │   ├── output_formatter.py [קובץ חדש]
│   │   │   └── validator.py [קובץ חדש]
│   │   └── base_optimization.py
│   ├── campaign_creator
│   │   ├── processors
│   │   │   ├── __init__.py
│   │   │   ├── base_processor.py
│   │   │   ├── halloween_testing.py
│   │   │   ├── keyword_processor.py
│   │   │   └── product_targeting_processor.py
│   │   ├── validators
│   │   │   ├── __init__.py
│   │   │   ├── base_validator.py
│   │   │   ├── halloween_testing.py
│   │   │   ├── keyword_validator.py
│   │   │   └── product_targeting_validator.py
│   │   ├── __init__.py
│   │   ├── builder.py
│   │   ├── constants.py
│   │   ├── data_dive_reader.py
│   │   ├── data_rova_reader.py
│   │   ├── formatter.py
│   │   ├── orchestrator.py
│   │   ├── session_builder.py
│   │   └── validation.py
│   ├── common
│   │   ├── excluded_portfolios.py
│   │   ├── numeric_validator_py.py
│   │   ├── portfolio_filter.py
│   │   └── state_validator_py.py
│   └── processors
│       ├── excel_base_formatter.py
│       └── output_formatter.py
├── config
│   ├── campaign_config.py
│   ├── constants.py
│   ├── optimization_config.py [לערוך - הוספת EMPTY_PORTFOLIOS_CONFIG]
│   ├── settings.py
│   └── ui_text.py [לערוך - הוספת טקסטים עבור Empty Portfolios]
├── data
│   ├── readers
│   │   ├── csv_reader.py
│   │   └── excel_reader.py
│   ├── validators
│   │   ├── bulk_validator.py
│   │   ├── campaign_validators.py
│   │   ├── portfolio_validator.py
│   │   └── template_validator.py
│   ├── writers
│   │   ├── campaign_bulk_writer.py
│   │   └── excel_writer.py
│   ├── campaign_template_generator.py
│   └── template_generator.py
├── utils
│   ├── file_utils.py
│   ├── filename_generator.py
│   └── page_utils.py
├── readme-file.md
└── requirements.txt
```