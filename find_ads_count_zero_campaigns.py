#!/usr/bin/env python3

import pandas as pd

def find_ads_count_zero_campaigns():
    """Find campaigns where Product Ads exist but Ads Count is 0 in expected file"""
    
    expected_file = "PRD/Portfilio Optimizer/Excel Examples/Example - Output 3 checkboxes.xlsx"
    
    print("🔍 FINDING CAMPAIGNS WITH ADS COUNT=0 BUT PRODUCT ADS EXIST")
    print("="*80)
    
    try:
        # Load expected file
        expected_sheets = pd.read_excel(expected_file, sheet_name=None, dtype=str, na_filter=False, engine='openpyxl')
        
        # Get Campaign and Product Ad sheets
        expected_campaigns = expected_sheets["Campaign"]
        expected_product_ads = expected_sheets["Product Ad"]
        
        print(f"Expected campaigns: {len(expected_campaigns)}")
        print(f"Expected Product Ads: {len(expected_product_ads)}")
        
        # Find campaigns with Ads Count = 0
        zero_ads_count_campaigns = expected_campaigns[expected_campaigns["Ads Count"] == "0"]
        print(f"Campaigns with Ads Count = 0: {len(zero_ads_count_campaigns)}")
        
        # Check which of these have Product Ads
        inconsistent_campaigns = []
        
        for idx, campaign_row in zero_ads_count_campaigns.iterrows():
            campaign_id = str(campaign_row["Campaign ID"])
            portfolio_name = campaign_row.get("Portfolio Name (Informational only)", "N/A")
            
            # Look for Product Ads with this Campaign ID
            matching_product_ads = expected_product_ads[expected_product_ads["Campaign ID"].astype(str) == campaign_id]
            
            if len(matching_product_ads) > 0:
                inconsistent_campaigns.append({
                    'campaign_id': campaign_id,
                    'portfolio_name': portfolio_name,
                    'ads_count': campaign_row["Ads Count"],
                    'actual_product_ads': len(matching_product_ads),
                    'product_ad_asins': [row["ASIN"] for idx, row in matching_product_ads.iterrows()]
                })
        
        print(f"\n🚨 INCONSISTENT CAMPAIGNS (Ads Count=0 but Product Ads exist): {len(inconsistent_campaigns)}")
        
        # Show first 3 examples
        for i, campaign in enumerate(inconsistent_campaigns[:3]):
            print(f"\n{i+1}. Campaign ID: {campaign['campaign_id']}")
            print(f"   Portfolio Name: {campaign['portfolio_name']}")
            print(f"   Ads Count: {campaign['ads_count']}")
            print(f"   Actual Product Ads: {campaign['actual_product_ads']}")
            print(f"   Product Ad ASINs: {campaign['product_ad_asins']}")
            
            # Check for patterns
            portfolio_name = campaign['portfolio_name']
            ignore_patterns = ["Flat", "Same", "Defense", "Offense"]
            ignored_portfolio_names = ["Pause", "Terminal", "Top Terminal"]
            
            is_ignored_exact = portfolio_name in ignored_portfolio_names
            is_ignored_pattern = any(pattern in portfolio_name for pattern in ignore_patterns)
            
            if is_ignored_exact or is_ignored_pattern:
                print(f"   🚫 This portfolio matches IGNORE patterns")
            else:
                print(f"   ✅ This portfolio does NOT match ignore patterns")
        
        if len(inconsistent_campaigns) > 3:
            print(f"\n... and {len(inconsistent_campaigns) - 3} more inconsistent campaigns")
            
        # Summary of patterns
        print(f"\n📋 PATTERN ANALYSIS:")
        ignore_pattern_count = 0
        non_ignore_pattern_count = 0
        
        for campaign in inconsistent_campaigns:
            portfolio_name = campaign['portfolio_name']
            ignore_patterns = ["Flat", "Same", "Defense", "Offense"]
            ignored_portfolio_names = ["Pause", "Terminal", "Top Terminal"]
            
            is_ignored_exact = portfolio_name in ignored_portfolio_names
            is_ignored_pattern = any(pattern in portfolio_name for pattern in ignore_patterns)
            
            if is_ignored_exact or is_ignored_pattern:
                ignore_pattern_count += 1
            else:
                non_ignore_pattern_count += 1
        
        print(f"Campaigns with ignore patterns: {ignore_pattern_count}")
        print(f"Campaigns without ignore patterns: {non_ignore_pattern_count}")
        
        # Return first 3 campaign IDs
        campaign_ids = [campaign['campaign_id'] for campaign in inconsistent_campaigns[:3]]
        return campaign_ids
            
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    campaign_ids = find_ads_count_zero_campaigns()
    print(f"\n🎯 FIRST 3 CAMPAIGN IDS: {campaign_ids}")