#!/usr/bin/env python3
"""
Test the new expected output file: Example - Output 3 checkboxes.xlsx
"""

import pandas as pd
import sys
from pathlib import Path

def test_new_expected_file():
    # File paths
    actual_file = Path("/Applications/My Apps/Bid Opt App Aug 17, 2025/actual_output_all_3_opt.xlsx")
    expected_file = Path("/Applications/My Apps/Bid Opt App Aug 17, 2025/PRD/Portfilio Optimizer/Excel Examples/Example - Output 3 checkboxes.xlsx")
    
    print("=== Testing New Expected File ===")
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
    
    # Try loading both files
    try:
        print("\n--- Loading Actual File ---")
        actual_data = pd.read_excel(actual_file, sheet_name=None)
        print(f"✅ Actual file loaded successfully")
        print(f"Actual sheets: {list(actual_data.keys())}")
        for sheet_name, df in actual_data.items():
            print(f"  - {sheet_name}: {df.shape[0]} rows × {df.shape[1]} columns")
    except Exception as e:
        print(f"❌ Failed to load actual file: {e}")
        return False
    
    try:
        print("\n--- Loading Expected File ---")
        expected_data = pd.read_excel(expected_file, sheet_name=None)
        print(f"✅ Expected file loaded successfully!")
        print(f"Expected sheets: {list(expected_data.keys())}")
        for sheet_name, df in expected_data.items():
            print(f"  - {sheet_name}: {df.shape[0]} rows × {df.shape[1]} columns")
    except Exception as e:
        print(f"❌ Failed to load expected file: {e}")
        return False
    
    # Basic comparison
    print("\n--- Basic Comparison ---")
    
    # Sheet names
    actual_sheets = set(actual_data.keys())
    expected_sheets = set(expected_data.keys())
    
    if actual_sheets == expected_sheets:
        print("✅ Sheet names match perfectly")
    else:
        print("❌ Sheet names differ")
        print(f"  Missing in actual: {expected_sheets - actual_sheets}")
        print(f"  Extra in actual: {actual_sheets - expected_sheets}")
    
    # Sheet dimensions
    print("\n--- Sheet Dimensions Comparison ---")
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
    
    print(f"\n🎉 SUCCESS: New expected file can be loaded and compared!")
    return True, actual_data, expected_data

if __name__ == "__main__":
    success = test_new_expected_file()
    if isinstance(success, tuple):
        sys.exit(0)
    else:
        sys.exit(0 if success else 1)