# Phase 0: Template Update
**Date: 2025-08-22 | Time: 16:00**

## Background
The existing template has "Port Values" and "Top ASINs" sheets for bid optimization. We need to add a third sheet "Campaign Seeds" that will contain the seed data for campaign creation, making the template serve both optimization types.

## Goal
Add "Campaign Seeds" sheet to the existing template with columns for ASIN, Product Type, Niche, and 5 Hero Keywords.

## Files to Develop

### 1. `data/template_generator.py` (MODIFY)
**TODO:**
- [ ] Add _create_campaign_seeds_sheet() method
- [ ] Add columns: ASIN, Product Type, Niche, Hero Keyword 1-5
- [ ] Apply header formatting (same style as other sheets)
- [ ] Add sample data rows
- [ ] Add instructions below data
- [ ] Set column widths appropriately
- [ ] Call new method in generate_template()

### 2. `data/validators/template_validator.py` (MODIFY)
**TODO:**
- [ ] Add "Campaign Seeds" to optional_sheets list
- [ ] Create _validate_campaign_seeds_columns() method
- [ ] Check for required columns if sheet exists
- [ ] Allow sheet to be empty (optional for bid optimization)
- [ ] Update validate() to check new sheet
- [ ] Update error messages

### 3. `data/readers/excel_reader.py` (MODIFY)
**TODO:**
- [ ] Update read_template_file() to read Campaign Seeds
- [ ] Add Campaign Seeds to returned dictionary
- [ ] Handle case where sheet doesn't exist (backward compatibility)
- [ ] Create empty DataFrame if sheet missing
- [ ] Update success message to include sheet count

### 4. `config/constants.py` (MODIFY)
**TODO:**
- [ ] Add TEMPLATE_CAMPAIGN_SEEDS_COLUMNS list
- [ ] Add CAMPAIGN_SEEDS_SHEET_NAME constant
- [ ] Update TEMPLATE_REQUIRED_SHEETS (keep as is - don't require Campaign Seeds)
- [ ] Add TEMPLATE_OPTIONAL_SHEETS list

## Development Tests
- Template downloads with 3 sheets
- Old templates (2 sheets) still work
- Campaign Seeds sheet has correct columns
- Validation passes with or without Campaign Seeds
- Sample data appears correctly

## User Tests
- Download template
- See 3 sheets: Port Values, Top ASINs, Campaign Seeds
- See sample data in Campaign Seeds
- Can upload old templates without errors
- Can leave Campaign Seeds empty

## What User Will See
**Working:**
- Template has 3 sheets
- Campaign Seeds has 8 columns
- Sample data and instructions visible
- Existing bid optimization unaffected

**Not Working Yet:**
- Campaign Seeds data not used anywhere
- No campaign creation checkbox yet
- No processing logic for campaigns

## File Tree (Phase 0 Files Highlighted)
```
├── data
│   ├── readers
│   │   └── excel_reader.py ⭐ MODIFY
│   ├── validators
│   │   └── template_validator.py ⭐ MODIFY
│   └── template_generator.py ⭐ MODIFY
├── config
│   └── constants.py ⭐ MODIFY
```

## Campaign Seeds Sheet Structure
| Column | Description | Sample Data |
|--------|-------------|-------------|
| ASIN | Product identifier | B08N5WRWNW |
| Product Type | Category of product | Echo Dot |
| Niche | Market segment | Smart Home |
| Hero Keyword 1 | Primary keyword | alexa device |
| Hero Keyword 2 | Secondary keyword | smart speaker |
| Hero Keyword 3 | Additional keyword | voice assistant |
| Hero Keyword 4 | Additional keyword | echo dot 4th gen |
| Hero Keyword 5 | Additional keyword | amazon alexa |

---

**Next Phase:** Phase 1 - UI Checkbox (Add Testing Campaigns checkbox)