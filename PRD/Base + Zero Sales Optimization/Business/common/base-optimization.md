# איפיון Base Optimization

## 1. סקירה כללית

### מטרה
להגדיר מבנה בסיסי אחיד לכל האופטימיזציות במערכת.

### עקרונות
- כל אופטימיזציה יורשת מ-BaseOptimization
- ממשק אחיד לכל האופטימיזציות
- Validation וcleaning פנימיים
- עצמאות מלאה של כל אופטימיזציה

## 2. Class Structure

### Base Class Definition
```python
from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Tuple, List

class BaseOptimization(ABC):
    """Base class for all optimizations"""
    
    def __init__(self, name: str):
        self.name = name
        self.errors = []
        self.warnings = []
        self.stats = {}
    
    @abstractmethod
    def get_required_files(self) -> Dict[str, bool]:
        """Define which files this optimization requires"""
        pass
    
    @abstractmethod
    def validate(self, bulk_df: pd.DataFrame, template_df: pd.DataFrame) -> bool:
        """Validate data for this optimization"""
        pass
    
    @abstractmethod
    def clean(self, bulk_df: pd.DataFrame) -> pd.DataFrame:
        """Clean and filter data for this optimization"""
        pass
    
    @abstractmethod
    def process(self, bulk_df: pd.DataFrame, template_df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Main processing logic"""
        pass
    
    def execute(self, bulk_df: pd.DataFrame, template_df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Execute complete optimization flow"""
        
        # 1. Validate
        if not self.validate(bulk_df, template_df):
            raise ValidationError(f"Validation failed: {self.errors}")
        
        # 2. Clean
        cleaned_df = self.clean(bulk_df)
        
        # 3. Process
        result = self.process(cleaned_df, template_df)
        
        # 4. Post-process
        result = self.post_process(result)
        
        return result
    
    def post_process(self, result: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """Common post-processing for all optimizations"""
        
        # Set Operation to Update
        for sheet_name, df in result.items():
            df['Operation'] = 'Update'
        
        return result
```

## 3. Required Methods Implementation

### File Requirements
```python
def get_required_files(self) -> Dict[str, bool]:
    """
    Returns dictionary of required files
    
    Example:
    {
        'template': True,      # Always required
        'bulk_7': False,       # Not required
        'bulk_30': True,       # Required
        'bulk_60': False,      # Not required
        'data_rova': False     # Not required
    }
    """
    return {
        'template': True,
        'any_bulk': True  # At least one bulk file
    }
```

### Validation Method
```python
def validate(self, bulk_df: pd.DataFrame, template_df: pd.DataFrame) -> bool:
    """
    Validate data for optimization
    
    Should check:
    - Required columns exist
    - Data types are correct
    - Business rules are met
    - Portfolios match (if needed)
    
    Returns:
        bool: True if valid, False otherwise
        
    Side effects:
        - Populates self.errors list
        - Populates self.warnings list
    """
    
    is_valid = True
    
    # Example validation
    if 'Required Column' not in bulk_df.columns:
        self.errors.append("Missing required column")
        is_valid = False
    
    return is_valid
```

### Cleaning Method
```python
def clean(self, bulk_df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and filter data
    
    Should:
    - Filter rows based on optimization criteria
    - Remove invalid data
    - Handle missing values
    
    Returns:
        pd.DataFrame: Cleaned dataframe
    """
    
    # Example cleaning
    cleaned = bulk_df.copy()
    
    # Filter by entity types
    cleaned = cleaned[cleaned['Entity'].isin(self.get_valid_entities())]
    
    # Filter by state
    cleaned = cleaned[cleaned['State'] == 'enabled']
    
    return cleaned
```

### Processing Method
```python
def process(self, bulk_df: pd.DataFrame, template_df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Main processing logic
    
    Should:
    - Apply optimization logic
    - Calculate new values
    - Create output structure
    
    Returns:
        Dict[str, pd.DataFrame]: Dictionary of sheet names to dataframes
    """
    
    result = {}
    
    # Optimization-specific logic here
    
    return result
```

## 4. Helper Methods

### Common Utilities
```python
class BaseOptimization(ABC):
    
    def get_portfolio_settings(self, portfolio_name: str, template_df: pd.DataFrame) -> dict:
        """Get settings for a specific portfolio from template"""
        
        row = template_df[template_df['Portfolio Name'] == portfolio_name]
        
        if row.empty:
            return None
        
        return {
            'base_bid': row.iloc[0]['Base Bid'],
            'target_cpa': row.iloc[0].get('Target CPA', None)
        }
    
    def mark_error_rows(self, df: pd.DataFrame) -> pd.DataFrame:
        """Mark rows with errors for highlighting"""
        
        df['has_error'] = False
        
        # Common error conditions
        if 'Bid' in df.columns:
            df.loc[df['Bid'] < 0.02, 'has_error'] = True
            df.loc[df['Bid'] > 1.25, 'has_error'] = True
            df.loc[df['Bid'].isna(), 'has_error'] = True
        
        return df
    
    def calculate_stats(self, df: pd.DataFrame) -> dict:
        """Calculate common statistics"""
        
        stats = {
            'total_rows': len(df),
            'rows_with_errors': df['has_error'].sum() if 'has_error' in df.columns else 0
        }
        
        return stats
```

## 5. Error Handling

### Error Collection
```python
class BaseOptimization(ABC):
    
    def add_error(self, message: str):
        """Add error message"""
        self.errors.append(message)
    
    def add_warning(self, message: str):
        """Add warning message"""
        self.warnings.append(message)
    
    def has_errors(self) -> bool:
        """Check if there are any errors"""
        return len(self.errors) > 0
    
    def get_error_summary(self) -> str:
        """Get summary of all errors"""
        if not self.errors:
            return "No errors"
        return "; ".join(self.errors)
```

## 6. Implementation Example - Zero Sales

```python
class ZeroSalesOptimization(BaseOptimization):
    
    def __init__(self):
        super().__init__("Zero Sales")
        self.flat_portfolios = [
            'Flat 30', 'Flat 25', 'Flat 40',
            'Flat 25 | Opt', 'Flat 30 | Opt',
            'Flat 20', 'Flat 15', 'Flat 40 | Opt',
            'Flat 20 | Opt', 'Flat 15 | Opt'
        ]
    
    def get_required_files(self) -> Dict[str, bool]:
        return {
            'template': True,
            'any_bulk': True
        }
    
    def validate(self, bulk_df: pd.DataFrame, template_df: pd.DataFrame) -> bool:
        is_valid = True
        
        # Check required columns
        required_cols = ['Units', 'Clicks', 'Entity', 'Portfolio Name (Informational only)']
        for col in required_cols:
            if col not in bulk_df.columns:
                self.add_error(f"Missing required column: {col}")
                is_valid = False
        
        # Check portfolios
        bulk_portfolios = set(bulk_df['Portfolio Name (Informational only)'].unique())
        template_portfolios = set(template_df['Portfolio Name'].unique())
        
        missing = bulk_portfolios - template_portfolios - set(self.flat_portfolios)
        if missing:
            self.add_error(f"Missing portfolios in template: {missing}")
            is_valid = False
        
        return is_valid
    
    def clean(self, bulk_df: pd.DataFrame) -> pd.DataFrame:
        # Filter Units = 0
        cleaned = bulk_df[bulk_df['Units'] == 0].copy()
        
        # Remove Flat portfolios
        cleaned = cleaned[
            ~cleaned['Portfolio Name (Informational only)'].isin(self.flat_portfolios)
        ]
        
        # Filter entities
        valid_entities = ['Keyword', 'Product Targeting', 'Product Ad', 'Bidding Adjustment']
        cleaned = cleaned[cleaned['Entity'].isin(valid_entities)]
        
        return cleaned
    
    def process(self, bulk_df: pd.DataFrame, template_df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        # Split by entity
        keywords_pt = bulk_df[bulk_df['Entity'].isin(['Keyword', 'Product Targeting'])].copy()
        bidding_adj = bulk_df[bulk_df['Entity'] == 'Bidding Adjustment'].copy()
        product_ad = bulk_df[bulk_df['Entity'] == 'Product Ad'].copy()
        
        # Add helper columns and calculate bids for keywords_pt
        keywords_pt = self.add_helper_columns(keywords_pt, template_df)
        keywords_pt = self.calculate_new_bids(keywords_pt)
        
        return {
            'Clean Zero Sales': keywords_pt,
            'Bidding Adjustment Zero Sales': bidding_adj,
            'Product Ad Zero Sales': product_ad
        }
```

## 7. Registration System

### Optimization Registry
```python
class OptimizationRegistry:
    """Registry for all available optimizations"""
    
    _optimizations = {}
    
    @classmethod
    def register(cls, name: str, optimization_class):
        """Register an optimization"""
        cls._optimizations[name] = optimization_class
    
    @classmethod
    def get(cls, name: str) -> BaseOptimization:
        """Get an optimization instance"""
        if name not in cls._optimizations:
            raise ValueError(f"Unknown optimization: {name}")
        
        return cls._optimizations[name]()
    
    @classmethod
    def list_available(cls) -> List[str]:
        """List all available optimizations"""
        return list(cls._optimizations.keys())

# Registration
OptimizationRegistry.register('zero_sales', ZeroSalesOptimization)
# Future: OptimizationRegistry.register('portfolio_bid', PortfolioBidOptimization)
```

## 8. Batch Processing

### Processing Multiple Optimizations
```python
def process_selected_optimizations(
    selected: List[str],
    bulk_df: pd.DataFrame,
    template_df: pd.DataFrame
) -> Dict[str, Dict[str, pd.DataFrame]]:
    """Process multiple optimizations"""
    
    results = {}
    
    for opt_name in selected:
        try:
            # Get optimization instance
            optimization = OptimizationRegistry.get(opt_name)
            
            # Execute
            result = optimization.execute(bulk_df, template_df)
            
            # Store result
            results[opt_name] = result
            
            # Log success
            st.success(f"Completed {opt_name} optimization")
            
        except Exception as e:
            st.error(f"Failed {opt_name}: {str(e)}")
            continue
    
    return results
```

## 9. Future Extensions

### Advanced Features (TBD)
```python
class BaseOptimization(ABC):
    
    # Future: Configuration support
    def get_config(self) -> dict:
        """Get optimization configuration"""
        pass
    
    # Future: Parallel processing
    def can_parallelize(self) -> bool:
        """Check if optimization can be parallelized"""
        return False
    
    # Future: Caching
    def get_cache_key(self, bulk_df, template_df) -> str:
        """Generate cache key for results"""
        pass
```

## 10. Testing Base Class

### Test Framework
```python
class BaseOptimizationTest:
    """Base test class for optimizations"""
    
    def test_required_files(self, optimization):
        """Test that required files are defined"""
        required = optimization.get_required_files()
        assert 'template' in required
        assert isinstance(required['template'], bool)
    
    def test_validate_with_missing_columns(self, optimization):
        """Test validation with missing columns"""
        bulk_df = pd.DataFrame()
        template_df = pd.DataFrame()
        
        result = optimization.validate(bulk_df, template_df)
        assert result is False
        assert len(optimization.errors) > 0
    
    def test_clean_removes_invalid_rows(self, optimization):
        """Test that cleaning removes invalid rows"""
        # Test implementation specific to each optimization
        pass
```