# איפיון מבני קבצים - Bid Optimizer

## 1. Template File

### מבנה כללי
- **פורמט:** Excel (.xlsx) או CSV
- **גודל מקסימלי:** 1MB (קובץ קטן)
- **מספר לשוניות:** 2
- **קידוד:** UTF-8

### לשונית 1: Port Values
| עמודה | סוג | חובה | ערכים תקינים |
|--------|-----|------|---------------|
| Portfolio Name | String | כן | כל טקסט, ייחודי |
| Base Bid | Number/String | כן | 0.00-4 או "Ignore" |
| Target CPA | Number | לא | 0.00-4 או ריק |

#### דוגמה
```
Portfolio Name    | Base Bid | Target CPA
-----------------|----------|------------
Kids-Brand-US    | 1.25     | 5.00
Kids-Brand-EU    | 0.95     | 
Supplements-US   | Ignore   | 
Supplements-EU   | 2.10     | 8.50
```

### לשונית 2: Top ASINs
| עמודה | סוג | חובה | שימוש |
|--------|-----|------|--------|
| ASIN | String | לא | לשימוש עתידי באופטימיזציות |

#### דוגמה
```
ASIN
-----------
B001234567
B002345678
B003456789
```

**הערה:** לשונית Top ASINs לא בשימוש ב-Zero Sales, נשמרת לאופטימיזציות עתידיות.

## 2. Bulk Files

### מבנה כללי (זהה לכל סוגי ה-Bulk)
- **פורמט:** Excel (.xlsx) או CSV
- **גודל מקסימלי:** 40MB
- **מספר שורות מקסימלי:** 500,000
- **Sheet נדרש:** "Sponsored Products Campaigns"
- **מספר עמודות:** בדיוק 48
- **קידוד:** UTF-8

### סוגי Bulk Files
| סוג | תיאור | טווח נתונים | שימוש |
|-----|--------|-------------|--------|
| Bulk 7 | נתוני 7 ימים אחרונים | 7 days | TBD - אופטימיזציות עתידיות |
| Bulk 30 | נתוני 30 ימים אחרונים | 30 days | Zero Sales ואחרות |
| Bulk 60 | נתוני 60 ימים אחרונים | 60 days | TBD - אופטימיזציות עתידיות |

### 48 העמודות (בסדר מדויק)
```
1. Product
2. Entity
3. Operation
4. Campaign ID
5. Ad Group ID
6. Portfolio ID
7. Ad ID
8. Keyword ID
9. Product Targeting ID
10. Campaign Name
11. Ad Group Name
12. Campaign Name (Informational only)
13. Ad Group Name (Informational only)
14. Portfolio Name (Informational only)
15. Start Date
16. End Date
17. Targeting Type
18. State
19. Campaign State (Informational only)
20. Ad Group State (Informational only)
21. Daily Budget
22. SKU
23. ASIN
24. Eligibility Status (Informational only)
25. Reason for Ineligibility (Informational only)
26. Ad Group Default Bid
27. Ad Group Default Bid (Informational only)
28. Bid
29. Keyword Text
30. Native Language Keyword
31. Native Language Locale
32. Match Type
33. Bidding Strategy
34. Placement
35. Percentage
36. Product Targeting Expression
37. Resolved Product Targeting Expression (Informational only)
38. Impressions
39. Clicks
40. Click-through Rate
41. Spend
42. Sales
43. Orders
44. Units
45. Conversion Rate
46. ACOS
47. CPC
48. ROAS
```

### Entity Types
| ערך | תיאור | נכלל ב-Zero Sales |
|-----|-------|-------------------|
| Keyword | מילות מפתח | ✓ |
| Product Targeting | מיקוד מוצרים | ✓ |
| Product Ad | מודעות מוצר | ✓ |
| Bidding Adjustment | התאמות הצעות מחיר | ✓ |
| Campaign | קמפיין | ✗ |
| Ad Group | קבוצת מודעות | ✗ |

## 3. Data Rova File

### מבנה
- **פורמט:** TBD
- **תוכן:** נתוני benchmarking
- **שימוש:** אופטימיזציות עתידיות

**הערה:** איפיון מלא יתווסף בעתיד

## 4. Output Files

### Working File
- **פורמט:** Excel (.xlsx)
- **שם קובץ:** `Working_File_YYYY-MM-DD_HH-MM.xlsx`
- **מספר sheets:** תלוי באופטימיזציות שנבחרו

#### Sheets ל-Zero Sales
| Sheet Name | תוכן | עמודות עזר |
|-----------|------|------------|
| Clean Zero Sales | Keywords + Product Targeting | כן |
| Bidding Adjustment Zero Sales | Bidding Adjustments | לא |
| Product Ad Zero Sales | Product Ads | לא |

### Clean File
- **פורמט:** Excel (.xlsx)
- **שם קובץ:** `Clean_File_YYYY-MM-DD_HH-MM.xlsx`
- **מספר sheets:** תלוי באופטימיזציות שנבחרו

**הערה:** כרגע זהה ל-Working File. בעתיד Clean לא יכלול עמודות עזר.

## 5. עמודות עזר (Helper Columns)

### מיקום
נוספות משמאל לעמודה Bid (עמודה 28)

### רשימת עמודות עזר
| עמודה | תיאור | נוסחה/מקור |
|--------|-------|------------|
| Old Bid | ערך Bid מקורי | =Bid |
| calc1 | חישוב ביניים | תלוי במקרה |
| calc2 | חישוב ביניים | תלוי במקרה |
| Target CPA | מה-Template | VLOOKUP מ-Template |
| Base Bid | מה-Template | VLOOKUP מ-Template |
| Adj. CPA | CPA מותאם | =Target CPA × (1 + Max BA/100) |
| Max BA | אחוז מקסימלי | MAX של Percentage לקמפיין |

## 6. פורמטים של נתונים

### מספרים
| סוג | פורמט | דוגמה |
|-----|--------|--------|
| IDs | טקסט | "1234567890" |
| Bid | 3 ספרות אחרי הנקודה | 1.250 |
| Budget | 2 ספרות אחרי הנקודה | 25.00 |
| Percentage | מספר שלם | 50 (= 50%) |

### תאריכים
- **פורמט:** MM/DD/YYYY
- **דוגמה:** 01/15/2024

### טקסט
- **קידוד:** UTF-8
- **Case sensitive:** כן
- **תווים מיוחדים:** נתמכים

## 7. קבצים מיוחדים

### Flat Portfolios
רשימת portfolios שלא נכללים באופטימיזציות:
```
Flat 30
Flat 25
Flat 40
Flat 25 | Opt
Flat 30 | Opt
Flat 20
Flat 15
Flat 40 | Opt
Flat 20 | Opt
Flat 15 | Opt
```

## 8. שינויי Operation

### לפני עיבוד
```
Operation: Create / Update / Delete (מעורב)
```

### אחרי עיבוד
```
Operation: Update (כל השורות)
```

## 9. מגבלות וביצועים

### מגבלות גודל
| פרמטר | מגבלה | הערה |
|--------|-------|-------|
| גודל קובץ | 40MB | חל על כל קובץ |
| מספר שורות | 500,000 | ל-Bulk file |
| מספר portfolios | 1,000 | ל-Template |
| אורך טקסט | 255 תווים | לכל תא |

### זמני קריאה צפויים
| גודל | זמן קריאה |
|------|-----------|
| 5MB | 2-3 שניות |
| 10MB | 5-7 שניות |
| 20MB | 10-15 שניות |
| 40MB | 20-30 שניות |

## 10. Validation של קבצים

### בדיקות Template
```python
def validate_template(df):
    # לשונית Port Values
    if 'Portfolio Name' not in df.columns:
        return "Missing Portfolio Name column"
    
    if df['Portfolio Name'].duplicated().any():
        return "Duplicate portfolio names found"
    
    # Base Bid validation
    invalid_bids = df[
        (df['Base Bid'] != 'Ignore') & 
        ((df['Base Bid'] < 0) | (df['Base Bid'] > 4))
    ]
    if len(invalid_bids) > 0:
        return "Invalid Base Bid values"
```

### בדיקות Bulk
```python
def validate_bulk(df):
    if len(df.columns) != 48:
        return f"Expected 48 columns, found {len(df.columns)}"
    
    if len(df) > 500000:
        return f"File has {len(df)} rows, maximum is 500,000"
    
    if len(df) == 0:
        return "File is empty"
```