#!/usr/bin/env python3

import pandas as pd
import numpy as np

def comprehensive_file_comparison():
    """Perform detailed cell-by-cell comparison of actual vs expected files"""
    
    actual_file = "actual_output_all_3_opt.xlsx"
    expected_file = "PRD/Portfilio Optimizer/Excel Examples/Example - Output 3 checkboxes.xlsx"
    
    print("🔍 COMPREHENSIVE FILE COMPARISON")
    print("="*80)
    
    try:
        # Load files with standardized settings
        actual_sheets = pd.read_excel(actual_file, sheet_name=None, dtype=str, na_filter=False, engine='openpyxl')
        expected_sheets = pd.read_excel(expected_file, sheet_name=None, dtype=str, na_filter=False, engine='openpyxl')
        
        print("📊 SHEET STRUCTURE COMPARISON:")
        print(f"Actual sheets: {list(actual_sheets.keys())}")
        print(f"Expected sheets: {list(expected_sheets.keys())}")
        
        # Compare each sheet
        all_sheets_identical = True
        
        for sheet_name in expected_sheets.keys():
            if sheet_name not in actual_sheets:
                print(f"\n❌ MISSING SHEET: {sheet_name}")
                all_sheets_identical = False
                continue
                
            actual_df = actual_sheets[sheet_name]
            expected_df = expected_sheets[sheet_name]
            
            print(f"\n📋 SHEET: {sheet_name}")
            print(f"  Dimensions - Actual: {actual_df.shape}, Expected: {expected_df.shape}")
            
            # Check dimensions
            if actual_df.shape != expected_df.shape:
                print(f"  ❌ DIMENSION MISMATCH")
                all_sheets_identical = False
                
                # Show row/column differences
                if actual_df.shape[0] != expected_df.shape[0]:
                    print(f"    Row count difference: {actual_df.shape[0]} vs {expected_df.shape[0]}")
                if actual_df.shape[1] != expected_df.shape[1]:
                    print(f"    Column count difference: {actual_df.shape[1]} vs {expected_df.shape[1]}")
                    print(f"    Actual columns: {list(actual_df.columns)}")
                    print(f"    Expected columns: {list(expected_df.columns)}")
                continue
            
            # Check column names
            if list(actual_df.columns) != list(expected_df.columns):
                print(f"  ❌ COLUMN NAME MISMATCH")
                print(f"    Actual: {list(actual_df.columns)}")
                print(f"    Expected: {list(expected_df.columns)}")
                all_sheets_identical = False
                continue
            
            # Perform cell-by-cell comparison
            differences = []
            for i in range(len(actual_df)):
                for j, col in enumerate(actual_df.columns):
                    actual_val = str(actual_df.iloc[i, j])
                    expected_val = str(expected_df.iloc[i, j])
                    
                    if actual_val != expected_val:
                        differences.append({
                            'row': i,
                            'col': col,
                            'actual': actual_val,
                            'expected': expected_val
                        })
            
            if not differences:
                print(f"  ✅ IDENTICAL")
            else:
                print(f"  ❌ {len(differences)} CELL DIFFERENCES")
                all_sheets_identical = False
                
                # Show first 10 differences for analysis
                for diff in differences[:10]:
                    print(f"    Row {diff['row']}, Col '{diff['col']}': '{diff['actual']}' vs '{diff['expected']}'")
                
                if len(differences) > 10:
                    print(f"    ... and {len(differences) - 10} more differences")
                
                # Analyze pattern in differences
                if sheet_name in ["Campaign", "Top Campaigns"]:
                    analyze_campaign_differences(actual_df, expected_df, differences, sheet_name)
        
        print(f"\n🎯 OVERALL RESULT:")
        if all_sheets_identical:
            print("✅ FILES ARE IDENTICAL")
        else:
            print("❌ FILES HAVE DIFFERENCES")
            
        return all_sheets_identical
            
    except Exception as e:
        print(f"❌ Error during comparison: {e}")
        import traceback
        traceback.print_exc()
        return False

def analyze_campaign_differences(actual_df, expected_df, differences, sheet_name):
    """Analyze specific patterns in campaign sheet differences"""
    
    print(f"\n🔍 ANALYZING {sheet_name} DIFFERENCES:")
    
    # Check if differences are just row ordering
    if "Campaign ID" in actual_df.columns:
        actual_ids = set(actual_df["Campaign ID"].tolist())
        expected_ids = set(expected_df["Campaign ID"].tolist())
        
        missing_ids = expected_ids - actual_ids
        extra_ids = actual_ids - expected_ids
        
        if not missing_ids and not extra_ids:
            print("  📋 Same Campaign IDs - likely row ordering difference")
            
            # Sort both dataframes by Campaign ID and compare
            actual_sorted = actual_df.sort_values("Campaign ID").reset_index(drop=True)
            expected_sorted = expected_df.sort_values("Campaign ID").reset_index(drop=True)
            
            # Check if sorting resolves differences
            sorted_differences = []
            for i in range(len(actual_sorted)):
                for col in actual_sorted.columns:
                    actual_val = str(actual_sorted.iloc[i][col])
                    expected_val = str(expected_sorted.iloc[i][col])
                    
                    if actual_val != expected_val:
                        sorted_differences.append({
                            'row': i,
                            'col': col,
                            'actual': actual_val,
                            'expected': expected_val
                        })
            
            if not sorted_differences:
                print("  ✅ IDENTICAL AFTER SORTING BY CAMPAIGN ID")
            else:
                print(f"  ❌ {len(sorted_differences)} differences remain after sorting")
                # Show sample differences
                for diff in sorted_differences[:5]:
                    print(f"    Row {diff['row']}, Col '{diff['col']}': '{diff['actual']}' vs '{diff['expected']}'")
        else:
            if missing_ids:
                print(f"  ❌ Missing Campaign IDs: {missing_ids}")
            if extra_ids:
                print(f"  ❌ Extra Campaign IDs: {extra_ids}")

if __name__ == "__main__":
    result = comprehensive_file_comparison()
    print(f"\n🎯 FINAL RESULT: {'PASS' if result else 'FAIL'}")