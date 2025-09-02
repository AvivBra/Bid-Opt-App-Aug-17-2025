# Organize Top Campaigns Integration Test Specification

## Test-Fix Loop (Allowed Code Files)

**Allowed for automatic fixes:**
/Applications/My Apps/Bid Opt App Aug 17, 2025/PRD/Portfilio Optimizer/Logic/merging-specification.md
/Applications/My Apps/Bid Opt App Aug 17, 2025/PRD/Portfilio Optimizer/Logic/Campaigns w:o Portfolios logic.md
  - business/portfolio_optimizations/results_manager.py
  - business/portfolio_optimizations/orchestrator.py
  - business/portfolio_optimizations/service.py


**Process:** Automatically identify and fix issues in these files, then retest until success criteria are met.

## Test-Report (Non-Editable Files)

**Not allowed for automatic fixes:**
All the rest except from those mentioned as Allowed for automatic fixes

**Process:** Generate detailed report for user review - never modify these files.

## Success Criteria

The test-fix loop continues until all 3 criteria are met:

### a. 100% Compliance with Spec
100% compliance with the relevant spec in:
- for the first test of a scenario if only the "campaigns wo portfolios" checkbox checked:
/Applications/My Apps/Bid Opt App Aug 17, 2025/PRD/Portfilio Optimizer/Excel Examples/Output example bulk - only campaign wo portfolios checkbox.xlsx

- for the second scenario of both "campaigns wo portfolios" + "empty portfolios" checked:
/Applications/My Apps/Bid Opt App Aug 17, 2025/PRD/Portfilio Optimizer/Excel Examples/Output example both checkboxes in portfolio optiization are checked.xlsx

### b. Identical Output File  
App outcome file at the end of the simulation is identical to the example file in 

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