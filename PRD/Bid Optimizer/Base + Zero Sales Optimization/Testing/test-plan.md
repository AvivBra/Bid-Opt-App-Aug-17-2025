# איפיון תוכנית בדיקות - Bid Optimizer

## 1. סקירה כללית

### מטרות הבדיקות
- וידוא נכונות החישובים
- בדיקת יציבות המערכת
- אימות ביצועים
- בדיקת חוויית משתמש

### סוגי בדיקות
- Unit Tests
- Integration Tests
- Performance Tests
- UI/UX Tests
- End-to-End Tests

## 2. Unit Tests

### Zero Sales Calculations
```python
def test_zero_sales_bid_calculation_case_a():
    """Test: No Target CPA + 'up and' in name"""
    
    # Setup
    row = {
        'Base Bid': 1.0,
        'Target CPA': None,
        'Campaign Name (Informational only)': 'Campaign up and running',
        'Clicks': 10
    }
    
    # Execute
    result = calculate_bid(row)
    
    # Assert
    assert result == 0.5  # Base Bid * 0.5
```

### Validation Tests
```python
def test_template_validation_missing_columns():
    """Test template validation with missing columns"""
    
    # Setup
    df = pd.DataFrame({
        'Portfolio Name': ['Test'],
        'Base Bid': [1.0]
        # Missing Target CPA
    })
    
    # Execute
    result = validate_template_structure(df)
    
    # Assert
    assert not result['is_valid']
    assert 'Missing column: Target CPA' in result['errors']
```

### File Reading Tests
```python
def test_read_bulk_file_excel():
    """Test reading Excel bulk file"""
    
    # Setup
    file_path = 'tests/fixtures/sample_bulk.xlsx'
    
    # Execute
    df = read_bulk_file(file_path)
    
    # Assert
    assert len(df.columns) == 48
    assert 'Sponsored Products Campaigns' in df.attrs.get('sheet_name', '')
```

## 3. Integration Tests

### Upload Flow
```python
def test_complete_upload_flow():
    """Test complete file upload flow"""
    
    # Setup
    template_file = create_test_template()
    bulk_file = create_test_bulk()
    
    # Execute
    upload_template(template_file)
    upload_bulk('30', bulk_file)
    
    # Assert
    assert st.session_state.template_file is not None
    assert st.session_state.bulk_30_file is not None
    assert st.session_state.get('validation_state') == 'ready'
```

### Processing Flow
```python
def test_zero_sales_processing_flow():
    """Test Zero Sales optimization flow"""
    
    # Setup
    setup_test_files()
    st.session_state.selected_optimizations = ['zero_sales']
    
    # Execute
    results = process_optimizations()
    
    # Assert
    assert 'zero_sales' in results
    assert 'Clean Zero Sales' in results['zero_sales']
    assert len(results['zero_sales']['Clean Zero Sales']) > 0
```

## 4. Performance Tests

### Large File Test
```python
@pytest.mark.performance
def test_large_file_processing():
    """Test processing of maximum size file"""
    
    # Setup - Create 40MB file with 500K rows
    large_file = create_large_test_file(
        size_mb=40,
        num_rows=500000
    )
    
    # Execute and measure time
    start_time = time.time()
    result = process_file(large_file)
    elapsed = time.time() - start_time
    
    # Assert
    assert result is not None
    assert elapsed < 180  # Should complete within 3 minutes
```

### Memory Usage Test
```python
def test_memory_usage():
    """Test memory usage stays within limits"""
    
    import psutil
    
    # Setup
    process = psutil.Process()
    initial_memory = process.memory_info().rss / 1024 / 1024
    
    # Execute
    process_large_file()
    
    # Measure
    peak_memory = process.memory_info().rss / 1024 / 1024
    memory_increase = peak_memory - initial_memory
    
    # Assert
    assert memory_increase < 2048  # Less than 2GB increase
```

## 5. End-to-End Tests

### Happy Path
```python
def test_e2e_happy_path():
    """Test successful end-to-end flow"""
    
    # 1. Upload template
    upload_template(get_fixture('valid_template.xlsx'))
    
    # 2. Upload bulk file
    upload_bulk('30', get_fixture('valid_bulk_30.xlsx'))
    
    # 3. Select optimization
    select_optimization('zero_sales')
    
    # 4. Process
    click_process_button()
    wait_for_completion()
    
    # 5. Download results
    working_file = download_working_file()
    clean_file = download_clean_file()
    
    # Assertions
    assert working_file is not None
    assert clean_file is not None
    verify_output_structure(working_file)
```

### Error Recovery
```python
def test_e2e_error_recovery():
    """Test recovery from errors"""
    
    # 1. Upload invalid template
    upload_template(get_fixture('invalid_template.xlsx'))
    
    # 2. Verify error displayed
    assert error_message_displayed()
    
    # 3. Upload correct template
    upload_template(get_fixture('valid_template.xlsx'))
    
    # 4. Verify recovery
    assert st.session_state.validation_state == 'valid'
```

## 6. UI/UX Tests

### Visual Regression
```python
def test_ui_dark_mode_theme():
    """Test dark mode theme applied correctly"""
    
    # Setup
    page = load_application()
    
    # Verify colors
    assert page.background_color == '#0F0F0F'
    assert page.primary_color == '#8B5CF6'
    assert page.text_color == '#FFFFFF'
```

### Responsive Design
```python
def test_ui_desktop_only():
    """Test mobile warning displayed"""
    
    # Setup - Set mobile viewport
    set_viewport(width=375, height=667)
    
    # Load page
    page = load_application()
    
    # Assert
    assert "Please use a desktop browser" in page.text
```

## 7. Test Data

### Fixtures
```yaml
fixtures/
  valid_template.xlsx:
    - Port Values sheet with 5 portfolios
    - Top ASINs sheet with 10 ASINs
  
  valid_bulk_30.xlsx:
    - 10,000 rows
    - All 48 columns
    - Mix of Entity types
  
  edge_cases/:
    - empty_template.xlsx
    - huge_bulk.xlsx (40MB)
    - corrupted_file.xlsx
    - missing_columns.xlsx
```

### Test Data Generation
```python
def create_test_template(num_portfolios: int = 5) -> BytesIO:
    """Generate test template file"""
    
    port_values = pd.DataFrame({
        'Portfolio Name': [f'Portfolio_{i}' for i in range(num_portfolios)],
        'Base Bid': [1.0 + i * 0.1 for i in range(num_portfolios)],
        'Target CPA': [5.0 + i for i in range(num_portfolios)]
    })
    
    top_asins = pd.DataFrame({
        'ASIN': [f'B00{i:07d}' for i in range(10)]
    })
    
    return create_excel_file({
        'Port Values': port_values,
        'Top ASINs': top_asins
    })
```

## 8. Test Scenarios

### Scenario Matrix
| Scenario | Template | Bulk | Optimization | Expected Result |
|----------|----------|------|--------------|-----------------|
| Happy Path | Valid | Valid 30 | Zero Sales | Success |
| Missing Portfolio | Valid | Extra portfolios | Zero Sales | Error + Recovery |
| All Ignored | All Ignore | Valid | Zero Sales | Error |
| No Zero Units | Valid | No zero units | Zero Sales | Empty output |
| Large File | Valid | 40MB file | Zero Sales | Success < 3min |

## 9. Automated Testing

### CI/CD Pipeline
```yaml
name: Test Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run unit tests
      run: pytest tests/unit --cov=app --cov=business
    
    - name: Run integration tests
      run: pytest tests/integration
    
    - name: Check coverage
      run: coverage report --fail-under=80
```

## 10. Manual Testing

### Test Cases Checklist
- [ ] Upload template with spaces in portfolio names
- [ ] Upload bulk file with special characters
- [ ] Process with all portfolios marked as Ignore
- [ ] Upload files in wrong order
- [ ] Click process multiple times rapidly
- [ ] Download files with Hebrew system locale
- [ ] Test with slow internet connection
- [ ] Test with multiple browser tabs

## 11. Performance Benchmarks

### Target Metrics
```python
PERFORMANCE_TARGETS = {
    'file_upload': {
        '5MB': 2,    # seconds
        '20MB': 10,
        '40MB': 20
    },
    'processing': {
        '10K_rows': 5,
        '100K_rows': 30,
        '500K_rows': 180
    },
    'memory_usage': {
        'max_increase': 2048  # MB
    }
}
```

## 12. Bug Tracking

### Bug Report Template
```markdown
## Bug Report

**Description:**
Brief description of the bug

**Steps to Reproduce:**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Environment:**
- OS: Windows/Mac/Linux
- Browser: Chrome/Firefox/Edge
- File Size: 
- Row Count:

**Screenshots:**
If applicable

**Priority:** Critical/High/Medium/Low
```

## 13. Test Coverage

### Coverage Goals
```python
# Minimum coverage requirements
COVERAGE_REQUIREMENTS = {
    'overall': 80,
    'business_logic': 90,  # Critical calculations
    'file_handlers': 85,
    'ui_components': 70,
    'utilities': 75
}
```

### Coverage Report
```bash
# Generate coverage report
pytest --cov=. --cov-report=html

# View report
open htmlcov/index.html
```

## 14. User Acceptance Testing

### UAT Scenarios
1. **Business User Test**
   - Upload real portfolio data
   - Run Zero Sales optimization
   - Verify results match expectations
   - Download and use in Amazon

2. **Performance Test**
   - Upload largest typical file
   - Measure processing time
   - Verify system remains responsive

3. **Error Handling Test**
   - Intentionally cause errors
   - Verify clear error messages
   - Test recovery procedures

### UAT Sign-off Criteria
- All test scenarios pass
- No critical bugs
- Performance meets requirements
- User documentation complete
- Training provided