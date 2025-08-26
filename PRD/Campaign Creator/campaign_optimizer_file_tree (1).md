# עץ קבצים - Campaign Optimizer
**תאריך:** 26.08.2025  
**שעה:** 15:40

## עץ קבצים מעודכן

```
├── app
│   ├── components
│   │   ├── bid_optimizer.py
│   │   └── campaign_optimizer.py 📝
│   ├── state
│   │   ├── bid_state.py
│   │   ├── campaign_state.py 📝
│   │   └── session_manager.py 📝
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
│   ├── main.py 📝
│   └── navigation.py 📝
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
│   │   └── base_optimization.py
│   ├── campaign_creator 🆕
│   │   ├── __init__.py 🆕
│   │   ├── constants.py 🆕
│   │   ├── orchestrator.py 🆕
│   │   ├── template_validator.py 🆕
│   │   ├── output_formatter.py 🆕
│   │   ├── testing 🆕
│   │   │   ├── __init__.py 🆕
│   │   │   ├── processor.py 🆕
│   │   │   └── cleaner.py 🆕
│   │   ├── testing_pt 🆕
│   │   │   ├── __init__.py 🆕
│   │   │   ├── processor.py 🆕
│   │   │   └── cleaner.py 🆕
│   │   ├── phrase 🆕
│   │   │   ├── __init__.py 🆕
│   │   │   ├── processor.py 🆕
│   │   │   └── cleaner.py 🆕
│   │   ├── broad 🆕
│   │   │   ├── __init__.py 🆕
│   │   │   ├── processor.py 🆕
│   │   │   └── cleaner.py 🆕
│   │   ├── expanded 🆕
│   │   │   ├── __init__.py 🆕
│   │   │   ├── processor.py 🆕
│   │   │   └── cleaner.py 🆕
│   │   ├── halloween_testing 🆕
│   │   │   ├── __init__.py 🆕
│   │   │   ├── processor.py 🆕
│   │   │   └── cleaner.py 🆕
│   │   ├── halloween_testing_pt 🆕
│   │   │   ├── __init__.py 🆕
│   │   │   ├── processor.py 🆕
│   │   │   └── cleaner.py 🆕
│   │   ├── halloween_phrase 🆕
│   │   │   ├── __init__.py 🆕
│   │   │   ├── processor.py 🆕
│   │   │   └── cleaner.py 🆕
│   │   ├── halloween_broad 🆕
│   │   │   ├── __init__.py 🆕
│   │   │   ├── processor.py 🆕
│   │   │   └── cleaner.py 🆕
│   │   └── halloween_expanded 🆕
│   │       ├── __init__.py 🆕
│   │       ├── processor.py 🆕
│   │       └── cleaner.py 🆕
│   ├── common
│   │   ├── excluded_portfolios.py
│   │   ├── numeric_validator_py.py
│   │   ├── portfolio_filter.py
│   │   └── state_validator_py.py
│   ├── campaign_common 🆕
│   │   ├── __init__.py 🆕
│   │   ├── keyword_processor.py 🆕
│   │   ├── asin_validator.py 🆕
│   │   └── campaign_builder.py 🆕
│   └── processors
│       ├── excel_base_formatter.py
│       └── output_formatter.py
├── config
│   ├── constants.py 📝
│   ├── optimization_config.py
│   ├── settings.py
│   └── ui_text.py 📝
├── data
│   ├── readers
│   │   ├── csv_reader.py
│   │   └── excel_reader.py
│   ├── validators
│   │   ├── bulk_validator.py
│   │   ├── portfolio_validator.py
│   │   └── template_validator.py
│   ├── writers
│   │   ├── excel_writer.py
│   │   └── campaign_bulk_writer.py 🆕
│   ├── template_generator.py 📝
│   └── campaign_template_generator.py 🆕
├── utils
│   ├── file_utils.py
│   ├── filename_generator.py 📝
│   └── page_utils.py
```

## מקרא
- 🆕 **קבצים חדשים** - קבצים שיש ליצור עבור Campaign Creator
- 📝 **קבצים לעריכה** - קבצים קיימים שצריכים עדכון
- ללא סימון - קבצים שנשארים ללא שינוי