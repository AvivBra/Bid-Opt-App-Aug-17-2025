#!/usr/bin/env python3

import pandas as pd

def debug_column_processing():
    """Debug what happens during empty portfolios column processing"""
    
    # Load the actual input file to see initial state
    input_file = "PRD/Portfilio Optimizer/Excel Examples/Example - Bulk 60.xlsx"
    print("🔍 DEBUGGING EMPTY PORTFOLIOS COLUMN PROCESSING")
    print("="*80)
    
    try:
        # Load initial portfolios from input
        input_sheets = pd.read_excel(input_file, sheet_name=None, dtype=str, na_filter=False, engine='openpyxl')
        
        # Find portfolios sheet (might be named differently)
        portfolios_sheet_name = None
        for sheet_name in input_sheets.keys():
            if 'portfolio' in sheet_name.lower():
                portfolios_sheet_name = sheet_name
                break
        
        if portfolios_sheet_name:
            initial_portfolios = input_sheets[portfolios_sheet_name]
            print(f"📊 INITIAL PORTFOLIOS from {portfolios_sheet_name}:")
            print(f"  Shape: {initial_portfolios.shape}")
            print(f"  Columns: {list(initial_portfolios.columns)}")
            print()
        
        # Check what we have after all processing
        actual_file = "actual_output_all_3_opt.xlsx"
        if pd.io.common.file_exists(actual_file):
            actual_sheets = pd.read_excel(actual_file, sheet_name=None, dtype=str, na_filter=False, engine='openpyxl')
            final_portfolios = actual_sheets["Portfolios"]
            print(f"📊 FINAL PORTFOLIOS from output:")
            print(f"  Shape: {final_portfolios.shape}")
            print(f"  Columns: {list(final_portfolios.columns)}")
            print()
        
        # Check expected file
        expected_file = "PRD/Portfilio Optimizer/Excel Examples/Example - Output 3 checkboxes.xlsx"
        expected_sheets = pd.read_excel(expected_file, sheet_name=None, dtype=str, na_filter=False, engine='openpyxl')
        expected_portfolios = expected_sheets["Portfolios"]
        print(f"📊 EXPECTED PORTFOLIOS:")
        print(f"  Shape: {expected_portfolios.shape}")
        print(f"  Columns: {list(expected_portfolios.columns)}")
        print()
        
        # Find the difference
        actual_cols = list(final_portfolios.columns) if 'final_portfolios' in locals() else []
        expected_cols = list(expected_portfolios.columns)
        
        print(f"🔍 COLUMN COMPARISON:")
        print(f"  Expected: {expected_cols}")
        print(f"  Actual  : {actual_cols}")
        
        # Find specific differences
        if actual_cols:
            old_portfolio_actual_idx = actual_cols.index('Old Portfolio Name ') if 'Old Portfolio Name ' in actual_cols else -1
            old_portfolio_expected_idx = expected_cols.index('Old Portfolio Name ') if 'Old Portfolio Name ' in expected_cols else -1
            camp_count_actual_idx = actual_cols.index('Camp Count') if 'Camp Count' in actual_cols else -1
            camp_count_expected_idx = expected_cols.index('Camp Count') if 'Camp Count' in expected_cols else -1
            
            print(f"\n📍 KEY COLUMN POSITIONS:")
            print(f"  'Old Portfolio Name ' - Expected: {old_portfolio_expected_idx}, Actual: {old_portfolio_actual_idx}")
            print(f"  'Camp Count' - Expected: {camp_count_expected_idx}, Actual: {camp_count_actual_idx}")
            
            # Analyze the pattern
            portfolio_name_idx = expected_cols.index('Portfolio Name') if 'Portfolio Name' in expected_cols else -1
            print(f"  'Portfolio Name' - Expected: {portfolio_name_idx}")
            
            if portfolio_name_idx >= 0 and old_portfolio_expected_idx >= 0:
                print(f"  Expected 'Old Portfolio Name ' is {old_portfolio_expected_idx - portfolio_name_idx} positions after 'Portfolio Name'")
            
            if portfolio_name_idx >= 0 and old_portfolio_actual_idx >= 0:
                actual_portfolio_idx = actual_cols.index('Portfolio Name') if 'Portfolio Name' in actual_cols else -1
                if actual_portfolio_idx >= 0:
                    print(f"  Actual 'Old Portfolio Name ' is {old_portfolio_actual_idx - actual_portfolio_idx} positions after 'Portfolio Name'")
        
    except Exception as e:
        print(f"❌ Error during debugging: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_column_processing()