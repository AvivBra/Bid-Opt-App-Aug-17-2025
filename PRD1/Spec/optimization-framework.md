# Framework לאופטימיזציות - Bid Optimizer

## 1. סקירה כללית

### מטרה
להגדיר מבנה אחיד לכל האופטימיזציות באפליקציה, כך שכל אופטימיזציה תהיה מודול עצמאי עם ממשק ברור.

### עקרונות
- כל אופטימיזציה יורשת ממחלקת בסיס
- כל אופטימיזציה מגדירה את הקבצים שהיא דורשת
- כל אופטימיזציה מבצעת ולידציה וניקוי עצמאיים
- כל אופטימיזציה מחזירה תוצאות בפורמט אחיד

## 2. מחלקת הבסיס

### BaseOptimization Class
```python
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple
import pandas as pd

class BaseOptimization(ABC):
    """מחלקת בסיס לכל האופטימיזציות"""
    
    # תכונות שכל אופטימיזציה חייבת להגדיר
    name: str = "Base Optimization"
    description: str = "Base optimization class"
    
    @property
    @abstractmethod
    def required_files(self) -> List[str]:
        """רשימת הקבצים הנדרשים לאופטימיזציה"""
        pass
    
    @abstractmethod
    def validate(self, files: Dict[str, pd.DataFrame]) -> ValidationResult:
        """ולידציה של הקבצים והנתונים"""
        pass
    
    @abstractmethod
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """ניקוי הנתונים הספציפי לאופטימיזציה"""
        pass
    
    @abstractmethod
    def process(self, files: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """ביצוע האופטימיזציה"""
        pass
```

## 3. ValidationResult Model

### מבנה תוצאת ולידציה
```python
@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    missing_files: List[str]
    invalid_data: Dict[str, List[str]]
    stats: Dict[str, any]
```

### דוגמה לתוצאה
```python
ValidationResult(
    is_valid=False,
    errors=["Missing portfolio: Port_ABC"],
    warnings=["5 rows have bid > 1.25"],
    missing_files=["bulk_60"],
    invalid_data={"template": ["Invalid Base Bid in row 5"]},
    stats={"total_rows": 1234, "valid_rows": 1200}
)
```

## 4. מבנה תיקיית אופטימיזציה

### מבנה סטנדרטי
```
optimization_name/
├── __init__.py
├── validator.py    # ValidationLogic class
├── cleaner.py     # DataCleaner class
└── processor.py   # OptimizationProcessor class
```

### תוכן __init__.py
```python
from .validator import ValidationLogic
from .cleaner import DataCleaner
from .processor import OptimizationProcessor

class OptimizationName(BaseOptimization):
    name = "Optimization Name"
    description = "Description of what this optimization does"
    
    def __init__(self):
        self.validator = ValidationLogic()
        self.cleaner = DataCleaner()
        self.processor = OptimizationProcessor()
    
    @property
    def required_files(self):
        return ["template", "bulk_60"]
    
    def validate(self, files):
        return self.validator.validate(files)
    
    def clean(self, df):
        return self.cleaner.clean(df)
    
    def process(self, files):
        return self.processor.process(files)
```

## 5. Validator Component

### תפקיד
- בדיקת קיום הקבצים הנדרשים
- בדיקת מבנה הקבצים
- בדיקת תקינות הנתונים
- בדיקות לוגיות ספציפיות

### דוגמה
```python
class ValidationLogic:
    def validate(self, files: Dict) -> ValidationResult:
        errors = []
        warnings = []
        
        # בדיקת קבצים
        if "bulk_60" not in files:
            errors.append("Bulk 60 file is required")
        
        # בדיקת נתונים
        if files.get("bulk_60") is not None:
            df = files["bulk_60"]
            if "Units" not in df.columns:
                errors.append("Units column missing")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
```

## 6. Cleaner Component

### תפקיד
- סינון שורות לא רלוונטיות
- ניקוי ערכים לא תקינים
- טיפול בערכים חסרים
- הכנת הנתונים לעיבוד

### דוגמה
```python
class DataCleaner:
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        # סינון לפי Entity
        df = df[df['Entity'].isin(['Keyword', 'Product Targeting'])]
        
        # סינון לפי State
        df = df[df['State'] == 'enabled']
        
        # ניקוי ערכים ריקים
        df = df.dropna(subset=['Bid'])
        
        return df
```

## 7. Processor Component

### תפקיד
- ביצוע הלוגיקה העסקית
- חישוב ערכים חדשים
- עדכון Bid values
- יצירת עמודות עזר

### דוגמה
```python
class OptimizationProcessor:
    def process(self, files: Dict) -> Dict[str, pd.DataFrame]:
        template_df = files['template']
        bulk_df = files['bulk_60']
        
        # ניקוי
        cleaned_df = self.cleaner.clean(bulk_df)
        
        # עיבוד
        processed_df = cleaned_df.copy()
        processed_df['Operation'] = 'Update'
        
        # לוגיקה ספציפית
        # ...
        
        return {
            'working': processed_df,
            'clean': processed_df[original_columns]
        }
```

## 8. רישום אופטימיזציה חדשה

### בקובץ orchestrator.py
```python
from optimizations.zero_sales import ZeroSales
from optimizations.portfolio_bid import PortfolioBid

AVAILABLE_OPTIMIZATIONS = {
    'zero_sales': ZeroSales,
    'portfolio_bid': PortfolioBid,
    # הוספת אופטימיזציות חדשות כאן
}
```

## 9. זרימת עבודה של אופטימיזציה

### שלבים
1. **בדיקת קבצים** - האם כל הקבצים הנדרשים קיימים?
2. **ולידציה** - האם הנתונים תקינים?
3. **ניקוי** - הכנת הנתונים לעיבוד
4. **עיבוד** - ביצוע האופטימיזציה
5. **החזרת תוצאות** - DataFrames מעובדים

### טיפול בשגיאות
```python
try:
    result = optimization.process(files)
except Exception as e:
    return {
        'error': str(e),
        'optimization': optimization.name
    }
```

## 10. דוגמה מלאה - Zero Sales

### required_files
```python
["template", "bulk_60"]
```

### validate
- בודק שקיים template
- בודק שקיים bulk_60
- בודק שיש עמודת Units
- בודק התאמת פורטפוליוז

### clean
- משאיר רק Entity = Keyword/Product Targeting
- משאיר רק State = enabled
- מסנן Units = 0

### process
- מחשב Bid חדש לפי נוסחאות
- מוסיף עמודות עזר
- מעדכן Operation = Update

## 11. בדיקות נדרשות

### Unit Tests
```python
def test_required_files():
    opt = ZeroSales()
    assert "bulk_60" in opt.required_files

def test_validation():
    opt = ZeroSales()
    result = opt.validate({})
    assert not result.is_valid

def test_processing():
    opt = ZeroSales()
    result = opt.process(test_files)
    assert 'working' in result
```

## 12. הרחבה עתידית

### הוספת אופטימיזציה חדשה
1. יצירת תיקייה חדשה תחת optimizations/
2. יישום 4 הקבצים הנדרשים
3. רישום ב-orchestrator
4. כתיבת בדיקות
5. עדכון UI עם השם החדש