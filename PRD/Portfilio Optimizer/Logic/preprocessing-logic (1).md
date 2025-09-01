# לוגיקת עיבוד מקדים - Portfolio Optimizer
**תאריך: 31 באוגוסט 2025 | שעה: 20:15**

## שלב עיבוד מקדים

**הערה:** תהליך זה צריך להתבצע בקובץ קוד נפרד שיקרא `cleaning` ולהיכנס לפעולה מיד אחרי `validator`.

לפני הפעלת העיבודים של הצ'קבוקסים שנבחרו, יש לבצע את הפעולות הבאות:

### 1. יצירת לשונית Campaign
- מעבירים את כל השורות שבהן `Entity = Campaign` ללשונית נפרדת
- קוראים ללשונית החדשה: **Campaign**

### 2. יצירת לשונית Product Ad
- מעבירים את כל השורות שבהן `Entity = Product Ad` ללשונית נפרדת  
- קוראים ללשונית החדשה: **Product Ad**

### 3. ניקוי לשונית Sponsored Products Campaign
- מוחקים את כל השורות שנשארו בלשונית **Sponsored Products Campaign**

### 4. מחיקת לשוניות מיותרות
- מוחקים כל לשונית שאינה:
  - Portfolios
  - Product Ad
  - Campaign

*זה אומר שכל השורות שהיו במקור בלשונית Sponsored Products Campaign ולא הועברו ל-Campaign או Product Ad ימחקו יחד עם הלשונית Sponsored Products Campaign