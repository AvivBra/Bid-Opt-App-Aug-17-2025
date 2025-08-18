# מפרט קלט/פלט - Bid Optimizer

## 1. סקירת קבצי קלט

### 5 סוגי קבצים
| קובץ | תיאור | חובה | פורמט |
|------|--------|-------|--------|
| Template | הגדרות פורטפוליו | תלוי באופטימיזציה | Excel/CSV |
| Bulk 30 | נתוני 30 ימים | תלוי באופטימיזציה | Excel/CSV |
| Bulk 60 | נתוני 60 ימים | תלוי באופטימיזציה | Excel/CSV |
| Bulk 7 | נתוני 7 ימים | תלוי באופטימיזציה | Excel/CSV |
| Data Rova | נתוני רווחיות | תלוי באופטימיזציה | Excel/CSV |

### מגבלות כלליות
- גודל מקסימלי: 40MB לקובץ
- מספר שורות מקסימלי: 500,000
- קידוד: UTF-8

## 2. Template File

### מבנה
- פורמט: Excel (.xlsx) או CSV
- מספר לשוניות: 2

### לשונית 1: Port Values
| # | שם עמודה | סוג | חובה | ערכים תקינים |
|---|----------|-----|-------|---------------|
| 1 | Portfolio Name | String | כן | כל טקסט |
| 2 | Base Bid | Number/String | כן | 0.00-999.99 או "Ignore" |
| 3 | Target CPA | Number | לא | 0.00-9999.99 או ריק |

### לשונית 2: Top ASINs
| # | שם עמודה | סוג | חובה | ערכים תקינים |
|---|----------|-----|-------|---------------|
| 1 | ASIN | String | כן | ASIN תקני של Amazon |

### דוגמה - Port Values
```
Portfolio Name    | Base Bid | Target CPA
-----------------|----------|------------
Kids-Brand-US    | 1.25     | 5.00
Kids-Brand-EU    | 0.95     | 
Supplements-US   | Ignore   | 
Supplements-EU   | 2.10     | 8.50
```

### דוגמה - Top ASINs
```
ASIN
----------
B08N5WRWNW
B07XQXZXJC
B09MDHXV6B
```

## 3. Bulk Files (30/60/7)

### מבנה משותף
- פורמט: Excel (.xlsx) או CSV
- Sheet נדרש: "Sponsored Products Campaigns"
- 48 עמודות סטנדרטיות

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

### הבדלים בין Bulk Files
- **Bulk 30**: נתונים מ-30 הימים האחרונים
- **Bulk 60**: נתונים מ-60 הימים האחרונים
- **Bulk 7**: נתונים מ-7 הימים האחרונים
- המבנה זהה, רק טווח הזמן שונה

## 4. Data Rova File

### מבנה
- פורמט: Excel (.xlsx) או CSV
- פרטים מדויקים יסופקו בהמשך
- יכיל נתוני רווחיות ומרג'ינים

## 5. קבצי פלט

### 2 סוגי קבצים
1. **Working File** - כולל עמודות עזר לבדיקה
2. **Clean File** - רק נתונים נקיים לטעינה

### מבנה שמות
```
Auto Optimized Bulk | {Type} | {Date} | {Time}.xlsx

דוגמאות:
Auto Optimized Bulk | Working | 2024-01-15 | 14-30.xlsx
Auto Optimized Bulk | Clean | 2024-01-15 | 14-30.xlsx
```

### תוכן הקבצים
#### Working File
- לשונית לכל אופטימיזציה: "Working {OptimizationName}"
- כולל את כל 48 העמודות המקוריות
- עמודות עזר נוספות (תלוי באופטימיזציה)
- כל השורות עם Operation="Update"

#### Clean File
- לשונית לכל אופטימיזציה: "Clean {OptimizationName}"
- רק 48 העמודות המקוריות
- כל השורות עם Operation="Update"
- מוכן לטעינה חזרה ל-Amazon

### לשוניות נוספות
אם קיימות לשוניות נוספות בקבצי המקור (כגון "Portfolios"), הן יועתקו כמו שהן לקבצי הפלט.

## 6. פורמט נתונים

### מספרים
- IDs: נשמרים כטקסט למניעת scientific notation
- Bid: עד 3 ספרות אחרי הנקודה (0.000)
- Budget: עד 2 ספרות אחרי הנקודה (0.00)
- Percentages: כמספר עשרוני (0.15 = 15%)

### תאריכים
- פורמט: MM/DD/YYYY
- דוגמה: 01/15/2024

### טקסט
- קידוד: UTF-8
- תווים מיוחדים: נתמכים
- Case sensitive: כן

## 7. ולידציות בסיסיות

### בדיקות גודל
- קובץ > 40MB: נדחה מיידית
- קובץ > 500K שורות: נדחה

### בדיקות פורמט
- חייב להיות .xlsx או .csv
- חייב להיות קריא
- חייב להכיל נתונים (לא ריק)

### בדיקות ספציפיות
כל אופטימיזציה מבצעת ולידציות נוספות על הקבצים שלה - ראה מסמכי האופטימיזציות.