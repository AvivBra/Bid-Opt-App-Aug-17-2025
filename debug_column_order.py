#!/usr/bin/env python3

import pandas as pd

def debug_column_insertion():
    """Test column insertion logic"""
    
    # Create a test DataFrame with the same structure as Portfolios
    test_df = pd.DataFrame({
        'Product': ['test'],
        'Entity': ['test'],
        'Operation': ['test'],
        'Portfolio ID': ['test'],
        'Portfolio Name': ['test'],
        'Budget Amount': ['test'],
        'Budget Currency Code': ['test'],
        'Budget Policy': ['test'],
        'Budget Start Date': ['test'],
        'Budget End Date': ['test'],
        'State (Informational only)': ['test'],
        'In Budget (Informational only)': ['test']
    })
    
    print("Original columns:", list(test_df.columns))
    
    # Step 1: Insert Old Portfolio Name after Portfolio Name
    portfolio_name_col_idx = test_df.columns.get_loc('Portfolio Name')
    print(f"Portfolio Name at index: {portfolio_name_col_idx}")
    
    test_df.insert(portfolio_name_col_idx + 1, 'Old Portfolio Name ', test_df['Portfolio Name'])
    print("After inserting Old Portfolio Name:", list(test_df.columns))
    
    # Step 2: Add Camp Count at the end
    test_df['Camp Count'] = 0
    print("After adding Camp Count:", list(test_df.columns))
    
    expected_order = ['Product', 'Entity', 'Operation', 'Portfolio ID', 'Portfolio Name', 'Old Portfolio Name ', 'Budget Amount', 'Budget Currency Code', 'Budget Policy', 'Budget Start Date', 'Budget End Date', 'State (Informational only)', 'In Budget (Informational only)', 'Camp Count']
    
    print("\nExpected:", expected_order)
    print("Actual  :", list(test_df.columns))
    print("Match   :", list(test_df.columns) == expected_order)

if __name__ == "__main__":
    debug_column_insertion()