#!/usr/bin/env python3

import pandas as pd

def analyze_top_column_differences():
    """Analyze the specific Top column differences after sorting"""
    
    actual_file = "actual_output_all_3_opt.xlsx"
    expected_file = "PRD/Portfilio Optimizer/Excel Examples/Example - Output 3 checkboxes.xlsx"
    
    print("🔍 TOP COLUMN DIFFERENCE ANALYSIS")
    print("="*80)
    
    try:
        # Load campaign sheets
        actual_sheets = pd.read_excel(actual_file, sheet_name=None, dtype=str, na_filter=False, engine='openpyxl')
        expected_sheets = pd.read_excel(expected_file, sheet_name=None, dtype=str, na_filter=False, engine='openpyxl')
        
        actual_campaign = actual_sheets["Campaign"].copy()
        expected_campaign = expected_sheets["Campaign"].copy()
        
        # Sort both by Campaign ID for fair comparison
        actual_sorted = actual_campaign.sort_values("Campaign ID").reset_index(drop=True)
        expected_sorted = expected_campaign.sort_values("Campaign ID").reset_index(drop=True)
        
        print("📊 FINDING TOP COLUMN DIFFERENCES:")
        
        differences = []
        for i in range(len(actual_sorted)):
            if actual_sorted.iloc[i]["Top"] != expected_sorted.iloc[i]["Top"]:
                differences.append({
                    'index': i,
                    'campaign_id': actual_sorted.iloc[i]["Campaign ID"],
                    'asin_pa': actual_sorted.iloc[i]["ASIN PA"],
                    'portfolio_name': actual_sorted.iloc[i]["Portfolio Name (Informational only)"],
                    'actual_top': actual_sorted.iloc[i]["Top"],
                    'expected_top': expected_sorted.iloc[i]["Top"]
                })
        
        print(f"Found {len(differences)} Top column differences:")
        print()
        
        for diff in differences:
            print(f"Campaign ID: {diff['campaign_id']}")
            print(f"  ASIN PA: {diff['asin_pa']}")
            print(f"  Portfolio Name: {diff['portfolio_name']}")
            print(f"  Actual Top: '{diff['actual_top']}'")
            print(f"  Expected Top: '{diff['expected_top']}'")
            
            # Check if this ASIN should be in Top sheet template
            template_file = "PRD/Portfilio Optimizer/Excel Examples/Filled Template Exampe.xlsx"
            template_sheets = pd.read_excel(template_file, sheet_name=None, dtype=str, na_filter=False, engine='openpyxl')
            
            # Check all template sheets for this ASIN
            found_in_template = False
            for sheet_name, template_df in template_sheets.items():
                if "Top ASINs" in template_df.columns:
                    if diff['asin_pa'] in template_df["Top ASINs"].values:
                        found_in_template = True
                        print(f"  ✅ Found in template sheet: {sheet_name}")
                        break
            
            if not found_in_template:
                print(f"  ❌ NOT found in template")
            
            # Check ignore patterns from spec
            portfolio_name = diff['portfolio_name']
            ignore_patterns = ["Flat", "Same", "Defense", "Offense"]
            ignored_portfolio_names = ["Pause", "Terminal", "Top Terminal"]
            
            is_ignored_exact = portfolio_name in ignored_portfolio_names
            is_ignored_pattern = any(pattern in portfolio_name for pattern in ignore_patterns)
            
            if is_ignored_exact or is_ignored_pattern:
                print(f"  🚫 Should be IGNORED per spec (patterns: {ignore_patterns}, exact: {ignored_portfolio_names})")
            else:
                print(f"  ✅ NOT ignored per spec")
            
            print()
            
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    analyze_top_column_differences()