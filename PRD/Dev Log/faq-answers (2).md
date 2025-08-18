# מסמך FAQ מאוחד - תשובות לכל השאלות

**תאריך:** 18 באוגוסט 2025, 10:00 (שעון ישראל)  
**אל:** מנהל האיפיון החדש  
**מאת:** מנהל הפרויקט  

### 6. Clean Files
**סטטוס:** TBC - כרגע רק Working File

---

## ⚠️ חידוד קריטי ⚠️
**באיפיון הנוכחי מתייחסים אך ורק ל-Zero Sales!**  
- כל 13 האופטימיזציות האחרות = **TBC**
- כל מה שקשור לעמוד השני (Campaigns Optimizer) = **TBC**  
- כל מה שקשור ל-Negation/Harvesting = **TBC**
- כל מה שקשור ל-Data Rova = **TBC**
- **Clean Files = TBC** (כרגע Working File בלבד)

**המטרה:** להשלים איפיון מלא ל-Zero Sales עם Working File בלבד.

---

## קטגוריה א': מידע שנמצא במקורות - קרא שוב

### 1. רשימת 13 האופטימיזציות הנוספות
**איפה:** מכתב סעיף 4  
**תשובה:** Portfolio Bid, Budget Optimization, Keyword Optimization, ASIN Targeting + 9 ללא שמות

### 2. 48 עמודות ו-Informational Only
**איפה:** מכתב סעיף 4  
**תשובה:** רשימה מלאה שם. Informational: 12,13,14,19,20,24,25,27,37 - אסור למחוק

### 3. חישוב Max BA
**איפה:** processing.md  
**תשובה:** עמודה Percentage (#35), MAX לפי Campaign ID

### 4. Portfolio כ-"Ignore"
**איפה:** מכתב סעיף 4  
**תשובה:** Base Bid = "Ignore"

### 5. Operation בפלט
**איפה:** processing.md שלב 5  
**תשובה:** תמיד "Update"

---

## קטגוריה ב': סתירות שדורשות הבהרה

### 1. Bulk 30 vs 60 ⚠️
**הבהרה:** Zero Sales משתמש ב-**Bulk 60** (processing.md נכון, heb טעות)  
**מסמך לתיקון:** processing-heb.md

---

## קטגוריה ג': TBC - לא רלוונטי עכשיו

### 1. Data Rova
**סטטוס:** TBC - Benchmarking API, לא צריך placeholder

### 2. Campaigns Optimizer
**סטטוס:** TBC - Negation/Harvesting בעמוד שני עתידי

### 3. Product Ad Entity
**סטטוס:** TBC - רלוונטי לאופטימיזציות עתידיות

### 4. Bulk 7/30/60
**סטטוס:** כרגע רק 60 ל-Zero Sales, השאר TBC

### 5. סדר אופטימיזציות
**סטטוס:** עצמאיות - אין סדר או תלויות

---

## קטגוריה ד': הבהרות טכניות

### 1. Entity Types
**Keyword/Product Targeting:** טיפול זהה ב-Zero Sales  
**Bidding Adjustment:** נשאר ללא שינוי  
**Product Ad:** לא נכלל ב-Zero Sales

### 2. IDs וחישובים
**Campaign ID:** לחישוב Max BA  
**calc1/calc2:** שלבי ביניים לנוסחה

### 3. Portfolio Rules
**10 Flat portfolios:** תמיד לסנן (רשימה במכתב)  
**Case sensitive:** כן  
**סדר עמודות:** זהה לקלט

### 4. Template Structure
**Port Values:** Portfolio Name, Base Bid, Target CPA  
**Top ASINs:** TBC לעתיד

### 5. State Values
**אפשרויות:** enabled/paused/archived

---

## קטגוריה ה': הנחיות לפיתוח

### 1. Pink Highlighting
**איך:** openpyxl עם conditional_format

### 2. ביצועים
**יעד:** 60 שניות ל-500K שורות

### 3. ממשק Sidebar
**קיים:** Bid Optimizer  
**TBC:** Campaigns Optimizer

---

## סיכום מסמכים שדורשים תיקון:

1. **processing-heb.md** - שינוי מ-Bulk 30 ל-Bulk 60

---

**הערה סופית:** 6 מתוך 13 השאלות הראשונות נענו במקורות הקיימים.