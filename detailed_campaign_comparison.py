#!/usr/bin/env python3

import pandas as pd

def detailed_campaign_analysis():
    """Find exactly which campaigns are missing between actual and expected files"""
    
    actual_file = "actual_output_all_3_opt.xlsx"
    expected_file = "PRD/Portfilio Optimizer/Excel Examples/Example - Output 3 checkboxes.xlsx"
    
    print("🔍 DETAILED CAMPAIGN COMPARISON")
    print("="*80)
    
    try:
        # Load files
        actual_sheets = pd.read_excel(actual_file, sheet_name=None, dtype=str, na_filter=False)
        expected_sheets = pd.read_excel(expected_file, sheet_name=None, dtype=str, na_filter=False)
        
        # Combine all campaigns from both sheets in each file
        actual_campaign = actual_sheets["Campaign"]
        actual_top = actual_sheets["Top Campaigns"] if "Top Campaigns" in actual_sheets else pd.DataFrame()
        actual_all_campaigns = pd.concat([actual_campaign, actual_top], ignore_index=True)
        
        expected_campaign = expected_sheets["Campaign"]  
        expected_top = expected_sheets["Top Campaigns"] if "Top Campaigns" in expected_sheets else pd.DataFrame()
        expected_all_campaigns = pd.concat([expected_campaign, expected_top], ignore_index=True)
        
        print(f"ACTUAL: {len(actual_campaign)} + {len(actual_top)} = {len(actual_all_campaigns)} total campaigns")
        print(f"EXPECTED: {len(expected_campaign)} + {len(expected_top)} = {len(expected_all_campaigns)} total campaigns")
        print(f"DIFFERENCE: {len(expected_all_campaigns) - len(actual_all_campaigns)} campaigns missing")
        
        # Get Campaign IDs
        if "Campaign ID" in actual_all_campaigns.columns and "Campaign ID" in expected_all_campaigns.columns:
            actual_campaign_ids = set(actual_all_campaigns["Campaign ID"].tolist())
            expected_campaign_ids = set(expected_all_campaigns["Campaign ID"].tolist())
            
            missing_campaigns = expected_campaign_ids - actual_campaign_ids
            extra_campaigns = actual_campaign_ids - expected_campaign_ids
            
            print(f"\n🔍 CAMPAIGN ID ANALYSIS:")
            print(f"Missing Campaign IDs: {len(missing_campaigns)}")
            for cid in sorted(missing_campaigns):
                # Find this campaign in expected file
                campaign_info = expected_all_campaigns[expected_all_campaigns["Campaign ID"] == cid]
                if len(campaign_info) > 0:
                    row = campaign_info.iloc[0]
                    portfolio = row.get("Portfolio Name (Informational only)", "N/A")
                    entity = row.get("Entity", "N/A") 
                    print(f"  {cid}: Entity={entity}, Portfolio={portfolio}")
            
            print(f"\nExtra Campaign IDs: {len(extra_campaigns)}")
            for cid in sorted(extra_campaigns):
                print(f"  {cid}")
                
            print(f"\nCommon Campaign IDs: {len(actual_campaign_ids & expected_campaign_ids)}")
            
            # If no missing Campaign IDs but different totals, check for duplicates or other issues
            if len(missing_campaigns) == 0 and len(expected_all_campaigns) != len(actual_all_campaigns):
                print(f"\n🚨 ANOMALY: Same Campaign IDs but different total counts!")
                print(f"Expected has {len(expected_all_campaigns)} rows vs Actual has {len(actual_all_campaigns)} rows")
                
                # Check for duplicates in expected
                expected_duplicates = expected_all_campaigns.duplicated(subset=['Campaign ID']).sum()
                actual_duplicates = actual_all_campaigns.duplicated(subset=['Campaign ID']).sum()
                
                print(f"Duplicates in expected: {expected_duplicates}")
                print(f"Duplicates in actual: {actual_duplicates}")
                
                if expected_duplicates > 0:
                    print("Duplicate Campaign IDs in expected file:")
                    expected_duplicate_ids = expected_all_campaigns[expected_all_campaigns.duplicated(subset=['Campaign ID'], keep=False)]['Campaign ID'].unique()
                    for dup_id in expected_duplicate_ids:
                        dup_rows = expected_all_campaigns[expected_all_campaigns['Campaign ID'] == dup_id]
                        print(f"  {dup_id} appears {len(dup_rows)} times")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    detailed_campaign_analysis()