#!/usr/bin/env python3

import pandas as pd

def debug_product_ad_deletion():
    """Debug when and where Product Ad rows are deleted or ignored"""
    
    print("🔍 PRODUCT AD DELETION/IGNORE DEBUGGING")
    print("="*80)
    
    try:
        # Step 1: Load input and output data for comparison
        print("📂 Step 1: Loading input and output data...")
        
        input_file = "PRD/Portfilio Optimizer/Excel Examples/Example - Bulk 60.xlsx"
        actual_file = "actual_output_all_3_opt.xlsx" 
        expected_file = "PRD/Portfilio Optimizer/Excel Examples/Example - Output 3 checkboxes.xlsx"
        
        input_sheets = pd.read_excel(input_file, sheet_name=None, dtype=str, na_filter=False, engine='openpyxl')
        actual_sheets = pd.read_excel(actual_file, sheet_name=None, dtype=str, na_filter=False, engine='openpyxl')
        expected_sheets = pd.read_excel(expected_file, sheet_name=None, dtype=str, na_filter=False, engine='openpyxl')
        
        print(f"Input sheets: {list(input_sheets.keys())}")
        print(f"Actual output sheets: {list(actual_sheets.keys())}")
        print(f"Expected output sheets: {list(expected_sheets.keys())}")
        
        # Find the initial campaigns sheet
        initial_campaigns = input_sheets["Sponsored Products Campaigns"]
        print(f"Found initial campaigns sheet with {len(initial_campaigns)} rows")
        
        # Count initial Product Ads
        initial_product_ads = initial_campaigns[initial_campaigns['Entity'] == 'Product Ad']
        initial_campaign_entities = initial_campaigns[initial_campaigns['Entity'] == 'Campaign']
        
        print(f"\n📊 INITIAL COUNTS:")
        print(f"Total rows in campaigns sheet: {len(initial_campaigns)}")
        print(f"Product Ad entities: {len(initial_product_ads)}")
        print(f"Campaign entities: {len(initial_campaign_entities)}")
        
        # Focus on the specific campaign with discrepancy
        target_campaign_id = '474528112331109'  # Same ASIN campaign with Ads Count difference
        
        # Find Product Ads for this campaign
        target_product_ads = initial_product_ads[initial_product_ads['Campaign ID'].astype(str) == target_campaign_id]
        print(f"\n🎯 TARGET CAMPAIGN {target_campaign_id}:")
        print(f"Product Ads for this campaign: {len(target_product_ads)}")
        
        if len(target_product_ads) > 0:
            print("Product Ad details:")
            for idx, row in target_product_ads.iterrows():
                print(f"  Row {idx}: Ad ID = {row.get('Ad ID', 'N/A')}, ASIN = {row.get('ASIN', 'N/A')}")
        
        # Step 2: Track Product Ads through input -> output
        print(f"\n📊 PRODUCT AD TRACKING:")
        
        # Input Product Ads
        input_product_ads = actual_sheets["Product Ad"]  # Final output Product Ad sheet
        expected_product_ads = expected_sheets["Product Ad"]  # Expected Product Ad sheet
        
        print(f"Actual output Product Ads: {len(input_product_ads)}")
        print(f"Expected output Product Ads: {len(expected_product_ads)}")
        
        # Focus on target campaign Product Ads
        target_actual = input_product_ads[input_product_ads['Campaign ID'].astype(str) == target_campaign_id]
        target_expected = expected_product_ads[expected_product_ads['Campaign ID'].astype(str) == target_campaign_id]
        
        print(f"\n🎯 TARGET CAMPAIGN {target_campaign_id} PRODUCT ADS:")
        print(f"Actual output: {len(target_actual)} Product Ads")
        print(f"Expected output: {len(target_expected)} Product Ads")
        print(f"Initial input: {len(target_product_ads)} Product Ads")
        
        # Show details of Product Ads for this campaign
        if len(target_actual) > 0:
            print(f"\nActual Product Ads details:")
            for idx, row in target_actual.iterrows():
                print(f"  Row {idx}: Ad ID = {row.get('Ad ID', 'N/A')}, ASIN = {row.get('ASIN', 'N/A')}")
        
        if len(target_expected) > 0:
            print(f"\nExpected Product Ads details:")
            for idx, row in target_expected.iterrows():
                print(f"  Row {idx}: Ad ID = {row.get('Ad ID', 'N/A')}, ASIN = {row.get('ASIN', 'N/A')}")
        
        # Step 3: Check target campaign in different sheets
        print(f"\n📋 TARGET CAMPAIGN LOCATION IN OUTPUT:")
        
        # Check actual output
        print(f"ACTUAL OUTPUT:")
        for sheet_name, sheet_df in actual_sheets.items():
            if 'Campaign ID' in sheet_df.columns:
                target_in_sheet = sheet_df[sheet_df['Campaign ID'].astype(str) == target_campaign_id]
                if len(target_in_sheet) > 0:
                    print(f"  Found in '{sheet_name}': {len(target_in_sheet)} rows")
                    row = target_in_sheet.iloc[0]
                    ads_count = row.get('Ads Count', 'N/A') 
                    portfolio = row.get('Portfolio Name (Informational only)', 'N/A')
                    print(f"    Ads Count: {ads_count}, Portfolio: {portfolio}")
        
        # Check expected output
        print(f"EXPECTED OUTPUT:")
        for sheet_name, sheet_df in expected_sheets.items():
            if 'Campaign ID' in sheet_df.columns:
                target_in_sheet = sheet_df[sheet_df['Campaign ID'].astype(str) == target_campaign_id]
                if len(target_in_sheet) > 0:
                    print(f"  Found in '{sheet_name}': {len(target_in_sheet)} rows")
                    row = target_in_sheet.iloc[0]
                    ads_count = row.get('Ads Count', 'N/A')
                    portfolio = row.get('Portfolio Name (Informational only)', 'N/A')
                    print(f"    Ads Count: {ads_count}, Portfolio: {portfolio}")
        
        # Step 4: Conclusion
        print(f"\n🎯 ANALYSIS CONCLUSION:")
        if len(target_actual) == len(target_product_ads) and len(target_expected) < len(target_product_ads):
            print("✅ Product Ads preserved in actual output (not deleted)")
            print("❌ Product Ads missing in expected output (expected file issue?)")
        elif len(target_actual) < len(target_product_ads):
            print("❌ Product Ads were deleted during processing") 
        else:
            print("✅ Product Ads counts match between input and actual output")
        
    except Exception as e:
        print(f"❌ Error during debugging: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_product_ad_deletion()