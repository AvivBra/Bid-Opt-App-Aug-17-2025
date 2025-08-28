# Zero Sales Optimization - Logic

## Overview
Zero Sales optimization identifies keywords and products with no sales (Units = 0) and adjusts their bids to reduce wasted spend while maintaining visibility.

## Required Files
- **Template File:** Port Values sheet (Portfolio Name, Base Bid, Target CPA)
- **Bulk 60 File:** 60 days of campaign data with 48 columns

## Process Flow

### Step 1: Initial Data Split
Separate Bulk data by Entity type:
- **Targeting sheet:** Keyword + Product Targeting (will be cleaned and processed)
- **Bidding Adjustment sheet:** Bidding Adjustment rows (kept as-is, no cleaning)

Note: Product Ad entities are not included in this optimization.

### Step 2: Data Cleaning (Targeting sheet only)
Apply filters to Targeting sheet:
1. Keep only rows where Units = 0
2. Remove rows from these 10 excluded portfolios:
   - Flat 30, Flat 25, Flat 40
   - Flat 25 | Opt, Flat 30 | Opt  
   - Flat 20, Flat 15
   - Flat 40 | Opt, Flat 20 | Opt, Flat 15 | Opt
3. Remove rows from portfolios marked as "Ignore" in Template
- שם העמודה שבה נמצאים שמות הפוטפוליוז בבלק הוא Portfolio Name (Informational only) 


### Step 3: Add Helper Columns
Add 7 helper columns to the LEFT of Bid column (Targeting sheet only):
1. **Max BA:** Maximum Percentage value for the Campaign ID from Bidding Adjustment data
2. **Base Bid:** Value from Template for the portfolio
3. **Target CPA:** Value from Template for the portfolio  
4. **Adj. CPA:** Target CPA × (1 + Max BA/100)
5. **calc1:** Intermediate calculation (see Step 4)
6. **calc2:** Intermediate calculation (see Step 4)
7. **Old Bid:** Original Bid value before changes

### Step 4: Calculate New Bid
Apply one of four calculation cases based on Target CPA and Campaign Name:

#### Case A: Target CPA is empty + Campaign name contains "up and"
- New Bid = Base Bid × 0.5

#### Case B: Target CPA is empty + Campaign name does NOT contain "up and"  
- New Bid = Base Bid

#### Case C: Target CPA has value + Campaign name contains "up and"
1. calc1 = Adj. CPA × 0.5 / (Clicks + 1)
2. calc2 = calc1 - (Base Bid × 0.5)
3. If calc1 ≤ 0: New Bid = calc2
4. Otherwise: New Bid = Base Bid × 0.5

#### Case D: Target CPA has value + Campaign name does NOT contain "up and"
1. calc1 = Adj. CPA / (Clicks + 1)
2. calc2 = calc1 - (Base Bid / (1 + Max BA / 100))
3. If calc1 ≤ 0: New Bid = calc2
4. Otherwise: New Bid = Base Bid / (1 + Max BA / 100)

### Step 5: Post-Processing
1. Set Operation = "Update" for all rows in both sheets
2. Round all Bid values to 3 decimal places
3. Mark rows with pink highlighting if:
   - Bid < 0.02 (below minimum)
   - Bid > 1.25 (above maximum)
   - Clicks > 15 (high clicks without sales)
   - Bid calculation failed (NaN)

## Output Structure

### Working File Only (No Clean File in current phase)
**Filename:** Auto Optimized Bulk | Working | YYYY-MM-DD | HH-MM.xlsx

**Sheets:**
1. **Targeting:** Keywords + Product Targeting with all 48 columns + 7 helper columns
2. **Bidding Adjustment:** Bidding Adjustment rows with 48 columns only (no helper columns)

## Error Handling

### Validation Errors (Stop Processing)
- Missing required files
- Missing portfolios in Template (not in excluded list)
- No rows with Units = 0
- All portfolios marked as Ignore

### Calculation Warnings (Continue Processing)
- Bid below minimum (mark pink)
- Bid above maximum (mark pink)
- High clicks without sales (mark pink)
- Calculation errors (mark pink)

## Performance Targets
- Files up to 40MB
- Up to 500,000 rows
- Processing time < 60 seconds for maximum file size

## Key Business Rules
1. Always add 1 to Clicks to avoid division by zero
2. If portfolio not found in Template during processing: stop and request new Template
3. Bidding Adjustment rows are never filtered or modified (except Operation = "Update")
4. Helper columns only added to Targeting sheet
5. The text "up and" in campaign name triggers different bid reduction strategy