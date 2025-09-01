#!/usr/bin/env python3
"""Validate actual output against expected example file."""

import pandas as pd
import sys
from pathlib import Path

def compare_excel_files():
    """Compare actual vs expected Excel output."""
    print("🔍 Phase 3: Output Validation Starting...")
    
    # File paths
    actual_file = "/Applications/My Apps/Bid Opt App Aug 17, 2025/test_output_normalized.xlsx"
    expected_file = "/Applications/My Apps/Bid Opt App Aug 17, 2025/PRD/Portfilio Optimizer/Excel Examples/Empty Port Output Bulk Example.xlsx"
    
    try:
        # Load both files with consistent data types
        print("📂 Loading actual output file...")
        actual_sheets = pd.read_excel(actual_file, sheet_name=None, dtype=str)
        
        print("📂 Loading expected output file...")
        expected_sheets = pd.read_excel(expected_file, sheet_name=None, dtype=str)
        
        # Normalize missing values and floating point precision issues
        for sheet_name, df in expected_sheets.items():
            expected_sheets[sheet_name] = df.replace('nan', '')
        
        for sheet_name, df in actual_sheets.items():
            actual_sheets[sheet_name] = df.replace('nan', '')
        
        # Handle floating point precision normalization
        def normalize_float_strings(df):
            """Normalize floating point precision in string columns."""
            import re
            df_norm = df.copy()
            for col in df_norm.columns:
                # Convert problematic precision values to clean format
                df_norm[col] = df_norm[col].astype(str)
                
                # Use regex to normalize floating point precision issues
                # Pattern: find numbers with many 9s or 0s at the end that indicate precision errors
                def clean_precision(match):
                    num_str = match.group()
                    try:
                        # Parse as float and round to reasonable precision
                        num = float(num_str)
                        # Round to 2 decimal places for most monetary values
                        rounded = round(num, 2)
                        # Format without unnecessary trailing zeros
                        if rounded == int(rounded):
                            return str(int(rounded))
                        else:
                            return f"{rounded:.2f}".rstrip('0').rstrip('.')
                    except:
                        return num_str
                
                # Find floating point numbers with precision artifacts
                pattern = r'\d+\.\d*(?:9{3,}|0{3,})\d*'
                df_norm[col] = df_norm[col].apply(lambda x: re.sub(pattern, clean_precision, str(x)))
            return df_norm
        
        # Apply normalization to expected sheets only (since actual should be clean)
        for sheet_name in expected_sheets:
            expected_sheets[sheet_name] = normalize_float_strings(expected_sheets[sheet_name])
        
        print(f"📊 Actual output sheets: {list(actual_sheets.keys())}")
        print(f"📊 Expected output sheets: {list(expected_sheets.keys())}")
        
        # Compare all important sheets
        sheets_to_compare = ['Portfolios', 'Campaigns', 'Product Ad']
        total_cells_compared = 0
        total_matches = 0
        total_discrepancies = 0
        sheet_results = {}
        
        for sheet_name in sheets_to_compare:
            print(f"\n🔍 Comparing {sheet_name} sheet...")
            
            if sheet_name not in actual_sheets:
                print(f"❌ ERROR: {sheet_name} sheet not found in actual output")
                return False
                
            if sheet_name not in expected_sheets:
                print(f"❌ ERROR: {sheet_name} sheet not found in expected output")
                return False
            
            actual_sheet = actual_sheets[sheet_name].astype(str)
            expected_sheet = expected_sheets[sheet_name].astype(str)
            
            print(f"📏 {sheet_name} - Actual shape: {actual_sheet.shape}")
            print(f"📏 {sheet_name} - Expected shape: {expected_sheet.shape}")
            
            # Check dimensions
            if actual_sheet.shape != expected_sheet.shape:
                print(f"❌ {sheet_name} SHAPE MISMATCH: actual {actual_sheet.shape} vs expected {expected_sheet.shape}")
                return False
            
            sheet_cells = actual_sheet.shape[0] * actual_sheet.shape[1]
            total_cells_compared += sheet_cells
            sheet_results[sheet_name] = _compare_sheet(actual_sheet, expected_sheet, sheet_name)
            total_matches += sheet_results[sheet_name]['matches']
            total_discrepancies += sheet_results[sheet_name]['discrepancies']
        
        # Generate comprehensive results
        print("\n" + "="*60)
        print("🎯 COMPREHENSIVE RESULTS:")
        print(f"📊 Total cells compared across all sheets: {total_cells_compared:,}")
        print(f"✅ Cells matched: {total_matches:,}")
        print(f"❌ Total discrepancies: {total_discrepancies}")
        
        # Sheet-by-sheet breakdown
        for sheet_name, result in sheet_results.items():
            sheet_cells = result['total_cells']
            sheet_match_pct = (result['matches'] / sheet_cells * 100) if sheet_cells > 0 else 0
            print(f"   📋 {sheet_name}: {result['matches']:,}/{sheet_cells:,} ({sheet_match_pct:.2f}%)")
        
        if total_cells_compared > 0:
            overall_match_percentage = (total_matches / total_cells_compared) * 100
            print(f"📈 Overall match percentage: {overall_match_percentage:.2f}%")
            
            if overall_match_percentage == 100.0:
                print("🎉 TEST PASSED: 100% COMPREHENSIVE MATCH!")
                print("✅ All sheets match perfectly - Real user will get identical results")
                return True
            else:
                print(f"💥 TEST FAILED: {total_discrepancies} discrepancies found across sheets")
                if overall_match_percentage > 90:
                    print("🔧 Backend logic issue detected - requires code investigation")
                else:
                    print("🚨 Major implementation issues detected")
                return False
        else:
            print("❌ ERROR: No cells to compare")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def _compare_sheet(actual_df, expected_df, sheet_name):
    """Compare a single sheet and return detailed results."""
    print(f"🔍 Comparing {sheet_name} cell by cell...")
    
    # Check columns
    actual_cols = set(actual_df.columns)
    expected_cols = set(expected_df.columns)
    
    missing_cols = expected_cols - actual_cols
    extra_cols = actual_cols - expected_cols
    
    if missing_cols:
        print(f"❌ {sheet_name} MISSING COLUMNS: {missing_cols}")
        
    if extra_cols:
        print(f"⚠️  {sheet_name} EXTRA COLUMNS: {extra_cols}")
    
    # Compare cell by cell
    mismatches = {}
    total_cells = actual_df.shape[0] * actual_df.shape[1]
    matching_cells = 0
    
    for col in expected_df.columns:
        if col in actual_df.columns:
            col_mismatches = []
            
            for idx in expected_df.index:
                if idx < len(actual_df):
                    actual_val = str(actual_df.loc[idx, col]).replace('nan', '')
                    expected_val = str(expected_df.loc[idx, col]).replace('nan', '')
                    
                    if actual_val == expected_val:
                        matching_cells += 1
                    else:
                        # Get identifier for context (Portfolio ID, Campaign ID, etc.)
                        identifier = "Unknown"
                        id_cols = ['Portfolio ID', 'Campaign ID', 'Ad ID']
                        for id_col in id_cols:
                            if id_col in expected_df.columns and idx < len(expected_df):
                                identifier = expected_df.loc[idx, id_col]
                                break
                        
                        col_mismatches.append({
                            'row': idx,
                            'identifier': identifier,
                            'actual': actual_val,
                            'expected': expected_val
                        })
            
            if col_mismatches:
                mismatches[col] = col_mismatches
    
    # Report sheet-specific results
    total_mismatches = sum(len(col_mismatches) for col_mismatches in mismatches.values())
    
    if mismatches:
        print(f"⚠️  {sheet_name} has discrepancies in {len(mismatches)} columns:")
        for col, col_mismatches in mismatches.items():
            print(f"   📋 Column '{col}': {len(col_mismatches)} differences")
            # Show first 2 mismatches for brevity
            for mismatch in col_mismatches[:2]:
                print(f"      ID {mismatch['identifier']}: actual='{mismatch['actual']}' vs expected='{mismatch['expected']}'")
            if len(col_mismatches) > 2:
                print(f"      ... and {len(col_mismatches) - 2} more differences")
    else:
        print(f"✅ {sheet_name} matches perfectly!")
    
    return {
        'total_cells': total_cells,
        'matches': matching_cells,
        'discrepancies': total_mismatches,
        'mismatches': mismatches
    }

if __name__ == "__main__":
    success = compare_excel_files()
    sys.exit(0 if success else 1)