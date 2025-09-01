# מסמך איפיון - Portfolios Organization

**תאריך:** 29/08/2025  
**שעה:** 09:36

## 2.5 Campaign Count Column Method
To identify empty portfolios, add a count column to each portfolio that counts campaigns using a COUNTIFS-like approach. For each portfolio row, count how many rows in the Campaigns sheet have matching Portfolio ID values. Portfolios with a count of 0 are considered empty.

## 3. התעלמות מפורטפוליו מסוימים
בעת חיפוש פורטפוליו ריקים, יש להתעלם מפורטפוליו שעונים על התנאים הבאים:
- **Tab:** Portfolios
- **Portfolio Name:** "Paused" או "Terminal"

## 4. עדכון קמפיינים ללא פורטפוליו

### 4.1 זיהוי קמפיינים ללא פורטפוליו
מציאת כל השורות שעונות על התנאים:
- **Tab:** Sponsored Products Campaigns
- **Entity:** Campaign
- **Portfolio ID:** Empty (ריק)

### 4.2 עדכון קמפיינים
בכל השורות שנמצאו, לבצע את העדכונים הבאים:

| שדה | ערך חדש |
|-----|---------|
| Portfolio ID | 84453417629173 |
| Operation | update |

### 4.3 תחולה
העדכון יחול על כל השורות ב-Tab "Sponsored Products Campaigns" שבהן:
- **Entity:** Campaign
- **Portfolio ID:** ריק