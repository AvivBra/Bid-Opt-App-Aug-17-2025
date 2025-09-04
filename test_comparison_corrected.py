#!/usr/bin/env python3

import pandas as pd
import sys
from pathlib import Path

def compare_files_detailed():
    """Compare the actual output with expected output file"""
    
    # File paths
    actual_file = ".playwright-mcp/portfolio-optimized-20250904-082448.xlsx"
    expected_file = "PRD/Portfilio Optimizer/Excel Examples/Example - Output 3 checkboxes.xlsx"
    
    print(f"🔍 Comparing files:")
    print(f"   Actual: {actual_file}")
    print(f"   Expected: {expected_file}")
    print("-" * 80)
    
    try:
        # Load both files with standardized settings per spec
        actual_sheets = pd.read_excel(actual_file, sheet_name=None, dtype=str, na_filter=False)
        expected_sheets = pd.read_excel(expected_file, sheet_name=None, dtype=str, na_filter=False)
        
        print(f"✅ Both files loaded successfully")
        
        # Compare sheet names
        actual_sheet_names = set(actual_sheets.keys())
        expected_sheet_names = set(expected_sheets.keys())
        
        print(f"\n📊 SHEET COMPARISON:")
        print(f"   Actual sheets: {sorted(actual_sheet_names)}")
        print(f"   Expected sheets: {sorted(expected_sheet_names)}")
        
        if actual_sheet_names == expected_sheet_names:
            print(f"   ✅ Sheet names match perfectly")
        else:
            print(f"   ❌ Sheet names differ:")
            if actual_sheet_names - expected_sheet_names:
                print(f"      Extra in actual: {actual_sheet_names - expected_sheet_names}")
            if expected_sheet_names - actual_sheet_names:
                print(f"      Missing in actual: {expected_sheet_names - actual_sheet_names}")
        
        # Compare each sheet
        all_identical = True
        total_differences = 0
        
        for sheet_name in sorted(expected_sheet_names):
            print(f"\n🔍 Comparing sheet: '{sheet_name}'")
            
            if sheet_name not in actual_sheets:
                print(f"   ❌ Sheet missing in actual file")
                all_identical = False
                continue
            
            actual_df = actual_sheets[sheet_name]
            expected_df = expected_sheets[sheet_name]
            
            # Compare dimensions
            print(f"   Dimensions: Actual {actual_df.shape}, Expected {expected_df.shape}")
            
            if actual_df.shape != expected_df.shape:
                print(f"   ❌ Dimensions differ")
                all_identical = False
                continue
            
            # Compare column names
            if list(actual_df.columns) != list(expected_df.columns):
                print(f"   ❌ Column names differ")
                print(f"      Actual: {list(actual_df.columns)}")
                print(f"      Expected: {list(expected_df.columns)}")
                all_identical = False
                continue
            
            # Cell-by-cell comparison
            differences = 0
            for row_idx in range(len(actual_df)):
                for col_name in actual_df.columns:
                    actual_val = str(actual_df.iloc[row_idx][col_name])
                    expected_val = str(expected_df.iloc[row_idx][col_name])
                    
                    if actual_val != expected_val:
                        differences += 1
                        total_differences += 1
                        if differences <= 10:  # Show first 10 differences per sheet
                            print(f"   ❌ Row {row_idx+1}, Col '{col_name}': '{actual_val}' ≠ '{expected_val}'")
            
            if differences == 0:
                print(f"   ✅ Sheet contents identical ({len(actual_df)} rows)")
            else:
                print(f"   ❌ Found {differences} cell differences")
                all_identical = False
        
        # Final result
        print(f"\n" + "="*80)
        if all_identical and actual_sheet_names == expected_sheet_names:
            print(f"🎉 SUCCESS: Files are 100% identical!")
            print(f"   ✅ Same sheet structure")
            print(f"   ✅ Same dimensions")
            print(f"   ✅ Same column headers")
            print(f"   ✅ Same cell content")
            return True
        else:
            print(f"❌ FAILURE: Files differ (Total differences: {total_differences})")
            return False
            
    except Exception as e:
        print(f"❌ Error during comparison: {e}")
        return False

if __name__ == "__main__":
    success = compare_files_detailed()
    sys.exit(0 if success else 1)