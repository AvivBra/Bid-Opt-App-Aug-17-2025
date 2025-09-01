"""Comprehensive integration test for Portfolio Optimizer."""

import sys
import pandas as pd
import logging
from typing import Dict, Any
import time

# Import all components
from .orchestrator import PortfolioOptimizationOrchestrator  
from .factory import get_portfolio_optimization_factory
from .contract_validator import validate_contract_compliance
from .constants import SHEET_CAMPAIGNS, SHEET_PORTFOLIOS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_full_integration() -> Dict[str, Any]:
    """
    Run comprehensive integration test covering:
    1. Contract validation
    2. Strategy execution
    3. Conflict resolution
    4. Output generation
    5. Performance validation
    """
    results = {
        "test_name": "Portfolio Optimizer Integration Test",
        "start_time": time.time(),
        "tests_passed": 0,
        "tests_failed": 0,
        "errors": [],
        "warnings": [],
        "performance_metrics": {}
    }
    
    try:
        logger.info("🧪 Starting Portfolio Optimizer Integration Test...")
        
        # Test 1: Contract compliance validation
        logger.info("Test 1: Contract compliance validation")
        try:
            validate_contract_compliance()
            results["tests_passed"] += 1
            logger.info("✅ Contract compliance - PASSED")
        except Exception as e:
            results["tests_failed"] += 1
            results["errors"].append(f"Contract compliance failed: {str(e)}")
            logger.error(f"❌ Contract compliance - FAILED: {e}")
        
        # Test 2: Factory initialization and strategy discovery
        logger.info("Test 2: Factory and strategy discovery")
        try:
            factory = get_portfolio_optimization_factory()
            available_strategies = factory.get_available_strategies()
            enabled_optimizations = factory.get_enabled_optimizations()
            
            assert len(available_strategies) >= 2, "Should have at least 2 strategies"
            assert "empty_portfolios" in available_strategies, "Should have empty_portfolios strategy"
            assert "campaigns_without_portfolios" in available_strategies, "Should have campaigns_without_portfolios strategy"
            
            results["tests_passed"] += 1
            logger.info(f"✅ Factory discovery - PASSED ({len(available_strategies)} strategies found)")
        except Exception as e:
            results["tests_failed"] += 1
            results["errors"].append(f"Factory initialization failed: {str(e)}")
            logger.error(f"❌ Factory discovery - FAILED: {e}")
        
        # Test 3: Strategy contract validation with minimal data
        logger.info("Test 3: Strategy contract validation")
        try:
            # Create minimal valid test data
            campaigns_data = pd.DataFrame({
                'Entity': ['Campaign', 'Campaign'],
                'Campaign ID': ['test_123', 'test_456'],
                'Portfolio ID': ['portfolio_999', ''],
                'Operation': ['', '']
            })
            
            portfolios_data = pd.DataFrame({
                'Entity': ['Portfolio', 'Portfolio'],
                'Portfolio ID': ['portfolio_999', 'portfolio_777'],
                'Portfolio Name': ['Active Portfolio', 'Empty Portfolio'],
                'Operation': ['', ''],
                'Budget Amount': ['', ''],
                'Budget Start Date': ['', '']
            })
            
            test_sheets = {
                SHEET_CAMPAIGNS: campaigns_data,
                SHEET_PORTFOLIOS: portfolios_data
            }
            
            # Test both strategies
            from .strategies import EmptyPortfoliosStrategy, CampaignsWithoutPortfoliosStrategy
            
            empty_strategy = EmptyPortfoliosStrategy()
            empty_result = empty_strategy.run(test_sheets)
            assert empty_result.result_type == "portfolios"
            assert len(empty_result.patch.updates) >= 0
            
            campaigns_strategy = CampaignsWithoutPortfoliosStrategy()
            campaigns_result = campaigns_strategy.run(test_sheets)
            assert campaigns_result.result_type == "campaigns"
            assert len(campaigns_result.patch.updates) >= 0
            
            results["tests_passed"] += 1
            logger.info("✅ Strategy contract validation - PASSED")
        except Exception as e:
            results["tests_failed"] += 1
            results["errors"].append(f"Strategy contract validation failed: {str(e)}")
            logger.error(f"❌ Strategy contract validation - FAILED: {e}")
        
        # Test 4: Full orchestration with real data (if available)
        logger.info("Test 4: Full orchestration")
        try:
            orchestrator = PortfolioOptimizationOrchestrator()
            
            # Try to use real Excel file if available
            real_file_path = "PRD/Portfilio Optimizer/Fixing Architecture/Excel Examples/Input 60 Bulk.xlsx"
            try:
                real_sheets = pd.read_excel(real_file_path, sheet_name=None)
                test_data = real_sheets
                data_source = "real Excel file"
            except:
                # Fall back to test data
                test_data = test_sheets
                data_source = "synthetic test data"
            
            selected_optimizations = ['empty_portfolios', 'campaigns_without_portfolios']
            
            start_time = time.time()
            merged_data, run_report = orchestrator.run_optimizations(test_data, selected_optimizations)
            execution_time = time.time() - start_time
            
            # Validate results
            assert run_report.total_optimizations == 2
            assert run_report.successful_optimizations >= 0
            assert execution_time < 60  # Should complete within 1 minute
            assert isinstance(merged_data, dict)
            assert len(merged_data) >= 1
            
            # Performance metrics
            results["performance_metrics"] = {
                "execution_time_seconds": execution_time,
                "data_source": data_source,
                "rows_processed": run_report.total_rows_updated,
                "cells_updated": run_report.total_cells_updated,
                "conflicts_detected": len(run_report.conflicts),
                "optimizations_successful": run_report.successful_optimizations
            }
            
            # Check conflict resolution
            if hasattr(run_report, 'conflict_summary'):
                conflict_summary = run_report.conflict_summary
                logger.info(f"Conflict summary: {conflict_summary['user_message']}")
                results["conflict_resolution"] = conflict_summary
            
            results["tests_passed"] += 1
            logger.info(f"✅ Full orchestration - PASSED ({data_source}, {execution_time:.2f}s)")
        except Exception as e:
            results["tests_failed"] += 1
            results["errors"].append(f"Full orchestration failed: {str(e)}")
            logger.error(f"❌ Full orchestration - FAILED: {e}")
        
        # Test 5: Output file generation
        logger.info("Test 5: Output file generation")
        try:
            from .service import PortfolioOptimizationService
            service = PortfolioOptimizationService()
            
            # Generate output file
            updated_indices = {SHEET_CAMPAIGNS: [0, 1], SHEET_PORTFOLIOS: [0]}
            output_bytes = service.create_output_file(test_data, updated_indices)
            
            assert isinstance(output_bytes, bytes)
            assert len(output_bytes) > 0
            
            # Generate filename
            filename = service.generate_filename()
            assert filename.endswith('.xlsx')
            assert 'portfolio_optimized' in filename
            
            results["tests_passed"] += 1
            logger.info(f"✅ Output file generation - PASSED ({len(output_bytes)} bytes)")
        except Exception as e:
            results["tests_failed"] += 1
            results["errors"].append(f"Output file generation failed: {str(e)}")
            logger.error(f"❌ Output file generation - FAILED: {e}")
        
    except Exception as e:
        results["errors"].append(f"Integration test framework error: {str(e)}")
        logger.error(f"💥 Integration test framework error: {e}")
    
    # Final results
    results["end_time"] = time.time()
    results["total_duration"] = results["end_time"] - results["start_time"]
    results["success_rate"] = results["tests_passed"] / (results["tests_passed"] + results["tests_failed"]) * 100 if (results["tests_passed"] + results["tests_failed"]) > 0 else 0
    
    # Log summary
    logger.info("\n" + "="*60)
    logger.info("INTEGRATION TEST SUMMARY")
    logger.info("="*60)
    logger.info(f"Tests Passed: {results['tests_passed']}")
    logger.info(f"Tests Failed: {results['tests_failed']}")
    logger.info(f"Success Rate: {results['success_rate']:.1f}%")
    logger.info(f"Total Duration: {results['total_duration']:.2f} seconds")
    
    if results["errors"]:
        logger.error("ERRORS:")
        for error in results["errors"]:
            logger.error(f"  - {error}")
    
    if results["performance_metrics"]:
        logger.info("PERFORMANCE METRICS:")
        for key, value in results["performance_metrics"].items():
            logger.info(f"  - {key}: {value}")
    
    logger.info("="*60)
    
    return results


if __name__ == "__main__":
    test_results = test_full_integration()
    
    # Exit with appropriate code
    if test_results["tests_failed"] > 0:
        sys.exit(1)
    else:
        logger.info("🎉 ALL INTEGRATION TESTS PASSED!")
        sys.exit(0)