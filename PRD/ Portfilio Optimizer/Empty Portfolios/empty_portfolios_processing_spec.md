# Empty Portfolios - איפיון תהליך עיבוד
## תאריך: 28/08/2025 | שעה: 20:00

## תהליך העיבוד

### שלב 1: בדיקת התאמות
לכל שורה בלשונית **Portfolios**:
- התאמה לפי **Portfolio ID** בין הלשוניות
- ספירת שורות ב-**Sponsored Products Campaigns** עם:
  - אותו Portfolio ID
  - Entity = Campaign

### שלב 2: זיהוי פורטפוליו ריקים
פורטפוליו נחשב ריק אם:
1. יש לו שם מילולי (לא מספרי) בעמודה **Portfolio Name** בלשונית **Portfolios**
2. אין לו קמפיינים כלל לפי ההתאמה בין הלשוניות

### שלב 3: עדכון פורטפוליו ריקים
בלשונית **Portfolios**, לכל פורטפוליו ריק:
- **Portfolio Name** ← הערך המספרי הקטן ביותר שלא קיים כבר בעמודה
- **Operation** ← update
- **Budget Amount** ← empty
- **Budget Start Date** ← empty

## פלט

### לשונית Portfolios
- שורות של פורטפוליו ריקים מסומנות בצהוב

### לשונית Sponsored Products Campaigns
- השארת רק שורות עם **Entity = Campaign**