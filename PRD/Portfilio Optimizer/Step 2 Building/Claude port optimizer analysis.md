# Portfolio Optimization Function Hierarchy & Flow Analysis

Based on comprehensive analysis of the portfolio optimization codebase, this document maps out the complete function hierarchy and call flow.

## **MAIN SYSTEM ARCHITECTURE**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           PORTFOLIO OPTIMIZATION SYSTEM                 │
└─────────────────────────────────────────────────────────────────────────┘

                                    ┌─────────────────┐
                                    │  User Interface │
                                    │ CampaignOptimi- │
                                    │ zerPage.render()│
                                    │ (campaign_opti- │
                                    │ mizer.py:23)    │
                                    └─────────┬───────┘
                                              │
                                    ┌─────────▼───────┐
                                    │ Factory Pattern │
                                    │ PortfolioOptimi-│
                                    │ zationFactory   │
                                    │ (factory.py:12) │
                                    └─────────┬───────┘
                                              │
                ┌─────────────────────────────┼─────────────────────────────┐
                │                             │                             │
        ┌───────▼────────┐           ┌───────▼────────┐           ┌───────▼────────┐
        │ discover_optimi-│           │ create_optimiz-│           │ get_available_ │
        │ zations()       │           │ ation()        │           │ optimizations()│
        │ (factory.py:25) │           │ (factory.py:170)│          │ (factory.py:149)│
        └────────────────┘           └────────────────┘           └────────────────┘
                │                             │                             │
                │                             │                             │
                ▼                             ▼                             ▼
        ┌────────────────┐           ┌────────────────┐           ┌────────────────┐
        │ Dynamic Module │           │ Results        │           │ UI Checkbox    │
        │ Discovery      │           │ Processing     │           │ Generation     │
        └────────────────┘           └────────┬───────┘           └────────────────┘
                                              │
                                    ┌─────────▼───────┐
                                    │ PortfolioOptimi-│
                                    │ zationResultsMan│
                                    │ ager            │
                                    │ (results_mana-  │
                                    │ ger.py:11)      │
                                    └─────────┬───────┘
                                              │
                    ┌─────────────────────────┼─────────────────────────┐
                    │                         │                         │
            ┌───────▼────────┐       ┌───────▼────────┐       ┌───────▼────────┐
            │ add_result()   │       │ create_combined│       │ get_processing_│
            │ (results_man-  │       │ _output()      │       │ summary()      │
            │ ager.py:24)    │       │ (results_man-  │       │ (results_man-  │
            └────────────────┘       │ ager.py:63)    │       │ ager.py:352)   │
                                     └────────────────┘       └────────────────┘
```

## **DETAILED ORCHESTRATION FLOW**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     OPTIMIZATION ORCHESTRATORS                         │
└─────────────────────────────────────────────────────────────────────────┘

Factory.create_optimization() calls one of:

┌─────────────────────────────────┐    ┌─────────────────────────────────┐
│  Empty Portfolios Orchestrator │    │ Campaigns w/o Portfolios Orch. │
│  EmptyPortfoliosOrchestrator    │    │ CampaignsWithoutPortfolios-     │
│  (empty_portfolios/orchestrator │    │ Orchestrator                    │
│  .py:13)                        │    │ (campaigns_without_portfolios/  │
└─────────────────┬───────────────┘    │ orchestrator.py:13)             │
                  │                    └─────────────────┬───────────────┘
                  │                                      │
                  │ run(bulk_data, combined_mode=True)   │ run(bulk_data, combined_mode=True)
                  │ (line 23)                            │ (line 23)
                  ▼                                      ▼

        ┌─────────────────────────────────────────────────────────────────┐
        │               STANDARDIZED PROCESSING PIPELINE                  │
        │                    (Both Orchestrators)                         │
        └─────────────────────────────────────────────────────────────────┘

Step 1: VALIDATION
        ┌─────────────────────┐              ┌─────────────────────┐
        │ EmptyPortfolios-    │              │ CampaignsWithout-   │
        │ Validator.validate()│              │ PortfoliosValidator │
        │ (validator.py)      │              │ .validate()         │
        └─────────┬───────────┘              │ (validator.py)      │
                  │                          └─────────┬───────────┘
                  │                                    │
                  ▼                                    ▼
            [Validation Details]                 [Validation Details]
            - Check required columns             - Check required columns  
            - Validate data structure            - Validate data structure

Step 2: CLEANING  
        ┌─────────────────────┐              ┌─────────────────────┐
        │ EmptyPortfolios-    │              │ CampaignsWithout-   │
        │ Cleaner.clean()     │              │ PortfoliosCleaner   │
        │ (cleaner.py)        │              │ .clean()            │
        └─────────┬───────────┘              │ (cleaner.py)        │
                  │                          └─────────┬───────────┘
                  │                                    │
                  ▼                                    ▼
            [Data Cleaning]                      [Data Cleaning]
            - Remove invalid rows                - Filter Entity=Campaign
            - Standardize formats                - Handle missing values

Step 3: PROCESSING
        ┌─────────────────────┐              ┌─────────────────────┐
        │ EmptyPortfolios-    │              │ CampaignsWithout-   │
        │ Processor.process() │              │ PortfoliosProcessor │
        │ (processor.py:22)   │              │ .process()          │
        └─────────┬───────────┘              │ (processor.py:18)   │
                  │                          └─────────┬───────────┘
                  │                                    │
                  ▼                                    ▼
```

## **SPECIFIC PROCESSING LOGIC FLOWS**

### **Empty Portfolios Processing** (processor.py:22)

```
EmptyPortfoliosProcessor.process()
┌─────────────────────────────────────────────────────────────────┐
│ 1. Find portfolios_with_campaigns                               │
│    - Extract Campaign Portfolio IDs (line 43-46)               │
│    - Create set of portfolios that have campaigns              │
│                                                                 │
│ 2. Identify empty portfolios (line 55-99)                      │
│    - Loop through all portfolios                               │
│    - Check: has_no_campaigns AND is_name_not_numeric           │
│    - Check: NOT in EXCLUDED_PORTFOLIO_NAMES                    │
│    - Store empty_portfolio_indices                             │
│                                                                 │
│ 3. Update empty portfolios (line 116-170)                      │
│    - Find smallest unused numeric name                         │
│    - Update Portfolio Name, Operation, Budget Amount           │
│    - Track updated_indices for Results Manager                 │
│                                                                 │
│ 4. Return processed data with tracking                         │
│    - Full DataFrames with updates applied                      │
│    - self.updated_indices stored for precise merging           │
└─────────────────────────────────────────────────────────────────┘
```

### **Campaigns Without Portfolios Processing** (processor.py:18)

```
CampaignsWithoutPortfoliosProcessor.process()
┌─────────────────────────────────────────────────────────────────┐
│ 1. Get filtered campaigns (Entity = Campaign)                  │
│    - campaigns_filtered from cleaned data                      │
│    - campaigns_full for output (line 32-35)                   │
│                                                                 │
│ 2. Find campaigns without portfolio (line 41-44)              │
│    - campaigns_without_portfolio_mask = Portfolio ID.isna()    │
│    - Filter campaigns that need portfolio assignment          │
│                                                                 │
│ 3. Update campaigns in full dataframe (line 51-76)            │
│    - Loop through campaigns_without_portfolio                 │
│    - Find matching rows in campaigns_full by Campaign ID      │
│    - Set Portfolio ID = TARGET_PORTFOLIO_ID (line 63-65)     │
│    - Set Operation = UPDATE_OPERATION                          │
│    - Track updated_indices                                     │
│                                                                 │
│ 4. Return processed data                                       │
│    - campaigns_filtered and campaigns_full                     │
│    - self.updated_indices for Results Manager                 │
└─────────────────────────────────────────────────────────────────┘
```

## **RESULTS MANAGEMENT & OUTPUT FLOW**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      RESULTS COMBINATION FLOW                          │
└─────────────────────────────────────────────────────────────────────────┘

After orchestrators complete, Results Manager combines results:

PortfolioOptimizationResultsManager.create_combined_output(original_sheets)
(results_manager.py:63)
┌─────────────────────────────────────────────────────────────────┐
│ 1. Keep ALL original data (line 76-91)                         │
│    - campaigns_data = original_sheets["Sponsored Products..."]  │
│    - portfolios_data = original_sheets["Portfolios"]          │
│                                                                 │
│ 2. Apply optimizations in CHAIN (line 94-250)                 │
│    - Loop through self.combined_results                        │
│    - For each successful result:                               │
│      ┌─────────────────────────────────────────────────────────│
│      │ if result_type == "campaigns":                          │
│      │   - Use updated_indices for precise merging (127-145)  │
│      │   - campaigns_data.loc[idx] = processed_df.loc[idx]    │
│      │   - Count campaigns_updated_count                      │
│      │                                                         │
│      │ elif result_type == "portfolios":                      │
│      │   - Use updated_indices for precise merging (195-209) │
│      │   - portfolios_data.loc[idx] = processed_df.loc[idx]  │
│      │   - Count portfolios_updated_count                     │
│      └─────────────────────────────────────────────────────────│
│                                                                 │
│ 3. Create Excel output (line 253-290)                         │
│    - _create_excel_file(campaigns_data, portfolios_data)      │
│    - Apply text formatting to prevent scientific notation     │
│    - Write both sheets to BytesIO                             │
│                                                                 │
│ 4. Build comprehensive summary                                 │
│    - Total/successful optimizations count                      │
│    - campaigns_updated/portfolios_updated counts              │
│    - Processing summary from each orchestrator                │
└─────────────────────────────────────────────────────────────────┘
```

## **KEY FUNCTION REFERENCES & CALL HIERARCHY**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           FUNCTION REFERENCE MAP                        │
└─────────────────────────────────────────────────────────────────────────┘

📁 app/components/campaign_optimizer.py
   └── CampaignerOptimizerPage.render() [line 23]
       ├── factory.get_portfolio_optimization_factory() [line 54]
       ├── factory.get_enabled_optimizations() [line 55]
       ├── orchestrator.run(all_sheets, combined_mode=True) [line 312-314]
       └── results_manager.create_combined_output(all_sheets) [line 392-394]

📁 business/portfolio_optimizations/factory.py
   └── PortfolioOptimizationFactory [line 12]
       ├── __init__() [line 20] → _discover_optimizations() [line 23]
       ├── _discover_optimizations() [line 25] → _register_optimization() [line 46]
       ├── create_optimization() [line 170] → orchestrator_class() [line 186]
       └── get_enabled_optimizations() [line 158]

📁 business/portfolio_optimizations/results_manager.py
   └── PortfolioOptimizationResultsManager [line 11]
       ├── add_result() [line 24] → stores result in combined_results [line 49]
       ├── create_combined_output() [line 63] → _create_excel_file() [line 253]
       └── _create_excel_file() [line 309] → apply_text_format_before_write() [line 330]

📁 business/portfolio_optimizations/empty_portfolios/orchestrator.py
   └── EmptyPortfoliosOrchestrator [line 13]
       └── run() [line 23]
           ├── validator.validate() [line 41]
           ├── cleaner.clean() [line 54]  
           ├── processor.process() [line 59]
           └── processor.get_updated_indices() [line 72]

📁 business/portfolio_optimizations/empty_portfolios/processor.py
   └── EmptyPortfoliosProcessor [line 14]
       └── process() [line 22]
           ├── _is_numeric_string() [line 185] - helper for portfolio name validation
           ├── _is_excluded_portfolio() [line 199] - check excluded names
           └── get_updated_indices() [line 215] - returns tracking indices

📁 business/portfolio_optimizations/campaigns_without_portfolios/orchestrator.py
   └── CampaignsWithoutPortfoliosOrchestrator [line 13]
       └── run() [line 23]
           ├── validator.validate() [line 41]
           ├── cleaner.clean() [line 54]
           ├── processor.process() [line 59]
           └── processor.get_updated_indices() [line 72]

📁 business/portfolio_optimizations/campaigns_without_portfolios/processor.py
   └── CampaignsWithoutPortfoliosProcessor [line 10]
       └── process() [line 18]
           ├── Find campaigns_without_portfolio_mask [line 41]
           ├── Update campaigns_full with TARGET_PORTFOLIO_ID [line 63-65] 
           └── get_updated_indices() [line 101] - returns tracking indices
```

## **SUMMARY: Complete Function Hierarchy**

The portfolio optimization system follows this hierarchical flow:

**1. Entry Point** → **2. Factory Discovery** → **3. User Selection** → **4. Orchestration** → **5. Results Combination** → **6. Output Generation**

### **Key Architectural Patterns:**

1. **Factory Pattern**: `PortfolioOptimizationFactory` dynamically discovers optimization modules by scanning subdirectories for `orchestrator.py` files

2. **Orchestration Pattern**: Each optimization follows the same pipeline:
   - **Validation** → **Cleaning** → **Processing** → **Output Formatting**

3. **Results Management Pattern**: `PortfolioOptimizationResultsManager` intelligently combines results from multiple optimizations using precise index tracking

4. **Precise Data Merging**: The system uses `updated_indices` to track exactly which rows were modified, enabling accurate combination of multiple optimization results without data loss

### **Critical Integration Points:**

- **campaigns_without_portfolios** updates the **Campaigns** sheet (result_type="campaigns")
- **empty_portfolios** updates the **Portfolios** sheet (result_type="portfolios") 
- Results Manager chains these updates sequentially, preserving all original data while applying only the specific changes from each optimization

### **Data Flow Summary:**

1. **User uploads Excel file** with multiple sheets
2. **Factory discovers** available optimizations dynamically
3. **User selects** which optimizations to run
4. **Each orchestrator** processes its optimization independently:
   - Validates input data structure
   - Cleans and filters relevant data
   - Applies optimization logic
   - Tracks precise row indices that were modified
5. **Results Manager** combines all optimization results:
   - Preserves ALL original data
   - Applies only the specific changes from each optimization
   - Uses `updated_indices` for precise merging
   - Prevents data loss or corruption
6. **Final output** contains the original data with all optimizations applied

This architecture allows for modular, extensible portfolio optimizations that can run independently or in combination while maintaining data integrity throughout the process.

## **Extension Points for New Optimizations**

To add a new optimization:

1. **Create new directory** under `business/portfolio_optimizations/`
2. **Implement standard components**:
   - `orchestrator.py` with `run()` method
   - `validator.py` for input validation
   - `cleaner.py` for data preparation
   - `processor.py` with `process()` and `get_updated_indices()` methods
   - `output_formatter.py` for standalone output
   - `constants.py` for configuration
3. **Follow the standard interface**:
   - `run(bulk_data, combined_mode=True)` 
   - Return `(processed_df, processing_details)`
   - Include `updated_indices` in processing_details
4. **Factory will automatically discover** the new optimization
5. **Results Manager will automatically integrate** it into the combination flow

The system is designed to be highly extensible while maintaining consistency and data integrity across all optimizations.