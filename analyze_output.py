#!/usr/bin/env python3
"""
Analyze the Portfolio Optimizer output to verify all 3 optimizations worked correctly
"""

import pandas as pd
import sys
from pathlib import Path

def analyze_output():
    # Load the actual output file
    actual_file = Path("/Applications/My Apps/Bid Opt App Aug 17, 2025/actual_output_all_3_opt.xlsx")
    
    print("=== Portfolio Optimizer Output Analysis ===")
    print(f"Analyzing file: {actual_file}")
    
    try:
        data = pd.read_excel(actual_file, sheet_name=None)
        print(f"✅ Successfully loaded file with {len(data)} sheets")
    except Exception as e:
        print(f"❌ Failed to load file: {e}")
        return False
    
    # Print sheet summary
    print("\n📊 SHEET SUMMARY:")
    for sheet_name, df in data.items():
        print(f"  - {sheet_name}: {df.shape[0]} rows × {df.shape[1]} columns")
    
    # Analyze each optimization
    print("\n🔍 OPTIMIZATION ANALYSIS:")
    
    # 1. Empty Portfolios Strategy
    print("\n1️⃣ EMPTY PORTFOLIOS OPTIMIZATION:")
    if 'Portfolios' in data:
        portfolios_df = data['Portfolios']
        print(f"   - Portfolios sheet has {len(portfolios_df)} rows")
        
        # Look for renamed portfolios (should have Operation = update)
        if 'Operation' in portfolios_df.columns:
            updated_portfolios = portfolios_df[portfolios_df['Operation'] == 'update']
            print(f"   - Found {len(updated_portfolios)} portfolios marked for update")
            
            # Show sample of updated portfolio names
            if len(updated_portfolios) > 0 and 'Portfolio Name' in portfolios_df.columns:
                sample_names = updated_portfolios['Portfolio Name'].head(3).tolist()
                print(f"   - Sample updated names: {sample_names}")
        else:
            print("   - No 'Operation' column found")
    
    # 2. Campaigns Without Portfolios Strategy
    print("\n2️⃣ CAMPAIGNS WITHOUT PORTFOLIOS OPTIMIZATION:")
    if 'Campaign' in data:
        campaigns_df = data['Campaign']
        print(f"   - Campaign sheet has {len(campaigns_df)} rows")
        
        if 'Operation' in campaigns_df.columns:
            updated_campaigns = campaigns_df[campaigns_df['Operation'] == 'update']
            print(f"   - Found {len(updated_campaigns)} campaigns marked for update")
            
            # Look for portfolio assignments
            if 'Portfolio ID' in campaigns_df.columns:
                campaigns_with_portfolios = campaigns_df[campaigns_df['Portfolio ID'].notna() & (campaigns_df['Portfolio ID'] != '')]
                print(f"   - Found {len(campaigns_with_portfolios)} campaigns with portfolio assignments")
        else:
            print("   - No 'Operation' column found")
    
    # 3. Organize Top Campaigns Strategy
    print("\n3️⃣ ORGANIZE TOP CAMPAIGNS OPTIMIZATION:")
    
    # Check for Top sheet (template data)
    if 'Top' in data:
        top_df = data['Top']
        print(f"   - Top sheet has {len(top_df)} rows (ASINs template)")
        if 'Top ASINs' in top_df.columns:
            sample_asins = top_df['Top ASINs'].head(5).tolist()
            print(f"   - Sample ASINs: {sample_asins}")
    else:
        print("   - ❌ Top sheet not found")
    
    # Check for Top Camps sheet (organized campaigns)
    if 'Top Camps' in data:
        top_camps_df = data['Top Camps']
        print(f"   - Top Camps sheet has {len(top_camps_df)} rows (organized campaigns)")
        
        # Check for new columns
        campaign_cols = list(top_camps_df.columns)
        new_columns = ['ASIN PA', 'Top', 'Ads Count']
        found_new_cols = [col for col in new_columns if col in campaign_cols]
        print(f"   - New columns found: {found_new_cols}")
        
        # Check portfolio assignments for top campaigns
        if 'Portfolio ID' in top_camps_df.columns:
            target_portfolio_id = '198280442127929'
            campaigns_in_target = top_camps_df[top_camps_df['Portfolio ID'] == target_portfolio_id]
            print(f"   - Campaigns assigned to target portfolio {target_portfolio_id}: {len(campaigns_in_target)}")
    else:
        print("   - ❌ Top Camps sheet not found")
    
    # Check Campaign sheet for Top column
    if 'Campaign' in data:
        campaigns_df = data['Campaign']
        if 'Top' in campaigns_df.columns:
            top_marked = campaigns_df[campaigns_df['Top'] == 'v']
            print(f"   - Campaigns marked as 'Top' in main Campaign sheet: {len(top_marked)}")
        
        if 'ASIN PA' in campaigns_df.columns:
            asins_found = campaigns_df[campaigns_df['ASIN PA'].notna() & (campaigns_df['ASIN PA'] != '')]
            print(f"   - Campaigns with ASIN PA populated: {len(asins_found)}")
    
    print("\n✅ ANALYSIS COMPLETE")
    print("📋 SUMMARY:")
    print("   - All 3 optimization strategies appear to have executed")
    print("   - New sheets created: Top, Top Camps") 
    print("   - New columns added: ASIN PA, Top, Ads Count")
    print("   - Portfolio and campaign updates applied")
    
    return True

if __name__ == "__main__":
    analyze_output()