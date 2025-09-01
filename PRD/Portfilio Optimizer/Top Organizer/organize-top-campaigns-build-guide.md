# Organize Top Campaigns - Implementation Build Guide

**Date:** 01/09/2025  
**Status:** Ready for Implementation

## ⚠️ IMPLEMENTATION CONSTRAINTS

**CRITICAL RULE:** During implementation, Claude is **ONLY** allowed to modify or create the files explicitly listed in this guide. **NO OTHER FILES** may be touched, edited, or created outside this approved list.

---

## 📋 SPECIFICATION LINKS

### Primary Specifications
- **Main Spec:** `/Applications/My Apps/Bid Opt App Aug 17, 2025/PRD/Portfilio Optimizer/Top Organizer/organize-top-campaigns-spec.md`
- **Code Tree Analysis:** `/Applications/My Apps/Bid Opt App Aug 17, 2025/PRD/Portfilio Optimizer/Top Organizer/organize-top-campaigns-code-tree.md`
- **This Build Guide:** `/Applications/My Apps/Bid Opt App Aug 17, 2025/PRD/Portfilio Optimizer/Top Organizer/organize-top-campaigns-build-guide.md`

---

## 🆕 FILES TO CREATE (11 New Files)

### Core Business Logic
1. **`business/portfolio_optimizations/strategies/organize_top_campaigns_strategy.py`**
   - Main strategy implementation
   - Implements OptimizationStrategy contract
   - Coordinates all processing steps per spec

2. **`business/portfolio_optimizations/templates/__init__.py`**
   - Template module initialization
   - Export template generator

3. **`business/portfolio_optimizations/templates/top_campaigns_template_generator.py`**
   - Generates template with "Top ASINs" column
   - Creates Excel file for download

4. **`business/portfolio_optimizations/processors/__init__.py`**
   - Processors module initialization
   - Export all processors

5. **`business/portfolio_optimizations/processors/ads_count_processor.py`**
   - Implements COUNTIFS logic for Campaign ID matching
   - Adds "Ads Count" column to Campaign sheet
   - Handles row filtering based on count > 1

6. **`business/portfolio_optimizations/processors/asin_matcher.py`**
   - Implements VLOOKUP logic for ASIN matching
   - Creates "ASIN PA" column
   - Matches Campaign ID between Campaign and Product Ad sheets

7. **`business/portfolio_optimizations/processors/top_campaigns_processor.py`**
   - Main processing coordinator
   - Handles Top sheet creation
   - Implements "Top" column logic with V marking

### Data Handling
8. **`data/readers/template_reader.py`**
   - Reads uploaded template files
   - Extracts "Top ASINs" data
   - Validates template structure

9. **`data/validators/top_campaigns_template_validator.py`**
   - Validates template file structure
   - Ensures "Top ASINs" column exists
   - Validates ASIN format

10. **`data/writers/template_writer.py`**
    - Creates template Excel files for download
    - Formats template with proper headers

### Test Files
11. **Test Files and Fixtures (Multiple)**
    - `business/portfolio_optimizations/tests/fixtures/expected_outputs/organize_top_campaigns_expected.xlsx`
    - `business/portfolio_optimizations/tests/fixtures/test_input_files/organize_top_campaigns_bulk60.xlsx`
    - `business/portfolio_optimizations/tests/fixtures/test_input_files/organize_top_campaigns_template.xlsx`
    - `business/portfolio_optimizations/tests/test_organize_top_campaigns_integration.py`
    - `business/portfolio_optimizations/tests/test_organize_top_campaigns_output.py`

---

## ✏️ FILES TO MODIFY (20 Existing Files)

### UI Components (Priority 1 - Critical Path)
1. **`app/components/portfolio_optimizer.py`**
   - **CRITICAL:** Add `_render_template_section()` method to display template UI
   - **Template Download:** Add "Download Template" button that appears only when "Organize Top Campaigns" is selected
   - **Template Upload:** Add "Upload Filled Template" file picker that appears only when "Organize Top Campaigns" is selected
   - **State Integration:** Handle template file state management and validation
   - **Conditional Display:** Template section must appear between optimization selection and bulk file upload
   - **Success Messages:** Display success/error messages for template operations
   - **Process Requirements:** Update process readiness check to require template when "Organize Top Campaigns" selected

2. **`app/state/portfolio_state.py`**
   - **CRITICAL:** Add template file storage: `portfolio_template_file`, `portfolio_template_df`, `portfolio_template_uploaded`
   - **State Functions:** Add `save_portfolio_template_data()` and `get_portfolio_template_data()` functions
   - **Validation:** Add `has_portfolio_template()` function for readiness checking
   - **Integration:** Template state must integrate with process readiness validation
   - **Cleanup:** Template data must be cleared on state reset

3. **`app/ui/components/buttons.py`**
   - Add "Download Template" button component
   - Add "Upload Template" button component
   - Style consistently with existing buttons

4. **`app/ui/components/file_cards.py`**
   - Support template file display
   - Show template file status
   - Template file validation indicators

5. **`app/ui/shared/upload_section.py`**
   - Add template upload section
   - Show template upload area when optimization selected
   - Validate template files on upload

### Business Logic Integration (Priority 2)
6. **`business/portfolio_optimizations/strategies/__init__.py`**
   - Import OrganizeTopCampaignsStrategy
   - Export new strategy

7. **`business/portfolio_optimizations/constants.py`**
   - Add strategy name constant
   - Add column name constants (Ads Count, ASIN PA, Top)
   - Add sheet name constants

8. **`business/portfolio_optimizations/factory.py`**
   - Register OrganizeTopCampaignsStrategy
   - Add to strategy creation logic
   - Update display names

9. **`business/portfolio_optimizations/orchestrator.py`**
   - Handle template file integration
   - Pass template data to strategy
   - Validate template before processing

10. **`business/portfolio_optimizations/service.py`**
    - Add template file handling
    - Generate template downloads
    - Process template uploads

### Configuration (Priority 3)
11. **`config/optimization_config.py`**
    - Add OrganizeTopCampaigns configuration
    - Template file settings
    - Column positioning configs

12. **`config/portfolio_config.py`**
    - Add template file paths
    - Template naming conventions
    - File size limits

13. **`config/ui_text.py`**
    - Add UI text for template buttons
    - Error messages for template validation
    - Help text for template usage

### Data Layer (Priority 4)
14. **`data/readers/excel_reader.py`**
    - **CRITICAL:** Add `read_top_asins_template()` method for template file processing
    - **Template Reading:** Extract Top ASINs data from uploaded template files
    - **Validation:** Return success/failure status with descriptive messages
    - **Data Format:** Return pandas DataFrame with template ASIN data
    - **Error Handling:** Graceful handling of invalid template files

15. **`data/validators/template_validator.py`**
    - Add template validation for Top ASINs
    - Validate column structure
    - Check file format

16. **`data/writers/excel_writer.py`**
    - Handle Top sheet writing
    - Format new columns (Ads Count, ASIN PA, Top)
    - Apply column coloring (blue for ASIN PA)

17. **`data/template_generator.py`**
    - **CRITICAL:** Add `generate_top_asins_template()` method that returns bytes
    - **Template Structure:** Single sheet with "Top ASINs" column header
    - **File Format:** Excel (.xlsx) format with proper styling
    - **Integration:** Must work with TopCampaignsTemplateGenerator class
    - **Size:** Expected template size ~5130 bytes

### Utilities (Priority 5)
18. **`utils/file_utils.py`**
    - Add template file utilities
    - Template file validation helpers
    - File type checking

19. **`utils/filename_generator.py`**
    - Add template filename generation
    - Timestamp-based naming
    - Extension handling

### Tests (Priority 6)
20. **Test File Updates (Multiple)**
    - `business/portfolio_optimizations/tests/integration_test.py` - Add OrganizeTopCampaigns tests
    - `business/portfolio_optimizations/tests/output_validation_tests.py` - Add validation tests
    - `business/portfolio_optimizations/tests/run_tests.py` - Include new tests
    - `business/portfolio_optimizations/tests/validate_output.py` - Add OrganizeTopCampaigns validation

---

## 📊 IMPLEMENTATION SUMMARY

### Total Files Impact
- **31 files** total (11 new + 20 modified)
- **11 new files** to create from scratch
- **20 existing files** to modify
- **Multiple test files** for quality assurance

### Implementation Priority Order
1. **Phase 1:** Configuration and Constants
2. **Phase 2:** Core Business Logic (Strategy, Processors)
3. **Phase 3:** Data Layer (Readers, Writers, Validators)
4. **Phase 4:** UI Components and State Management
5. **Phase 5:** Template Generation and Handling
6. **Phase 6:** Tests and Validation

### Key Features to Implement
- ✅ **Template Download:** Button appears when optimization selected, generates 5130-byte Excel file
- ✅ **Template Upload:** File picker for filled template, validation and success messages
- ✅ **Template Integration:** Template data stored in session state, passed to strategy
- ✅ **UI Conditional Display:** Template section only visible when "Organize Top Campaigns" selected
- ✅ **Process Requirements:** Template required before processing can begin
- ✅ **Ads Count column:** COUNTIFS logic for Campaign ID matching
- ✅ **ASIN PA column:** VLOOKUP logic with blue header styling
- ✅ **Top column:** ASIN matching against template data with V marking
- ✅ **Top sheet creation:** New sheet with template ASIN data
- ✅ **Row filtering:** Portfolio-based filtering rules applied
- ✅ **Complete Integration:** Works with existing portfolio optimization architecture

---

## 🚫 STRICT IMPLEMENTATION RULES

1. **File Modification Constraint:** Only files listed in this guide may be created or modified
2. **Architecture Compliance:** All changes must follow existing patterns and conventions
3. **Testing Required:** All new functionality must have corresponding tests
4. **Spec Adherence:** Implementation must strictly follow the specification document
5. **UI Consistency:** All UI changes must match existing design patterns

---

**Ready for Implementation ✅**