# מבנה קבצי Bulk

## סקירה כללית

קבצי Bulk הם קבצי הנתונים העיקריים המגיעים מ-Amazon Ads. הם מכילים את כל המידע על הקמפיינים, ביצועים ומטריקות לתקופה מוגדרת.

## מאפיינים טכניים

### פורמט קובץ
- **סוג:** Excel (.xlsx) או CSV
- **קידוד:** UTF-8
- **שם Sheet נדרש:** "Sponsored Products Campaigns"
- **מספר Sheets:** 1 (רק השני הראשון נקרא)

### מגבלות גודל
| פרמטר | מגבלה | הערה |
|--------|-------|-------|
| גודל קובץ | 40MB | מקסימום מוחלט |
| מספר שורות | 500,000 | כולל כותרת |
| מספר עמודות | 48 | בדיוק, לא פחות ולא יותר |
| אורך תא | 255 תווים | לכל תא בודד |

## סוגי Bulk Files

### Bulk 7 Days
- **תיאור:** נתוני 7 ימים אחרונים
- **שימוש:** TBC - אופטימיזציות עתידיות
- **סטטוס:** לא בשימוש כרגע

### Bulk 30 Days
- **תיאור:** נתוני 30 ימים אחרונים
- **שימוש:** TBC - אופטימיזציות עתידיות
- **סטטוס:** לא בשימוש כרגע

### Bulk 60 Days
- **תיאור:** נתוני 60 ימים אחרונים
- **שימוש:** Zero Sales Optimization
- **סטטוס:** **בשימוש פעיל**

## מבנה העמודות

### 48 עמודות חובה (בסדר מדויק)

#### קבוצה א': מזהים (1-10)
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

#### קבוצה ב': שמות ומצבים (11-20)
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

#### קבוצה ג': הגדרות (21-30)
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

#### קבוצה ד': מיקוד ואסטרטגיה (31-37)
31. Native Language Locale
32. Match Type
33. Bidding Strategy
34. Placement
35. Percentage
36. Product Targeting Expression
37. Resolved Product Targeting Expression (Informational only)

#### קבוצה ה': מטריקות ביצועים (38-48)
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

## דוגמה למבנה נתונים

### שורה טיפוסית - Keyword
```
Product: Sponsored Products
Entity: Keyword
Operation: Update
Campaign ID: 123456789
Ad Group ID: 987654321
Portfolio ID: 111222333
...
Bid: 1.25
Keyword Text: blue widget
...
Units: 0
...
```

### שורה טיפוסית - Bidding Adjustment
```
Product: Sponsored Products
Entity: Bidding Adjustment
Operation: Update
Campaign ID: 123456789
...
Placement: Top of Search
Percentage: 50
...
```

## וולידציות נדרשות

### בדיקות מבנה
1. **קיום Sheet:** "Sponsored Products Campaigns" חייב להיות קיים
2. **מספר עמודות:** בדיוק 48, לא פחות ולא יותר
3. **סדר עמודות:** חייב להתאים לסדר המוגדר
4. **שמות עמודות:** חייבים להיות זהים (Case Sensitive)

### בדיקות נתונים
1. **Entity Types:** רק הערכים המוגדרים
2. **State:** enabled/paused/archived בלבד
3. **ערכים מספריים:** חייבים להיות מספרים או ריקים
4. **Campaign ID:** חייב להיות קיים בכל שורה

## טיפול בשגיאות

### שגיאות קריטיות (עוצרות עיבוד)
- חסר Sheet "Sponsored Products Campaigns"
- מספר עמודות שונה מ-48
- חסרות עמודות חובה
- קובץ גדול מ-40MB
- יותר מ-500,000 שורות

### אזהרות (ממשיכות עיבוד)
- ערכי Entity לא מוכרים (מסוננים)
- ערכי State לא תקינים (מסוננים)
- ערכים מספריים לא תקינים (מטופלים כ-0)

## ביצועים

### זמני קריאה צפויים
| גודל קובץ | זמן קריאה |
|-----------|-----------|
| עד 5MB | 2-3 שניות |
| 5-10MB | 5-7 שניות |
| 10-20MB | 10-15 שניות |
| 20-40MB | 20-30 שניות |

### אופטימיזציות
- קריאת Sheet ספציפי בלבד
- המרת טיפוסים אחרי הקריאה
- שימוש ב-chunks לקבצים גדולים

## הערות חשובות

1. **Bulk 60 בלבד:** כרגע רק Bulk 60 בשימוש פעיל
2. **Sheet ראשון:** גם אם יש כמה Sheets, רק הראשון נקרא
3. **עמודות Informational:** 9 עמודות לא משתתפות בחישובים
4. **Portfolio Name:** עמודה 14 קריטית לסינון Flat Portfolios
5. **Units:** עמודה 44 קריטית ל-Zero Sales

---

**עדכון אחרון:** 18 באוגוסט 2025, 12:45