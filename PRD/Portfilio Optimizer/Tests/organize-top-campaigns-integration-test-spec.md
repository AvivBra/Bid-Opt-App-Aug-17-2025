# Organize Top Campaigns Integration Test Specification

## Test-Fix Loop (Allowed Code Files)

**Allowed for automatic fixes:**
- `/Applications/My Apps/Bid Opt App Aug 17, 2025/business/portfolio_optimizations/`
- `/Applications/My Apps/Bid Opt App Aug 17, 2025/data/writers/excel_writer.py`
- `/Applications/My Apps/Bid Opt App Aug 17, 2025/pages/portfolio_optimizer.py` (template functionality only)

**Process:** Automatically identify and fix issues in these files, then retest until success criteria are met.

## Test-Report (Non-Editable Files)

**Not allowed for automatic fixes:**
- `/Applications/My Apps/Bid Opt App Aug 17, 2025/app.py`
- `/Applications/My Apps/Bid Opt App Aug 17, 2025/data/loaders/`
- `/Applications/My Apps/Bid Opt App Aug 17, 2025/utils/`
- `/Applications/My Apps/Bid Opt App Aug 17, 2025/business/portfolio_optimizations/strategies/campaigns_without_portfolios_strategy.py`
- `/Applications/My Apps/Bid Opt App Aug 17, 2025/business/portfolio_optimizations/strategies/empty_portfolios_strategy.py`
- All other files not listed in allowed section

**Process:** Generate detailed report for user review - never modify these files.

## Success Criteria

The test-fix loop continues until all 3 criteria are met:

### a. 100% Compliance with Spec
100% compliance with the relevant spec in `/Applications/My Apps/Bid Opt App Aug 17, 2025/PRD/Portfilio Optimizer`

### b. Identical Output File  
App outcome file at the end of the simulation is identical to the example file in `/Applications/My Apps/Bid Opt App Aug 17, 2025/PRD/Portfilio Optimizer/Excel Examples/Output Bulk Example for Organize Top Campaigns.xlsx`

### c. Real User Simulation
The test was operated by simulating a real user operation of the app via Playwright MCP