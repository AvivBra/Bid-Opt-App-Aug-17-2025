# Organize Top Campaigns - Code File Tree Analysis

## Complete Code File Tree for Implementation

Based on the spec and existing architecture, here's the complete file tree showing what needs to be added or modified:

```
├── app
│   ├── components
│   │   ├── bid_optimizer.py
│   │   ├── campaign_optimizer.py
│   │   └── portfolio_optimizer.py ✓ MODIFY (add UI for template download/upload)
│   ├── state
│   │   ├── bid_state.py
│   │   ├── campaign_state.py
│   │   ├── portfolio_state.py ✓ MODIFY (add template file management state)
│   │   └── session_manager.py
│   ├── ui
│   │   ├── components
│   │   │   ├── alerts.py
│   │   │   ├── buttons.py ✓ MODIFY (add template download/upload buttons)
│   │   │   ├── checklist.py
│   │   │   ├── download_buttons.py
│   │   │   ├── file_cards.py ✓ MODIFY (support template file display)
│   │   │   └── progress_bar.py
│   │   ├── shared
│   │   │   ├── output_section.py
│   │   │   ├── page_header.py
│   │   │   ├── upload_section.py ✓ MODIFY (add template upload section)
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
│   │   ├── strategies
│   │   │   ├── __init__.py ✓ MODIFY (import OrganizeTopCampaignsStrategy)
│   │   │   ├── campaigns_without_portfolios_strategy.py
│   │   │   ├── empty_portfolios_strategy.py
│   │   │   └── organize_top_campaigns_strategy.py ★ NEW FILE
│   │   ├── templates
│   │   │   ├── __init__.py ★ NEW FILE
│   │   │   └── top_campaigns_template_generator.py ★ NEW FILE
│   │   ├── processors
│   │   │   ├── __init__.py ★ NEW FILE
│   │   │   ├── ads_count_processor.py ★ NEW FILE
│   │   │   ├── asin_matcher.py ★ NEW FILE
│   │   │   └── top_campaigns_processor.py ★ NEW FILE
│   │   ├── tests
│   │   │   ├── fixtures
│   │   │   │   ├── expected_outputs
│   │   │   │   │   └── organize_top_campaigns_expected.xlsx ★ NEW FILE
│   │   │   │   └── test_input_files
│   │   │   │       ├── organize_top_campaigns_bulk60.xlsx ★ NEW FILE
│   │   │   │       └── organize_top_campaigns_template.xlsx ★ NEW FILE
│   │   │   ├── utilities
│   │   │   │   ├── __init__.py
│   │   │   │   └── inspect_expected_output.py
│   │   │   ├── __init__.py
│   │   │   ├── integration_test.py ✓ MODIFY (add OrganizeTopCampaigns tests)
│   │   │   ├── output_validation_tests.py ✓ MODIFY (add validation tests)
│   │   │   ├── run_tests.py ✓ MODIFY (include new tests)
│   │   │   ├── test_both_checkboxes_integration.py
│   │   │   ├── test_empty_portfolios_output.py
│   │   │   ├── test_organize_top_campaigns_integration.py ★ NEW FILE
│   │   │   ├── test_organize_top_campaigns_output.py ★ NEW FILE
│   │   │   ├── validate_output.py ✓ MODIFY (add OrganizeTopCampaigns validation)
│   │   │   └── verify_empty_portfolios_output.py
│   │   ├── __init__.py
│   │   ├── cleaning.py
│   │   ├── constants.py ✓ MODIFY (add OrganizeTopCampaigns constants)
│   │   ├── contract_validator.py
│   │   ├── contracts.py
│   │   ├── factory.py ✓ MODIFY (register OrganizeTopCampaignsStrategy)
│   │   ├── orchestrator.py ✓ MODIFY (handle template file integration)
│   │   ├── results_manager.py
│   │   └── service.py ✓ MODIFY (add template file handling)
│   └── processors
│       ├── excel_base_formatter.py ✓ MODIFY (add Top sheet formatting)
│       └── output_formatter.py
├── config
│   ├── campaign_config.py
│   ├── constants.py
│   ├── optimization_config.py ✓ MODIFY (add OrganizeTopCampaigns config)
│   ├── portfolio_config.py ✓ MODIFY (add template file paths)
│   ├── settings.py
│   └── ui_text.py ✓ MODIFY (add new UI text for templates)
├── data
│   ├── readers
│   │   ├── csv_reader.py
│   │   ├── excel_reader.py ✓ MODIFY (handle template file reading)
│   │   └── template_reader.py ★ NEW FILE
│   ├── validators
│   │   ├── bulk_validator.py
│   │   ├── campaign_validators.py
│   │   ├── portfolio_validator.py
│   │   ├── template_validator.py ✓ MODIFY (add template validation for Top ASINs)
│   │   └── top_campaigns_template_validator.py ★ NEW FILE
│   ├── writers
│   │   ├── campaign_bulk_writer.py
│   │   ├── excel_writer.py ✓ MODIFY (handle Top sheet writing)
│   │   └── template_writer.py ★ NEW FILE
│   ├── campaign_template_generator.py
│   └── template_generator.py ✓ MODIFY (add top campaigns template generation)
├── utils
│   ├── file_utils.py ✓ MODIFY (add template file utilities)
│   ├── filename_generator.py ✓ MODIFY (add template filename generation)
│   └── page_utils.py
├── BidOptimizer.command
├── readme-file.md
└── requirements.txt
```

## Legend:
- ★ NEW FILE - Must be created from scratch
- ✓ MODIFY - Existing file that needs modifications
- (no mark) - Existing file that doesn't need changes

## Summary of Changes Required:

### New Files to Create (11 files):
1. `business/portfolio_optimizations/strategies/organize_top_campaigns_strategy.py`
2. `business/portfolio_optimizations/templates/__init__.py`
3. `business/portfolio_optimizations/templates/top_campaigns_template_generator.py`
4. `business/portfolio_optimizations/processors/__init__.py`
5. `business/portfolio_optimizations/processors/ads_count_processor.py`
6. `business/portfolio_optimizations/processors/asin_matcher.py`
7. `business/portfolio_optimizations/processors/top_campaigns_processor.py`
8. `data/readers/template_reader.py`
9. `data/validators/top_campaigns_template_validator.py`
10. `data/writers/template_writer.py`
11. Test files and fixtures (multiple)

### Existing Files to Modify (20 files):
1. `app/components/portfolio_optimizer.py` - Add template download/upload UI
2. `app/state/portfolio_state.py` - Add template file state management
3. `app/ui/components/buttons.py` - Add template buttons
4. `app/ui/components/file_cards.py` - Support template file display
5. `app/ui/shared/upload_section.py` - Add template upload section
6. `business/portfolio_optimizations/strategies/__init__.py` - Import new strategy
7. `business/portfolio_optimizations/constants.py` - Add constants
8. `business/portfolio_optimizations/factory.py` - Register new strategy
9. `business/portfolio_optimizations/orchestrator.py` - Handle template integration
10. `business/portfolio_optimizations/service.py` - Add template file handling
11. `config/optimization_config.py` - Add configuration
12. `config/portfolio_config.py` - Add template paths
13. `config/ui_text.py` - Add UI text
14. `data/readers/excel_reader.py` - Handle template reading
15. `data/validators/template_validator.py` - Add template validation
16. `data/writers/excel_writer.py` - Handle Top sheet writing
17. `data/template_generator.py` - Add template generation
18. `utils/file_utils.py` - Add template utilities
19. `utils/filename_generator.py` - Add template filename generation
20. Test files (multiple)

## Total Impact:
- **31 files** need to be created or modified
- **11 new files** to implement core functionality
- **20 existing files** to modify for integration
- **Multiple test files** to ensure quality

This implementation will integrate seamlessly with the existing portfolio optimization architecture while adding the new Organize Top Campaigns functionality with template download/upload capabilities.