#!/usr/bin/env python3

import pandas as pd

def debug_top_sheet():
    """Debug the Top sheet issue"""
    
    actual_file = ".playwright-mcp/portfolio-optimized-20250904-082448.xlsx"
    
    print("🔍 Debugging Top sheet:")
    
    try:
        sheets = pd.read_excel(actual_file, sheet_name=None, dtype=str, na_filter=False)
        
        if "Top" in sheets:
            top_df = sheets["Top"]
            print(f"Actual Top sheet:")
            print(f"  Columns: {list(top_df.columns)}")
            print(f"  Shape: {top_df.shape}")
            if len(top_df) > 0:
                print(f"  First few rows:")
                print(top_df.head(3))
        else:
            print("No Top sheet found in actual file")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_top_sheet()