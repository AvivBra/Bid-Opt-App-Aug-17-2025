# Updated File Tree with Organized Data Structure
**Date: 2025-08-22 | Time: 15:00**

## Proposed File Structure with New Folders

```
├── app
│   ├── pages
│   │   └── bid_optimizer.py ⚡
│   ├── state
│   │   ├── bid_state.py ⚡
│   │   └── session_manager.py ⚡
│   ├── ui
│   │   ├── components
│   │   │   ├── alerts.py
│   │   │   ├── buttons.py
│   │   │   ├── checklist.py ⚡⚡
│   │   │   ├── download_buttons.py
│   │   │   ├── file_cards.py
│   │   │   └── progress_bar.py
│   │   ├── shared
│   │   │   ├── output_section.py
│   │   │   ├── page_header.py
│   │   │   ├── upload_section.py
│   │   │   └── validation_section.py ⚡
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
│   │   └── base_optimization.py
│   ├── campaign_creation 🆕
│   │   ├── __init__.py 🆕
│   │   ├── base_campaign_creator.py 🆕
│   │   ├── testing_campaigns 🆕
│   │   │   ├── __init__.py 🆕
│   │   │   ├── orchestrator.py 🆕
│   │   │   ├── validator.py 🆕
│   │   │   ├── cleaner.py 🆕
│   │   │   └── processor.py 🆕
│   │   ├── testing_pt_campaigns 🆕
│   │   │   ├── __init__.py 🆕
│   │   │   ├── orchestrator.py 🆕
│   │   │   ├── validator.py 🆕
│   │   │   ├── cleaner.py 🆕
│   │   │   └── processor.py 🆕
│   │   ├── phrase_campaigns 🆕
│   │   │   ├── __init__.py 🆕
│   │   │   ├── orchestrator.py 🆕
│   │   │   ├── validator.py 🆕
│   │   │   ├── cleaner.py 🆕
│   │   │   └── processor.py 🆕
│   │   ├── broad_campaigns 🆕
│   │   │   ├── __init__.py 🆕
│   │   │   ├── orchestrator.py 🆕
│   │   │   ├── validator.py 🆕
│   │   │   ├── cleaner.py 🆕
│   │   │   └── processor.py 🆕
│   │   └── expanded_campaigns 🆕
│   │       ├── __init__.py 🆕
│   │       ├── orchestrator.py 🆕
│   │       ├── validator.py 🆕
│   │       ├── cleaner.py 🆕
│   │       └── processor.py 🆕
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
│   ├── constants.py ⚡
│   ├── optimization_config.py ⚡⚡
│   ├── settings.py
│   └── ui_text.py ⚡
├── data
│   ├── readers (COMMON - stays here)
│   │   ├── csv_reader.py
│   │   └── excel_reader.py
│   ├── validators (COMMON - stays here)
│   │   ├── bulk_validator.py
│   │   ├── portfolio_validator.py
│   │   └── template_validator.py
│   ├── writers (COMMON - stays here)
│   │   └── excel_writer.py
│   ├── template_generator.py (COMMON - stays here)
│   │
│   ├── zero_sales 🆕
│   │   ├── __init__.py 🆕
│   │   └── zero_sales_template_generator.py 🆕 (specific templates if needed)
│   │
│   ├── campaign_creation 🆕
│   │   ├── __init__.py 🆕
│   │   ├── readers 🆕
│   │   │   ├── __init__.py 🆕
│   │   │   ├── campaign_excel_reader.py 🆕
│   │   │   └── campaign_csv_reader.py 🆕
│   │   ├── writers 🆕
│   │   │   ├── __init__.py 🆕
│   │   │   └── campaign_excel_writer.py 🆕
│   │   ├── validators 🆕
│   │   │   ├── __init__.py 🆕
│   │   │   ├── campaign_template_validator.py 🆕
│   │   │   └── campaign_bulk_validator.py 🆕
│   │   ├── template_generator 🆕
│   │   │   ├── __init__.py 🆕
│   │   │   └── campaign_template_generator.py 🆕
│   │   ├── testing_campaigns 🆕
│   │   │   ├── __init__.py 🆕
│   │   │   ├── template_config.py 🆕
│   │   │   └── data_mapper.py 🆕
│   │   ├── testing_pt_campaigns 🆕
│   │   │   ├── __init__.py 🆕
│   │   │   ├── template_config.py 🆕
│   │   │   └── data_mapper.py 🆕
│   │   ├── phrase_campaigns 🆕
│   │   │   ├── __init__.py 🆕
│   │   │   ├── template_config.py 🆕
│   │   │   └── data_mapper.py 🆕
│   │   ├── broad_campaigns 🆕
│   │   │   ├── __init__.py 🆕
│   │   │   ├── template_config.py 🆕
│   │   │   └── data_mapper.py 🆕
│   │   └── expanded_campaigns 🆕
│   │       ├── __init__.py 🆕
│   │       ├── template_config.py 🆕
│   │       └── data_mapper.py 🆕
├── utils
│   ├── file_utils.py
│   ├── filename_generator.py
│   └── page_utils.py
├── readme-file.md
├── requirements.txt
└── simple_test_top_nav.py
```

## Summary of New Structure

### Business Layer (`business/`)
- **campaign_creation/** - All campaign creation business logic
  - Each campaign type has its own folder with full MVC-like structure
  - `base_campaign_creator.py` - Abstract base class like `base_optimization.py`

### Data Layer (`data/`)
- **Common files stay in root** - Used by all optimizations (readers, writers, validators)
- **zero_sales/** - Zero Sales specific data handling (if needed in future)
- **campaign_creation/** - Campaign creation specific data handling
  - `readers/` - Campaign-specific readers
  - `writers/` - Campaign-specific writers
  - `validators/` - Campaign-specific validators
  - `template_generator/` - Campaign template generation
  - Each campaign type folder contains specific configurations and mappings

## File Count Summary
- **Existing files to modify**: 8 files
- **New folders to create**: 22 folders
- **New files to create**: ~60 files (including __init__.py files)

## Benefits of This Structure
1. **Clear separation** between bid optimization and campaign creation
2. **Dedicated readers/writers** for campaign-specific formats
3. **Reusable components** in data root for common operations
4. **Easy to add new campaign types** - just add a new folder
5. **Consistent patterns** across all optimization types
6. **No breaking changes** to existing Zero Sales functionality