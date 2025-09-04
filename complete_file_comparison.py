#!/usr/bin/env python3
"""
Complete file comparison with the new expected output file
Following the exact test specification methodology
"""

import pandas as pd
import sys
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_files():
    """Load both files with standardized formatting"""
    actual_file = Path("/Applications/My Apps/Bid Opt App Aug 17, 2025/actual_output_all_3_opt_final.xlsx")
    expected_file = Path("/Applications/My Apps/Bid Opt App Aug 17, 2025/PRD/Portfilio Optimizer/Excel Examples/Example - Output 3 checkboxes.xlsx")
    
    try:
        # Load with standardized format as per test spec
        actual_data = pd.read_excel(actual_file, sheet_name=None, dtype=str, na_filter=False)
        expected_data = pd.read_excel(expected_file, sheet_name=None, dtype=str, na_filter=False)
        
        return actual_data, expected_data
    except Exception as e:
        logger.error(f"Error loading files: {e}")
        return None, None

def analyze_structural_differences(actual_data, expected_data):
    """Analyze structural differences between files"""
    logger.info("🔍 ANALYZING STRUCTURAL DIFFERENCES")
    
    differences = []
    
    # 1. Sheet names and order
    actual_sheets = list(actual_data.keys())
    expected_sheets = list(expected_data.keys())
    
    logger.info(f"Actual sheets: {actual_sheets}")
    logger.info(f"Expected sheets: {expected_sheets}")
    
    if actual_sheets != expected_sheets:
        differences.append("Sheet names/order mismatch")
        missing_in_actual = set(expected_sheets) - set(actual_sheets)
        extra_in_actual = set(actual_sheets) - set(expected_sheets)
        
        if missing_in_actual:
            differences.append(f"Missing sheets in actual: {missing_in_actual}")
        if extra_in_actual:
            differences.append(f"Extra sheets in actual: {extra_in_actual}")
    
    # 2. Sheet dimensions
    for sheet_name in expected_sheets:
        if sheet_name in actual_data:
            actual_shape = actual_data[sheet_name].shape
            expected_shape = expected_data[sheet_name].shape
            
            if actual_shape != expected_shape:
                differences.append(f"Sheet '{sheet_name}' dimension mismatch: actual {actual_shape} vs expected {expected_shape}")
        else:
            differences.append(f"Sheet '{sheet_name}' missing in actual")
    
    # 3. Column headers for matching sheets
    for sheet_name in expected_sheets:
        if sheet_name in actual_data:
            actual_cols = list(actual_data[sheet_name].columns)
            expected_cols = list(expected_data[sheet_name].columns)
            
            if actual_cols != expected_cols:
                differences.append(f"Sheet '{sheet_name}' column headers mismatch")
                logger.info(f"  Actual columns: {actual_cols[:5]}...")
                logger.info(f"  Expected columns: {expected_cols[:5]}...")
    
    return differences

def analyze_content_differences(actual_data, expected_data):
    """Analyze content differences in matching sheets"""
    logger.info("🔍 ANALYZING CONTENT DIFFERENCES")
    
    content_issues = []
    
    # Focus on sheets that exist in both files
    common_sheets = set(actual_data.keys()) & set(expected_data.keys())
    
    for sheet_name in common_sheets:
        actual_df = actual_data[sheet_name]
        expected_df = expected_data[sheet_name]
        
        # Skip if dimensions don't match (already reported)
        if actual_df.shape != expected_df.shape:
            continue
        
        logger.info(f"Comparing content in sheet: {sheet_name}")
        
        # Sample comparison for first few cells
        mismatches = 0
        total_cells = 0
        sample_issues = []
        
        min_rows = min(len(actual_df), len(expected_df))
        min_cols = min(len(actual_df.columns), len(expected_df.columns))
        
        for row_idx in range(min(min_rows, 10)):  # Check first 10 rows only for now
            for col_idx in range(min_cols):
                total_cells += 1
                actual_val = str(actual_df.iloc[row_idx, col_idx])
                expected_val = str(expected_df.iloc[row_idx, col_idx])
                
                if actual_val != expected_val:
                    mismatches += 1
                    if len(sample_issues) < 5:  # Collect first 5 mismatches
                        col_name = expected_df.columns[col_idx]
                        sample_issues.append({
                            'sheet': sheet_name,
                            'row': row_idx + 1,
                            'col': col_name,
                            'actual': actual_val[:50] + "..." if len(actual_val) > 50 else actual_val,
                            'expected': expected_val[:50] + "..." if len(expected_val) > 50 else expected_val
                        })
        
        if mismatches > 0:
            match_rate = ((total_cells - mismatches) / total_cells * 100) if total_cells > 0 else 0
            content_issues.append({
                'sheet': sheet_name,
                'mismatches': mismatches,
                'total_cells': total_cells,
                'match_rate': match_rate,
                'sample_issues': sample_issues
            })
    
    return content_issues

def main():
    logger.info("=== Portfolio Optimizer File Comparison (New Expected File) ===")
    
    # Load files
    actual_data, expected_data = load_files()
    if actual_data is None or expected_data is None:
        return False
    
    logger.info("✅ Both files loaded successfully")
    
    # Analyze structural differences
    logger.info("\n" + "="*60)
    structural_diffs = analyze_structural_differences(actual_data, expected_data)
    
    if structural_diffs:
        logger.error(f"❌ STRUCTURAL DIFFERENCES FOUND ({len(structural_diffs)} issues):")
        for i, diff in enumerate(structural_diffs, 1):
            logger.error(f"  {i}. {diff}")
    else:
        logger.info("✅ No structural differences found")
    
    # Analyze content differences  
    logger.info("\n" + "="*60)
    content_issues = analyze_content_differences(actual_data, expected_data)
    
    if content_issues:
        logger.error(f"❌ CONTENT DIFFERENCES FOUND:")
        for issue in content_issues:
            logger.error(f"\nSheet '{issue['sheet']}':")
            logger.error(f"  - Mismatches: {issue['mismatches']}/{issue['total_cells']} cells")
            logger.error(f"  - Match rate: {issue['match_rate']:.1f}%")
            
            for sample in issue['sample_issues']:
                logger.error(f"    Row {sample['row']}, Col '{sample['col']}':")
                logger.error(f"      Actual:   '{sample['actual']}'")
                logger.error(f"      Expected: '{sample['expected']}'")
    else:
        logger.info("✅ No content differences found")
    
    # Final summary
    logger.info("\n" + "="*60)
    logger.info("COMPARISON SUMMARY")
    logger.info("="*60)
    
    total_issues = len(structural_diffs) + len(content_issues)
    
    if total_issues == 0:
        logger.info("🎉 FILES ARE IDENTICAL!")
        return True
    else:
        logger.error(f"❌ {total_issues} categories of differences found")
        logger.info("Files are NOT identical - fixes needed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)