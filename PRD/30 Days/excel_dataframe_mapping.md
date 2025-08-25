# Excel-DataFrame Mapping
**תאריך: 17/08/2025 12:15**

## לשונית: Targeting

### עמודות לפי סדר הופעה (58 עמודות):

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
28. **Max BA** *(עמודת עזר חדשה)*
29. **Base Bid** *(עמודת עזר חדשה)*
30. **Target CPA** *(עמודת עזר חדשה)*
31. **Adj. CPA** *(עמודת עזר חדשה)*
32. **Old Bid** *(עמודת עזר חדשה)*
33. **Temp Bid** *(עמודת עזר חדשה)*
34. Bid
35. **Max_Bid** *(עמודת עזר חדשה)*
36. **calc3** *(עמודת עזר חדשה)*
37. **calc2** *(עמודת עזר חדשה)*
38. **calc1** *(עמודת עזר חדשה)*
39. Keyword Text
40. Native Language Keyword
41. Native Language Locale
42. Match Type
43. Bidding Strategy
44. Placement
45. Percentage
46. Product Targeting Expression
47. Resolved Product Targeting Expression (Informational only)
48. Impressions
49. Clicks
50. Click-through Rate
51. Spend
52. Sales
53. Orders
54. Units
55. Conversion Rate
56. ACOS
57. CPC
58. ROAS

### הערות:
- **עמודות עזר חדשות (10):** Max BA, Base Bid, Target CPA, Adj. CPA, Old Bid, Temp Bid, Max_Bid, calc3, calc2, calc1
- **עמודות מקוריות מהבאלק:** 48 עמודות
- **סה"כ:** 58 עמודות בלשונית Targeting

### מיפוי DataFrame:
```python
column_mapping = {
    # Original columns (1-48)
    'product': 'Product',
    'entity': 'Entity', 
    'operation': 'Operation',
    'campaign_id': 'Campaign ID',
    'ad_group_id': 'Ad Group ID',
    'portfolio_id': 'Portfolio ID',
    'campaign_name': 'Campaign Name (Informational only)',
    'portfolio': 'Portfolio Name (Informational only)',
    'state': 'State',
    'campaign_state': 'Campaign State (Informational only)',
    'ad_group_state': 'Ad Group State (Informational only)',
    'bid': 'Bid',
    'match_type': 'Match Type',
    'percentage': 'Percentage',
    'product_targeting_expression': 'Product Targeting Expression',
    'clicks': 'Clicks',
    'units': 'Units',
    'conversion_rate': 'Conversion Rate',
    
    # Helper columns (added during processing)
    'max_ba': 'Max BA',
    'base_bid': 'Base Bid',
    'target_cpa': 'Target CPA',
    'adj_cpa': 'Adj. CPA',
    'old_bid': 'Old Bid',
    'temp_bid': 'Temp Bid',
    'max_bid': 'Max_Bid',
    'calc3': 'calc3',
    'calc2': 'calc2',
    'calc1': 'calc1'
}
```

---

## לשונית: Bidding Adjustment

### עמודות לפי סדר הופעה (48 עמודות מקוריות בלבד):

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

### הערות:
- **ללא עמודות עזר** - רק העמודות המקוריות מהבאלק
- **Entity = "Bidding Adjustment"** עבור כל השורות בלשונית זו
- **Operation = "Update"** עבור כל השורות
- **ללא צביעה בוורוד** בלשונית זו (גם אם יש שגיאות)

---

## לשונית: For Harvesting

### עמודות לפי סדר הופעה (58 עמודות - זהה ל-Targeting):
זהה בדיוק ללשונית Targeting מבחינת מבנה העמודות

### הערות:
- **מכיל שורות עם Target CPA = NULL**
- **שורות אלו מועברות מלשונית Targeting**
- **כולל כל עמודות העזר**

---

## טיפוסי נתונים לעמודות קריטיות

### עמודות מספריות (float):
```python
numeric_columns = {
    'Bid': float,  # 0.02 - 4.00, 3 decimal places
    'Old Bid': float,  # Copy of original Bid
    'Base Bid': float,  # From template, 0.02 - 4.00
    'Target CPA': float,  # From template, nullable
    'Adj. CPA': float,  # Calculated: Target CPA / (1 + Max BA/100)
    'Max BA': float,  # Max Percentage per Campaign ID
    'Percentage': float,  # From bulk data
    'Clicks': float,  # Convert to numeric, default 0
    'Units': float,  # Convert to numeric, must be > 0 for Bids 30
    'Conversion Rate': float,  # Percentage as decimal
    'Temp Bid': float,  # Intermediate calculation
    'Max_Bid': float,  # 0.8 or 1.25 based on units
    'calc1': float,  # Intermediate calculation
    'calc2': float,  # Intermediate calculation  
    'calc3': float,  # Temp_Bid - Max_Bid
    'Impressions': float,
    'Spend': float,
    'Sales': float,
    'Orders': float,
    'ACOS': float,
    'CPC': float,
    'ROAS': float
}
```

### עמודות טקסט (string):
```python
string_columns = {
    'Entity': str,  # "Keyword", "Product Targeting", "Bidding Adjustment"
    'Operation': str,  # Always "Update" in output
    'Portfolio Name (Informational only)': str,
    'Campaign Name (Informational only)': str,  # Check for "up and"
    'State': str,  # "enabled", "paused", "archived"
    'Campaign State (Informational only)': str,  # "enabled"
    'Ad Group State (Informational only)': str,  # "enabled"
    'Match Type': str,  # "Exact", "Phrase", "Broad"
    'Product Targeting Expression': str,  # Check for "asin=B0"
    'Keyword Text': str,
    'Placement': str,
    'Bidding Strategy': str
}
```

### עמודות ID (string - למרות שנראות כמספרים):
```python
id_columns = {
    'Campaign ID': str,  # Format as text to prevent scientific notation
    'Ad Group ID': str,
    'Portfolio ID': str,
    'Ad ID': str,
    'Keyword ID': str,
    'Product Targeting ID': str
}
```

### המרות קריטיות:
- **IDs**: נשמרים כ-string עם number_format = "@" באקסל
- **Bid values**: מעוגלים ל-3 ספרות אחרי הנקודה
- **Percentage/Conversion Rate**: כאחוזים (0-100)
- **NULL handling**: pd.isna() לבדיקה, np.nan לערכים ריקים