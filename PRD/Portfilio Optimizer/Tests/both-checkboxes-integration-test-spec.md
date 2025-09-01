# Both Checkboxes Integration Test Specification

## Executive Summary

• **100% Output Accuracy Required**: All fixes MUST result in output 100% identical to expected example - no exceptions
• **100% PRD Compliance Required**: All fixes MUST comply 100% with PRD specifications in `/Applications/My Apps/Bid Opt App Aug 17, 2025/PRD/Portfilio Optimizer/`
• **Zero Visual Interference**: Runs completely invisibly in background - no windows, pop-ups, or interruption to your work
• **Fully Autonomous Execution**: Claude Code executes complete test start-to-finish without any user input required
• **Both Optimizations Integration**: Tests BOTH "Empty Portfolios" AND "Campaigns w/o Portfolios" optimizations running together with proper merging
• **Perfect Match Validation**: Validates 100% identical match with `/Applications/My Apps/Bid Opt App Aug 17, 2025/PRD/Portfilio Optimizer/Excel Examples/Output example both checkboxes in portfolio optiization are checked.xlsx`

---

## Test Phases

### Phase 1: Environment Setup (Invisible Background Operation)
- Launch Portfolio Optimizer app on localhost:8501
- Initialize headless Chromium browser (completely invisible - no windows appear on screen)
- Verify access to input file: `PRD/Portfilio Optimizer/Excel Examples/Input Bulk Example.xlsx`
- Verify access to expected output: `PRD/Portfilio Optimizer/Excel Examples/Output example both checkboxes in portfolio optiization are checked.xlsx`

### Phase 2: User Flow Simulation (Automated & Invisible)
- Navigate to Portfolio Optimizer page (automated clicking - no visual browser)
- Ensure all optimization checkboxes are unchecked first (reset to clean state)
- Select BOTH "Empty Portfolios" AND "Campaigns w/o Portfolios" optimization checkboxes (automated selection)
- Upload input file via file picker (programmatic upload - no file dialog appears)
- Click "Process Optimizations" button (automated clicking)
- Wait for processing completion (monitoring without UI)
- Download output file to temporary location (silent download - no download dialog)

### Phase 3: Output Validation (Background File Processing)

#### Phase 3A: File Structure & Content Loading
- Load actual output file with pandas (silent file access - no UI)
- Load expected output file with pandas (background processing)
- Validate Excel file integrity and readability

#### Phase 3B: Content Normalization
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

#### Phase 3C: Structural Validation
- Verify sheet order and naming consistency
- Expected sheets: "Portfolios", "Campaign", "Product Ad", "Sheet3"
- Validate column positioning and exact naming
- Check row and column count precision across sheets
- Ensure data type consistency for corresponding cells

#### Phase 3D: PRD Compliance Validation
- **Preprocessing Compliance Check**:
  - Verify original "Sponsored Products Campaigns" sheet no longer exists
  - Confirm "Campaigns" sheet contains only Entity="Campaign" rows
  - Confirm "Product Ad" sheet contains only Entity="Product Ad" rows
  - Validate only required sheets present (Portfolios, Campaigns, Product Ad, Sheet3)

- **Empty Portfolios Logic Validation**:
  - Check "Camp Count" column exists in Portfolios sheet
  - Validate Camp Count calculations match actual campaign counts
  - Verify "Old Portfolio Name" backup column created
  - Validate portfolio name changes follow logic (Camp Count=0, name not in exclusions)
  - Check Operation="update" for modified portfolios
  - Verify Budget Amount="" and Budget Start Date="" for modified portfolios  
  - Confirm Budget Policy="No Cap" for modified portfolios

- **Campaigns Without Portfolios Logic Validation**:
  - Identify all campaigns with originally empty Portfolio ID
  - Verify exactly these campaigns get Portfolio ID="84453417629173"
  - Confirm Operation="update" for these campaigns
  - Validate no other campaigns modified

- **Contract Compliance Validation**:
  - Verify protected columns unchanged (Entity, Campaign ID, Portfolio ID in Portfolios)
  - Check cell-level modifications (not row-level)
  - Validate processing order effects (Empty Portfolios first, then Campaigns w/o Portfolios)
  - Confirm no unauthorized columns or data types modified

#### Phase 3E: Comprehensive Cell Comparison
- Compare ALL sheets (Portfolios, Campaign, Product Ad, Sheet3) cell-by-cell (100% comprehensive validation)
- Apply content normalization rules during comparison
- Flag cells that differ after all normalization attempts
- Generate detailed mismatch reports with cell coordinates and content types
- Calculate match percentage across all sheets and identify discrepancies in any sheet

#### Phase 3F: Integration Logic Validation
- Verify both optimizations executed in correct sequence
- Check conflict resolution applied correctly (if any conflicts occurred)
- Validate merging specification compliance (cell-level patches)
- Confirm yellow highlighting present on all modified rows

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
- **Comprehensive Validation**: 
  - Portfolios sheet (~214×12) must match perfectly
  - Campaign sheet (~976×48) must match perfectly  
  - Product Ad sheet (~984×48) must match perfectly
  - Sheet3 metadata must match perfectly
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

### PRD Compliance Requirements

#### 1. Preprocessing Logic Compliance (`preprocessing-logic.md`)
- **Sheet Restructuring**: Verify "Sponsored Products Campaigns" split correctly:
  - Entity="Campaign" rows → "Campaigns" sheet 
  - Entity="Product Ad" rows → "Product Ad" sheet
  - Original "Sponsored Products Campaigns" sheet deleted
  - Unused sheets deleted (keeping only: Portfolios, Campaigns, Product Ad)

#### 2. Empty Portfolios Logic Compliance (`empty-portfolios-logic.md`)
- **Camp Count Column**: Verify "Camp Count" helper column created in Portfolios sheet
- **Camp Count Calculation**: Each portfolio's count matches actual campaigns with that Portfolio ID
- **Old Portfolio Name**: Verify "Old Portfolio Name" backup column created in Portfolios sheet
- **Portfolio Name Logic**: Portfolios with Camp Count=0 AND Portfolio Name not in ["Paused", "Terminal", "Top Terminal", numeric] get lowest available number as new name
- **Operation Updates**: Modified portfolios get Operation="update" 
- **Budget Clearing**: Modified portfolios get Budget Amount="" and Budget Start Date=""
- **Budget Policy**: Modified portfolios get Budget Policy="No Cap"

#### 3. Campaigns Without Portfolios Logic Compliance (`Campaigns w:o Portfolios logic.md`)
- **Target Identification**: Find campaigns with Entity="Campaign" AND empty Portfolio ID
- **Portfolio Assignment**: All 5 target campaigns get Portfolio ID="84453417629173"
- **Operation Setting**: All 5 target campaigns get Operation="update"
- **Scope Limitation**: Only affects Entity="Campaign" rows in Campaigns sheet

#### 4. Merging Specification Compliance (`merging-specification.md`)
- **Cell-Level Updates**: Only individual cells that changed differ from input - not entire rows
- **Patch Application**: Sequential application of patches from each optimization
- **Conflict Resolution**: Later optimization wins if same cell modified twice
- **Change Tracking**: Every modification traceable to specific optimization
- **Update Limits**: Maximum 500,000 cell updates, maximum 60 seconds merge time

#### 5. Portfolio Flow Sequence Compliance (`portfolio-flow-sequence.md`)
- **Processing Order**: Empty Portfolios runs first, then Campaigns w/o Portfolios
- **Session State**: Proper state management through all 7 phases
- **Data Flow**: orchestrator → factory → strategies → results_manager → service
- **Output Generation**: Excel file with yellow highlighting on updated rows

#### 6. Optimization Contract Compliance (`optimization-contract-spec.md`)
- **Function Signature**: Both strategies implement `run(all_sheets) -> OptimizationResult`
- **Result Structure**: result_type, merge_keys, patch fields mandatory
- **Patch Content**: Only changed rows, not full data
- **No In-Place Modification**: Original data preserved, work on copies
- **Performance Limits**: Max 30 seconds per optimization, 500k rows, 40MB file
- **Protected Columns**: Entity, Campaign ID, Portfolio ID never modified
- **Metrics Reporting**: Rows checked/updated/failed counts for each optimization

#### 7. Results Manager Contract Compliance (`results-manager-contract-spec.md`)
- **Sheet Mapping**: campaigns→"Campaigns", portfolios→"Portfolios"
- **Merge Algorithm**: Target row identification by merge keys, column-level updates only
- **Conflict Policy**: "Last wins" with detailed logging
- **Protected Columns**: Entity, Campaign ID (in Campaigns), Portfolio ID (in Portfolios)
- **Processing Order**: empty_portfolios first, campaigns_without_portfolios second
- **Run Report**: Total optimizations, success count, rows updated per sheet, execution time

#### 8. Output File Structure Compliance
- **Sheet Order**: Portfolios, Campaigns, Product Ad (+ Sheet3 metadata if present)
- **Column Preservation**: All original columns maintained in exact order
- **Row Highlighting**: Yellow background on all modified rows
- **ID Formatting**: Text format (not scientific notation) for all ID columns
- **Data Types**: Consistent data types between input and output

### Test Fail Scenarios

#### Critical Failures (100% PRD Non-Compliance)
- **Preprocessing Failures**:
  - Original "Sponsored Products Campaigns" sheet still exists
  - "Campaigns" sheet missing or contains non-Campaign entities
  - "Product Ad" sheet missing or contains non-Product Ad entities
  - Unauthorized sheets present beyond required sheets
- **Empty Portfolios Logic Failures**:
  - "Camp Count" column missing from Portfolios sheet
  - Camp Count calculations incorrect (don't match actual campaign counts)
  - "Old Portfolio Name" backup column missing
  - Portfolio names changed incorrectly (wrong logic application)
  - Missing Operation="update" on modified portfolios
  - Budget Amount/Start Date not cleared on modified portfolios
  - Budget Policy not set to "No Cap" on modified portfolios
- **Campaigns Without Portfolios Logic Failures**:
  - Wrong Portfolio ID assigned (not "84453417629173")
  - Missing Operation="update" on target campaigns
  - Wrong campaigns modified (not the 5 originally empty Portfolio ID campaigns)
  - Additional campaigns incorrectly modified
- **Contract Violations**:
  - Protected columns modified (Entity, Campaign ID, Portfolio ID in Portfolios)
  - Full row modifications instead of cell-level changes
  - Wrong processing order executed
  - Unauthorized column modifications
- **Integration Failures**:
  - Wrong optimization execution order
  - Improper conflict resolution
  - Missing yellow highlighting on modified rows
  - Incorrect merging specification implementation

#### Output Quality Failures
- Missing sheets or columns
- Cell value discrepancies > 0% after comprehensive normalization
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

## Integration Logic Validation

### Expected Changes Analysis
Based on input file analysis:
- **Input**: 5 campaigns in "Sponsored Products Campaigns" sheet have empty Portfolio ID
- **Expected**: These 5 campaigns should receive Portfolio ID="84453417629173" and Operation="update"
- **Campaigns IDs**: 495869931307668, 382943963558716, 526956141409691, 318139964703398, 448927690638691

### Merging Specification Compliance
- **Cell-Level Updates**: Only specific cells that changed should be different from input
- **Conflict Resolution**: If both optimizations target same cell, later optimization wins
- **Protected Columns**: Entity, Campaign ID, Portfolio ID (in Portfolios sheet) must not be corrupted
- **Change Tracking**: Every modification must be traceable to specific optimization logic

### Sheet Mapping Validation
- **Input → Output Mapping**:
  - "Sponsored Products Campaigns" → "Campaign"
  - "Portfolios" → "Portfolios" 
  - "RAS Campaigns" → "Product Ad"
  - "Sheet3" → "Sheet3"

---

## Automated Issue Resolution Protocol

### Portfolio Optimizations Files (Auto-Fix Enabled)
- **Scope**: Files in `/Applications/My Apps/Bid Opt App Aug 17, 2025/business/portfolio_optimizations/` and `/Applications/My Apps/Bid Opt App Aug 17, 2025/app/components/portfolio_optimizer.py`
- **Action**: Automatically identify and fix code issues causing test failures
- **Mandatory Requirements**: 
  - All fixes MUST result in 100% identical output to expected example
  - All fixes MUST comply 100% with PRD specifications
  - Must follow exact campaigns-without-portfolios logic and empty portfolios logic
  - Must implement proper cell-level merging per specification
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
- **Continue Working**: Use computer normally during test (3-5 minutes)  
- **Zero Interruption**: No visual interference with your workflow
- **Get Results**: Terminal output shows completion and results

### Duration
- Total test time: 3-5 minutes
- User flow simulation: 90 seconds
- File processing: 60 seconds  
- Output validation: 30 seconds

### Output
- Binary pass/fail result
- Confidence level (96% or environment risk warning)
- Discrepancy count and locations if applicable
- Auto-fix iteration count (if portfolio optimization issues found)
- Issue report for non-portfolio files (if applicable)
- Recommended action based on results

---

## Test Data Specifications

### Input File Details
- **Path**: `PRD/Portfilio Optimizer/Excel Examples/Input Bulk Example.xlsx`
- **Sheets**: Portfolios (~214 rows), Sponsored Products Campaigns (~24,822 rows), RAS Campaigns (0 rows), Sheet3 (metadata)
- **Target Data**: 5 campaigns without Portfolio ID in "Sponsored Products Campaigns" sheet

### Expected Output File Details  
- **Path**: `PRD/Portfilio Optimizer/Excel Examples/Output example both checkboxes in portfolio optiization are checked.xlsx`
- **Sheets**: Portfolios (~214 rows), Campaign (~976 rows), Product Ad (~984 rows), Sheet3 (metadata)
- **Expected Changes**: All 5 target campaigns should have Portfolio ID="84453417629173" and Operation="update"

### Validation Tolerance Levels
- **Monetary Values**: ±0.01 precision tolerance after normalization
- **Date Values**: Format variations acceptable if semantically identical
- **Boolean Values**: Any valid boolean representation accepted after standardization  
- **Text Values**: Case-insensitive comparison for non-critical fields
- **ID Values**: Exact match required after padding/formatting normalization
- **Percentage Values**: Format differences acceptable (0.5 vs 50% handled consistently)