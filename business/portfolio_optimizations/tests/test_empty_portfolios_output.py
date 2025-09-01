"""Test script to validate empty portfolios output matches example exactly."""

import pandas as pd
import logging
from pathlib import Path
import sys
import os

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from ..orchestrator import PortfolioOptimizationOrchestrator
from ..cleaning import clean_data_structure


def setup_logging():
    """Setup logging for the test."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)


def load_test_data(logger):
    """Load the input Excel file."""
    input_path = project_root / "PRD" / "Portfilio Optimizer" / "Excel Examples" / "Input Bulk Example.xlsx"
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    logger.info(f"Loading input file: {input_path}")
    
    # Load all sheets
    all_sheets = pd.read_excel(input_path, sheet_name=None, dtype=str)
    logger.info(f"Loaded sheets: {list(all_sheets.keys())}")
    
    return all_sheets


def load_expected_output(logger):
    """Load the expected output Excel file."""
    output_path = project_root / "PRD" / "Portfilio Optimizer" / "Excel Examples" / "Empty Port Output Bulk Example.xlsx"
    
    if not output_path.exists():
        raise FileNotFoundError(f"Expected output file not found: {output_path}")
    
    logger.info(f"Loading expected output file: {output_path}")
    
    # Load all sheets
    expected_sheets = pd.read_excel(output_path, sheet_name=None, dtype=str)
    logger.info(f"Expected output sheets: {list(expected_sheets.keys())}")
    
    return expected_sheets


def run_empty_portfolios_optimization(all_sheets, logger):
    """Run the empty portfolios optimization."""
    logger.info("Starting empty portfolios optimization")
    
    # Initialize orchestrator
    orchestrator = PortfolioOptimizationOrchestrator()
    
    # Run only empty_portfolios strategy
    optimizations = ["empty_portfolios"]
    
    logger.info("Running optimization")
    final_sheets, run_report = orchestrator.run_optimizations(all_sheets, optimizations)
    
    logger.info(f"Optimization complete. Run report: {run_report.successful_optimizations} successful, {len(run_report.failed_optimizations)} failed")
    
    return final_sheets


def compare_portfolios_sheet(actual_df, expected_df, logger):
    """Compare the Portfolios sheet in detail."""
    logger.info("Comparing Portfolios sheet...")
    
    # Convert both to string for comparison and normalize missing values
    actual_df = actual_df.astype(str)
    expected_df = expected_df.astype(str)
    
    # Normalize missing values - replace 'nan' with empty string
    expected_df = expected_df.replace('nan', '')
    
    # Check dimensions
    if actual_df.shape != expected_df.shape:
        logger.error(f"Shape mismatch: actual {actual_df.shape} vs expected {expected_df.shape}")
        return False
    
    # Check columns
    actual_cols = set(actual_df.columns)
    expected_cols = set(expected_df.columns)
    
    if actual_cols != expected_cols:
        logger.error(f"Column mismatch:")
        logger.error(f"  Missing: {expected_cols - actual_cols}")
        logger.error(f"  Extra: {actual_cols - expected_cols}")
        return False
    
    # Sort by Portfolio ID for consistent comparison
    actual_sorted = actual_df.sort_values('Portfolio ID').reset_index(drop=True)
    expected_sorted = expected_df.sort_values('Portfolio ID').reset_index(drop=True)
    
    # Compare each column
    discrepancies = 0
    for col in expected_df.columns:
        if col == 'Portfolio ID':
            continue  # Skip key column
            
        actual_col = actual_sorted[col]
        expected_col = expected_sorted[col]
        
        differences = actual_col != expected_col
        if differences.any():
            diff_count = differences.sum()
            logger.error(f"Column '{col}' has {diff_count} differences:")
            
            # Show first 5 differences
            diff_indices = actual_sorted[differences].index[:5]
            for idx in diff_indices:
                portfolio_id = actual_sorted.loc[idx, 'Portfolio ID']
                actual_val = actual_col.iloc[idx]
                expected_val = expected_col.iloc[idx]
                logger.error(f"  Portfolio ID {portfolio_id}: actual='{actual_val}' vs expected='{expected_val}'")
            
            discrepancies += diff_count
    
    if discrepancies == 0:
        logger.info("✅ Portfolios sheet matches expected output exactly!")
        return True
    else:
        logger.error(f"❌ Found {discrepancies} total discrepancies in Portfolios sheet")
        return False


def validate_empty_portfolios_logic(actual_df, logger):
    """Validate that the empty portfolios logic was applied correctly."""
    logger.info("Validating empty portfolios logic...")
    
    # Check that all rows with Camp Count = 0 and Portfolio Name not in excluded list
    # and not numeric have been renamed to numeric
    excluded_names = ["Paused", "Terminal", "Top Terminal"]
    
    portfolio_rows = actual_df[actual_df['Entity'] == 'Portfolio']
    empty_portfolios = portfolio_rows[portfolio_rows['Camp Count'].astype(int) == 0]
    
    issues = 0
    for idx, row in empty_portfolios.iterrows():
        name = str(row['Portfolio Name']).strip()
        old_name = str(row['Old Portfolio Name']).strip()
        
        # Skip if excluded name or already numeric
        if name in excluded_names or old_name.isdigit():
            continue
            
        # Should be renamed to numeric
        if not name.isdigit():
            logger.error(f"Portfolio ID {row['Portfolio ID']}: should be renamed but name is '{name}'")
            issues += 1
        
        # Should have Operation = update
        if row['Operation'] != 'update':
            logger.error(f"Portfolio ID {row['Portfolio ID']}: Operation should be 'update' but is '{row['Operation']}'")
            issues += 1
        
        # Should have Budget Policy = No Cap
        if row['Budget Policy'] != 'No Cap':
            logger.error(f"Portfolio ID {row['Portfolio ID']}: Budget Policy should be 'No Cap' but is '{row['Budget Policy']}'")
            issues += 1
    
    if issues == 0:
        logger.info("✅ Empty portfolios logic validation passed!")
        return True
    else:
        logger.error(f"❌ Found {issues} logic validation issues")
        return False


def main():
    """Main test function."""
    logger = setup_logging()
    logger.info("=== Starting Empty Portfolios Output Validation Test ===")
    
    try:
        # Load test data
        logger.info("Step 1: Loading input data")
        all_sheets = load_test_data(logger)
        
        # Load expected output
        logger.info("Step 2: Loading expected output")
        expected_sheets = load_expected_output(logger)
        
        # Run optimization
        logger.info("Step 3: Running empty portfolios optimization")
        actual_sheets = run_empty_portfolios_optimization(all_sheets, logger)
        
        # Compare results
        logger.info("Step 4: Comparing actual vs expected output")
        
        # Focus on Portfolios sheet
        if 'Portfolios' not in actual_sheets:
            logger.error("❌ Portfolios sheet not found in actual output")
            return False
        
        if 'Portfolios' not in expected_sheets:
            logger.error("❌ Portfolios sheet not found in expected output")
            return False
        
        # Compare Portfolios sheet
        portfolios_match = compare_portfolios_sheet(
            actual_sheets['Portfolios'], 
            expected_sheets['Portfolios'], 
            logger
        )
        
        # Validate logic
        logic_valid = validate_empty_portfolios_logic(actual_sheets['Portfolios'], logger)
        
        # Final result
        if portfolios_match and logic_valid:
            logger.info("🎉 TEST PASSED: Output matches expected result exactly!")
            return True
        else:
            logger.error("💥 TEST FAILED: Output does not match expected result")
            return False
            
    except Exception as e:
        logger.error(f"Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)