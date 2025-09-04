#!/usr/bin/env python3

import pandas as pd

def find_missing_campaigns():
    """Identify specific campaigns that are missing and why they're filtered out"""
    
    print("🔍 MISSING CAMPAIGNS ANALYSIS")
    print("="*80)
    
    # Load files
    actual_file = "actual_output_all_3_opt.xlsx"
    expected_file = "PRD/Portfilio Optimizer/Excel Examples/Example - Output 3 checkboxes.xlsx"
    
    try:
        # Load campaign sheets
        actual_sheets = pd.read_excel(actual_file, sheet_name=None, dtype=str, na_filter=False)
        expected_sheets = pd.read_excel(expected_file, sheet_name=None, dtype=str, na_filter=False)
        
        # Get campaign data (combine Campaign and Top Campaigns sheets)
        actual_campaigns = actual_sheets["Campaign"].copy()
        actual_top = actual_sheets["Top Campaigns"].copy() if "Top Campaigns" in actual_sheets else pd.DataFrame()
        actual_all = pd.concat([actual_campaigns, actual_top], ignore_index=True)
        
        expected_campaigns = expected_sheets["Campaign"].copy()
        expected_top = expected_sheets["Top Campaigns"].copy() if "Top Campaigns" in expected_sheets else pd.DataFrame()
        expected_all = pd.concat([expected_campaigns, expected_top], ignore_index=True)
        
        print(f"📊 CAMPAIGN COUNTS:")
        print(f"Actual: {len(actual_campaigns)} (Campaign) + {len(actual_top)} (Top) = {len(actual_all)} total")
        print(f"Expected: {len(expected_campaigns)} (Campaign) + {len(expected_top)} (Top) = {len(expected_all)} total")
        
        # Find missing campaigns by Campaign ID
        if "Campaign ID" in actual_all.columns and "Campaign ID" in expected_all.columns:
            actual_ids = set(actual_all["Campaign ID"].tolist())
            expected_ids = set(expected_all["Campaign ID"].tolist())
            
            missing_ids = expected_ids - actual_ids
            extra_ids = actual_ids - expected_ids
            
            print(f"\n🔍 MISSING CAMPAIGNS: {len(missing_ids)}")
            for campaign_id in sorted(missing_ids):
                # Find this campaign in expected file
                campaign_row = expected_all[expected_all["Campaign ID"] == campaign_id].iloc[0]
                portfolio_name = campaign_row.get("Portfolio Name (Informational only)", "N/A")
                ads_count = "Unknown"
                
                print(f"  Campaign ID: {campaign_id}")
                print(f"    Portfolio Name: {portfolio_name}")
                print(f"    In which sheet: {'Campaign' if campaign_id in expected_campaigns['Campaign ID'].tolist() else 'Top Campaigns'}")
                print()
                
            if extra_ids:
                print(f"🔍 EXTRA CAMPAIGNS: {len(extra_ids)}")
                for campaign_id in sorted(extra_ids):
                    print(f"  Campaign ID: {campaign_id}")
            
            # Now let's analyze WHY these are filtered by checking original input
            print(f"\n🔍 FILTERING ANALYSIS:")
            input_file = "PRD/Portfilio Optimizer/Excel Examples/Example - Bulk 60.xlsx"
            input_sheets = pd.read_excel(input_file, sheet_name=None, dtype=str, na_filter=False)
            input_campaigns = input_sheets["Sponsored Products Campaigns"]
            
            # Get campaign entities only
            campaign_entities = input_campaigns[input_campaigns["Entity"] == "Campaign"]
            
            for campaign_id in sorted(missing_ids):
                if campaign_id in campaign_entities["Campaign ID"].tolist():
                    campaign_row = campaign_entities[campaign_entities["Campaign ID"] == campaign_id].iloc[0]
                    portfolio_name = campaign_row.get("Portfolio Name (Informational only)", "N/A")
                    
                    # Calculate ads count
                    product_ads_input = actual_sheets["Product Ad"]
                    ads_count = len(product_ads_input[product_ads_input["Campaign ID"].astype(str) == campaign_id])
                    
                    print(f"\nCampaign ID: {campaign_id}")
                    print(f"  Portfolio Name: {portfolio_name}")
                    print(f"  Ads Count: {ads_count}")
                    
                    # Check filtering rules
                    ignore_portfolios = ["Pause", "Terminal", "Top Terminal"]
                    filter_keywords = ["Flat", "Same", "Defense", "Offense"]
                    
                    is_ignored = portfolio_name in ignore_portfolios
                    has_filter_keyword = any(keyword in portfolio_name for keyword in filter_keywords)
                    
                    print(f"  Should be ignored (Pause/Terminal/Top Terminal): {is_ignored}")
                    print(f"  Contains filter keywords (Flat/Same/Defense/Offense): {has_filter_keyword}")
                    print(f"  Ads Count > 1 (should delete if not ignored): {ads_count > 1}")
                    
                    # Determine why it should be filtered
                    if not is_ignored and ads_count > 1:
                        print(f"  ❌ SHOULD BE FILTERED: Ads Count > 1 and not ignored")
                    elif not is_ignored and has_filter_keyword:
                        print(f"  ❌ SHOULD BE FILTERED: Contains filter keywords and not ignored")
                    else:
                        print(f"  ✅ SHOULD BE KEPT: Meets specification criteria")
                        print(f"  🚨 THIS IS THE ISSUE: Campaign should be kept but my implementation removes it")
            
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    find_missing_campaigns()