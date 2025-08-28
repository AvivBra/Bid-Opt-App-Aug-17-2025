# אופטימיזציית Zero Sales - וולידציה

## עמודות נדרשות מקובץ Template (Port Values sheet)
נדרשות בדיוק 3 עמודות בסדר הבא: Portfolio Name (חובה, טקסט, case sensitive), Base Bid (חובה, מספר או "Ignore"), Target CPA (אופציונלי, מספר או ריק).

## רשימת 48 העמודות בקובץ Bulk 60 (בסדר המדויק)
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

## בדיקות תקינות

### בדיקות קובץ
- גודל הקובץ חייב להיות מתחת ל-40MB
- מספר השורות מוגבל ל-500,000
- הפורמט חייב להיות Excel (.xlsx) או CSV
- ב-Bulk חייב להיות Sheet בשם "Sponsored Products Campaigns"

### בדיקות מבנה
- קובץ Template חייב להכיל בדיוק 3 עמודות בסדר הנכון
- קובץ Bulk חייב להכיל בדיוק 48 עמודות בסדר הנכון
- כותרות העמודות חייבות להתאים במדויק לשמות הנדרשים

### בדיקות נתונים ב-Template
- Portfolio Name לא יכול להיות ריק ולא יכולות להיות כפילויות
- Base Bid חייב להיות מספר בין 0.02 ל-4 או המילה "Ignore"
- Target CPA אם קיים חייב להיות מספר בין 0.01 ל-4 או להישאר ריק
- חייב להיות לפחות פורטפוליו אחד עם Base Bid מספרי (לא "Ignore")

### בדיקות נתונים ב-Bulk
- Units חייב להיות ערך מספרי (יכול להיות 0)
- חייבת להיות לפחות שורה אחת עם Units = 0 אחרי כל הסינונים

## טיפול בשגיאות

### שגיאות חוסמות (עוצרות עיבוד)
- **חסר קובץ Template:** הודעה "Template file is required", פתרון - העלה קובץ Template
- **חסר קובץ Bulk:** הודעה "Bulk 60 file is required", פתרון - העלה קובץ Bulk 60
- **קובץ גדול מ-40MB:** הודעה "File exceeds 40MB limit", פתרון - הקטן את הקובץ
- **חסרות עמודות ב-Template:** הודעה "Missing columns in Template", פתרון - בדוק מבנה Template
- **חסרות עמודות ב-Bulk:** הודעה "Bulk file must have 48 columns", פתרון - בדוק מבנה Bulk
- **חסרים פורטפוליוז:** הודעה "Missing portfolios: [list], reupload template", פתרון - העלה Template מתוקן (Bulk נשמר)
- **אין שורות עם Units=0:** הודעה "No zero sales data found", פתרון - בדוק נתונים
- **כל הפורטפוליוז Ignore:** הודעה "All portfolios marked as Ignore", פתרון - הגדר Base Bid מספרי

### אזהרות (ממשיכות עיבוד)
- **Portfolio Name לא נמצא:** הודעה "Portfolio [name] not in Template", השפעה - שורה לא תעובד
- **Base Bid = "Ignore":** הודעה "Portfolio [name] ignored", השפעה - פורטפוליו לא יעובד
- **ערך לא תקין ב-Bid:** הודעה "Invalid bid value in row X", השפעה - שורה תסומן בורוד
- **Units לא מספרי:** הודעה "Non-numeric Units in row X", השפעה - שורה תדולג

## תהליך העלאת טמפלייט מתוקן
כאשר המערכת מזהה פורטפוליוז חסרים, היא שומרת את קובץ הבאלק בזיכרון ומאפשרת למשתמש להעלות טמפלייט חדש. לאחר שהמשתמש העלה טמפלייט מתוקן, המערכת מריצה את כל הוולידציה מחדש אך לא דורשת העלאת באלק חדש. אם הוולידציה עוברת בהצלחה עם הטמפלייט החדש, המערכת ממשיכה לעיבוד.

## סדר בדיקות
1. **בדיקת קבצים** - קיום, גודל, פורמט
2. **בדיקת מבנה** - עמודות, כותרות
3. **בדיקת התאמה** - פורטפוליוז מ-Bulk קיימים ב-Template
4. **בדיקת נתונים** - ערכים תקינים, לוגיקה עסקית
5. **בדיקת תוצאה** - יש נתונים לעיבוד אחרי סינון