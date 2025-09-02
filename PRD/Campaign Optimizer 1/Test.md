# Organize Top Campaigns Integration Test Specification

## Test-Fix Loop (Allowed Code Files)

**Allowed for automatic fixes:**
NEW FILES TO CREATE:

  /Applications/My Apps/Bid Opt App Aug 17,
  2025/app/components/campaign_optimizer_1.py
  /Applications/My Apps/Bid Opt App Aug 17,
  2025/app/state/campaign_optimizer_1_state.py
  /Applications/My Apps/Bid Opt App Aug 17, 
  2025/business/campaign_optimizer_1/__init__.py
  /Applications/My Apps/Bid Opt App Aug 17, 
  2025/business/campaign_optimizer_1/cleaning.py
  /Applications/My Apps/Bid Opt App Aug 17, 
  2025/business/campaign_optimizer_1/constants.py
  /Applications/My Apps/Bid Opt App Aug 17, 
  2025/business/campaign_optimizer_1/factory.py
  /Applications/My Apps/Bid Opt App Aug 17, 
  2025/business/campaign_optimizer_1/orchestrator.py
  /Applications/My Apps/Bid Opt App Aug 17, 
  2025/business/campaign_optimizer_1/service.py
  /Applications/My Apps/Bid Opt App Aug 17, 
  2025/business/campaign_optimizer_1/strategies/__init__.py
  /Applications/My Apps/Bid Opt App Aug 17, 
  2025/business/campaign_optimizer_1/strategies/seven_days_budget_strategy.py
  /Applications/My Apps/Bid Opt App Aug 17,
  2025/config/campaign_optimizer_1_config.py
  /Applications/My Apps/Bid Opt App Aug 17, 
  2025/data/validators/campaign_optimizer_1_validators.py
  /Applications/My Apps/Bid Opt App Aug 17,
  2025/data/writers/campaign_optimizer_1_writer.py

  FILES TO MODIFY:

  /Applications/My Apps/Bid Opt App Aug 17, 2025/app/navigation.py
  /Applications/My Apps/Bid Opt App Aug 17, 2025/app/ui/components/buttons.py
  /Applications/My Apps/Bid Opt App Aug 17, 2025/app/ui/components/checklist.py
  /Applications/My Apps/Bid Opt App Aug 17,
  2025/app/ui/shared/validation_section.py
  /Applications/My Apps/Bid Opt App Aug 17, 2025/config/ui_text.py
  /Applications/My Apps/Bid Opt App Aug 17, 2025/data/writers/excel_writer.py
  /Applications/My Apps/Bid Opt App Aug 17, 2025/utils/filename_generator.py


**Process:** Automatically identify and fix issues in these files, then retest until success criteria are met.

## Test-Report (Non-Editable Files)

**Not allowed for automatic fixes:**
All the rest except from those mentioned as Allowed for automatic fixes

**Process:** Generate detailed report for user review - never modify these files.

## Success Criteria

The test-fix loop continues until all 3 criteria are met:

### a. 100% Compliance with Spec
100% compliance with the relevant spec in:
/Applications/My Apps/Bid Opt App Aug 17, 2025/PRD/Campaign Optimizer 1


### a. use the correct inputs:
for the upload Bulk 7:
/Applications/My Apps/Bid Opt App Aug 17, 2025/PRD/Campaign Optimizer 1/Input Excel Example - Bulk 7 Days.xlsx

for the ACOS Standard value - fill: 0.17

### b. Identical Output File  
App outcome file at the end of the simulation is identical to the example file in 
/Applications/My Apps/Bid Opt App Aug 17, 2025/PRD/Campaign Optimizer 1/Output Excel Example - Bulk 7 Days (.17 ACOS).xlsx

### c. Real User Simulation
The test was operated by simulating a real user operation of the app via Playwright MCP

### Before reporting success ask yourself if you can v all the below:
1. Are 100% of every single cell in the outpot excel file identical to the matching example file cell? v / x 
2. Did I verify this with a playwright test simulating real human use? v/x
3. Is every change I mage complies 100% with the relevant epc in /Applications/My Apps/Bid Opt App Aug 17, 2025/PRD/Portfilio Optimizer? v/x

4. 100% Identical Definition:

  "Every cell value at the same row and column position contains exactly the same string representation when both files 
  are loaded with identical data type formatting (dtype=str, na_filter=False), after excluding timestamp-based columns 
  like file names or generation dates."

  Key Requirements:
  1. Same sheet structure (identical sheet names and order)
  2. Same dimensions (identical rows × columns per sheet)
  3. Same column headers (identical column names and order)
  4. Same cell content (exact string match after standardized loading)
  5. Exclude dynamic fields (file names with timestamps, generation dates)

  Verification Method:
  pd.read_excel(file, sheet_name=None, dtype=str, na_filter=False)
  # Then cell-by-cell string comparison: str(actual_cell) == str(expected_cell)

Only if all have v - you reached 100% success. If not than keep fixing. If youmust stop - report partial success and explain what was not met. 

If you stop before 100% success - you should provide a good reason for it - eather you needed help from me, or passed 10 trials of fixing something with no success