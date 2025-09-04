#!/usr/bin/env python3

import pandas as pd

def analyze_spec_vs_expected():
    """Analyze if expected file contradicts specifications"""
    
    expected_file = "PRD/Portfilio Optimizer/Excel Examples/Example - Output 3 checkboxes.xlsx"
    input_file = "PRD/Portfilio Optimizer/Excel Examples/Example - Bulk 60.xlsx"
    
    print("🔍 SPECIFICATION vs EXPECTED FILE ANALYSIS")
    print("="*80)
    
    try:
        # Load expected file
        expected_sheets = pd.read_excel(expected_file, sheet_name=None, dtype=str, na_filter=False)
        input_sheets = pd.read_excel(input_file, sheet_name=None, dtype=str, na_filter=False)
        
        print("\n1. CAMPAIGNS W/O PORTFOLIOS ANALYSIS:")
        print("-" * 50)
        
        # Check input campaigns data
        if "Sponsored Products Campaigns" in input_sheets:
            campaigns_df = input_sheets["Sponsored Products Campaigns"]
            print(f"Input campaigns total: {len(campaigns_df)}")
            
            # Apply EXACT spec criteria from PRD
            campaigns_without_portfolio = campaigns_df[
                (campaigns_df["Entity"] == "Campaign") &
                ((campaigns_df["Portfolio ID"] == '') | 
                 (campaigns_df["Portfolio ID"].isna()) |
                 (campaigns_df["Portfolio ID"] == 'nan'))
            ]
            
            print(f"Campaigns matching spec criteria (Entity='Campaign' AND Portfolio ID=Empty): {len(campaigns_without_portfolio)}")
            
            if len(campaigns_without_portfolio) > 0:
                print("Found campaign IDs that match spec:")
                for idx, row in campaigns_without_portfolio.iterrows():
                    print(f"  - {row['Campaign ID']} (Portfolio ID: '{row['Portfolio ID']}')")
        
        # Check if expected file has Terminal sheet
        has_terminal = "Terminal" in expected_sheets
        print(f"Expected file has Terminal sheet: {has_terminal}")
        
        if has_terminal:
            terminal_df = expected_sheets["Terminal"]
            print(f"Terminal sheet has {len(terminal_df)} rows")
            if len(terminal_df) > 0:
                print("Terminal sheet Campaign IDs:")
                if "Campaign ID" in terminal_df.columns:
                    campaign_entities = terminal_df[terminal_df["Entity"] == "Campaign"]
                    for idx, row in campaign_entities.iterrows():
                        print(f"  - {row['Campaign ID']}")
        
        print(f"\n📋 SPECIFICATION REQUIREMENT:")
        print(f"Per PRD/Portfilio Optimizer/Logic/Campaigns w:o Portfolios logic.md:")
        print(f"- Find campaigns where Entity='Campaign' AND Portfolio ID=Empty")
        print(f"- Move ONLY those campaigns to Terminal sheet")
        
        print(f"\n📊 EXPECTED FILE BEHAVIOR:")
        if has_terminal and len(expected_sheets["Terminal"]) > 0:
            print(f"- Expected file HAS Terminal sheet with campaigns")
            print(f"- This suggests expected file assumes some campaigns match spec criteria")
        else:
            print(f"- Expected file has no/empty Terminal sheet")  
            print(f"- This suggests no campaigns match spec criteria")
        
        print(f"\n🔍 CONTRADICTION CHECK:")
        input_matches_spec = len(campaigns_without_portfolio) if 'campaigns_without_portfolio' in locals() else 0
        expected_has_terminal_data = len(expected_sheets["Terminal"]) if has_terminal else 0
        
        if input_matches_spec == 0 and expected_has_terminal_data > 0:
            print("❌ CONTRADICTION FOUND:")
            print("   - Spec analysis: No campaigns match criteria in input")
            print("   - Expected file: Has campaigns in Terminal sheet")
            print("   - CONCLUSION: Expected file contradicts specification")
        elif input_matches_spec > 0 and expected_has_terminal_data == 0:
            print("❌ CONTRADICTION FOUND:")
            print("   - Spec analysis: Campaigns DO match criteria in input")
            print("   - Expected file: No campaigns in Terminal sheet")  
            print("   - CONCLUSION: My implementation is wrong")
        else:
            print("✅ NO CONTRADICTION:")
            print("   - Spec analysis and expected file are consistent")
        
        print(f"\n2. EMPTY PORTFOLIOS COLUMN ORDER ANALYSIS:")
        print("-" * 50)
        
        # Check Empty Portfolios spec for column order
        if "Portfolios" in expected_sheets:
            portfolios_df = expected_sheets["Portfolios"]
            print("Expected Portfolios columns:")
            for i, col in enumerate(portfolios_df.columns):
                print(f"  {i+1:2d}. {col}")
        
        print(f"\n3. TOP SHEET STRUCTURE ANALYSIS:")
        print("-" * 50)
        
        if "Top" in expected_sheets:
            top_df = expected_sheets["Top"]
            print(f"Expected Top sheet:")
            print(f"  Columns: {list(top_df.columns)}")
            print(f"  Shape: {top_df.shape}")
            
    except Exception as e:
        print(f"❌ Error during analysis: {e}")

if __name__ == "__main__":
    analyze_spec_vs_expected()