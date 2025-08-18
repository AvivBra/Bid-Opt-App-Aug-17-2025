# מפרט קבצי Bulk - Bid Optimizer

## 1. סקירה כללית

### 3 סוגי קבצי Bulk
1. **Bulk 30** - נתוני 30 ימים אחרונים
2. **Bulk 60** - נתוני 60 ימים אחרונים  
3. **Bulk 7** - נתוני 7 ימים אחרונים

### מאפיינים משותפים
- מבנה זהה לחלוטין (48 עמודות)
- אותו פורמט וסדר עמודות
- ההבדל היחיד: טווח הזמן של הנתונים

## 2. מבנה הקובץ

### דרישות בסיסיות
- פורמט: Excel (.xlsx) או CSV
- Sheet נדרש: "Sponsored Products Campaigns"
- מספר עמודות: 48 בדיוק
- סדר עמודות: קבוע וזהה לכל הקבצים
- קידוד: UTF-8

## 3. רשימת 48 העמודות

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

## 4. עמודות קריטיות לאופטימיזציות

### עמודות זיהוי
- **Entity** - סוג הפריט (Keyword, Product Targeting, etc.)
- **State** - סטטוס (enabled, paused, archived)
- **Portfolio Name (Informational only)** - שם הפורטפוליו

### עמודות ביצועים
- **Impressions** - חשיפות
- **Clicks** - קליקים
- **Sales** - מכירות
- **Units** - יחידות שנמכרו
- **Spend** - הוצאה

### עמודות ל-Bid
- **Bid** - ההצעה הנוכחית
- **Ad Group Default Bid** - ברירת מחדל

## 5. ערכי Entity אפשריים

```
- Keyword
- Product Targeting
- Product Ad
- Bidding Adjustment
- Campaign
- Ad Group
```

## 6. ערכי State אפשריים

```
- enabled
- paused
- archived
```

## 7. פורמט תאריכים

- פורמט: MM/DD/YYYY
- דוגמה: 01/15/2024
- Start Date/End Date: תאריכי הקמפיין

## 8. טווחי זמן

### Bulk 30
- נתונים מ-30 הימים האחרונים
- שימוש: אופטימיזציות לטווח בינוני

### Bulk 60
- נתונים מ-60 הימים האחרונים
- שימוש: Zero Sales ואופטימיזציות ארוכות טווח

### Bulk 7
- נתונים מ-7 הימים האחרונים
- שימוש: אופטימיזציות מהירות ותגובתיות

## 9. ולידציות

### בדיקות מבנה
- קיום Sheet "Sponsored Products Campaigns"
- 48 עמודות בדיוק
- סדר עמודות נכון
- שמות עמודות תואמים

### בדיקות נתונים
- IDs בפורמט נכון (לא scientific notation)
- ערכי Bid חיוביים
- תאריכים בפורמט תקין

## 10. שימוש באופטימיזציות

### Zero Sales
- דורש: Bulk 60
- משתמש בעמודות: Units, Clicks, Portfolio Name, Bid

### Portfolio Bid (עתידי)
- דורש: Bulk 30
- משתמש בעמודות: [יוגדר בהמשך]

### אופטימיזציות נוספות
- כל אחת תגדיר איזה Bulk היא צריכה

## 11. טיפול בקבצים גדולים

### מגבלות
- מקסימום 40MB
- מקסימום 500,000 שורות

### ביצועים
- קריאה: עד 5 שניות ל-100K שורות
- עיבוד: תלוי באופטימיזציה

## 12. לשוניות נוספות

אם קיימות לשוניות נוספות בקובץ (כגון "Portfolios"), הן יועתקו כמו שהן לקבצי הפלט ללא שינוי.