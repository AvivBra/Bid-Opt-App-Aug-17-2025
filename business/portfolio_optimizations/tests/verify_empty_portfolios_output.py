#!/usr/bin/env python3
"""
Script to verify Empty Portfolios optimization output against specification.
Compares input and output Excel files to validate 6-step logic implementation.
"""

import pandas as pd
import sys
from pathlib import Path

# Define file paths
INPUT_FILE = "PRD/Portfilio Optimizer/Excel Examples/Input Bulk Example.xlsx"
OUTPUT_FILE = "PRD/Portfilio Optimizer/Excel Examples/Empty Port Output Bulk Example.xlsx"

# Column names from specification
COL_ENTITY = "Entity"
COL_CAMPAIGN_ID = "Campaign ID"
COL_PORTFOLIO_ID = "Portfolio ID"
COL_PORTFOLIO_NAME = "Portfolio Name"
COL_OLD_PORTFOLIO_NAME = "Old Portfolio Name"
COL_CAMP_COUNT = "Camp Count"
COL_OPERATION = "Operation"
COL_BUDGET_AMOUNT = "Budget Amount"
COL_BUDGET_START_DATE = "Budget Start Date"
COL_BUDGET_POLICY = "Budget Policy"

# Constants from specification
EXCLUDED_PORTFOLIO_NAMES = ["Paused", "Terminal", "Top Terminal"]
ENTITY_CAMPAIGN = "Campaign"
ENTITY_PORTFOLIO = "Portfolio"
OPERATION_UPDATE = "update"
BUDGET_POLICY_NO_CAP = "No Cap"


def read_excel_files():
    """Read input and output Excel files."""
    print("📁 Reading Excel files...")
    
    try:
        input_sheets = pd.read_excel(INPUT_FILE, sheet_name=None)
        output_sheets = pd.read_excel(OUTPUT_FILE, sheet_name=None)
        
        print(f"✅ Input file: {len(input_sheets)} sheets")
        print(f"✅ Output file: {len(output_sheets)} sheets")
        
        return input_sheets, output_sheets
    
    except Exception as e:
        print(f"❌ Error reading Excel files: {e}")
        return None, None


def verify_step_1_camp_count_column(input_portfolios, output_portfolios):
    """Verify Step 1: Camp Count column added."""
    print("\n📋 STEP 1: Verifying Camp Count column")
    
    issues = []
    
    # Check if Camp Count column exists in output
    if COL_CAMP_COUNT not in output_portfolios.columns:
        issues.append("❌ Camp Count column missing from output")
    else:
        print("✅ Camp Count column exists in output")
    
    return issues


def verify_step_2_campaign_counting(input_campaigns, output_portfolios):
    """Verify Step 2: Campaign counting logic."""
    print("\n🔢 STEP 2: Verifying campaign counting logic")
    
    issues = []
    
    if COL_CAMP_COUNT not in output_portfolios.columns:
        issues.append("❌ Cannot verify counting - Camp Count column missing")
        return issues
    
    # Get campaign entities from input
    campaign_entities = input_campaigns[input_campaigns[COL_ENTITY] == ENTITY_CAMPAIGN]
    
    # Count campaigns per portfolio ID
    expected_counts = campaign_entities[COL_PORTFOLIO_ID].value_counts()
    
    # Check each portfolio's count
    portfolio_rows = output_portfolios[output_portfolios[COL_ENTITY] == ENTITY_PORTFOLIO]
    
    for idx, row in portfolio_rows.iterrows():
        portfolio_id = str(row[COL_PORTFOLIO_ID])
        expected_count = expected_counts.get(portfolio_id, 0)
        actual_count = row[COL_CAMP_COUNT]
        
        if actual_count != expected_count:
            issues.append(f"❌ Portfolio {portfolio_id}: expected {expected_count} campaigns, got {actual_count}")
    
    if not issues:
        print(f"✅ Campaign counting correct for {len(portfolio_rows)} portfolios")
    
    return issues


def verify_step_3_old_portfolio_name(input_portfolios, output_portfolios):
    """Verify Step 3: Old Portfolio Name backup."""
    print("\n💾 STEP 3: Verifying Old Portfolio Name backup")
    
    issues = []
    
    if COL_OLD_PORTFOLIO_NAME not in output_portfolios.columns:
        issues.append("❌ Old Portfolio Name column missing from output")
        return issues
    
    # Check that original names were backed up
    input_portfolio_rows = input_portfolios[input_portfolios[COL_ENTITY] == ENTITY_PORTFOLIO].copy()
    output_portfolio_rows = output_portfolios[output_portfolios[COL_ENTITY] == ENTITY_PORTFOLIO].copy()
    
    # Reset indices to align properly
    input_portfolio_rows = input_portfolio_rows.reset_index(drop=True)
    output_portfolio_rows = output_portfolio_rows.reset_index(drop=True)
    
    for i in range(min(len(input_portfolio_rows), len(output_portfolio_rows))):
        input_name = input_portfolio_rows.iloc[i][COL_PORTFOLIO_NAME]
        backup_name = output_portfolio_rows.iloc[i][COL_OLD_PORTFOLIO_NAME]
        
        if str(input_name) != str(backup_name):
            issues.append(f"❌ Row {i}: Original name '{input_name}' not backed up correctly (got '{backup_name}')")
    
    if not issues:
        print(f"✅ Original portfolio names backed up correctly for {len(input_portfolio_rows)} portfolios")
    
    return issues


def verify_step_4_empty_portfolio_renaming(input_portfolios, output_portfolios):
    """Verify Step 4: Empty portfolio identification and renaming."""
    print("\n🔍 STEP 4: Verifying empty portfolio renaming")
    
    issues = []
    
    if COL_CAMP_COUNT not in output_portfolios.columns:
        issues.append("❌ Cannot verify renaming - Camp Count column missing")
        return issues
    
    # Find portfolios that should be renamed (Camp Count = 0, not excluded names)
    portfolio_rows = output_portfolios[output_portfolios[COL_ENTITY] == ENTITY_PORTFOLIO].copy()
    
    empty_portfolios = portfolio_rows[
        (portfolio_rows[COL_CAMP_COUNT] == 0) &
        (~portfolio_rows[COL_OLD_PORTFOLIO_NAME].isin(EXCLUDED_PORTFOLIO_NAMES))
    ]
    
    print(f"📊 Found {len(empty_portfolios)} empty portfolios that should be renamed")
    
    # Check if they were renamed with numeric names
    renamed_count = 0
    for idx, row in empty_portfolios.iterrows():
        new_name = str(row[COL_PORTFOLIO_NAME])
        if new_name.isdigit():
            renamed_count += 1
            print(f"✅ Portfolio {row[COL_PORTFOLIO_ID]} renamed to '{new_name}'")
        else:
            issues.append(f"❌ Portfolio {row[COL_PORTFOLIO_ID]} should be renamed but has non-numeric name '{new_name}'")
    
    # Check for duplicate numeric names
    all_names = portfolio_rows[COL_PORTFOLIO_NAME].astype(str)
    numeric_names = [name for name in all_names if name.isdigit()]
    if len(numeric_names) != len(set(numeric_names)):
        issues.append("❌ Duplicate numeric portfolio names found")
    
    if renamed_count > 0 and not issues:
        print(f"✅ {renamed_count} empty portfolios renamed with unique numeric names")
    
    return issues


def verify_step_5_operation_field(output_portfolios):
    """Verify Step 5: Operation field set to 'update'."""
    print("\n⚙️  STEP 5: Verifying Operation field updates")
    
    issues = []
    
    # Find portfolios with numeric names (these should have been updated)
    portfolio_rows = output_portfolios[output_portfolios[COL_ENTITY] == ENTITY_PORTFOLIO]
    updated_portfolios = portfolio_rows[portfolio_rows[COL_PORTFOLIO_NAME].astype(str).str.isdigit()]
    
    for idx, row in updated_portfolios.iterrows():
        operation = row.get(COL_OPERATION, "")
        if operation != OPERATION_UPDATE:
            issues.append(f"❌ Portfolio {row[COL_PORTFOLIO_ID]} should have Operation='{OPERATION_UPDATE}', got '{operation}'")
    
    if not issues and len(updated_portfolios) > 0:
        print(f"✅ Operation field set to '{OPERATION_UPDATE}' for {len(updated_portfolios)} updated portfolios")
    elif len(updated_portfolios) == 0:
        print("ℹ️  No portfolios were renamed, so no Operation updates expected")
    
    return issues


def verify_step_6_budget_fields(input_portfolios, output_portfolios):
    """Verify Step 6: Budget field handling."""
    print("\n💰 STEP 6: Verifying budget field updates")
    
    issues = []
    
    # Find portfolios with numeric names (these should have been updated)
    portfolio_rows = output_portfolios[output_portfolios[COL_ENTITY] == ENTITY_PORTFOLIO]
    updated_portfolios = portfolio_rows[portfolio_rows[COL_PORTFOLIO_NAME].astype(str).str.isdigit()]
    
    budget_policy_issues = 0
    budget_cleared_issues = 0
    
    for idx, row in updated_portfolios.iterrows():
        portfolio_id = row[COL_PORTFOLIO_ID]
        
        # Check Budget Policy
        if COL_BUDGET_POLICY in row and row[COL_BUDGET_POLICY] != BUDGET_POLICY_NO_CAP:
            issues.append(f"❌ Portfolio {portfolio_id} should have Budget Policy='{BUDGET_POLICY_NO_CAP}', got '{row[COL_BUDGET_POLICY]}'")
            budget_policy_issues += 1
        
        # Check if budget fields were cleared (compare with input)
        input_row = input_portfolios[
            (input_portfolios[COL_ENTITY] == ENTITY_PORTFOLIO) &
            (input_portfolios[COL_PORTFOLIO_ID] == portfolio_id)
        ]
        
        if not input_row.empty:
            input_budget_amount = input_row.iloc[0].get(COL_BUDGET_AMOUNT, "")
            input_budget_start = input_row.iloc[0].get(COL_BUDGET_START_DATE, "")
            
            output_budget_amount = row.get(COL_BUDGET_AMOUNT, "")
            output_budget_start = row.get(COL_BUDGET_START_DATE, "")
            
            # If input had values, output should be empty
            if pd.notna(input_budget_amount) and str(input_budget_amount).strip():
                if pd.notna(output_budget_amount) and str(output_budget_amount).strip():
                    issues.append(f"❌ Portfolio {portfolio_id} Budget Amount should be cleared")
                    budget_cleared_issues += 1
            
            if pd.notna(input_budget_start) and str(input_budget_start).strip():
                if pd.notna(output_budget_start) and str(output_budget_start).strip():
                    issues.append(f"❌ Portfolio {portfolio_id} Budget Start Date should be cleared")
                    budget_cleared_issues += 1
    
    if not issues and len(updated_portfolios) > 0:
        print(f"✅ Budget Policy and field clearing correct for {len(updated_portfolios)} updated portfolios")
    elif len(updated_portfolios) == 0:
        print("ℹ️  No portfolios were renamed, so no budget updates expected")
    
    return issues


def generate_compliance_report(all_issues):
    """Generate final compliance report."""
    print("\n" + "="*60)
    print("📊 EMPTY PORTFOLIOS OPTIMIZATION COMPLIANCE REPORT")
    print("="*60)
    
    total_steps = 6
    failed_steps = len([step for step in all_issues if all_issues[step]])
    passed_steps = total_steps - failed_steps
    
    print(f"✅ Steps Passed: {passed_steps}/{total_steps}")
    print(f"❌ Steps Failed: {failed_steps}/{total_steps}")
    print(f"📈 Compliance Rate: {(passed_steps/total_steps)*100:.1f}%")
    
    if failed_steps == 0:
        print("\n🎉 PERFECT COMPLIANCE! All steps implemented correctly.")
    else:
        print(f"\n⚠️  COMPLIANCE ISSUES FOUND:")
        for step, issues in all_issues.items():
            if issues:
                print(f"\n{step}:")
                for issue in issues:
                    print(f"  {issue}")
    
    return failed_steps == 0


def main():
    """Main verification function."""
    print("🔍 Empty Portfolios Output Verification")
    print("="*50)
    
    # Read Excel files
    input_sheets, output_sheets = read_excel_files()
    if not input_sheets or not output_sheets:
        sys.exit(1)
    
    # Get relevant sheets
    input_campaigns = input_sheets.get("Sponsored Products Campaigns")
    input_portfolios = input_sheets.get("Portfolios")
    output_portfolios = output_sheets.get("Portfolios")
    
    if input_campaigns is None or input_portfolios is None or output_portfolios is None:
        print("❌ Required sheets not found in Excel files")
        sys.exit(1)
    
    print(f"\n📊 Data Overview:")
    print(f"  Input Campaigns: {len(input_campaigns)} rows")
    print(f"  Input Portfolios: {len(input_portfolios)} rows")
    print(f"  Output Portfolios: {len(output_portfolios)} rows")
    
    # Verify each step
    all_issues = {}
    
    all_issues["Step 1"] = verify_step_1_camp_count_column(input_portfolios, output_portfolios)
    all_issues["Step 2"] = verify_step_2_campaign_counting(input_campaigns, output_portfolios)
    all_issues["Step 3"] = verify_step_3_old_portfolio_name(input_portfolios, output_portfolios)
    all_issues["Step 4"] = verify_step_4_empty_portfolio_renaming(input_portfolios, output_portfolios)
    all_issues["Step 5"] = verify_step_5_operation_field(output_portfolios)
    all_issues["Step 6"] = verify_step_6_budget_fields(input_portfolios, output_portfolios)
    
    # Generate final report
    is_compliant = generate_compliance_report(all_issues)
    
    sys.exit(0 if is_compliant else 1)


if __name__ == "__main__":
    main()