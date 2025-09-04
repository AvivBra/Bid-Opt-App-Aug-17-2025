#!/usr/bin/env python3

import pandas as pd

def check_output_sheets():
    """Check sheet names in output files to understand Product Ad structure"""
    
    actual_file = ".playwright-mcp/portfolio-optimized-20250904-082448.xlsx"
    expected_file = "PRD/Portfilio Optimizer/Excel Examples/Example - Output 3 checkboxes.xlsx"
    
    print("🔍 OUTPUT FILES SHEET ANALYSIS")
    print("="*60)
    
    try:
        print("\n📊 ACTUAL OUTPUT FILE:")
        actual_sheets = pd.read_excel(actual_file, sheet_name=None, dtype=str, na_filter=False)
        for sheet_name, df in actual_sheets.items():
            print(f"  {sheet_name}: {df.shape}")
            if sheet_name == "Product Ad" and len(df) > 0:
                print(f"    Columns: {list(df.columns)}")
                print(f"    Sample Campaign IDs: {list(df['Campaign ID'].head(5)) if 'Campaign ID' in df.columns else 'No Campaign ID col'}")
        
        print("\n📊 EXPECTED OUTPUT FILE:")
        expected_sheets = pd.read_excel(expected_file, sheet_name=None, dtype=str, na_filter=False)
        for sheet_name, df in expected_sheets.items():
            print(f"  {sheet_name}: {df.shape}")
            if sheet_name == "Product Ad" and len(df) > 0:
                print(f"    Columns: {list(df.columns)}")
                print(f"    Sample Campaign IDs: {list(df['Campaign ID'].head(5)) if 'Campaign ID' in df.columns else 'No Campaign ID col'}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_output_sheets()