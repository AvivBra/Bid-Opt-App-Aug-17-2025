#!/usr/bin/env python3

import pandas as pd

def analyze_ads_count_differences():
    """Analyze specific Ads Count differences between actual and expected files"""
    
    actual_file = "actual_output_all_3_opt.xlsx"
    expected_file = "PRD/Portfilio Optimizer/Excel Examples/Example - Output 3 checkboxes.xlsx"
    
    print("🔍 ADS COUNT DIFFERENCES ANALYSIS")
    print("="*80)
    
    try:
        # Load both files
        actual_sheets = pd.read_excel(actual_file, sheet_name=None, dtype=str, na_filter=False, engine='openpyxl')
        expected_sheets = pd.read_excel(expected_file, sheet_name=None, dtype=str, na_filter=False, engine='openpyxl')
        
        # Check Campaign sheet differences
        actual_campaign = actual_sheets["Campaign"].copy()
        expected_campaign = expected_sheets["Campaign"].copy()
        
        # Sort both by Campaign ID for fair comparison
        actual_sorted = actual_campaign.sort_values("Campaign ID").reset_index(drop=True)
        expected_sorted = expected_campaign.sort_values("Campaign ID").reset_index(drop=True)
        
        print("📊 CAMPAIGN SHEET ADS COUNT ANALYSIS:")
        print(f"Actual campaigns: {len(actual_sorted)}")
        print(f"Expected campaigns: {len(expected_sorted)}")
        
        # Find Ads Count differences
        ads_count_diffs = []
        for i in range(len(actual_sorted)):
            if actual_sorted.iloc[i]["Ads Count"] != expected_sorted.iloc[i]["Ads Count"]:
                ads_count_diffs.append({
                    'index': i,
                    'campaign_id': actual_sorted.iloc[i]["Campaign ID"],
                    'portfolio_name': actual_sorted.iloc[i]["Portfolio Name (Informational only)"],
                    'actual_ads_count': actual_sorted.iloc[i]["Ads Count"],
                    'expected_ads_count': expected_sorted.iloc[i]["Ads Count"]
                })
        
        print(f"\n🔍 FOUND {len(ads_count_diffs)} ADS COUNT DIFFERENCES:")
        for diff in ads_count_diffs:
            print(f"\nCampaign ID: {diff['campaign_id']}")
            print(f"  Portfolio Name: {diff['portfolio_name']}")
            print(f"  Actual Ads Count: {diff['actual_ads_count']}")
            print(f"  Expected Ads Count: {diff['expected_ads_count']}")
            print(f"  Difference: {int(diff['actual_ads_count']) - int(diff['expected_ads_count'])}")
        
        # Check Portfolios sheet differences  
        actual_portfolios = actual_sheets["Portfolios"].copy()
        expected_portfolios = expected_sheets["Portfolios"].copy()
        
        print(f"\n📊 PORTFOLIOS SHEET CAMP COUNT ANALYSIS:")
        print(f"Actual portfolios: {len(actual_portfolios)}")
        print(f"Expected portfolios: {len(expected_portfolios)}")
        
        # Find Camp Count differences
        camp_count_diffs = []
        for i in range(len(actual_portfolios)):
            if actual_portfolios.iloc[i]["Camp Count"] != expected_portfolios.iloc[i]["Camp Count"]:
                camp_count_diffs.append({
                    'index': i,
                    'portfolio_id': actual_portfolios.iloc[i]["Portfolio ID"],
                    'portfolio_name': actual_portfolios.iloc[i]["Portfolio Name"],
                    'actual_camp_count': actual_portfolios.iloc[i]["Camp Count"],
                    'expected_camp_count': expected_portfolios.iloc[i]["Camp Count"]
                })
        
        print(f"\n🔍 FOUND {len(camp_count_diffs)} CAMP COUNT DIFFERENCES:")
        for diff in camp_count_diffs:
            print(f"\nPortfolio ID: {diff['portfolio_id']}")
            print(f"  Portfolio Name: {diff['portfolio_name']}")
            print(f"  Actual Camp Count: {diff['actual_camp_count']}")
            print(f"  Expected Camp Count: {diff['expected_camp_count']}")
            print(f"  Difference: {int(diff['actual_camp_count']) - int(diff['expected_camp_count'])}")
            
        # Cross-reference: check if campaigns in differing portfolios are related to ads count issues
        print(f"\n🔗 CROSS-REFERENCE ANALYSIS:")
        print("Checking if campaigns with Ads Count differences belong to portfolios with Camp Count differences...")
        
        if ads_count_diffs and camp_count_diffs:
            for ads_diff in ads_count_diffs:
                campaign_portfolio = ads_diff['portfolio_name']
                print(f"\nCampaign {ads_diff['campaign_id']} belongs to portfolio '{campaign_portfolio}'")
                
                # Find matching portfolio in camp count differences
                for camp_diff in camp_count_diffs:
                    if camp_diff['portfolio_name'] == campaign_portfolio:
                        print(f"  ✅ Found matching portfolio with Camp Count difference:")
                        print(f"     Portfolio Camp Count: {camp_diff['actual_camp_count']} vs {camp_diff['expected_camp_count']}")
                        break
                else:
                    print(f"  ❌ No matching portfolio found in Camp Count differences")
        
        # Check for patterns
        print(f"\n📋 PATTERN ANALYSIS:")
        if ads_count_diffs:
            print("Ads Count difference patterns:")
            for diff in ads_count_diffs:
                portfolio_name = diff['portfolio_name']
                print(f"  - Portfolio '{portfolio_name}': {diff['actual_ads_count']} vs {diff['expected_ads_count']}")
                
                # Check if this portfolio has ignored patterns
                ignore_patterns = ["Flat", "Same", "Defense", "Offense"]
                ignored_portfolio_names = ["Pause", "Terminal", "Top Terminal"]
                
                is_ignored_exact = portfolio_name in ignored_portfolio_names
                is_ignored_pattern = any(pattern in portfolio_name for pattern in ignore_patterns)
                
                if is_ignored_exact or is_ignored_pattern:
                    print(f"    🚫 This portfolio is IGNORED per spec")
                else:
                    print(f"    ✅ This portfolio is NOT ignored")
            
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    analyze_ads_count_differences()