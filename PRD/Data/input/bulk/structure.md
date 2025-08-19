# מבנה קבצי Bulk

## סקירה כללית

קבצי Bulk הם קבצי הנתונים המגיעים מ-Amazon Ads עם מידע על קמפיינים, ביצועים ומטריקות.

## מאפיינים טכניים

### פורמט קובץ
- **סוג:** Excel (.xlsx) או CSV
- **שם Sheet נדרש:** "Sponsored Products Campaigns"
- **גודל קובץ:** עד 40MB
- **מספר שורות:** עד 500,000
- **מספר עמודות:** בדיוק 48

## סוגי Bulk Files

### Bulk 60 Days (פעיל)
- **תיאור:** נתוני 60 ימים אחרונים
- **שימוש:** Zero Sales Optimization
- **סטטוס:** פעיל

### Bulk 30 Days (TBC)
- **סטטוס:** לא פעיל - לפיתוח עתידי

### Bulk 7 Days (TBC)
- **סטטוס:** לא פעיל - לפיתוח עתידי

## מבנה 48 העמודות (בסדר מדויק)

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

## 9 עמודות Informational

עמודות שלא משתתפות בחישובים (לקריאה בלבד):
- עמודה 12: Campaign Name (Informational only)
- עמודה 13: Ad Group Name (Informational only)
- עמודה 14: Portfolio Name (Informational only)
- עמודה 19: Campaign State (Informational only)
- עמודה 20: Ad Group State (Informational only)
- עמודה 24: Eligibility Status (Informational only)
- עמודה 25: Reason for Ineligibility (Informational only)
- עמודה 27: Ad Group Default Bid (Informational only)
- עמודה 37: Resolved Product Targeting Expression (Informational only)

## הערות חשובות

- **סדר קבוע:** אסור לשנות את סדר העמודות
- **Case Sensitive:** כל ההשוואות רגישות לאותיות
- **ערכים ריקים:** עמודות מספריות יכולות להיות ריקות או 0

---

**עדכון אחרון:** 18 באוגוסט 2025, 20:00