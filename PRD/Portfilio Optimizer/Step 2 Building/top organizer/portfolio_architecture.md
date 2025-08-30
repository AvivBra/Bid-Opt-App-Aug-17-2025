# Portfolio Optimizer - ארכיטקטורת קבצים מעודכנת
**תאריך:** 29/08/2025  
**שעה:** 17:35

## עץ קבצים מעודכן

```
├── app
│   ├── components
│   │   ├── bid_optimizer.py
│   │   ├── campaign_optimizer.py
│   │   └── portfolio_optimizer.py                    [✏️ עריכה]
│   ├── state
│   │   ├── bid_state.py
│   │   ├── campaign_state.py
│   │   ├── portfolio_state.py                        [✏️ עריכה]
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
│   │   ├── empty_portfolios
│   │   │   ├── __init__.py
│   │   │   ├── cleaner.py
│   │   │   ├── constants.py
│   │   │   ├── orchestrator.py
│   │   │   ├── output_formatter.py
│   │   │   ├── processor.py
│   │   │   └── validator.py
│   │   ├── zero_sales
│   │   │   ├── cleaner.py
│   │   │   ├── orchestrator.py
│   │   │   ├── processor.py
│   │   │   └── validator.py
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
│   ├── portfolio_optimizations
│   │   ├── campaigns_without_portfolios
│   │   │   ├── __init__.py
│   │   │   ├── cleaner.py
│   │   │   ├── constants.py
│   │   │   ├── orchestrator.py
│   │   │   ├── output_formatter.py
│   │   │   ├── processor.py
│   │   │   └── validator.py
│   │   ├── empty_portfolios
│   │   │   ├── __init__.py
│   │   │   ├── cleaner.py
│   │   │   ├── constants.py
│   │   │   ├── orchestrator.py
│   │   │   ├── output_formatter.py
│   │   │   ├── processor.py
│   │   │   └── validator.py
│   │   ├── top_non_top_organization           [🆕 תיקייה חדשה]
│   │   │   ├── __init__.py                    [🆕 קובץ חדש]
│   │   │   ├── cleaner.py                     [🆕 קובץ חדש]
│   │   │   ├── constants.py                   [🆕 קובץ חדש]
│   │   │   ├── orchestrator.py                [🆕 קובץ חדש]
│   │   │   ├── output_formatter.py            [🆕 קובץ חדש]
│   │   │   ├── processor.py                   [🆕 קובץ חדש]
│   │   │   └── validator.py                   [🆕 קובץ חדש]
│   │   ├── __init__.py
│   │   ├── factory.py                         [✏️ עריכה]
│   │   ├── portfolio_base_optimization.py
│   │   └── results_manager.py
│   └── processors
│       ├── excel_base_formatter.py
│       └── output_formatter.py
├── config
│   ├── campaign_config.py
│   ├── constants.py
│   ├── optimization_config.py                 [✏️ עריכה]
│   ├── portfolio_config.py                    [✏️ עריכה]
│   ├── settings.py
│   └── ui_text.py
├── data
│   ├── readers
│   │   ├── csv_reader.py
│   │   └── excel_reader.py
│   ├── validators
│   │   ├── bulk_validator.py
│   │   ├── campaign_validators.py
│   │   ├── portfolio_validator.py
│   │   └── template_validator.py              [✏️ עריכה]
│   ├── writers
│   │   ├── campaign_bulk_writer.py
│   │   └── excel_writer.py
│   ├── campaign_template_generator.py
│   └── template_generator.py
├── utils
│   ├── file_utils.py
│   ├── filename_generator.py
│   └── page_utils.py
├── BidOptimizer.command
├── readme-file.md
└── requirements.txt
```

## מקרא

| סימן | משמעות |
|------|---------|
| 🆕 | קובץ/תיקייה חדשים |
| ✏️ | קובץ שדורש עריכה |
| (ללא סימן) | קובץ קיים ללא שינוי |