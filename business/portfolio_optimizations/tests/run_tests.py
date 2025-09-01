#!/usr/bin/env python3
"""Test runner for Portfolio Optimization tests."""

import sys
import os
from pathlib import Path

# Add the parent directory to Python path so imports work correctly
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

def run_output_validation_test():
    """Run the output validation test."""
    print("🚀 Running Output Validation Test...")
    try:
        from business.portfolio_optimizations.tests.validate_output import compare_excel_files
        result = compare_excel_files()
        print("✅ Output validation test completed")
        return result
    except Exception as e:
        print(f"❌ Output validation test failed: {str(e)}")
        return False

def run_integration_test():
    """Run the integration test."""
    print("🚀 Running Integration Test...")
    try:
        from business.portfolio_optimizations.tests.integration_test import test_full_integration
        result = test_full_integration()
        print("✅ Integration test completed")
        return result
    except Exception as e:
        print(f"❌ Integration test failed: {str(e)}")
        return False

def run_empty_portfolios_test():
    """Run the empty portfolios strategy test."""
    print("🚀 Running Empty Portfolios Strategy Test...")
    try:
        from business.portfolio_optimizations.tests.test_empty_portfolios_output import main
        result = main()
        print("✅ Empty portfolios test completed")
        return result
    except Exception as e:
        print(f"❌ Empty portfolios test failed: {str(e)}")
        return False

def run_prd_compliance_test():
    """Run the PRD compliance validation test."""
    print("🚀 Running PRD Compliance Validation...")
    try:
        from business.portfolio_optimizations.tests.verify_empty_portfolios_output import main
        result = main()
        print("✅ PRD compliance test completed")
        return result
    except Exception as e:
        print(f"❌ PRD compliance test failed: {str(e)}")
        return False

def run_inspect_utility():
    """Run the expected output inspection utility."""
    print("🔍 Running Expected Output Inspection Utility...")
    try:
        import subprocess
        import sys
        utility_path = Path(__file__).parent / "utilities" / "inspect_expected_output.py"
        result = subprocess.run([sys.executable, str(utility_path)], 
                              capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"Stderr: {result.stderr}")
        print("✅ Inspection utility completed")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Inspection utility failed: {str(e)}")
        return False

def run_all_tests():
    """Run all portfolio optimization tests."""
    print("🧪 Starting Portfolio Optimization Test Suite")
    print("=" * 60)
    
    results = {}
    
    # Run output validation test
    results['output_validation'] = run_output_validation_test()
    print()
    
    # Run integration test
    results['integration'] = run_integration_test()
    print()
    
    # Run empty portfolios strategy test
    results['empty_portfolios'] = run_empty_portfolios_test()
    print()
    
    # Run PRD compliance test
    results['prd_compliance'] = run_prd_compliance_test()
    print()
    
    # Summary
    print("=" * 60)
    print("📊 Test Summary:")
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {test_name}: {status}")
    
    return results

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "validation":
            run_output_validation_test()
        elif cmd == "integration":
            run_integration_test()
        elif cmd == "empty_portfolios":
            run_empty_portfolios_test()
        elif cmd == "prd_compliance":
            run_prd_compliance_test()
        elif cmd == "inspect":
            run_inspect_utility()
        else:
            print("Usage: python run_tests.py [validation|integration|empty_portfolios|prd_compliance|inspect]")
            print("  validation      - Run comprehensive output validation")
            print("  integration     - Run full integration test")
            print("  empty_portfolios - Run empty portfolios strategy test")
            print("  prd_compliance  - Run PRD compliance validation")
            print("  inspect         - Run expected output inspection utility")
            print("  Or run without arguments to run all tests")
    else:
        run_all_tests()