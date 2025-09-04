#!/usr/bin/env python3

import pandas as pd

def analyze_top_campaigns_differences():
    """Analyze Top Campaigns selection and Campaign count differences"""
    
    actual_file = ".playwright-mcp/portfolio-optimized-20250904-082448.xlsx"
    expected_file = "PRD/Portfilio Optimizer/Excel Examples/Example - Output 3 checkboxes.xlsx"
    input_file = "PRD/Portfilio Optimizer/Excel Examples/Example - Bulk 60.xlsx"
    
    print("🔍 TOP CAMPAIGNS & CAMPAIGN COUNT ANALYSIS")
    print("="*80)
    
    try:
        # Load files
        actual_sheets = pd.read_excel(actual_file, sheet_name=None, dtype=str, na_filter=False)
        expected_sheets = pd.read_excel(expected_file, sheet_name=None, dtype=str, na_filter=False)
        input_sheets = pd.read_excel(input_file, sheet_name=None, dtype=str, na_filter=False)
        
        print("\n1. CAMPAIGN COUNT DIFFERENCE ANALYSIS:")
        print("-" * 50)
        
        # Campaign sheet analysis
        if "Campaign" in actual_sheets and "Campaign" in expected_sheets:
            actual_campaigns = actual_sheets["Campaign"]
            expected_campaigns = expected_sheets["Campaign"]
            input_campaigns = input_sheets["Sponsored Products Campaigns"] if "Sponsored Products Campaigns" in input_sheets else None
            
            print(f"Input file campaigns: {len(input_campaigns) if input_campaigns is not None else 'N/A'}")
            print(f"Actual output campaigns: {len(actual_campaigns)}")
            print(f"Expected output campaigns: {len(expected_campaigns)}")
            print(f"Difference: {len(actual_campaigns) - len(expected_campaigns)} rows")
            
            # Check if there are Terminal sheets affecting counts
            actual_has_terminal = "Terminal" in actual_sheets
            expected_has_terminal = "Terminal" in expected_sheets
            
            print(f"Actual has Terminal sheet: {actual_has_terminal}")
            print(f"Expected has Terminal sheet: {expected_has_terminal}")
            
            if actual_has_terminal and expected_has_terminal:
                actual_terminal = actual_sheets["Terminal"]
                expected_terminal = expected_sheets["Terminal"]
                print(f"Actual Terminal campaigns: {len(actual_terminal)}")
                print(f"Expected Terminal campaigns: {len(expected_terminal)}")
            
        print(f"\n2. TOP CAMPAIGNS SELECTION ANALYSIS:")
        print("-" * 50)
        
        if "Top Campaigns" in actual_sheets and "Top Campaigns" in expected_sheets:
            actual_top = actual_sheets["Top Campaigns"]
            expected_top = expected_sheets["Top Campaigns"]
            
            print(f"Actual Top Campaigns count: {len(actual_top)}")
            print(f"Expected Top Campaigns count: {len(expected_top)}")
            
            # Get campaign entities only
            actual_campaigns_only = actual_top[actual_top["Entity"] == "Campaign"] if "Entity" in actual_top.columns else actual_top
            expected_campaigns_only = expected_top[expected_top["Entity"] == "Campaign"] if "Entity" in expected_top.columns else expected_top
            
            print(f"\nActual Top Campaigns (Entity=Campaign only):")
            if len(actual_campaigns_only) > 0 and "Campaign ID" in actual_campaigns_only.columns:
                for idx, row in actual_campaigns_only.iterrows():
                    asin = row.get("ASIN PA", "N/A")
                    impressions = row.get("Impressions", "N/A")
                    spend = row.get("Spend", "N/A")
                    print(f"  - Campaign ID: {row['Campaign ID']}, ASIN: {asin}, Impressions: {impressions}, Spend: {spend}")
            
            print(f"\nExpected Top Campaigns (Entity=Campaign only):")
            if len(expected_campaigns_only) > 0 and "Campaign ID" in expected_campaigns_only.columns:
                for idx, row in expected_campaigns_only.iterrows():
                    asin = row.get("ASIN PA", "N/A")
                    impressions = row.get("Impressions", "N/A") 
                    spend = row.get("Spend", "N/A")
                    print(f"  - Campaign ID: {row['Campaign ID']}, ASIN: {asin}, Impressions: {impressions}, Spend: {spend}")
            
        # Check template ASINs for context
        template_file = "PRD/Portfilio Optimizer/Excel Examples/Filled Template Exampe.xlsx"
        try:
            template_sheets = pd.read_excel(template_file, sheet_name=None, dtype=str, na_filter=False)
            if "Sheet1" in template_sheets:
                template_df = template_sheets["Sheet1"]
                print(f"\nTemplate ASINs count: {len(template_df)}")
                if "Top ASINs" in template_df.columns or len(template_df.columns) > 0:
                    first_col = template_df.columns[0]
                    print(f"Template first few ASINs: {list(template_df[first_col].head(5))}")
                    
                    # Check if our Top Campaigns ASINs match template
                    if len(actual_campaigns_only) > 0 and "ASIN PA" in actual_campaigns_only.columns:
                        actual_asins = set(actual_campaigns_only["ASIN PA"].tolist())
                        expected_asins = set(expected_campaigns_only["ASIN PA"].tolist()) if len(expected_campaigns_only) > 0 and "ASIN PA" in expected_campaigns_only.columns else set()
                        template_asins = set(template_df[first_col].tolist())
                        
                        print(f"\nASIN Matching Analysis:")
                        print(f"Actual ASINs in template: {actual_asins.intersection(template_asins)}")
                        print(f"Expected ASINs in template: {expected_asins.intersection(template_asins)}")
                        
        except Exception as e:
            print(f"Could not analyze template: {e}")
            
    except Exception as e:
        print(f"❌ Error during analysis: {e}")

if __name__ == "__main__":
    analyze_top_campaigns_differences()