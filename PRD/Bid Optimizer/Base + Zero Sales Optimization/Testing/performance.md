# איפיון ביצועים - Bid Optimizer

## 1. דרישות ביצועים

### יעדי זמן עיבוד
| גודל קובץ | מספר שורות | זמן מקסימלי |
|-----------|------------|-------------|
| < 5MB | < 50,000 |  דקה |
| 5-10MB | 50,000-100,000 | 2 דקות |
| 10-20MB | 100,000-250,000 | 4 דקות |
| 20-40MB | 250,000-500,000 | 5 דקות |

### מגבלות מערכת
- זיכרון מקסימלי: 4GB
- גודל קובץ מקסימלי: 40MB
- מספר שורות מקסימלי: 500,000
- מספר עמודות: 48 + עמודות עזר

## 2. אופטימיזציות קריאת קבצים

### קריאה יעילה
```python
def read_large_file_optimized(file_path: str, file_type: str) -> pd.DataFrame:
    """Read large files efficiently"""
    
    if file_type == 'bulk':
        # Read only necessary columns first
        essential_cols = [
            'Entity', 'State', 'Units', 'Portfolio Name (Informational only)',
            'Campaign ID', 'Bid', 'Clicks', 'Campaign Name (Informational only)'
        ]
        
        # Use chunking for very large files
        if get_file_size(file_path) > 20 * 1024 * 1024:  # 20MB
            return read_in_chunks(file_path, essential_cols)
        else:
            return pd.read_excel(
                file_path,
                sheet_name='Sponsored Products Campaigns',
                dtype={'Campaign ID': str, 'Portfolio ID': str},  # Specify dtypes
                na_values=['', 'NA', 'N/A'],
                keep_default_na=True
            )
```

### Chunked Reading
```python
def read_in_chunks(file_path: str, columns: list, chunk_size: int = 10000) -> pd.DataFrame:
    """Read file in chunks to manage memory"""
    
    chunks = []
    
    # Read Excel in chunks
    for chunk in pd.read_excel(
        file_path,
        sheet_name='Sponsored Products Campaigns',
        chunksize=chunk_size
    ):
        # Process chunk
        processed_chunk = process_chunk(chunk, columns)
        chunks.append(processed_chunk)
        
        # Update progress
        if st:
            progress = len(chunks) * chunk_size / total_rows
            st.progress(progress)
    
    # Combine chunks
    return pd.concat(chunks, ignore_index=True)
```

## 3. Memory Management

### Memory Monitoring
```python
def monitor_memory_usage():
    """Monitor memory usage during processing"""
    
    import psutil
    import gc
    
    # Get current memory usage
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_usage_mb = memory_info.rss / 1024 / 1024
    
    # Warning if high usage
    if memory_usage_mb > 3000:  # 3GB
        st.warning(f"High memory usage: {memory_usage_mb:.0f}MB")
        
        # Force garbage collection
        gc.collect()
        
        # Clear unnecessary data from session
        clear_temporary_data()
    
    return memory_usage_mb
```

### DataFrame Optimization
```python
def optimize_dataframe_memory(df: pd.DataFrame) -> pd.DataFrame:
    """Optimize DataFrame memory usage"""
    
    # Downcast numeric types
    for col in df.select_dtypes(include=['float']).columns:
        df[col] = pd.to_numeric(df[col], downcast='float')
    
    for col in df.select_dtypes(include=['int']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')
    
    # Convert object columns to category where appropriate
    for col in df.select_dtypes(include=['object']).columns:
        num_unique = df[col].nunique()
        num_total = len(df[col])
        
        # Convert to category if less than 50% unique
        if num_unique / num_total < 0.5:
            df[col] = df[col].astype('category')
    
    return df
```

## 4. Processing Optimization

### Vectorized Operations
```python
def calculate_bids_vectorized(df: pd.DataFrame) -> pd.DataFrame:
    """Use vectorized operations for bid calculation"""
    
    # Avoid loops - use vectorized operations
    
    # Case 1: No Target CPA + "up and"
    mask1 = df['Target CPA'].isna() & df['Campaign Name'].str.contains('up and', na=False)
    df.loc[mask1, 'Bid'] = df.loc[mask1, 'Base Bid'] * 0.5
    
    # Case 2: No Target CPA + no "up and"
    mask2 = df['Target CPA'].isna() & ~df['Campaign Name'].str.contains('up and', na=False)
    df.loc[mask2, 'Bid'] = df.loc[mask2, 'Base Bid']
    
    # Case 3 & 4: With Target CPA (vectorized calculation)
    mask3 = ~df['Target CPA'].isna()
    df.loc[mask3, 'calc1'] = df.loc[mask3, 'Adj. CPA'] / (df.loc[mask3, 'Clicks'] + 1)
    
    # Continue with vectorized operations...
    
    return df
```

### Parallel Processing
```python
def process_optimizations_parallel(optimizations: list) -> dict:
    """Process multiple optimizations in parallel"""
    
    from concurrent.futures import ThreadPoolExecutor
    import multiprocessing
    
    # Determine number of workers
    num_workers = min(len(optimizations), multiprocessing.cpu_count())
    
    results = {}
    
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        # Submit tasks
        futures = {
            executor.submit(process_single_optimization, opt): opt
            for opt in optimizations
        }
        
        # Collect results
        for future in futures:
            opt_name = futures[future]
            try:
                results[opt_name] = future.result(timeout=60)
            except TimeoutError:
                st.error(f"Optimization {opt_name} timed out")
    
    return results
```

## 5. Caching Strategies

### Session State Caching
```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_cached_template(file_hash: str) -> pd.DataFrame:
    """Cache template data"""
    return st.session_state.template_df

@st.cache_data
def calculate_portfolio_mappings(template_df: pd.DataFrame) -> dict:
    """Cache portfolio mappings"""
    return {
        row['Portfolio Name']: {
            'base_bid': row['Base Bid'],
            'target_cpa': row['Target CPA']
        }
        for _, row in template_df.iterrows()
    }
```

### Result Caching
```python
def cache_optimization_results(opt_name: str, result: dict):
    """Cache optimization results"""
    
    cache_key = f"opt_result_{opt_name}_{hash(str(result))}"
    st.session_state[cache_key] = {
        'result': result,
        'timestamp': datetime.now()
    }
```

## 6. Progress Tracking

### Granular Progress
```python
def track_processing_progress(total_steps: int):
    """Track and display granular progress"""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    time_estimate = st.empty()
    
    start_time = time.time()
    
    def update_progress(current_step: int, message: str):
        # Calculate progress
        progress = current_step / total_steps
        progress_bar.progress(progress)
        
        # Update status
        status_text.text(message)
        
        # Estimate remaining time
        elapsed = time.time() - start_time
        if current_step > 0:
            total_estimate = elapsed * total_steps / current_step
            remaining = total_estimate - elapsed
            time_estimate.text(f"Estimated time remaining: {remaining:.0f}s")
    
    return update_progress
```

## 7. Database Optimization (Future)

### Batch Operations
```python
def batch_database_operations(operations: list, batch_size: int = 1000):
    """Batch database operations for efficiency"""
    
    for i in range(0, len(operations), batch_size):
        batch = operations[i:i+batch_size]
        execute_batch(batch)
        
        # Update progress
        progress = (i + batch_size) / len(operations)
        st.progress(progress)
```

## 8. File Generation Optimization

### Streaming Excel Write
```python
def write_excel_streaming(sheets_data: dict, output_path: str):
    """Write Excel file using streaming to reduce memory"""
    
    from openpyxl import Workbook
    from openpyxl.writer.excel import save_virtual_workbook
    
    wb = Workbook(write_only=True)
    
    for sheet_name, df in sheets_data.items():
        ws = wb.create_sheet(title=sheet_name)
        
        # Write header
        ws.append(df.columns.tolist())
        
        # Write data in batches
        for idx in range(0, len(df), 1000):
            batch = df.iloc[idx:idx+1000]
            for row in batch.values:
                ws.append(row.tolist())
    
    # Save to BytesIO
    output = BytesIO()
    output.write(save_virtual_workbook(wb))
    output.seek(0)
    
    return output
```

## 9. UI Performance

### Lazy Loading
```python
def lazy_load_sections():
    """Load UI sections only when needed"""
    
    # Load only visible sections
    if st.session_state.get('show_upload_section', True):
        render_upload_section()
    
    # Load validation only if files uploaded
    if st.session_state.get('files_uploaded'):
        render_validation_section()
    
    # Load output only if processing complete
    if st.session_state.get('processing_complete'):
        render_output_section()
```

### Debouncing
```python
def debounce(wait_time: float = 0.5):
    """Debounce function calls"""
    
    def decorator(func):
        last_called = [0]
        
        def debounced(*args, **kwargs):
            current_time = time.time()
            if current_time - last_called[0] > wait_time:
                last_called[0] = current_time
                return func(*args, **kwargs)
        
        return debounced
    
    return decorator

@debounce(0.5)
def handle_checkbox_change():
    """Handle checkbox changes with debouncing"""
    pass
```

## 10. Error Recovery Performance

### Checkpoint System
```python
def create_processing_checkpoint(stage: str, data: dict):
    """Create checkpoint for recovery"""
    
    checkpoint = {
        'stage': stage,
        'data': data,
        'timestamp': datetime.now()
    }
    
    st.session_state[f'checkpoint_{stage}'] = checkpoint

def recover_from_checkpoint(stage: str) -> dict:
    """Recover from last checkpoint"""
    
    checkpoint = st.session_state.get(f'checkpoint_{stage}')
    if checkpoint:
        st.info(f"Recovering from checkpoint: {stage}")
        return checkpoint['data']
    return None
```

## 11. Monitoring Dashboard

### Performance Metrics
```python
def display_performance_metrics():
    """Display performance metrics dashboard"""
    
    metrics = {
        'memory_usage': get_memory_usage(),
        'processing_time': st.session_state.get('processing_time', 0),
        'rows_per_second': calculate_throughput(),
        'cache_hit_rate': get_cache_stats()
    }
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Memory", f"{metrics['memory_usage']:.0f}MB")
    with col2:
        st.metric("Time", f"{metrics['processing_time']:.1f}s")
    with col3:
        st.metric("Throughput", f"{metrics['rows_per_second']:.0f}/s")
    with col4:
        st.metric("Cache Hit", f"{metrics['cache_hit_rate']:.0%}")
```

## 12. Optimization Recommendations

### Auto-Optimization
```python
def recommend_optimizations(file_size: int, row_count: int) -> dict:
    """Recommend performance optimizations based on file characteristics"""
    
    recommendations = []
    
    if file_size > 20 * 1024 * 1024:  # 20MB
        recommendations.append("Consider splitting file into smaller chunks")
    
    if row_count > 100000:
        recommendations.append("Processing will use chunked mode automatically")
    
    if st.session_state.get('selected_optimizations', []) > 5:
        recommendations.append("Consider running fewer optimizations at once")
    
    return recommendations
```