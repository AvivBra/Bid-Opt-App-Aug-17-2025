# מפרט בדיקות ביצועים - Bid Optimizer

## 1. יעדי ביצועים

### זמני תגובה מקסימליים
| פעולה | 10K שורות | 100K שורות | 500K שורות |
|--------|-----------|-------------|--------------|
| קריאת קובץ | < 1 שניה | < 5 שניות | < 15 שניות |
| ולידציה | < 1 שניה | < 2 שניות | < 5 שניות |
| עיבוד Zero Sales | < 2 שניות | < 10 שניות | < 30 שניות |
| יצירת קבצי פלט | < 2 שניות | < 5 שניות | < 15 שניות |
| **סה"כ** | < 6 שניות | < 22 שניות | < 65 שניות |

### צריכת משאבים
- **זיכרון מקסימלי**: 2GB
- **CPU**: עד 80% בעיבוד
- **Disk I/O**: עד 50MB/s

## 2. בדיקות עומס (Load Tests)

### Test 1: Standard Load
```python
def test_standard_load():
    """Test with typical file sizes"""
    files = {
        'template': create_template(portfolios=20),
        'bulk_60': create_bulk(rows=50_000)
    }
    
    start = time.time()
    result = process_optimization('zero_sales', files)
    duration = time.time() - start
    
    assert duration < 10  # seconds
    assert result['modified_rows'] > 0
```

### Test 2: Heavy Load
```python
def test_heavy_load():
    """Test with large files"""
    files = {
        'template': create_template(portfolios=100),
        'bulk_60': create_bulk(rows=200_000)
    }
    
    start = time.time()
    result = process_optimization('zero_sales', files)
    duration = time.time() - start
    
    assert duration < 30  # seconds
    assert psutil.Process().memory_info().rss < 2 * 1024**3  # 2GB
```

### Test 3: Maximum Load
```python
def test_maximum_load():
    """Test with maximum allowed size"""
    files = {
        'template': create_template(portfolios=500),
        'bulk_60': create_bulk(rows=499_999)
    }
    
    start = time.time()
    result = process_optimization('zero_sales', files)
    duration = time.time() - start
    
    assert duration < 60  # seconds
    assert result['success'] == True
```

## 3. בדיקות לחץ (Stress Tests)

### Test 1: Beyond Limits
```python
def test_beyond_limits():
    """Test system behavior beyond limits"""
    
    # File size limit
    with pytest.raises(FileSizeError):
        upload_file(create_file(size_mb=41))
    
    # Row limit
    with pytest.raises(RowLimitError):
        process_bulk(create_bulk(rows=500_001))
    
    # Memory limit
    with pytest.raises(MemoryError):
        process_multiple_large_files(count=10)
```

### Test 2: Rapid Operations
```python
def test_rapid_operations():
    """Test rapid consecutive operations"""
    
    for i in range(10):
        upload_file(f'template_{i}.xlsx')
        validate()
        process()
        reset()
    
    # System should remain stable
    assert system_healthy()
```

### Test 3: Concurrent Users
```python
def test_concurrent_users():
    """Simulate multiple users (future feature)"""
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for i in range(5):
            future = executor.submit(process_user_session, i)
            futures.append(future)
        
        results = [f.result() for f in futures]
        assert all(r['success'] for r in results)
```

## 4. בדיקות זיכרון

### Test 1: Memory Leak Detection
```python
def test_memory_leak():
    """Ensure no memory leaks after processing"""
    
    initial_memory = get_memory_usage()
    
    for i in range(10):
        process_large_file()
        gc.collect()
    
    final_memory = get_memory_usage()
    leak = final_memory - initial_memory
    
    assert leak < 100 * 1024 * 1024  # Less than 100MB
```

### Test 2: Memory Cleanup
```python
def test_memory_cleanup():
    """Test memory is freed after reset"""
    
    # Process large file
    process_large_file()
    memory_during = get_memory_usage()
    
    # Reset
    reset_session()
    gc.collect()
    
    memory_after = get_memory_usage()
    assert memory_after < memory_during * 0.5
```

## 5. בדיקות I/O

### Test 1: File Read Performance
```python
@pytest.mark.benchmark
def test_file_read_performance(benchmark):
    """Benchmark file reading"""
    
    file_10mb = create_file(size_mb=10)
    file_20mb = create_file(size_mb=20)
    file_40mb = create_file(size_mb=40)
    
    result_10 = benchmark(read_file, file_10mb)
    assert benchmark.stats['mean'] < 2  # seconds
    
    result_20 = benchmark(read_file, file_20mb)
    assert benchmark.stats['mean'] < 4
    
    result_40 = benchmark(read_file, file_40mb)
    assert benchmark.stats['mean'] < 8
```

### Test 2: File Write Performance
```python
def test_file_write_performance():
    """Test output file generation speed"""
    
    data = create_dataframe(rows=100_000)
    
    start = time.time()
    write_excel(data, 'output.xlsx')
    duration = time.time() - start
    
    assert duration < 5  # seconds
    assert os.path.getsize('output.xlsx') > 0
```

## 6. בדיקות חישובים

### Test 1: Calculation Performance
```python
def test_calculation_performance():
    """Test Zero Sales calculations speed"""
    
    df = create_bulk(rows=100_000)
    
    start = time.time()
    for index, row in df.iterrows():
        new_bid = calculate_bid(row)
    duration = time.time() - start
    
    assert duration < 10  # seconds
```

### Test 2: Vectorized Operations
```python
def test_vectorized_performance():
    """Ensure vectorized operations are used"""
    
    df = create_bulk(rows=100_000)
    
    start = time.time()
    df['new_bid'] = df.apply(calculate_bid_vectorized, axis=1)
    duration = time.time() - start
    
    assert duration < 2  # Much faster than loop
```

## 7. בדיקות UI Response

### Test 1: UI Responsiveness
```python
def test_ui_responsiveness():
    """Test UI remains responsive during processing"""
    
    # Start heavy processing
    future = start_async_processing(rows=200_000)
    
    # UI should respond within 100ms
    start = time.time()
    click_button('cancel')
    response_time = time.time() - start
    
    assert response_time < 0.1  # 100ms
```

### Test 2: Progress Updates
```python
def test_progress_updates():
    """Test progress bar updates smoothly"""
    
    updates = []
    
    def capture_progress(percent):
        updates.append((time.time(), percent))
    
    process_with_callback(capture_progress)
    
    # Check updates are frequent and smooth
    assert len(updates) > 10
    for i in range(1, len(updates)):
        time_diff = updates[i][0] - updates[i-1][0]
        assert time_diff < 1  # Update at least every second
```

## 8. Benchmark Suite

```python
class BenchmarkSuite:
    """Complete benchmark suite"""
    
    @staticmethod
    def run_all():
        results = {}
        
        # File operations
        results['read_10k'] = benchmark_read(10_000)
        results['read_100k'] = benchmark_read(100_000)
        results['read_500k'] = benchmark_read(500_000)
        
        # Processing
        results['process_10k'] = benchmark_process(10_000)
        results['process_100k'] = benchmark_process(100_000)
        results['process_500k'] = benchmark_process(500_000)
        
        # Memory
        results['memory_10k'] = measure_memory(10_000)
        results['memory_100k'] = measure_memory(100_000)
        results['memory_500k'] = measure_memory(500_000)
        
        return results
    
    @staticmethod
    def compare_with_baseline(results):
        baseline = load_baseline()
        
        for key, value in results.items():
            if value > baseline[key] * 1.1:  # 10% regression
                raise PerformanceRegression(f"{key}: {value} > {baseline[key]}")
```

## 9. Performance Monitoring

### Metrics to Track
```python
PERFORMANCE_METRICS = {
    'file_read_time': [],
    'validation_time': [],
    'processing_time': [],
    'output_generation_time': [],
    'total_time': [],
    'peak_memory': [],
    'cpu_usage': [],
    'rows_per_second': []
}

def log_performance(operation, duration, rows=None):
    PERFORMANCE_METRICS[f'{operation}_time'].append(duration)
    if rows:
        PERFORMANCE_METRICS['rows_per_second'].append(rows / duration)
```

### Performance Report
```python
def generate_performance_report():
    return {
        'average_times': {
            op: np.mean(times) 
            for op, times in PERFORMANCE_METRICS.items()
        },
        'percentiles': {
            op: {
                'p50': np.percentile(times, 50),
                'p95': np.percentile(times, 95),
                'p99': np.percentile(times, 99)
            }
            for op, times in PERFORMANCE_METRICS.items()
        }
    }
```

## 10. CI/CD Integration

```yaml
performance-tests:
  stage: performance
  script:
    - python -m pytest tests/performance --benchmark-only
    - python -m pytest tests/performance --benchmark-compare
  artifacts:
    paths:
      - .benchmarks/
    reports:
      performance: performance-report.json
  only:
    - master
    - performance-improvements
```

## 11. Performance Optimization Checklist

- [ ] Use vectorized pandas operations
- [ ] Implement chunking for large files
- [ ] Use appropriate data types (int8, int16)
- [ ] Clear memory after each optimization
- [ ] Use generators for large iterations
- [ ] Cache repeated calculations
- [ ] Parallelize independent operations
- [ ] Use efficient file formats (parquet for temp)
- [ ] Minimize dataframe copies
- [ ] Profile and optimize hot paths