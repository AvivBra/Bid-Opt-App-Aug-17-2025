#!/usr/bin/env python3
"""
Campaign Optimizer 1 Validation Test
Test the complete processing pipeline and validate against expected output.
"""

import sys
import os
import pandas as pd
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from data.readers.excel_reader import ExcelReader
from business.campaign_optimizer_1.orchestrator import CampaignOptimizer1Orchestrator


def main():
    """Run the validation test."""
    print("🧪 Campaign Optimizer 1 Validation Test")
    print("=" * 50)
    
    # File paths
    input_file = "/Applications/My Apps/Bid Opt App Aug 17, 2025/PRD/Campaign Optimizer 1/Input Excel Example - Bulk 7 Days.xlsx"
    expected_output_file = "/Applications/My Apps/Bid Opt App Aug 17, 2025/PRD/Campaign Optimizer 1/Output Excel Example - Bulk 7 Days (.17 ACOS).xlsx"
    
    try:
        # Step 1: Read input file
        print("\n📁 Step 1: Reading input file...")
        reader = ExcelReader()
        
        with open(input_file, 'rb') as f:
            input_bytes = f.read()
        
        success, message, input_df = reader.read_bulk_file(input_bytes, "input.xlsx")
        if not success:
            raise Exception(f"Failed to read input file: {message}")
        
        print(f"✅ Input file loaded: {len(input_df):,} rows")
        
        # Step 2: Process with orchestrator
        print("\n⚙️  Step 2: Processing with orchestrator...")
        input_data = {"Sponsored Products Campaigns": input_df}
        
        orchestrator = CampaignOptimizer1Orchestrator()
        output_bytes = orchestrator.process(input_data)
        
        print("✅ Processing completed")
        
        # Step 3: Read processed output
        print("\n📊 Step 3: Reading processed output...")
        processed_reader = ExcelReader()
        success, message, processed_df = processed_reader.read_bulk_file(output_bytes, "output.xlsx")
        if not success:
            raise Exception(f"Failed to read output file: {message}")
            
        print(f"✅ Output file processed: {len(processed_df):,} rows")
        
        # Step 4: Read expected output file
        print("\n🎯 Step 4: Reading expected output file...")
        with open(expected_output_file, 'rb') as f:
            expected_bytes = f.read()
        
        expected_reader = ExcelReader()
        success, message, expected_df = expected_reader.read_bulk_file(expected_bytes, "expected.xlsx")
        if not success:
            raise Exception(f"Failed to read expected file: {message}")
            
        print(f"✅ Expected file loaded: {len(expected_df):,} rows")
        
        # Step 5: Validate results
        print("\n🔍 Step 5: Validating results...")
        validation_passed = validate_outputs(processed_df, expected_df)
        
        if validation_passed:
            print("\n🎉 VALIDATION PASSED!")
            print("✅ All validation criteria met")
            return True
        else:
            print("\n❌ VALIDATION FAILED!")
            print("❌ One or more validation criteria not met")
            return False
            
    except Exception as e:
        print(f"\n💥 ERROR: {str(e)}")
        return False


def values_match(actual: str, expected: str, tolerance: float = 1e-10) -> bool:
    """
    Compare two values with tolerance for floating point numbers.
    """
    if actual == expected:
        return True
    
    # Try to convert to float for numeric comparison
    try:
        actual_float = float(actual)
        expected_float = float(expected)
        return abs(actual_float - expected_float) <= tolerance
    except (ValueError, TypeError):
        # Not numeric, do string comparison
        return actual == expected


def validate_outputs(actual_df: pd.DataFrame, expected_df: pd.DataFrame) -> bool:
    """
    Validate actual output against expected output according to Test.md criteria.
    
    Returns True if validation passes, False otherwise.
    """
    print("\n   Performing cell-by-cell validation...")
    
    # Convert both DataFrames to string format as specified in Test.md
    actual_str_df = actual_df.astype(str, errors='ignore')
    expected_str_df = expected_df.astype(str, errors='ignore')
    
    # Check dimensions
    print(f"   📏 Checking dimensions...")
    if actual_str_df.shape != expected_str_df.shape:
        print(f"   ❌ Shape mismatch: actual {actual_str_df.shape} vs expected {expected_str_df.shape}")
        return False
    print(f"   ✅ Dimensions match: {actual_str_df.shape}")
    
    # Check column names
    print(f"   📋 Checking column headers...")
    if list(actual_str_df.columns) != list(expected_str_df.columns):
        print(f"   ❌ Column headers mismatch")
        print(f"   Actual columns: {list(actual_str_df.columns)[:5]}...")
        print(f"   Expected columns: {list(expected_str_df.columns)[:5]}...")
        return False
    print(f"   ✅ Column headers match: {len(actual_str_df.columns)} columns")
    
    # Cell-by-cell comparison (excluding timestamp-based columns)
    print(f"   🔬 Performing cell-by-cell comparison...")
    
    # Get columns to compare (exclude timestamp-based ones)
    columns_to_compare = [col for col in actual_str_df.columns 
                         if 'filename' not in col.lower() and 'timestamp' not in col.lower() 
                         and 'date' not in col.lower()]
    
    mismatches = []
    total_cells = len(columns_to_compare) * len(actual_str_df)
    matching_cells = 0
    
    for col in columns_to_compare:
        for idx in actual_str_df.index:
            actual_val = str(actual_str_df.loc[idx, col])
            expected_val = str(expected_str_df.loc[idx, col])
            
            # Handle floating point comparison for numeric columns
            if values_match(actual_val, expected_val):
                matching_cells += 1
            else:
                mismatches.append({
                    'row': idx,
                    'column': col,
                    'actual': actual_val,
                    'expected': expected_val
                })
                
                # Only show first 10 mismatches
                if len(mismatches) <= 10:
                    print(f"   ⚠️  Mismatch at row {idx}, col '{col}': '{actual_val}' vs '{expected_val}'")
    
    match_percentage = (matching_cells / total_cells) * 100 if total_cells > 0 else 0
    print(f"   📊 Cell match rate: {matching_cells:,}/{total_cells:,} ({match_percentage:.2f}%)")
    
    if mismatches:
        print(f"   ❌ Found {len(mismatches):,} cell mismatches")
        if len(mismatches) > 10:
            print(f"   (showing first 10 mismatches only)")
        return False
    
    print(f"   ✅ All {total_cells:,} cells match perfectly!")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)