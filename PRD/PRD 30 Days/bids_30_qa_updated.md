# שאלות ותשובות - Bids 30 Days Optimization
**תאריך: 17/08/2025 13:15**

## שאלות כלליות

### ש: מה ההבדל בין Zero Sales ל-Bids 30 Days?
**ת:** Zero Sales מטפל בשורות עם units=0, בעוד Bids 30 Days מטפל בשורות עם units>0 שעומדות בתנאים נוספים.

### ש: איזה קבצים נדרשים לאופטימיזציה זו?
**ת:** Template (זהה ל-Zero Sales) + Bulk 30 Days (במקום Bulk 60).

### ש: האם אפשר להריץ את שתי האופטימיזציות במקביל?
**ת:** לא, המערכת מאפשרת רק אופטימיזציה אחת בכל פעם.

## שאלות טכניות

### ש: מה עושים במקרים שיש NULL בעמודות חשובות לתהליך העיבוד או שיש error בתהליך החישוב?
**ת:** 
- צובעים את השורה בוורוד
- כותבים הערה בעמודת Bid (לדוגמה: "Error" או "Missing Value in [column name]")
- ממשיכים לעיבוד השורה הבאה
- בעת מסירת הפלט מציגים הודעות שגיאה על המסך: "[count] errored rows", "[count] rows missing critical values"

### ש: מה קורה לשורות עם Target CPA = NULL?
**ת:** הן מועברות לגיליון נפרד בשם "For Harvesting".

### ש: איך מחושב Max BA?
**ת:** הערך המקסימלי של Percentage עבור כל Campaign ID.

### ש: מה התנאים לסינון שורות ב-Bids 30 Days?
**ת:** units > 0 AND (units > 2 OR clicks > 30).

### ש: מהם 10 הפורטפוליו המוחרגים?
**ת:** Flat 30, Flat 25, Flat 40, Flat 25 | Opt, Flat 30 | Opt, Flat 20, Flat 15, Flat 40 | Opt, Flat 20 | Opt, Flat 15 | Opt.

## שאלות על הפלט

### ש: כמה גיליונות בקובץ הפלט?
**ת:** 3 גיליונות: Targeting, Bidding Adjustment, For Harvesting.

### ש: אילו עמודות עזר נוספות?
**ת:** Old Bid, calc1, calc2, Target CPA, Base Bid, Adj. CPA, Max BA, Temp Bid, Max_Bid, calc3.

### ש: מתי שורה נצבעת בוורוד?
**ת:** כאשר Conversion Rate < 0.08, Bid < 0.02, Bid > 1.25, או יש שגיאת חישוב.

### ש: האם יש צביעה בגיליון Bidding Adjustment?
**ת:** לא, צביעה בוורוד רק בגיליון Targeting.

## שאלות על החישובים

### ש: מה ההבדל בחישוב כשיש "up and" בשם הקמפיין?
**ת:** עם "up and": calc1 = Adj.CPA * 0.5 / (clicks/units). בלי: calc1 = Adj.CPA / (clicks/units).

### ש: מתי Temp Bid מחושב?
**ת:** כאשר calc2 >= 1.1 וגם (Match Type = "Exact" או Product Targeting מכיל "asin=B0").

### ש: איך נקבע Max_Bid?
**ת:** אם units < 3: Max_Bid = 0.8 / (1 + Max BA/100). אחרת: Max_Bid = 1.25 / (1 + Max BA/100).

### ש: מה קורה אם calc3 < 0?
**ת:** Bid = Max_Bid. אחרת Bid = Temp_Bid.

## שאלות על הממשק

### ש: איך מפעילים את כפתור Bulk 30?
**ת:** על ידי בחירת checkbox של Bids 30 Days.

### ש: מה קורה בעת החלפת אופטימיזציה?
**ת:** נתוני ה-Bulk הקודמים נמחקים מהסשן וצריך להעלות קובץ חדש.

### ש: איזה הודעות מוצגות בסיום העיבוד?
**ת:** "[X] rows with CVR < 8%", "[Y] errored rows", "[Z] rows with Bid < 0.02", "[W] rows with Bid > 1.25".

### ש: מאיפה מגיע הנתון של Conversion Rate?
**ת:** מעמודה 55 בקובץ הבאלק המקורי תחת השם "Conversion Rate".