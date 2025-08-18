# תוכנית בדיקות - Bid Optimizer

## 1. אסטרטגיית בדיקות

### רמות בדיקה
1. **Unit Tests** - פונקציות בודדות
2. **Integration Tests** - אינטגרציה בין מודולים
3. **E2E Tests** - תרחישים מלאים
4. **Performance Tests** - ביצועים ועומסים
5. **UAT** - בדיקות משתמש

### סביבות בדיקה
- **Development** - Mock Data
- **Testing** - נתונים מבוקרים
- **Staging** - נתונים כמו Production
- **Production** - נתונים אמיתיים

## 2. Unit Tests

### File Readers
```python
def test_read_valid_excel():
    df = ExcelReader.read('valid.xlsx')
    assert df is not None
    assert len(df.columns) == 48

def test_read_invalid_format():
    with pytest.raises(InvalidFormatError):
        ExcelReader.read('file.txt')

def test_read_large_file():
    with pytest.raises(FileSizeError):
        ExcelReader.read('huge_41mb.xlsx')
```

### Validators
```python
def test_validate_template():
    validator = TemplateValidator()
    result = validator.validate(template_df)
    assert result.is_valid == True

def test_missing_portfolios():
    validator = PortfolioValidator()
    result = validator.check_portfolios(template, bulk)
    assert len(result.missing) == 2
```

### Zero Sales Logic
```python
def test_zero_sales_calculation():
    processor = ZeroSalesProcessor()
    new_bid = processor.calculate_bid(
        base_bid=1.00,
        clicks=10,
        has_target_cpa=True,
        campaign_name="Brand up and coming"
    )
    assert new_bid == 0.50

def test_bid_minimum():
    result = processor.apply_limits(0.01)
    assert result == 0.02

def test_bid_maximum():
    result = processor.apply_limits(2.00)
    assert result == 1.25
```

## 3. Integration Tests

### Upload → Validation
```python
def test_upload_and_validate():
    # Upload files
    session.upload_file('template', template_file)
    session.upload_file('bulk_60', bulk_file)
    
    # Validate
    orchestrator = Orchestrator()
    results = orchestrator.validate_all(session)
    
    assert results['zero_sales'].is_valid
    assert session.state == 'ready'
```

### Validation → Processing
```python
def test_process_after_validation():
    # Setup valid state
    session = create_valid_session()
    
    # Process
    results = orchestrator.process_all(session)
    
    assert 'working' in results
    assert 'clean' in results
    assert len(results['working']) > 0
```

## 4. End-to-End Tests

### Scenario: Happy Path
```python
def test_e2e_happy_path():
    # 1. Upload files
    upload_template('valid_template.xlsx')
    upload_bulk_60('valid_bulk.xlsx')
    
    # 2. Select optimization
    select_optimization('zero_sales')
    
    # 3. Validate
    assert validation_status() == 'Ready'
    
    # 4. Process
    click_process()
    wait_for_completion()
    
    # 5. Download
    working = download_working_file()
    clean = download_clean_file()
    
    assert working.exists()
    assert clean.exists()
    assert working.sheets == ['Working Zero Sales']
```

### Scenario: Error Recovery
```python
def test_e2e_error_recovery():
    # Upload with missing portfolios
    upload_template('incomplete.xlsx')
    upload_bulk_60('full.xlsx')
    
    # See error
    assert 'Missing portfolios' in get_errors()
    
    # Fix and reupload
    upload_template('complete.xlsx')
    
    # Continue normally
    assert validation_status() == 'Ready'
```

## 5. Performance Tests

### Load Tests
| Test | Specification | Pass Criteria |
|------|--------------|---------------|
| 10K rows | Process time | < 5 seconds |
| 100K rows | Process time | < 30 seconds |
| 500K rows | Process time | < 60 seconds |
| 40MB file | Upload time | < 10 seconds |

### Stress Tests
```python
def test_maximum_load():
    # Upload maximum size
    upload_bulk_60('40mb_file.xlsx')  # Should work
    upload_bulk_60('41mb_file.xlsx')  # Should fail
    
    # Maximum rows
    df = create_dataframe(rows=500000)
    result = process(df)
    assert result.success
    
    # Over maximum
    df = create_dataframe(rows=500001)
    with pytest.raises(RowLimitError):
        process(df)
```

### Memory Tests
```python
def test_memory_usage():
    import psutil
    
    initial = psutil.Process().memory_info().rss
    
    # Process large file
    process_large_file('100k_rows.xlsx')
    
    peak = psutil.Process().memory_info().rss
    assert (peak - initial) < 2 * 1024 * 1024 * 1024  # 2GB
```

## 6. בדיקות UI

### Component Tests
```python
def test_upload_button():
    button = find_element('upload_template')
    assert button.enabled
    assert button.text == '📤 Upload Template'
    assert button.color == '#FF0000'

def test_progress_bar():
    start_processing()
    progress = find_element('progress_bar')
    assert progress.visible
    assert 0 <= progress.value <= 100
```

### Interaction Tests
```python
def test_file_replacement():
    upload_file('template', 'file1.xlsx')
    assert get_status('template') == '✓ file1.xlsx'
    
    upload_file('template', 'file2.xlsx')
    assert get_status('template') == '✓ file2.xlsx'

def test_checkbox_selection():
    select_optimization('zero_sales')
    select_optimization('portfolio_bid')
    
    selected = get_selected_optimizations()
    assert len(selected) == 2
```

## 7. Validation Tests

### Template Validation
```python
def test_template_validations():
    # Empty portfolio name
    template = create_template()
    template.loc[0, 'Portfolio Name'] = ''
    assert not validate_template(template)
    
    # Invalid Base Bid
    template.loc[0, 'Base Bid'] = 'ABC'
    assert not validate_template(template)
    
    # All Ignore
    template['Base Bid'] = 'Ignore'
    assert not validate_template(template)
```

### Bulk Validation
```python
def test_bulk_validations():
    # Missing columns
    bulk = create_bulk()
    bulk = bulk.drop('Units', axis=1)
    assert not validate_bulk(bulk)
    
    # Wrong sheet name
    bulk_file = create_excel()
    bulk_file.save_sheet('Wrong Name', data)
    assert not validate_bulk_file(bulk_file)
```

## 8. Test Data

### Valid Test Files
```
fixtures/
├── valid/
│   ├── template_complete.xlsx
│   ├── bulk_30_small.xlsx
│   ├── bulk_60_medium.xlsx
│   ├── bulk_7_large.xlsx
│   └── data_rova_sample.xlsx
```

### Invalid Test Files
```
fixtures/
├── invalid/
│   ├── template_missing_columns.xlsx
│   ├── template_all_ignore.xlsx
│   ├── bulk_no_sheet.xlsx
│   ├── bulk_wrong_columns.xlsx
│   └── file_corrupted.xlsx
```

### Edge Cases
```
fixtures/
├── edge/
│   ├── special_characters.xlsx
│   ├── unicode_portfolios.xlsx
│   ├── extreme_values.xlsx
│   ├── maximum_size.xlsx
│   └── single_row.xlsx
```

## 9. Test Automation

### CI/CD Pipeline
```yaml
test:
  stage: test
  script:
    - pytest tests/unit -v
    - pytest tests/integration -v
    - pytest tests/e2e --headless
    - pytest tests/performance --benchmark

coverage:
  script:
    - pytest --cov=app --cov-report=html
    - coverage report --fail-under=80
```

### Pre-commit Hooks
```python
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: unit-tests
        name: Unit Tests
        entry: pytest tests/unit
        language: system
        pass_filenames: false
```

## 10. Bug Report Template

```markdown
### Bug Information
**Title:** [Brief description]
**Severity:** Critical/High/Medium/Low
**Environment:** Dev/Test/Prod

### Steps to Reproduce
1. 
2. 
3. 

### Expected Result

### Actual Result

### Screenshots/Logs

### Additional Context
```

## 11. Test Schedule

| Phase | Duration | Focus |
|-------|----------|-------|
| Unit Testing | 1 day | Core functions |
| Integration | 1 day | Module interactions |
| E2E Testing | 2 days | User scenarios |
| Performance | 1 day | Load and stress |
| UAT | 2 days | User acceptance |
| Regression | 1 day | Final check |

**Total:** 8 days

## 12. Exit Criteria

### Ready for Production
- [ ] All unit tests pass (100%)
- [ ] Integration tests pass (100%)
- [ ] E2E happy path works
- [ ] No critical bugs
- [ ] Performance targets met
- [ ] Code coverage > 80%
- [ ] UAT sign-off received
- [ ] Documentation complete

## 13. Risk Areas

### High Risk
- Portfolio validation logic
- Bid calculations
- File size handling
- Memory management

### Medium Risk
- UI responsiveness
- Progress tracking
- Error messages
- Download functionality

### Low Risk
- Static content
- Styling
- Tooltips
- Labels