#!/usr/bin/env python3

import pandas as pd

def check_template():
    """Check template file structure"""
    
    template_file = "PRD/Portfilio Optimizer/Excel Examples/Filled Template Exampe.xlsx"
    expected_file = "PRD/Portfilio Optimizer/Excel Examples/Example - Output 3 checkboxes.xlsx"
    
    print("🔍 Checking Template file structure:")
    
    try:
        template_sheets = pd.read_excel(template_file, sheet_name=None, dtype=str, na_filter=False)
        print(f"Template sheets: {list(template_sheets.keys())}")
        
        for sheet_name, df in template_sheets.items():
            print(f"\nSheet '{sheet_name}':")
            print(f"  Columns: {list(df.columns)}")
            print(f"  Shape: {df.shape}")
            if len(df) > 0:
                print(f"  First few rows:")
                print(df.head(3))
    
    except Exception as e:
        print(f"Error reading template: {e}")
    
    print(f"\n" + "="*60)
    print("🔍 Checking Expected output Top sheet:")
    
    try:
        expected_sheets = pd.read_excel(expected_file, sheet_name=None, dtype=str, na_filter=False)
        
        if "Top" in expected_sheets:
            top_df = expected_sheets["Top"]
            print(f"Expected Top sheet:")
            print(f"  Columns: {list(top_df.columns)}")
            print(f"  Shape: {top_df.shape}")
            if len(top_df) > 0:
                print(f"  First few rows:")
                print(top_df.head(5))
        else:
            print("No Top sheet found in expected file")
    
    except Exception as e:
        print(f"Error reading expected file: {e}")

if __name__ == "__main__":
    check_template()