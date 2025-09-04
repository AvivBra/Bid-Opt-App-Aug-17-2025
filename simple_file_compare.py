#!/usr/bin/env python3
"""
Simple Portfolio Optimizer file comparison
Try multiple methods to load and compare Excel files
"""

import pandas as pd
import sys
import traceback
from pathlib import Path

def try_load_excel(file_path, method_name):
    """Try different methods to load Excel file"""
    print(f"\nTrying to load {file_path} with {method_name}...")
    
    try:
        if method_name == "openpyxl_basic":
            data = pd.read_excel(file_path, sheet_name=None, engine='openpyxl')
        elif method_name == "openpyxl_no_filter":
            data = pd.read_excel(file_path, sheet_name=None, engine='openpyxl', na_filter=False)
        elif method_name == "xlrd":
            data = pd.read_excel(file_path, sheet_name=None, engine='xlrd')
        elif method_name == "calamine":
            data = pd.read_excel(file_path, sheet_name=None, engine='calamine')
        else:
            data = pd.read_excel(file_path, sheet_name=None)
        
        print(f"✅ SUCCESS with {method_name}")
        print(f"Sheets found: {list(data.keys())}")
        for sheet_name, df in data.items():
            print(f"  - {sheet_name}: {df.shape[0]} rows × {df.shape[1]} columns")
        return data
        
    except Exception as e:
        print(f"❌ FAILED with {method_name}: {e}")
        return None

def main():
    # File paths
    actual_file = Path("/Applications/My Apps/Bid Opt App Aug 17, 2025/actual_output_all_3_opt.xlsx")
    expected_file = Path("/Applications/My Apps/Bid Opt App Aug 17, 2025/PRD/Portfilio Optimizer/Excel Examples/Output Bulk Example for all 3 opt.xlsx")
    
    print("=== Simple File Comparison Test ===")
    print(f"Actual file: {actual_file}")
    print(f"Expected file: {expected_file}")
    
    # Check file existence
    if not actual_file.exists():
        print(f"❌ Actual file not found: {actual_file}")
        return False
        
    if not expected_file.exists():
        print(f"❌ Expected file not found: {expected_file}")
        return False
    
    print(f"✅ Both files exist")
    
    # Try different loading methods
    methods = ["default", "openpyxl_basic", "openpyxl_no_filter"]
    
    actual_data = None
    expected_data = None
    
    # Load actual file
    print("\n" + "="*50)
    print("LOADING ACTUAL FILE")
    print("="*50)
    for method in methods:
        actual_data = try_load_excel(actual_file, method)
        if actual_data is not None:
            break
    
    if actual_data is None:
        print("❌ Could not load actual file with any method")
        return False
    
    # Load expected file  
    print("\n" + "="*50)
    print("LOADING EXPECTED FILE")
    print("="*50)
    for method in methods:
        expected_data = try_load_excel(expected_file, method)
        if expected_data is not None:
            break
    
    if expected_data is None:
        print("❌ Could not load expected file with any method")
        return False
    
    # Basic comparison
    print("\n" + "="*50)
    print("BASIC COMPARISON")
    print("="*50)
    
    # Sheet names
    actual_sheets = set(actual_data.keys())
    expected_sheets = set(expected_data.keys())
    
    print(f"Actual sheets: {sorted(actual_sheets)}")
    print(f"Expected sheets: {sorted(expected_sheets)}")
    
    if actual_sheets == expected_sheets:
        print("✅ Sheet names match")
    else:
        print("❌ Sheet names differ")
        print(f"  Missing in actual: {expected_sheets - actual_sheets}")
        print(f"  Extra in actual: {actual_sheets - expected_sheets}")
    
    # Sheet dimensions
    for sheet in expected_sheets:
        if sheet in actual_data:
            actual_shape = actual_data[sheet].shape
            expected_shape = expected_data[sheet].shape
            if actual_shape == expected_shape:
                print(f"✅ Sheet '{sheet}': dimensions match {actual_shape}")
            else:
                print(f"❌ Sheet '{sheet}': dimension mismatch")
                print(f"    Actual: {actual_shape}, Expected: {expected_shape}")
        else:
            print(f"❌ Sheet '{sheet}': missing in actual file")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)