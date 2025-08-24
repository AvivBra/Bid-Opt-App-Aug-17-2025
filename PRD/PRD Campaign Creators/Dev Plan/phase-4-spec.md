# Phase 4: Business Logic
**Date: 2025-08-22 | Time: 15:45**

## Background
With the base infrastructure in place, we now implement the specific business logic for Testing Campaigns. This includes validation, cleaning, and processing logic that transforms input templates into campaign structures following Amazon's format.

## Goal
Implement the complete business logic for creating testing campaigns from keyword templates.

## Files to Develop

### 1. `business/campaign_creation/testing_campaigns/__init__.py` (NEW FILE)
**TODO:**
- [ ] Import all module classes
- [ ] Define __all__ list
- [ ] Import TestingCampaignsCreation as main export

### 2. `business/campaign_creation/testing_campaigns/orchestrator.py` (NEW FILE)
**TODO:**
- [ ] Create TestingCampaignsCreation class inheriting BaseCampaignCreator
- [ ] Implement __init__ with "Testing Campaigns" name
- [ ] Implement validate() - check template structure
- [ ] Implement clean() - filter and prepare data
- [ ] Implement process() - main campaign creation logic
- [ ] Add logging for each step
- [ ] Return proper result dictionary

### 3. `business/campaign_creation/testing_campaigns/validator.py` (NEW FILE)
**TODO:**
- [ ] Create TestingCampaignsValidator class
- [ ] Add validate_template_structure() method
- [ ] Add validate_keyword_data() method
- [ ] Check for required columns
- [ ] Validate data types
- [ ] Return validation results with details

### 4. `business/campaign_creation/testing_campaigns/cleaner.py` (NEW FILE)
**TODO:**
- [ ] Create TestingCampaignsCleaner class
- [ ] Add clean_keywords() method
- [ ] Remove empty rows
- [ ] Standardize keyword format
- [ ] Handle special characters
- [ ] Return cleaned data with statistics

### 5. `business/campaign_creation/testing_campaigns/processor.py` (NEW FILE)
**TODO:**
- [ ] Create TestingCampaignsProcessor class
- [ ] Add create_campaign_structure() method
- [ ] Generate campaign names
- [ ] Set default bid values
- [ ] Create ad group structure
- [ ] Format for Amazon bulk upload
- [ ] Return processed campaign data

## Development Tests
- Orchestrator initializes correctly
- Validator catches invalid templates
- Cleaner removes invalid data
- Processor generates correct structure
- All methods return expected formats
- Logging works at each step

## User Tests
- No visible changes yet
- Application continues to run
- Zero Sales still functions
- No errors when checking checkbox

## What User Will See
**Working:**
- All existing functionality unchanged

**Not Working Yet:**
- Can't upload campaign files
- Process button doesn't use this logic
- No output generated

## File Tree (Phase 4 Files Highlighted)
```
├── business
│   ├── campaign_creation
│   │   └── testing_campaigns ⭐ NEW FOLDER
│   │       ├── __init__.py ⭐ NEW
│   │       ├── orchestrator.py ⭐ NEW
│   │       ├── validator.py ⭐ NEW
│   │       ├── cleaner.py ⭐ NEW
│   │       └── processor.py ⭐ NEW
```

---

**Next Phase:** Data Layer (File reading/writing for campaigns)