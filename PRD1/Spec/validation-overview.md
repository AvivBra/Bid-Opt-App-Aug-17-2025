# סקירת מערכת הולידציה - Bid Optimizer

## 1. עקרונות הולידציה

### גישה מבוזרת
- אין ולידציה גלובלית מרכזית
- כל אופטימיזציה מבצעת ולידציה עצמאית
- כל אופטימיזציה בודקת רק את הקבצים שהיא צריכה
- אופטימיזציה שלא עוברת ולידציה פשוט לא רצה

### ולידציה דו-שלבית
1. **ולידציה בסיסית** - מבנה קבצים, גודל, פורמט
2. **ולידציה ספציפית** - לוגיקה עסקית של האופטימיזציה

## 2. ולידציות בסיסיות (לכל הקבצים)

### בדיקות מבנה
- פורמט קובץ: .xlsx או .csv
- גודל: עד 40MB
- קריאות: הקובץ נפתח ללא שגיאות
- תוכן: יש נתונים (לא ריק)

### בדיקות ספציפיות לסוג קובץ
- **Template**: 2 לשוניות (Port Values, Top ASINs)
- **Bulk Files**: לשונית "Sponsored Products Campaigns" עם 48 עמודות
- **Data Rova**: מבנה ספציפי (יוגדר בהמשך)

## 3. זרימת ולידציה

```
User selects optimizations
↓
For each selected optimization:
    ↓
    1. Check required files exist
    ↓
    2. Run optimization.validate()
    ↓
    3. Store validation result
    ↓
    4. Update UI with status
```

## 4. תוצאות ולידציה

### מבנה ValidationResult
```python
{
    'optimization_name': str,
    'is_valid': bool,
    'errors': List[str],
    'warnings': List[str],
    'missing_files': List[str],
    'can_process': bool
}
```

### סטטוסים אפשריים
- ✅ **Ready** - ולידציה עברה, ניתן לעבד
- ❌ **Blocked** - חסרים קבצים או שגיאות קריטיות
- ⚠️ **Warning** - יש אזהרות אך ניתן להמשיך

## 5. הצגה ב-UI

### הודעות לכל אופטימיזציה
```
Zero Sales: ✅ Ready to process
Portfolio Bid: ❌ Missing Bulk 30 file
Budget Optimization: ⚠️ Some portfolios will be ignored
```

### כפתור Process
- **פעיל** - אם יש לפחות אופטימיזציה אחת מוכנה
- **מושבת** - אם אף אופטימיזציה לא מוכנה

## 6. ולידציות ספציפיות לאופטימיזציה

### כל אופטימיזציה מגדירה
- אילו קבצים היא דורשת
- אילו עמודות חייבות להיות
- אילו ערכים תקינים
- בדיקות לוגיות ספציפיות

### דוגמה - Zero Sales
```python
def validate(self, files):
    # בדיקת קבצים
    if 'template' not in files:
        return ValidationResult(is_valid=False, 
                              errors=['Template required'])
    
    if 'bulk_60' not in files:
        return ValidationResult(is_valid=False,
                              errors=['Bulk 60 required'])
    
    # בדיקת פורטפוליוז
    missing = self.check_portfolios(files)
    if missing:
        return ValidationResult(is_valid=False,
                              errors=[f'Missing portfolios: {missing}'])
    
    return ValidationResult(is_valid=True)
```

## 7. טיפול בשגיאות

### עקרונות
- הודעות ברורות ומדויקות
- ציון מה חסר או לא תקין
- הנחיות איך לתקן
- אפשרות להעלות קובץ מתוקן

### סוגי שגיאות
- **קובץ חסר** - "Bulk 60 file is required for Zero Sales"
- **מבנה שגוי** - "Template must have 'Port Values' sheet"
- **נתונים חסרים** - "Missing portfolios: ABC, DEF"
- **ערכים לא תקינים** - "Invalid Base Bid in row 5"