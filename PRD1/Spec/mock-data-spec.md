# מפרט Mock Data - Bid Optimizer

## 1. מטרת Mock Data

### יעדים
- בדיקת UI ללא לוגיקה עסקית
- סימולציה של כל התרחישים
- פיתוח מהיר של ממשק
- בדיקות ללא תלות בקבצים

### שימוש
- Phase A של הפיתוח (UI)
- בדיקות אוטומטיות
- הדגמות
- פיתוח features חדשים

## 2. תרחישי Mock

### תרחיש 4: Multiple Files
```python
MOCK_MULTIPLE = {
    'files': {
        'template': MockFile('template.xlsx', 125_000),
        'bulk_30': MockFile('bulk_30.xlsx', 1_800_000),
        'bulk_60': MockFile('bulk_60.xlsx', 2_300_000),
        'bulk_7': None,  # Not uploaded
        'data_rova': None  # Not uploaded
    },
    'validation': {
        'zero_sales': {
            'is_valid': True,
            'message': '✅ Ready (using Bulk 60)'
        },
        'portfolio_bid': {
            'is_valid': True,
            'message': '✅ Ready (using Bulk 30)'
        },
        'budget_optimization': {
            'is_valid': False,
            'errors': ['Missing Bulk 7 file'],
            'message': '❌ Missing required files'
        }
    }
}
```

## 3. Mock File Class

```python
class MockFile:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size
        self.uploaded_at = datetime.now()
        
    @property
    def size_mb(self):
        return self.size / (1024 * 1024)
    
    @property
    def extension(self):
        return self.name.split('.')[-1]
    
    def to_bytes_io(self):
        """Generate fake BytesIO object"""
        return BytesIO(b'Mock file content')
```

## 4. Mock DataFrames

### Template DataFrame
```python
def create_mock_template():
    return pd.DataFrame({
        'Portfolio Name': [
            'Kids-Brand-US',
            'Kids-Brand-EU', 
            'Supplements-US',
            'Supplements-EU'
        ],
        'Base Bid': [1.25, 0.95, 'Ignore', 2.10],
        'Target CPA': [5.00, None, None, 8.50]
    })
```

### Bulk DataFrame
```python
def create_mock_bulk(rows=1000):
    portfolios = ['Kids-Brand-US', 'Kids-Brand-EU', 
                  'Supplements-US', 'Supplements-EU']
    
    return pd.DataFrame({
        'Product': ['Sponsored Products'] * rows,
        'Entity': np.random.choice(['Keyword', 'Product Targeting'], rows),
        'Operation': [''] * rows,
        'Campaign ID': range(1000, 1000 + rows),
        'Portfolio Name (Informational only)': np.random.choice(portfolios, rows),
        'State': np.random.choice(['enabled', 'paused'], rows, p=[0.8, 0.2]),
        'Bid': np.random.uniform(0.5, 3.0, rows),
        'Units': np.random.choice([0, 1, 2, 5], rows, p=[0.3, 0.3, 0.2, 0.2]),
        'Clicks': np.random.randint(0, 100, rows),
        # ... 38 more columns
    })
```

## 5. Mock Validation Results

### Success Result
```python
MOCK_VALIDATION_SUCCESS = {
    'is_valid': True,
    'errors': [],
    'warnings': ['5 portfolios marked as Ignore'],
    'stats': {
        'total_portfolios': 10,
        'valid_portfolios': 10,
        'ignored_portfolios': 5
    },
    'message': '✅ All validations passed'
}
```

### Error Result
```python
MOCK_VALIDATION_ERROR = {
    'is_valid': False,
    'errors': [
        'Missing portfolios: ABC, DEF',
        'Invalid Base Bid in row 5'
    ],
    'warnings': [],
    'can_process': False,
    'message': '❌ Validation failed'
}
```

## 6. Mock Processing Results

### Processing Stats
```python
MOCK_PROCESSING_STATS = {
    'start_time': datetime.now(),
    'end_time': datetime.now() + timedelta(seconds=8),
    'total_rows': 5000,
    'modified_rows': 1234,
    'unchanged_rows': 3766,
    'error_rows': 12,
    'warnings': {
        'below_minimum': 5,
        'above_maximum': 3,
        'calculation_errors': 4
    }
}
```

### Output Files
```python
MOCK_OUTPUT_FILES = {
    'working': {
        'name': 'Auto Optimized Bulk | Working | 2024-01-15 | 14-30.xlsx',
        'size': 3_200_000,
        'sheets': ['Working Zero Sales'],
        'rows': 1234
    },
    'clean': {
        'name': 'Auto Optimized Bulk | Clean | 2024-01-15 | 14-30.xlsx',
        'size': 2_800_000,
        'sheets': ['Clean Zero Sales'],
        'rows': 1234
    }
}
```

## 7. Mock Progress Updates

```python
def mock_progress_generator():
    """Generate realistic progress updates"""
    stages = [
        (10, "Initializing..."),
        (20, "Reading files..."),
        (30, "Validating data..."),
        (50, "Processing Zero Sales..."),
        (70, "Applying calculations..."),
        (85, "Generating output files..."),
        (95, "Finalizing..."),
        (100, "Complete!")
    ]
    
    for percent, message in stages:
        yield {
            'percent': percent,
            'message': message,
            'current_optimization': 'Zero Sales',
            'time_elapsed': percent * 0.1  # seconds
        }
        time.sleep(0.5)  # Simulate processing
```

## 8. Mock Error Scenarios

### File Errors
```python
MOCK_FILE_ERRORS = {
    'too_large': {
        'error': 'File exceeds 40MB limit',
        'details': 'Your file: 41.2MB, Maximum: 40MB'
    },
    'wrong_format': {
        'error': 'Invalid file format',
        'details': 'Expected .xlsx or .csv, received .txt'
    },
    'corrupted': {
        'error': 'Cannot read file',
        'details': 'File may be corrupted or password protected'
    }
}
```

### Processing Errors
```python
MOCK_PROCESSING_ERRORS = {
    'calculation_error': {
        'optimization': 'Zero Sales',
        'error': 'Calculation failed',
        'rows_affected': [105, 234, 567],
        'suggestion': 'Check data in affected rows'
    },
    'memory_error': {
        'error': 'Insufficient memory',
        'details': 'File too large to process',
        'suggestion': 'Try with smaller file'
    }
}
```

## 9. Mock UI States

```python
MOCK_UI_STATES = {
    'initial': {
        'files_uploaded': {},
        'optimizations_selected': [],
        'validation_results': {},
        'can_process': False,
        'show_validation': False,
        'show_output': False
    },
    'files_uploaded': {
        'files_uploaded': {
            'template': True,
            'bulk_60': True
        },
        'show_validation': True,
        'can_process': False
    },
    'ready': {
        'validation_results': {'zero_sales': MOCK_VALIDATION_SUCCESS},
        'can_process': True,
        'process_button_text': 'Process Files'
    },
    'processing': {
        'show_progress': True,
        'progress': 45,
        'can_process': False,
        'disable_uploads': True
    },
    'complete': {
        'show_output': True,
        'output_files': MOCK_OUTPUT_FILES,
        'show_pink_notice': True,
        'pink_notice_text': '12 rows with errors'
    }
}
```

## 10. Mock Data Generator

```python
class MockDataGenerator:
    @staticmethod
    def generate_scenario(scenario_name: str):
        """Generate complete mock data for a scenario"""
        scenarios = {
            'valid': MockDataGenerator._valid_scenario,
            'missing': MockDataGenerator._missing_scenario,
            'large': MockDataGenerator._large_scenario,
            'error': MockDataGenerator._error_scenario
        }
        return scenarios[scenario_name]()
    
    @staticmethod
    def _valid_scenario():
        return {
            'files': MockDataGenerator.create_valid_files(),
            'validation': MOCK_VALIDATION_SUCCESS,
            'processing': MOCK_PROCESSING_STATS,
            'output': MOCK_OUTPUT_FILES
        }
    
    @staticmethod
    def create_valid_files():
        return {
            'template': create_mock_template(),
            'bulk_60': create_mock_bulk(5000)
        }
```

## 11. Usage in Development

### Enable Mock Mode
```python
# config/settings.py
MOCK_MODE = os.getenv('MOCK_MODE', 'False') == 'True'

# app/main.py
if MOCK_MODE:
    st.sidebar.selectbox(
        "Mock Scenario",
        ['valid', 'missing', 'large', 'error']
    )
```

### Replace Real Logic
```python
# app/state/session.py
def validate_files(self):
    if MOCK_MODE:
        return MockDataGenerator.generate_scenario(
            st.session_state.get('mock_scenario', 'valid')
        )['validation']
    else:
        # Real validation logic
        return self.orchestrator.validate_files(...)
```

## 12. Testing with Mock Data

```python
def test_ui_with_mock_data():
    # Enable mock mode
    os.environ['MOCK_MODE'] = 'True'
    
    # Test each scenario
    for scenario in ['valid', 'missing', 'large', 'error']:
        app = create_app()
        app.set_mock_scenario(scenario)
        
        # Verify UI shows correct state
        assert app.get_validation_message() == expected[scenario]
        assert app.can_process() == expected_state[scenario]
``` 1: Valid - הכל תקין
```python
MOCK_VALID = {
    'files': {
        'template': MockFile('template.xlsx', 125_000),
        'bulk_60': MockFile('bulk_60.xlsx', 2_300_000),
    },
    'validation': {
        'zero_sales': {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'message': '✅ Ready to process'
        }
    },
    'stats': {
        'total_rows': 5000,
        'portfolios': 4,
        'will_process': 1234
    }
}
```

### תרחיש 2: Missing Portfolios
```python
MOCK_MISSING = {
    'files': {
        'template': MockFile('template.xlsx', 125_000),
        'bulk_60': MockFile('bulk_60.xlsx', 2_300_000),
    },
    'validation': {
        'zero_sales': {
            'is_valid': False,
            'errors': ['Missing portfolios: Port_C, Port_D'],
            'missing_portfolios': ['Port_C', 'Port_D'],
            'message': '❌ Missing portfolios found'
        }
    }
}
```

### תרחיש 3: Large File
```python
MOCK_LARGE = {
    'files': {
        'template': MockFile('template.xlsx', 125_000),
        'bulk_60': MockFile('bulk_60.xlsx', 41_000_000),
    },
    'error': 'File exceeds 40MB limit',
    'validation': None
}
```

### תרחיש