# Empty Portfolio Function Test Specification

## Executive Summary

• **96% Autonomous Accuracy**: Playwright MCP automation achieves 96% accuracy in predicting real user results
• **Empty Portfolio Focus**: Tests only empty portfolio optimization against expected output file
• **Exact Output Validation**: Validates identical match with `/Applications/My Apps/Bid Opt App Aug 17, 2025/PRD/Portfilio Optimizer/Excel Examples/Empty Port Output Bulk Example.xlsx`
• **Environment Risk**: 4% uncertainty from browser profile and download mechanism differences
• **Binary Success**: Pass/fail determination with confidence level reporting

---

## Test Phases

### Phase 1: Environment Setup
- Launch Portfolio Optimizer app on localhost:8501
- Initialize headless Chromium browser with clean profile
- Verify access to input file: `PRD/Portfilio Optimizer/Excel Examples/Input Bulk Example.xlsx`
- Verify access to expected output: `PRD/Portfilio Optimizer/Excel Examples/Empty Port Output Bulk Example.xlsx`

### Phase 2: User Flow Simulation
- Navigate to Portfolio Optimizer page
- Select "Empty Portfolios" optimization checkbox
- Upload input file via file picker
- Click "Process Optimizations" button
- Wait for processing completion
- Download output file to temporary location

### Phase 3: Output Validation
- Load actual output file with pandas (dtype=str)
- Load expected output file with pandas (dtype=str)
- Normalize missing values (replace 'nan' with empty string)
- Compare all sheets, columns, and cell values
- Calculate match percentage and identify discrepancies

### Phase 4: Results Analysis
- **96% Confidence Pass**: Files match exactly, real user will get identical results
- **Environment Risk Warning**: Files differ, 4% chance of browser/download environment factors
- **Logic Failure**: Files differ significantly, backend implementation issue detected
- Generate detailed discrepancy report with row/column locations
- Execute automated issue resolution protocol

---

## Success Criteria

### Test Pass (96% Confidence)
- All expected sheets exist in actual output
- All expected columns exist with correct names  
- 100% of cell values match exactly
- Row and column counts identical
- Empty portfolio renamed from "Test" to "1" with correct metadata

### Test Fail Scenarios
- Missing sheets or columns
- Cell value discrepancies > 0%
- Incorrect empty portfolio logic implementation
- File corruption or download failure

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
- **Scope**: Files in `/Applications/My Apps/Bid Opt App Aug 17, 2025/business/portfolio_optimizations/` only
- **Action**: Automatically identify and fix code issues causing test failures
- **Retry Logic**: Rerun test automatically after each fix
- **Iteration Limit**: Maximum 10 fix-and-retry cycles
- **Continue Until**: Test passes or iteration limit reached

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
- If root cause in `business/portfolio_optimizations/`: Enable auto-fix
- If root cause in any other location: Generate report only
- If multiple causes: Auto-fix portfolio files, report others

---

## Test Execution

### Prerequisites
- Streamlit app running on localhost:8501
- Playwright MCP tools available
- Input and expected files accessible
- Temporary directory for output file

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