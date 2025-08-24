# Implementation Phases - Testing Campaigns
**Date: 2025-08-22 | Time: 15:25**

## Phase 0: Template Update
**Files to write:**
- `data/template_generator.py` (modify)
- `data/validators/template_validator.py` (modify)
- `data/readers/excel_reader.py` (modify)
- `config/constants.py` (modify)

**Goal:** Add "Campaign Seeds" sheet with Hero Keywords to existing template

**User will see:** Template now has 3 sheets instead of 2 (Port Values, Top ASINs, Campaign Seeds)

---

## Phase 1: UI Checkbox
**Files to write:**
- `app/ui/components/checklist.py` (modify)
- `config/optimization_config.py` (modify)
- `config/ui_text.py` (modify)
- `config/constants.py` (modify)

**Goal:** Add the checkbox to the interface

**User will see:** New checkbox "Create Testing Campaigns" appears under Zero Sales

---

## Phase 2: State Management
**Files to write:**
- `app/state/session_manager.py` (modify)
- `app/state/bid_state.py` (modify)
- `app/state/campaign_state.py` (new)

**Goal:** Store checkbox selection in session

**User will see:** Checkbox stays selected after clicking

---

## Phase 3: Base Infrastructure
**Files to write:**
- `business/campaign_creation/__init__.py` (new)
- `business/campaign_creation/base_campaign_creator.py` (new)

**Goal:** Create foundation for all campaign types

**User will see:** No visible change

---

## Phase 4: Business Logic
**Files to write:**
- `business/campaign_creation/testing_campaigns/__init__.py` (new)
- `business/campaign_creation/testing_campaigns/orchestrator.py` (new)
- `business/campaign_creation/testing_campaigns/validator.py` (new)
- `business/campaign_creation/testing_campaigns/cleaner.py` (new)
- `business/campaign_creation/testing_campaigns/processor.py` (new)

**Goal:** Implement campaign creation logic

**User will see:** No visible change

---

## Phase 5: Data Layer
**Files to write:**
- `data/campaign_creation/__init__.py` (new)
- `data/campaign_creation/readers/__init__.py` (new)
- `data/campaign_creation/readers/campaign_excel_reader.py` (new)
- `data/campaign_creation/writers/__init__.py` (new)
- `data/campaign_creation/writers/campaign_excel_writer.py` (new)
- `data/campaign_creation/validators/__init__.py` (new)
- `data/campaign_creation/validators/campaign_template_validator.py` (new)
- `data/campaign_creation/validators/campaign_bulk_validator.py` (new)
- `data/campaign_creation/template_generator/__init__.py` (new)
- `data/campaign_creation/template_generator/campaign_template_generator.py` (new)

**Goal:** Handle campaign-specific file formats

**User will see:** No visible change

---

## Phase 6: Integration
**Files to write:**
- `app/ui/shared/validation_section.py` (modify)
- `app/ui/shared/upload_section.py` (modify)
- `app/ui/shared/output_section.py` (modify)
- `app/pages/bid_optimizer.py` (modify)
- `business/processors/output_formatter.py` (modify)

**Goal:** Connect all components together

**User will see:** Full flow works - can select checkbox, upload files, process, and download results

---

## Total Files Count
- **New files:** 18
- **Modified files:** 15 (was 11, +4 from Phase 0)
- **Total:** 33 files

---

## Complete File Tree After Implementation

```
├── app
│   ├── pages
│   │   └── bid_optimizer.py [Phase 6 - modify]
│   ├── state
│   │   ├── bid_state.py [Phase 2 - modify]
│   │   ├── campaign_state.py [Phase 2 - NEW]
│   │   └── session_manager.py [Phase 2 - modify]
│   ├── ui
│   │   ├── components
│   │   │   ├── alerts.py
│   │   │   ├── buttons.py
│   │   │   ├── checklist.py [Phase 1 - modify]
│   │   │   ├── download_buttons.py
│   │   │   ├── file_cards.py
│   │   │   └── progress_bar.py
│   │   ├── shared
│   │   │   ├── output_section.py [Phase 6 - modify]
│   │   │   ├── page_header.py
│   │   │   ├── upload_section.py [Phase 6 - modify]
│   │   │   └── validation_section.py [Phase 6 - modify]
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
│   ├── campaign_creation [Phase 3 - NEW folder]
│   │   ├── __init__.py [Phase 3 - NEW]
│   │   ├── base_campaign_creator.py [Phase 3 - NEW]
│   │   └── testing_campaigns [Phase 4 - NEW folder]
│   │       ├── __init__.py [Phase 4 - NEW]
│   │       ├── orchestrator.py [Phase 4 - NEW]
│   │       ├── validator.py [Phase 4 - NEW]
│   │       ├── cleaner.py [Phase 4 - NEW]
│   │       └── processor.py [Phase 4 - NEW]
│   ├── common
│   │   ├── excluded_portfolios.py
│   │   ├── numeric_validator_py.py
│   │   ├── portfolio_filter.py
│   │   └── state_validator_py.py
│   └── processors
│       └── output_formatter.py [Phase 6 - modify]
├── claude
│   └── settings.local.json
├── config
│   ├── constants.py [Phase 0 & Phase 1 - modify]
│   ├── optimization_config.py [Phase 1 - modify]
│   ├── settings.py
│   └── ui_text.py [Phase 1 - modify]
├── data
│   ├── readers
│   │   ├── csv_reader.py
│   │   └── excel_reader.py [Phase 0 - modify]
│   ├── validators
│   │   ├── bulk_validator.py
│   │   ├── portfolio_validator.py
│   │   └── template_validator.py [Phase 0 - modify]
│   ├── writers
│   │   └── excel_writer.py
│   ├── template_generator.py [Phase 0 - modify]
│   └── campaign_creation [Phase 5 - NEW folder]
│       ├── __init__.py [Phase 5 - NEW]
│       ├── readers [Phase 5 - NEW folder]
│       │   ├── __init__.py [Phase 5 - NEW]
│       │   └── campaign_excel_reader.py [Phase 5 - NEW]
│       ├── writers [Phase 5 - NEW folder]
│       │   ├── __init__.py [Phase 5 - NEW]
│       │   └── campaign_excel_writer.py [Phase 5 - NEW]
│       ├── validators [Phase 5 - NEW folder]
│       │   ├── __init__.py [Phase 5 - NEW]
│       │   ├── campaign_template_validator.py [Phase 5 - NEW]
│       │   └── campaign_bulk_validator.py [Phase 5 - NEW]
│       └── template_generator [Phase 5 - NEW folder]
│           ├── __init__.py [Phase 5 - NEW]
│           └── campaign_template_generator.py [Phase 5 - NEW]
├── utils
│   ├── file_utils.py
│   ├── filename_generator.py
│   └── page_utils.py
├── readme-file.md
├── requirements.txt
└── simple_test_top_nav.py

## File Count Summary
- **Original files:** 43 files
- **New files to add:** 18 files
- **Files to modify:** 11 files
- **Final total:** 61 files
```