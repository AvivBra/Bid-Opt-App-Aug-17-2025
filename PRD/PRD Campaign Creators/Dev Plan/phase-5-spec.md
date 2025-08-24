# Phase 5: Data Layer
**Date: 2025-08-22 | Time: 15:45**

## Background
Campaign creation requires different file formats than bid optimization. We need dedicated readers, writers, validators, and template generators that understand the specific structure of campaign templates and can output Amazon-compatible bulk upload files.

## Goal
Create the data layer components to handle campaign-specific file formats for input and output.

## Files to Develop

### 1. `data/campaign_creation/__init__.py` (NEW FILE)
**TODO:**
- [ ] Import all submodules
- [ ] Define __all__ list
- [ ] Add module docstring

### 2. `data/campaign_creation/readers/__init__.py` (NEW FILE)
**TODO:**
- [ ] Import campaign_excel_reader
- [ ] Export reader classes

### 3. `data/campaign_creation/readers/campaign_excel_reader.py` (NEW FILE)
**TODO:**
- [ ] Create CampaignExcelReader class
- [ ] Add read_campaign_template() method
- [ ] Look for "Keywords" sheet
- [ ] Read campaign settings sheet
- [ ] Handle multiple template formats
- [ ] Return dictionary of DataFrames

### 4. `data/campaign_creation/writers/__init__.py` (NEW FILE)
**TODO:**
- [ ] Import campaign_excel_writer
- [ ] Export writer classes

### 5. `data/campaign_creation/writers/campaign_excel_writer.py` (NEW FILE)
**TODO:**
- [ ] Create CampaignExcelWriter class
- [ ] Add write_campaign_file() method
- [ ] Format for Amazon bulk upload
- [ ] Create multiple sheets if needed
- [ ] Apply cell formatting
- [ ] No error highlighting needed

### 6. `data/campaign_creation/validators/__init__.py` (NEW FILE)
**TODO:**
- [ ] Import validators
- [ ] Export validator classes

### 7. `data/campaign_creation/validators/campaign_template_validator.py` (NEW FILE)
**TODO:**
- [ ] Create CampaignTemplateValidator class
- [ ] Validate sheet existence
- [ ] Check required columns
- [ ] Validate keyword format
- [ ] Check for duplicates
- [ ] Return validation results

### 8. `data/campaign_creation/validators/campaign_bulk_validator.py` (NEW FILE)
**TODO:**
- [ ] Create CampaignBulkValidator class
- [ ] Validate bulk file structure
- [ ] Check campaign limits
- [ ] Verify required fields
- [ ] Return validation results

### 9. `data/campaign_creation/template_generator/__init__.py` (NEW FILE)
**TODO:**
- [ ] Import template generator
- [ ] Export generator class

### 10. `data/campaign_creation/template_generator/campaign_template_generator.py` (NEW FILE)
**TODO:**
- [ ] Create CampaignTemplateGenerator class
- [ ] Generate blank template structure
- [ ] Add Keywords sheet
- [ ] Add Settings sheet
- [ ] Include instructions
- [ ] Add sample data

## Development Tests
- Can read campaign template files
- Writer creates valid Excel files
- Validators catch invalid formats
- Template generator creates downloadable file
- All components integrate properly

## User Tests
- No visible changes
- Application runs normally
- Existing features work

## What User Will See
**Working:**
- Everything continues as before

**Not Working Yet:**
- Can't actually upload files
- Download template button not connected
- Process doesn't use these components

## File Tree (Phase 5 Files Highlighted)
```
├── data
│   └── campaign_creation ⭐ NEW FOLDER
│       ├── __init__.py ⭐ NEW
│       ├── readers ⭐ NEW FOLDER
│       │   ├── __init__.py ⭐ NEW
│       │   └── campaign_excel_reader.py ⭐ NEW
│       ├── writers ⭐ NEW FOLDER
│       │   ├── __init__.py ⭐ NEW
│       │   └── campaign_excel_writer.py ⭐ NEW
│       ├── validators ⭐ NEW FOLDER
│       │   ├── __init__.py ⭐ NEW
│       │   ├── campaign_template_validator.py ⭐ NEW
│       │   └── campaign_bulk_validator.py ⭐ NEW
│       └── template_generator ⭐ NEW FOLDER
│           ├── __init__.py ⭐ NEW
│           └── campaign_template_generator.py ⭐ NEW
```

---

**Next Phase:** Integration (Connect everything together)