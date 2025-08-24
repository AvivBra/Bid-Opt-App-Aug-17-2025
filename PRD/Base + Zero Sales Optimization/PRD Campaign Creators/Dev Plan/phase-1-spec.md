# Phase 1: UI Checkbox
**Date: 2025-08-22 | Time: 15:45**

## Background
The application currently has only "Zero Sales" optimization for adjusting bids on existing campaigns. We're adding a new feature "Create Testing Campaigns" that will generate new campaigns from templates, requiring a new checkbox in the UI alongside the existing Zero Sales checkbox.

## Goal
Add a visible, functional checkbox "Create Testing Campaigns" to the optimization selection interface.

## Files to Develop

### 1. `app/ui/components/checklist.py` (MODIFY)
**TODO:**
- [ ] Add new entry to OPTIMIZATIONS list after "Zero Sales"
- [ ] Set name: "Create Testing Campaigns"
- [ ] Set enabled: True
- [ ] Set description: "Generate testing campaigns from keyword templates"
- [ ] Keep all existing functionality intact

### 2. `config/optimization_config.py` (MODIFY)
**TODO:**
- [ ] Add CAMPAIGN_CREATION_CONFIG dictionary
- [ ] Define testing_campaigns configuration entry
- [ ] Set type field to 'campaign_creation' (not 'bid_optimization')
- [ ] Add enabled: True flag
- [ ] Define required_files list

### 3. `config/ui_text.py` (MODIFY)
**TODO:**
- [ ] Add OPTIMIZATION_TESTING_CAMPAIGNS constant
- [ ] Add help text for testing campaigns
- [ ] Add tooltip text
- [ ] Add validation messages for campaign creation

### 4. `config/constants.py` (MODIFY)
**TODO:**
- [ ] Add CAMPAIGN_CREATION_TYPES list
- [ ] Add MAX_CAMPAIGNS_PER_FILE constant
- [ ] Add CAMPAIGN_FILE_SIZE_LIMIT
- [ ] Add TESTING_CAMPAIGNS_REQUIRED_COLUMNS

## Development Tests
- Checkbox renders correctly
- Checkbox is enabled (not grayed out)
- Checkbox can be checked and unchecked
- Description text appears on hover
- No JavaScript errors in console

## User Tests
- Open the application
- See "Create Testing Campaigns" checkbox below "Zero Sales"
- Can click the checkbox
- Checkbox stays checked when clicked
- Can uncheck the checkbox

## What User Will See
**Working:**
- New checkbox appears with correct label
- Checkbox is interactive
- Hover shows description

**Not Working Yet:**
- Selecting checkbox won't affect file upload (Phase 2)
- No validation happens (Phase 6)
- Process button won't recognize selection (Phase 6)
- No actual campaign creation occurs (Phase 4)

## File Tree (Phase 1 Files Highlighted)
```
├── app
│   ├── ui
│   │   ├── components
│   │   │   ├── checklist.py ⭐ MODIFY
├── config
│   ├── constants.py ⭐ MODIFY
│   ├── optimization_config.py ⭐ MODIFY
│   └── ui_text.py ⭐ MODIFY
```

---

**Next Phase:** State Management (Save checkbox selection in session)