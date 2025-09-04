#!/usr/bin/env python3
"""
Compare Portfolio Optimizer output with expected file
Following the test specification for 100% identical verification
"""

import pandas as pd
import sys
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_files_with_standardized_format(actual_path, expected_path):
    """Load files with identical data type formatting as specified in test"""
    try:
        # Load actual file
        logger.info("Loading actual file...")
        actual_data_raw = pd.read_excel(actual_path, sheet_name=None, na_filter=False, engine='openpyxl')
        actual_data = {}
        for sheet_name, df in actual_data_raw.items():
            # Convert all columns to string, handling mixed types
            df_str = df.copy()
            for col in df_str.columns:
                df_str[col] = df_str[col].astype(str)
            actual_data[sheet_name] = df_str
        
        logger.info("Loading expected file...")
        expected_data_raw = pd.read_excel(expected_path, sheet_name=None, na_filter=False, engine='openpyxl')
        expected_data = {}
        for sheet_name, df in expected_data_raw.items():
            # Convert all columns to string, handling mixed types
            df_str = df.copy()
            for col in df_str.columns:
                df_str[col] = df_str[col].astype(str)
            expected_data[sheet_name] = df_str
            
        return actual_data, expected_data
    except Exception as e:
        logger.error(f"Error loading files: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return None, None

def compare_sheet_structure(actual_data, expected_data):
    """Compare sheet structure according to test specification"""
    issues = []
    
    # 1. Same sheet names and order
    actual_sheets = list(actual_data.keys())
    expected_sheets = list(expected_data.keys())
    
    if actual_sheets != expected_sheets:
        issues.append(f"Sheet names/order mismatch:\nActual: {actual_sheets}\nExpected: {expected_sheets}")
    
    # 2. Same dimensions per sheet
    for sheet_name in expected_sheets:
        if sheet_name not in actual_data:
            continue
            
        actual_shape = actual_data[sheet_name].shape
        expected_shape = expected_data[sheet_name].shape
        
        if actual_shape != expected_shape:
            issues.append(f"Sheet '{sheet_name}' dimension mismatch:\nActual: {actual_shape}\nExpected: {expected_shape}")
    
    # 3. Same column headers
    for sheet_name in expected_sheets:
        if sheet_name not in actual_data:
            continue
            
        actual_cols = list(actual_data[sheet_name].columns)
        expected_cols = list(expected_data[sheet_name].columns)
        
        if actual_cols != expected_cols:
            issues.append(f"Sheet '{sheet_name}' column headers mismatch:\nActual: {actual_cols}\nExpected: {expected_cols}")
    
    return issues

def is_dynamic_field(column_name):
    """Check if a column contains dynamic fields to exclude from comparison"""
    dynamic_patterns = [
        'timestamp', 'date', 'time', 'generated', 'filename', 
        'file_name', 'created', 'modified', 'version'
    ]
    column_lower = column_name.lower()
    return any(pattern in column_lower for pattern in dynamic_patterns)

def compare_cell_content(actual_data, expected_data):
    """Perform cell-by-cell string comparison as specified in test"""
    issues = []
    total_cells_compared = 0
    matching_cells = 0
    
    for sheet_name in expected_data.keys():
        if sheet_name not in actual_data:
            continue
            
        actual_sheet = actual_data[sheet_name]
        expected_sheet = expected_data[sheet_name]
        
        # Skip if dimensions don't match (already reported in structure check)
        if actual_sheet.shape != expected_sheet.shape:
            continue
        
        sheet_issues = []
        
        for col_idx, col_name in enumerate(expected_sheet.columns):
            if is_dynamic_field(col_name):
                logger.info(f"Skipping dynamic field: {sheet_name}.{col_name}")
                continue
                
            for row_idx in range(len(expected_sheet)):
                total_cells_compared += 1
                
                actual_cell = str(actual_sheet.iloc[row_idx, col_idx])
                expected_cell = str(expected_sheet.iloc[row_idx, col_idx])
                
                if actual_cell == expected_cell:
                    matching_cells += 1
                else:
                    sheet_issues.append({
                        'row': row_idx + 1,  # 1-based for user readability
                        'col': col_name,
                        'actual': actual_cell,
                        'expected': expected_cell
                    })
        
        if sheet_issues:
            issues.append({
                'sheet': sheet_name,
                'mismatches': sheet_issues[:10]  # Limit to first 10 issues per sheet
            })
    
    match_percentage = (matching_cells / total_cells_compared * 100) if total_cells_compared > 0 else 0
    
    return issues, total_cells_compared, matching_cells, match_percentage

def main():
    # File paths
    actual_file = Path("/Applications/My Apps/Bid Opt App Aug 17, 2025/.playwright-mcp/portfolio-optimized-20250904-065005.xlsx")
    expected_file = Path("/Applications/My Apps/Bid Opt App Aug 17, 2025/PRD/Portfilio Optimizer/Excel Examples/Output Bulk Example for all 3 opt.xlsx")
    
    logger.info("=== Portfolio Optimizer Integration Test - File Comparison ===")
    logger.info(f"Actual file: {actual_file}")
    logger.info(f"Expected file: {expected_file}")
    
    # Check if files exist
    if not actual_file.exists():
        logger.error(f"Actual file not found: {actual_file}")
        return False
        
    if not expected_file.exists():
        logger.error(f"Expected file not found: {expected_file}")
        return False
    
    # Load files with standardized formatting
    logger.info("Loading files with standardized formatting (dtype=str, na_filter=False)...")
    actual_data, expected_data = load_files_with_standardized_format(actual_file, expected_file)
    
    if actual_data is None or expected_data is None:
        return False
    
    logger.info(f"Actual file sheets: {list(actual_data.keys())}")
    logger.info(f"Expected file sheets: {list(expected_data.keys())}")
    
    # 1. Compare structure
    logger.info("Comparing sheet structure...")
    structure_issues = compare_sheet_structure(actual_data, expected_data)
    
    if structure_issues:
        logger.error("STRUCTURE MISMATCH FOUND:")
        for issue in structure_issues:
            logger.error(f"  - {issue}")
        return False
    else:
        logger.info("✅ Sheet structure matches perfectly")
    
    # 2. Compare cell content
    logger.info("Performing cell-by-cell comparison...")
    content_issues, total_cells, matching_cells, match_percentage = compare_cell_content(actual_data, expected_data)
    
    logger.info(f"Comparison results:")
    logger.info(f"  - Total cells compared: {total_cells}")
    logger.info(f"  - Matching cells: {matching_cells}")
    logger.info(f"  - Match percentage: {match_percentage:.2f}%")
    
    if content_issues:
        logger.error("CONTENT MISMATCHES FOUND:")
        for sheet_issue in content_issues:
            logger.error(f"\nSheet '{sheet_issue['sheet']}':")
            for mismatch in sheet_issue['mismatches']:
                logger.error(f"  Row {mismatch['row']}, Col '{mismatch['col']}': "
                           f"actual='{mismatch['actual'][:50]}...' vs expected='{mismatch['expected'][:50]}...'")
        return False
    
    if match_percentage == 100.0:
        logger.info("🎉 SUCCESS: Files are 100% identical!")
        logger.info("✅ All verification criteria met:")
        logger.info("  ✅ Same sheet structure")
        logger.info("  ✅ Same dimensions") 
        logger.info("  ✅ Same column headers")
        logger.info("  ✅ Same cell content (100% match)")
        return True
    else:
        logger.error(f"❌ PARTIAL MATCH: {match_percentage:.2f}% - Not meeting 100% success criteria")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)