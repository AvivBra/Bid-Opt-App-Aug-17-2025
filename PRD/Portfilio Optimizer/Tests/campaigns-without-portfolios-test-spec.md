# Campaigns Without Portfolios Function Test Specification

## Executive Summary

• **100% Output Accuracy Required**: All fixes MUST result in output 100% identical to expected example - no exceptions
• **100% PRD Compliance Required**: All fixes MUST comply 100% with PRD specifications in `/Applications/My Apps/Bid Opt App Aug 17, 2025/PRD/Portfilio Optimizer/`
• **Zero Visual Interference**: Runs completely invisibly in background - no windows, pop-ups, or interruption to your work
• **Fully Autonomous Execution**: Claude Code executes complete test start-to-finish without any user input required
• **Campaigns Without Portfolios Focus**: Tests EXCLUSIVELY campaigns without portfolios optimization in isolation - no other optimizations run
• **Test-Specific File Protection**: During this test execution, empty_portfolios_strategy.py is excluded from auto-fix to prevent interference with Empty Portfolios functionality
• **Perfect Match Validation**: Validates 100% identical match with `/Applications/My Apps/Bid Opt App Aug 17, 2025/PRD/Portfilio Optimizer/Excel Examples/Output example bulk - only campaign wo portfolios checkbox.xlsx`

---

## Test Phases

### Phase 1: Environment Setup (Invisible Background Operation)
- Launch Portfolio Optimizer app on localhost:8501
- Initialize headless Chromium browser (completely invisible - no windows appear on screen)
- Verify access to input file: `PRD/Portfilio Optimizer/Excel Examples/Input Bulk Example.xlsx`
- Verify access to expected output: `PRD/Portfilio Optimizer/Excel Examples/Output example bulk - only campaign wo portfolios checkbox.xlsx`

### Phase 2: User Flow Simulation (Automated & Invisible)
- Navigate to Portfolio Optimizer page (automated clicking - no visual browser)
- Ensure all optimization checkboxes are unchecked first (reset to clean state)
- Select ONLY "Campaigns w/o Portfolios" optimization checkbox (automated selection)
- Verify other optimization checkboxes (e.g., "Empty Portfolios") remain unchecked
- Upload input file via file picker (programmatic upload - no file dialog appears)
- Click "Process Optimizations" button (automated clicking)
- Wait for processing completion (monitoring without UI)
- Download output file to temporary location (silent download - no download dialog)

### Phase 3: Output Validation (Background File Processing)
- Load actual output file with pandas (silent file access - no UI)
- Load expected output file with pandas (background processing)
- **Content Normalization Phase**:
  - Normalize missing values (replace 'nan' with empty string)
  - Standardize floating point precision artifacts (e.g., "3.7399999999999998" → "3.74")
  - Trim leading/trailing whitespace from all cell values
  - Normalize boolean representations (True/False/1/0 standardization)
  - Handle empty string vs null value differences
  - Standardize date format variations within cells
  - Remove invisible characters (tabs, zero-width spaces)
  - Normalize number formatting (with/without commas, decimal consistency)
  - Standardize currency symbol presence/absence
  - Convert scientific notation to decimal representation where applicable
  - Handle Unicode character encoding differences
  - Standardize case sensitivity for text comparisons (when appropriate)
- **Structural Validation Phase**:
  - Verify sheet order and naming consistency
  - Validate column positioning and exact naming
  - Check row and column count precision across sheets
  - Ensure data type consistency for corresponding cells
- **Comprehensive Cell Comparison Phase**:
  - Compare ALL sheets (Portfolios, Campaigns, Product Ad) cell-by-cell (100% comprehensive validation)
  - Apply content normalization rules during comparison
  - Flag cells that differ after all normalization attempts
  - Generate detailed mismatch reports with cell coordinates and content types
- Calculate match percentage across all sheets and identify discrepancies in any sheet

### Phase 4: Results Analysis
- **96% Confidence Pass**: Files match exactly, real user will get identical results
- **Environment Risk Warning**: Files differ, 4% chance of browser/download environment factors
- **Logic Failure**: Files differ significantly, backend implementation issue detected
- Generate detailed discrepancy report with row/column locations
- Execute automated issue resolution protocol

---

## Success Criteria

### Test Pass (100% Confidence - MANDATORY)
- **Perfect Match Required**: 100.00% of ALL cells across ALL sheets match exactly after comprehensive normalization - no discrepancies allowed
- **Comprehensive Validation**: Portfolios sheet (214×14), Campaigns sheet (~976×49), Product Ad sheet (~984×49) all must match perfectly
- **Structural Requirements**:
  - All expected sheets exist in actual output with correct order
  - All expected columns exist with correct names and positioning in each sheet
  - Row and column counts identical across all sheets
  - Data types consistent for corresponding cells across sheets
- **Content Validation Requirements**:
  - Cell values match after applying comprehensive normalization rules
  - Floating point precision differences normalized within acceptable tolerance (±0.01 for monetary values)
  - Whitespace trimming applied consistently to all text values
  - Boolean representations standardized (True/False, 1/0, yes/no handled consistently)
  - Date/time formats validated for consistency within each sheet
  - Number formatting normalized (commas, decimals, scientific notation)
  - Unicode characters preserved and compared correctly
  - Invisible characters removed before comparison
  - Empty string vs null values handled consistently
  - Currency symbols standardized where applicable
- **PRD Compliance**: All campaigns with empty Portfolio ID assigned Portfolio ID "84453417629173" and Operation "update"
- **PRD Compliance**: Only campaigns in Campaigns sheet with Entity "Campaign" and empty Portfolio ID affected
- **PRD Compliance**: Empty Portfolios logic did NOT run (no portfolio name changes from input)
- **PRD Compliance**: No other optimization logic executed (isolated campaigns w/o portfolios only)
- **PRD Compliance**: Portfolios and Product Ad sheets remain unchanged from input (after normalization)

### Test Fail Scenarios
- Missing sheets or columns
- Cell value discrepancies > 0% after comprehensive normalization
- Incorrect campaigns without portfolios logic implementation
- Evidence of other optimization logic execution (e.g., portfolio name changes indicating Empty Portfolios ran)
- File corruption or download failure
- **Content-Specific Failures**:
  - Structural mismatches (sheet order, column positioning, row counts)
  - Data type inconsistencies between corresponding cells
  - Floating point precision errors exceeding normalization tolerance
  - Text encoding problems causing character corruption
  - Date/time format inconsistencies that cannot be normalized
  - Number formatting discrepancies (scientific notation, decimal places)
  - Boolean representation mismatches after standardization
  - Invisible character presence affecting cell comparison
  - Currency symbol inconsistencies in monetary values
  - ID/reference formatting differences (padding, case sensitivity)
  - Whitespace handling problems (leading/trailing/internal spaces)
  - Unicode character encoding differences causing display issues

---

## Cell Content Validation Methodology

### Normalization Rules Applied During Comparison
- **Floating Point Precision**: Numbers with precision artifacts (e.g., "3.7399999999999998") are normalized to clean format ("3.74")
- **Whitespace Handling**: Leading and trailing spaces removed from all cell values
- **Boolean Standardization**: All boolean representations converted to consistent format (True/False)
- **Null Value Handling**: Empty strings, "nan", null values normalized to empty string
- **Date Format Consistency**: Date values within cells validated for format consistency
- **Number Format Standards**: Commas in numbers, decimal consistency, scientific notation conversion
- **Unicode Preservation**: Character encoding differences handled while preserving meaning
- **Invisible Character Removal**: Tabs, zero-width spaces, and other invisible characters stripped
- **Currency Symbol Standardization**: Consistent currency representation where applicable
- **Case Sensitivity Rules**: Text comparisons use appropriate case handling for data type

### Validation Tolerance Levels
- **Monetary Values**: ±0.01 precision tolerance after normalization
- **Date Values**: Format variations acceptable if semantically identical
- **Boolean Values**: Any valid boolean representation accepted after standardization  
- **Text Values**: Case-insensitive comparison for non-critical fields
- **ID Values**: Exact match required after padding/formatting normalization
- **Percentage Values**: Format differences acceptable (0.5 vs 50% handled consistently)

### Edge Case Handling
- **Large Numbers**: Scientific notation vs decimal representation normalized
- **Phone Numbers**: Format variations handled (dashes, spaces, parentheses)
- **Zero Padding**: ID fields with different zero-padding levels normalized
- **Time Formats**: 24-hour vs 12-hour format differences handled
- **Special Characters**: Unicode normalization for accented characters
- **Line Breaks**: Internal line breaks within cells preserved during comparison

---

## Accuracy Assessment

### 96% Autonomous Accuracy Achievable
- **UI Simulation**: 99% (Streamlit consistency)
- **Backend Logic**: 99% (Pure Python processing)
- **File Validation**: 100% (Pandas comparison)
- **Browser Environment**: 94% (Clean profile vs user profile)
- **Download Mechanism**: 94% (Automated vs manual download)

### 4% Uncertainty Factors
- Browser extensions interference
- OS download folder integration differences
- Streamlit session cache artifacts
- File system hooks (antivirus, indexing)

---

## Risk Mitigation

### Environment Optimization
- Use fresh Streamlit app instance
- Clear browser cache before test
- Ensure adequate system resources
- Use standard download configurations

### Uncertainty Interpretation
- **Test Pass + Manual Fail**: Browser environment difference (4% scenario)
- **Test Fail**: Backend logic issue (requires code fix)
- **Test Pass**: 96% confidence in real user success

---

## Automated Issue Resolution Protocol

### Portfolio Optimizations Files (Auto-Fix Enabled)
- **Scope**: Files in `/Applications/My Apps/Bid Opt App Aug 17, 2025/business/portfolio_optimizations/` and `/Applications/My Apps/Bid Opt App Aug 17, 2025/app/components/portfolio_optimizer.py`
- **Test-Specific Exclusion**: During this test execution, do not modify `/Applications/My Apps/Bid Opt App Aug 17, 2025/business/portfolio_optimizations/strategies/empty_portfolios_strategy.py` to prevent unintended interference with Empty Portfolios logic while testing Campaigns w/o Portfolios in isolation
- **Action**: Automatically identify and fix code issues causing test failures
- **Mandatory Requirements**: 
  - All fixes MUST result in 100% identical output to expected example
  - All fixes MUST comply 100% with PRD specifications
  - Must follow exact 3-step campaigns-without-portfolios logic from "Campaigns w:o Portfolios logic.md"
- **Retry Logic**: Rerun test automatically after each fix
- **Iteration Limit**: Maximum 10 fix-and-retry cycles
- **Continue Until**: Perfect match (100.00%) achieved or iteration limit reached

### Other Code Files (Report Only - NO AUTO-FIX)
- **Scope**: Any files outside the portfolio optimizations folder
- **Action**: Generate detailed report for user review - NEVER modify these files
- **Report Contents**:
  - Exact file locations with identified issues
  - Specific problem descriptions and error traces  
  - Recommended solutions for user implementation
  - Impact assessment on test results
- **User Action Required**: Manual review and fixes by user

### Issue Classification Logic
- Trace test failure root cause to specific code files
- If root cause in `business/portfolio_optimizations/`: Enable auto-fix (EXCEPT empty_portfolios_strategy.py during this test)
- If root cause in `empty_portfolios_strategy.py`: Generate report only for this campaigns-without-portfolios test to maintain feature isolation
- If root cause in any other location: Generate report only
- If multiple causes: Auto-fix allowed portfolio files, report others including empty_portfolios_strategy.py

---

## Visual Interface & User Experience

### Zero Visual Interference Guarantee
- **No Browser Windows**: Headless Chromium runs completely invisibly
- **No Pop-ups or Dialogs**: No file dialogs, download notifications, or browser UI
- **No Screen Interference**: Takes zero visual space on your screen
- **Work Continuity**: You can type, browse, watch videos - zero interruption
- **Background CPU Only**: Uses minimal resources without visual indicators

### Autonomous Execution
- **Claude Code Control**: Full MCP Playwright automation without user input
- **Start-to-Finish**: Single command launches complete autonomous test
- **Self-Healing**: Automatically fixes portfolio optimization code issues
- **Terminal Output Only**: Results reported via text output when complete

---

## Test Execution

### Prerequisites
- Streamlit app running on localhost:8501
- Playwright MCP tools available (Claude Code has access)
- Input and expected files accessible
- Temporary directory for output file

### User Experience
- **Start Test**: Single command execution
- **Continue Working**: Use computer normally during test (2-3 minutes)  
- **Zero Interruption**: No visual interference with your workflow
- **Get Results**: Terminal output shows completion and results

### Duration
- Total test time: 2-3 minutes
- User flow simulation: 60 seconds
- File processing: 30 seconds  
- Output validation: 10 seconds

### Output
- Binary pass/fail result
- Confidence level (96% or environment risk warning)
- Discrepancy count and locations if applicable
- Auto-fix iteration count (if portfolio optimization issues found)
- Issue report for non-portfolio files (if applicable)
- Recommended action based on results