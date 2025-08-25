# מסמך ניקוי - Bids 30 Days
**תאריך: 13:05**

## שלבי ניקוי זהים ל-Zero Sales:
1. חלוקה לגיליונות לפי Entity type
2. הסרת 10 פורטפוליואים Flat מוגדרים
3. הסרת פורטפוליואים עם Base Bid=Ignore
4. השארת רק שורות עם enabled בכל העמודות:
   - State = enabled
   - Campaign State (Informational only) = enabled
   - Ad Group State (Informational only) = enabled

## שלבי ניקוי ייחודיים ל-Bids 30 Days:

### סינון שורות - משאירים רק שורות העומדות בתנאים:
```
(units > 0)
AND
(units > 2 OR clicks > 30)
```

### הערה על מקור הנתונים:
- עמודת Conversion Rate נמצאת במיקום 55 בקובץ הבאלק המקורי
- הערך צריך להיות בפורמט עשרוני (לדוגמה: 0.08 = 8%)