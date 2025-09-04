#!/usr/bin/env python3

import pandas as pd

def analyze_campaign_counts():
    """Systematically track campaign count through each filtering step"""
    
    print("🔍 CAMPAIGN COUNT ANALYSIS - STEP BY STEP")
    print("="*80)
    
    # File paths
    input_file = "PRD/Portfilio Optimizer/Excel Examples/Example - Bulk 60.xlsx"
    actual_file = ".playwright-mcp/portfolio-optimized-20250904-082448.xlsx"
    expected_file = "PRD/Portfilio Optimizer/Excel Examples/Example - Output 3 checkboxes.xlsx"
    
    try:
        # Load input file
        input_sheets = pd.read_excel(input_file, sheet_name=None, dtype=str, na_filter=False)
        campaigns_input = input_sheets["Sponsored Products Campaigns"]
        
        # Load actual output to get Product Ad data (since input processing creates this)
        actual_sheets = pd.read_excel(actual_file, sheet_name=None, dtype=str, na_filter=False)
        product_ads_input = actual_sheets["Product Ad"]
        
        print(f"📊 STARTING COUNTS:")
        print(f"Input campaigns total: {len(campaigns_input)}")
        print(f"Input product ads total: {len(product_ads_input)}")
        
        # Step 1: Filter to Campaign entities only
        campaign_entities = campaigns_input[campaigns_input["Entity"] == "Campaign"]
        print(f"\nStep 1 - Campaign entities only: {len(campaign_entities)}")
        
        # Step 2: Analyze Ads Count filtering (Spec Step 3)
        print(f"\n🔍 STEP 3 ANALYSIS - ADS COUNT FILTERING:")
        print("-" * 50)
        
        # Calculate Ads Count using COUNTIFS logic
        campaign_entities_copy = campaign_entities.copy()
        ads_counts = []
        
        for idx, campaign_row in campaign_entities_copy.iterrows():
            campaign_id = str(campaign_row["Campaign ID"])
            # Count occurrences in Product Ad sheet
            ads_count = len(product_ads_input[product_ads_input["Campaign ID"].astype(str) == campaign_id])
            ads_counts.append(ads_count)
        
        campaign_entities_copy["Ads Count"] = ads_counts
        
        # Identify ignore list (Portfolio Name = Pause, Terminal, Top Terminal)
        portfolio_col = "Portfolio Name (Informational only)"
        ignore_portfolios = ["Pause", "Terminal", "Top Terminal"]
        
        ignore_mask = campaign_entities_copy[portfolio_col].isin(ignore_portfolios)
        ignore_campaigns = campaign_entities_copy[ignore_mask]
        non_ignore_campaigns = campaign_entities_copy[~ignore_mask]
        
        print(f"Ignore list campaigns (kept): {len(ignore_campaigns)}")
        if len(ignore_campaigns) > 0:
            for portfolio in ignore_portfolios:
                count = len(ignore_campaigns[ignore_campaigns[portfolio_col] == portfolio])
                print(f"  - {portfolio}: {count} campaigns")
        
        print(f"Non-ignore campaigns: {len(non_ignore_campaigns)}")
        
        # Among non-ignore campaigns, check Ads Count > 1 (to be deleted)
        high_ads_count = non_ignore_campaigns[non_ignore_campaigns["Ads Count"] > 1]
        low_ads_count = non_ignore_campaigns[non_ignore_campaigns["Ads Count"] <= 1]
        
        print(f"Non-ignore with Ads Count > 1 (DELETE): {len(high_ads_count)}")
        print(f"Non-ignore with Ads Count <= 1 (KEEP): {len(low_ads_count)}")
        
        # Campaigns remaining after Step 3
        remaining_after_ads_filter = pd.concat([ignore_campaigns, low_ads_count], ignore_index=True)
        print(f"Remaining after Ads Count filter: {len(remaining_after_ads_filter)}")
        
        # Step 3: Analyze Portfolio Name filtering (Spec Step 4)
        print(f"\n🔍 STEP 4 ANALYSIS - PORTFOLIO NAME FILTERING:")
        print("-" * 50)
        
        # Keywords to filter out: Flat, Same, Defense, Offense
        filter_keywords = ["Flat", "Same", "Defense", "Offense"]
        
        # Apply to non-ignore campaigns only
        remaining_ignore = remaining_after_ads_filter[remaining_after_ads_filter[portfolio_col].isin(ignore_portfolios)]
        remaining_non_ignore = remaining_after_ads_filter[~remaining_after_ads_filter[portfolio_col].isin(ignore_portfolios)]
        
        keyword_filtered = pd.DataFrame()
        for keyword in filter_keywords:
            keyword_matches = remaining_non_ignore[remaining_non_ignore[portfolio_col].str.contains(keyword, case=False, na=False)]
            keyword_filtered = pd.concat([keyword_filtered, keyword_matches], ignore_index=True)
            print(f"Campaigns containing '{keyword}' (DELETE): {len(keyword_matches)}")
        
        # Remove duplicates from keyword filtering
        keyword_filtered = keyword_filtered.drop_duplicates()
        print(f"Total unique campaigns with keywords (DELETE): {len(keyword_filtered)}")
        
        # Campaigns that survive keyword filtering
        keyword_survivors = remaining_non_ignore[~remaining_non_ignore.index.isin(keyword_filtered.index)]
        
        # Final campaigns after all filtering
        final_campaigns = pd.concat([remaining_ignore, keyword_survivors], ignore_index=True)
        print(f"Remaining after Portfolio Name filter: {len(final_campaigns)}")
        
        # Step 4: Compare with actual output files
        print(f"\n📊 FINAL COMPARISON:")
        print("-" * 50)
        
        # Load expected file (actual_sheets already loaded above)
        expected_sheets = pd.read_excel(expected_file, sheet_name=None, dtype=str, na_filter=False)
        
        actual_campaign_count = len(actual_sheets["Campaign"])
        actual_top_campaigns_count = len(actual_sheets["Top Campaigns"]) if "Top Campaigns" in actual_sheets else 0
        
        expected_campaign_count = len(expected_sheets["Campaign"])
        expected_top_campaigns_count = len(expected_sheets["Top Campaigns"]) if "Top Campaigns" in expected_sheets else 0
        
        print(f"Manual calculation result: {len(final_campaigns)}")
        print(f"Actual implementation result: {actual_campaign_count} (Campaign) + {actual_top_campaigns_count} (Top Campaigns) = {actual_campaign_count + actual_top_campaigns_count}")
        print(f"Expected result: {expected_campaign_count} (Campaign) + {expected_top_campaigns_count} (Top Campaigns) = {expected_campaign_count + expected_top_campaigns_count}")
        
        print(f"\n🔍 DISCREPANCY ANALYSIS:")
        manual_total = len(final_campaigns)
        actual_total = actual_campaign_count + actual_top_campaigns_count  
        expected_total = expected_campaign_count + expected_top_campaigns_count
        
        print(f"Manual calculation vs Actual: {manual_total - actual_total} campaigns")
        print(f"Manual calculation vs Expected: {manual_total - expected_total} campaigns")
        print(f"Actual vs Expected: {actual_total - expected_total} campaigns")
        
        if manual_total == expected_total:
            print("✅ Expected file matches manual specification calculation")
        elif manual_total == actual_total:
            print("✅ Actual implementation matches manual specification calculation")
        else:
            print("❌ Neither implementation matches manual specification calculation")
            
    except Exception as e:
        print(f"❌ Error during analysis: {e}")

if __name__ == "__main__":
    analyze_campaign_counts()