# מסמך FAQ מאוחד - תשובות לכל השאלות

**תאריך:** 18 באוגוסט 2025  

---

## 🆕 עדכון אחרון: 18 באוגוסט 2025, 12:13

### שאלות ותשובות על הקבצים:

#### output-formats.md
**ש:** האם יש כותרות מיוחדות לשיטס?  
**ת:** "Targeting" ו-"Bidding Adjustment"

**ש:** האם צריך לשמור פורמט צבעים מהאקסל המקורי?  
**ת:** כן, ורוד נשאר ורוד בפלט. אין צבעים אחרים

**ש:** איך מיישמים Pink Highlighting?  
**ת:** המפתח יצטרך למצוא את הדרך (openpyxl)

#### README.md
**ש:** האם יש דרישות סביבה מיוחדות?  
**ת:** אותה סביבה של האפליקציה הקודמת, למחשב אחד עם קבצים ענקיים

**ש:** איזה גרסת פייתון/סטרימליט?  
**ת:** Python 3, Streamlit - המפתח יבדוק

**ש:** האם יש תלויות מיוחדות?  
**ת:** המפתח יצטרך להבין

---

## ⚠️ חידודים קודמים: 18 באוגוסט 2025, 10:00

### החלטות עיקריות:
- **פוקוס:** איפיון מלא רק ל-Zero Sales
- **Working File בלבד** - אין Clean File כרגע
- **כל השאר TBC** - 13 אופטימיזציות, Campaigns Optimizer, Data Rova

### מידע שנמצא במקורות:
- **13 אופטימיזציות:** Portfolio Bid, Budget Optimization, Keyword Optimization, ASIN Targeting + 9 ללא שמות
- **48 עמודות:** רשימה מלאה במכתב סעיף 4
- **Informational columns:** 12,13,14,19,20,24,25,27,37 - אסור למחוק
- **Max BA:** עמודה Percentage (#35), MAX לפי Campaign ID
- **Portfolio Ignore:** Base Bid = "Ignore"
- **Operation בפלט:** תמיד "Update"

### הבהרות טכניות:
- **Entity Types:** Keyword/Product Targeting מטופלים זהה, Bidding Adjustment ללא שינוי
- **10 Flat portfolios:** תמיד לסנן (רשימה במכתב)
- **Case sensitive:** כן
- **State values:** enabled/paused/archived
- **Pink Highlighting:** openpyxl עם conditional_format
- **ביצועים:** 60 שניות ל-500K שורות