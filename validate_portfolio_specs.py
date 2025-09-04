#!/usr/bin/env python3
"""
Validate Portfolio Optimizer output against specifications
Create comprehensive validation report for all 3 optimizations
"""

import pandas as pd
import sys
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def validate_empty_portfolios_strategy(data):
    """Validate Empty Portfolios optimization according to specs"""
    logger.info("🔍 VALIDATING EMPTY PORTFOLIOS STRATEGY")
    
    issues = []
    validations = []
    
    if 'Portfolios' not in data:
        issues.append("❌ Portfolios sheet missing")
        return issues, validations
    
    portfolios_df = data['Portfolios']
    
    # Check for Operation column
    if 'Operation' in portfolios_df.columns:
        updated_portfolios = portfolios_df[portfolios_df['Operation'] == 'update']
        validations.append(f"✅ Found {len(updated_portfolios)} portfolios marked for update")
        
        if len(updated_portfolios) > 0:
            # Check for renamed portfolios
            if 'Portfolio Name' in portfolios_df.columns:
                sample_names = updated_portfolios['Portfolio Name'].head(5).tolist()
                validations.append(f"✅ Sample updated portfolio names: {sample_names}")
            else:
                issues.append("❌ Portfolio Name column missing")
        else:
            issues.append("❌ No portfolios found for update (empty portfolios strategy may not have run)")
    else:
        issues.append("❌ Operation column missing from Portfolios sheet")
    
    return issues, validations

def validate_campaigns_without_portfolios_strategy(data):
    """Validate Campaigns Without Portfolios optimization according to specs"""
    logger.info("🔍 VALIDATING CAMPAIGNS WITHOUT PORTFOLIOS STRATEGY")
    
    issues = []
    validations = []
    
    if 'Campaign' not in data:
        issues.append("❌ Campaign sheet missing")
        return issues, validations
    
    campaigns_df = data['Campaign']
    
    # Check Portfolio ID assignments
    if 'Portfolio ID' in campaigns_df.columns:
        campaigns_with_portfolios = campaigns_df[campaigns_df['Portfolio ID'].notna() & (campaigns_df['Portfolio ID'] != '')]
        campaigns_without_portfolios = campaigns_df[campaigns_df['Portfolio ID'].isna() | (campaigns_df['Portfolio ID'] == '')]
        
        validations.append(f"✅ Total campaigns: {len(campaigns_df)}")
        validations.append(f"✅ Campaigns WITH portfolios: {len(campaigns_with_portfolios)}")
        validations.append(f"✅ Campaigns WITHOUT portfolios: {len(campaigns_without_portfolios)}")
        
        if len(campaigns_without_portfolios) == 0:
            validations.append("✅ SUCCESS: All campaigns have portfolio assignments")
        else:
            issues.append(f"❌ {len(campaigns_without_portfolios)} campaigns still without portfolio assignments")
    else:
        issues.append("❌ Portfolio ID column missing from Campaign sheet")
    
    return issues, validations

def validate_organize_top_campaigns_strategy(data):
    """Validate Organize Top Campaigns optimization according to detailed specs"""
    logger.info("🔍 VALIDATING ORGANIZE TOP CAMPAIGNS STRATEGY")
    
    issues = []
    validations = []
    
    # 1. Check for Top sheet (template data)
    if 'Top' in data:
        top_df = data['Top']
        validations.append(f"✅ Top sheet exists with {len(top_df)} rows")
        
        if 'Top ASINs' in top_df.columns:
            asins_count = len(top_df[top_df['Top ASINs'].notna() & (top_df['Top ASINs'] != '')])
            validations.append(f"✅ Found {asins_count} ASINs in Top sheet")
            
            # Sample ASINs
            sample_asins = top_df['Top ASINs'].head(3).tolist()
            validations.append(f"✅ Sample ASINs: {sample_asins}")
        else:
            issues.append("❌ Top ASINs column missing from Top sheet")
    else:
        issues.append("❌ Top sheet missing (should contain template ASINs)")
    
    # 2. Check for Top Camps sheet (organized campaigns)
    if 'Top Camps' in data:
        top_camps_df = data['Top Camps']
        validations.append(f"✅ Top Camps sheet exists with {len(top_camps_df)} rows")
        
        # Check for new columns according to spec
        required_new_columns = ['ASIN PA', 'Top', 'Ads Count']
        found_columns = []
        missing_columns = []
        
        for col in required_new_columns:
            if col in top_camps_df.columns:
                found_columns.append(col)
            else:
                missing_columns.append(col)
        
        if found_columns:
            validations.append(f"✅ New columns found in Top Camps: {found_columns}")
        if missing_columns:
            issues.append(f"❌ Missing required columns in Top Camps: {missing_columns}")
        
        # Check portfolio assignments to target portfolio (198280442127929)
        if 'Portfolio ID' in top_camps_df.columns:
            target_portfolio = '198280442127929'
            target_assigned = top_camps_df[top_camps_df['Portfolio ID'] == target_portfolio]
            validations.append(f"✅ Campaigns assigned to target portfolio {target_portfolio}: {len(target_assigned)}")
            
            if 'Operation' in top_camps_df.columns:
                operations = top_camps_df['Operation'].value_counts().to_dict()
                validations.append(f"✅ Operations in Top Camps: {operations}")
    else:
        issues.append("❌ Top Camps sheet missing (should contain organized campaigns)")
    
    # 3. Check main Campaign sheet for Top-related columns
    if 'Campaign' in data:
        campaigns_df = data['Campaign']
        
        # Check for Top column
        if 'Top' in campaigns_df.columns:
            top_marked = campaigns_df[campaigns_df['Top'] == 'v']
            empty_top = campaigns_df[campaigns_df['Top'].isna() | (campaigns_df['Top'] == '')]
            validations.append(f"✅ Campaigns marked as 'Top' (v): {len(top_marked)}")
            validations.append(f"✅ Campaigns with empty Top field: {len(empty_top)}")
        else:
            issues.append("❌ Top column missing from Campaign sheet")
        
        # Check for ASIN PA column
        if 'ASIN PA' in campaigns_df.columns:
            asin_populated = campaigns_df[campaigns_df['ASIN PA'].notna() & (campaigns_df['ASIN PA'] != '')]
            validations.append(f"✅ Campaigns with ASIN PA populated: {len(asin_populated)}")
            
            # Sample ASINs
            sample_asins = campaigns_df['ASIN PA'].dropna().head(3).tolist()
            validations.append(f"✅ Sample ASIN PA values: {sample_asins}")
        else:
            issues.append("❌ ASIN PA column missing from Campaign sheet")
        
        # Check for Ads Count column
        if 'Ads Count' in campaigns_df.columns:
            ads_count_populated = campaigns_df[campaigns_df['Ads Count'].notna() & (campaigns_df['Ads Count'] != '')]
            validations.append(f"✅ Campaigns with Ads Count populated: {len(ads_count_populated)}")
        else:
            issues.append("❌ Ads Count column missing from Campaign sheet")
    
    return issues, validations

def validate_sheet_structure(data):
    """Validate overall sheet structure"""
    logger.info("🔍 VALIDATING SHEET STRUCTURE")
    
    issues = []
    validations = []
    
    # Expected sheets based on spec
    expected_sheets = ['Portfolios', 'Campaign', 'Product Ad', 'Top', 'Top Camps']
    actual_sheets = list(data.keys())
    
    validations.append(f"✅ Total sheets found: {len(actual_sheets)}")
    validations.append(f"✅ Sheet names: {actual_sheets}")
    
    for sheet in expected_sheets:
        if sheet in actual_sheets:
            validations.append(f"✅ Required sheet present: {sheet}")
        else:
            issues.append(f"❌ Required sheet missing: {sheet}")
    
    # Additional sheets (allowed)
    extra_sheets = [s for s in actual_sheets if s not in expected_sheets]
    if extra_sheets:
        validations.append(f"✅ Additional sheets found: {extra_sheets}")
    
    return issues, validations

def main():
    # Load our actual output file
    actual_file = Path("/Applications/My Apps/Bid Opt App Aug 17, 2025/actual_output_all_3_opt.xlsx")
    
    logger.info("=== Portfolio Optimizer Specification Validation ===")
    logger.info(f"Validating file: {actual_file}")
    
    try:
        data = pd.read_excel(actual_file, sheet_name=None)
        logger.info(f"✅ Successfully loaded file")
    except Exception as e:
        logger.error(f"❌ Failed to load file: {e}")
        return False
    
    all_issues = []
    all_validations = []
    
    # Validate each component
    validators = [
        ("Sheet Structure", validate_sheet_structure),
        ("Empty Portfolios Strategy", validate_empty_portfolios_strategy),
        ("Campaigns Without Portfolios Strategy", validate_campaigns_without_portfolios_strategy),
        ("Organize Top Campaigns Strategy", validate_organize_top_campaigns_strategy)
    ]
    
    for validation_name, validator_func in validators:
        logger.info(f"\n{'='*60}")
        logger.info(f"VALIDATING: {validation_name}")
        logger.info(f"{'='*60}")
        
        issues, validations = validator_func(data)
        
        for validation in validations:
            logger.info(validation)
        
        for issue in issues:
            logger.error(issue)
        
        all_issues.extend(issues)
        all_validations.extend(validations)
    
    # Final summary
    logger.info(f"\n{'='*60}")
    logger.info("FINAL VALIDATION SUMMARY")
    logger.info(f"{'='*60}")
    
    logger.info(f"✅ Successful validations: {len(all_validations)}")
    logger.info(f"❌ Issues found: {len(all_issues)}")
    
    if len(all_issues) == 0:
        logger.info("🎉 ALL VALIDATIONS PASSED - Output meets Portfolio Optimizer specifications!")
        return True
    else:
        logger.error("❌ VALIDATION ISSUES FOUND - Output does not fully meet specifications")
        logger.error("Issues summary:")
        for i, issue in enumerate(all_issues, 1):
            logger.error(f"  {i}. {issue}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)