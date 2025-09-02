 ├── app
  │   ├── components
  │   │   ├── bid_optimizer.py
  │   │   ├── campaign_optimizer.py (UNCHANGED - existing functionality)
  │   │   ├── campaign_optimizer_1.py ✓ NEW (7 Days Budgets page)
  │   │   └── portfolio_optimizer.py
  │   ├── state
  │   │   ├── bid_state.py
  │   │   ├── campaign_state.py (UNCHANGED - existing state)
  │   │   ├── campaign_optimizer_1_state.py ✓ NEW (7-days budget state)
  │   │   ├── portfolio_state.py
  │   │   └── session_manager.py
  │   ├── ui
  │   │   ├── components
  │   │   │   ├── alerts.py
  │   │   │   ├── buttons.py ✓ MODIFY (add Bulk 7 button component)
  │   │   │   ├── checklist.py ✓ MODIFY (add 7 Days Budgets checkbox)
  │   │   │   ├── download_buttons.py
  │   │   │   ├── file_cards.py
  │   │   │   └── progress_bar.py
  │   │   ├── shared
  │   │   │   ├── output_section.py
  │   │   │   ├── page_header.py
  │   │   │   ├── upload_section.py
  │   │   │   └── validation_section.py ✓ MODIFY (add campaign optimizer 1 
  validation)
  │   │   ├── layout.py
  │   │   └── sidebar_backup.py
  │   ├── main.py
  │   └── navigation.py ✓ MODIFY (add Campaign Optimizer 1 route only)
  ├── business
  │   ├── bid_optimizations
  │   │   ├── [ALL EXISTING FILES UNCHANGED]
  │   ├── campaign_creator
  │   │   ├── [ALL EXISTING FILES UNCHANGED]
  │   ├── campaign_optimizer_1 ✓ NEW FOLDER
  │   │   ├── strategies
  │   │   │   ├── __init__.py ✓ NEW
  │   │   │   └── seven_days_budget_strategy.py ✓ NEW
  │   │   ├── __init__.py ✓ NEW
  │   │   ├── cleaning.py ✓ NEW
  │   │   ├── constants.py ✓ NEW
  │   │   ├── factory.py ✓ NEW
  │   │   ├── orchestrator.py ✓ NEW
  │   │   └── service.py ✓ NEW
  │   ├── common
  │   │   ├── [ALL EXISTING FILES UNCHANGED]
  │   ├── portfolio_optimizations
  │   │   ├── [ALL EXISTING FILES UNCHANGED]
  │   └── processors
  │       ├── [ALL EXISTING FILES UNCHANGED]
  ├── config
  │   ├── campaign_config.py (UNCHANGED)
  │   ├── campaign_optimizer_1_config.py ✓ NEW
  │   ├── constants.py
  │   ├── optimization_config.py
  │   ├── portfolio_config.py
  │   ├── settings.py
  │   └── ui_text.py ✓ MODIFY (add Campaign Optimizer 1 text only)
  ├── data
  │   ├── readers
  │   │   ├── [ALL EXISTING FILES UNCHANGED]
  │   ├── validators
  │   │   ├── bulk_validator.py
  │   │   ├── campaign_validators.py (UNCHANGED)
  │   │   ├── campaign_optimizer_1_validators.py ✓ NEW
  │   │   ├── [OTHER FILES UNCHANGED]
  │   ├── writers
  │   │   ├── campaign_bulk_writer.py (UNCHANGED)
  │   │   ├── campaign_optimizer_1_writer.py ✓ NEW
  │   │   ├── excel_writer.py ✓ MODIFY (add new output format)
  │   │   └── template_writer.py
  │   ├── [OTHER FILES UNCHANGED]
  ├── utils
  │   ├── file_utils.py
  │   ├── filename_generator.py ✓ MODIFY (add new filename pattern)
  │   └── page_utils.py
  ├── [ALL OTHER ROOT FILES UNCHANGED]