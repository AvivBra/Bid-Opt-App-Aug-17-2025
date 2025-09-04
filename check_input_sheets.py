#!/usr/bin/env python3

import pandas as pd

def check_input_sheets():
    """Check sheet names in input file"""
    
    input_file = "PRD/Portfilio Optimizer/Excel Examples/Example - Bulk 60.xlsx"
    
    try:
        sheets = pd.read_excel(input_file, sheet_name=None, dtype=str, na_filter=False)
        print(f"Input file sheet names: {list(sheets.keys())}")
        
        for sheet_name, df in sheets.items():
            print(f"\nSheet '{sheet_name}':")
            print(f"  Shape: {df.shape}")
            if len(df) > 0:
                print(f"  Columns: {list(df.columns)}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_input_sheets()