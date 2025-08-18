# מפרט קובץ Template - Bid Optimizer

## 1. סקירה כללית

### מטרה
קובץ Template מגדיר את הגדרות הפורטפוליו והASINs עבור האופטימיזציות.

### מבנה
- פורמט: Excel (.xlsx)
- 2 לשוניות חובה
- קידוד: UTF-8
- גודל מקסימלי: 40MB

## 2. לשונית Port Values

### מבנה
| מס׳ עמודה | שם עמודה | סוג | חובה | תיאור |
|-----------|-----------|-----|-------|--------|
| A | Portfolio Name | Text | כן | שם הפורטפוליו |
| B | Base Bid | Number/Text | כן | ערך בסיס או "Ignore" |
| C | Target CPA | Number | לא | יעד CPA |

### Portfolio Name
- **סוג**: טקסט חופשי
- **אורך**: עד 255 תווים
- **ייחודיות**: חייב להיות ייחודי
- **תווים מותרים**: כל התווים כולל מיוחדים
- **Case Sensitive**: כן

### Base Bid
- **ערכים תקינים**: 
  - מספר: 0.00 - 999.99
  - טקסט: "Ignore" (בדיוק כך)
- **דיוק**: עד 2 ספרות אחרי הנקודה
- **ברירת מחדל**: אין (חובה)

### Target CPA
- **ערכים תקינים**: 0.00 - 9999.99
- **דיוק**: עד 2 ספרות אחרי הנקודה
- **ריק מותר**: כן
- **משמעות ריק**: אין Target CPA

## 3. לשונית Top ASINs

### מבנה
| מס׳ עמודה | שם עמודה | סוג | חובה | תיאור |
|-----------|-----------|-----|-------|--------|
| A | ASIN | Text | כן | מזהה ASIN של Amazon |

### ASIN
- **פורמט**: 10 תווים (אותיות וספרות)
- **דוגמה**: B08N5WRWNW
- **ולידציה**: תבנית ASIN תקנית
- **ייחודיות**: מומלץ ייחודי
- **רגישות**: Case sensitive

## 4. דוגמאות

### Port Values - תקין
```
Portfolio Name     | Base Bid | Target CPA
------------------|----------|------------
Kids-Brand-US     | 1.25     | 5.00
Kids-Brand-EU     | 0.95     | 
Supplements-US    | Ignore   | 
Supplements-EU    | 2.10     | 8.50
Accessories-Global| 0.50     | 3.00
```

### Top ASINs - תקין
```
ASIN
----------
B08N5WRWNW
B07XQXZXJC
B09MDHXV6B
B06XYZ1234
B08ABC5678
```

## 5. ולידציות

### בדיקות מבנה
1. קיום 2 לשוניות
2. שמות לשוניות נכונים
3. מספר עמודות נכון
4. כותרות עמודות תואמות

### בדיקות Port Values
1. Portfolio Name לא ריק
2. אין כפילויות בשמות
3. Base Bid תקין (מספר או "Ignore")
4. Target CPA תקין (מספר או ריק)
5. לא כל הפורטפוליוז עם "Ignore"

### בדיקות Top ASINs
1. פורמט ASIN תקני
2. אורך 10 תווים
3. תווים תקינים (alphanumeric)

## 6. שגיאות נפוצות

### שגיאות מבנה
```
❌ "Missing sheet 'Port Values'"
❌ "Missing sheet 'Top ASINs'"
❌ "Wrong column order in Port Values"
❌ "Missing column 'Base Bid'"
```

### שגיאות נתונים
```
❌ "Empty Portfolio Name in row 5"
❌ "Duplicate portfolio: Kids-Brand-US"
❌ "Invalid Base Bid 'ABC' in row 3"
❌ "All portfolios marked as Ignore"
❌ "Invalid ASIN format in row 7"
```

## 7. מקרי קצה

### Base Bid מיוחדים
- "Ignore" - הפורטפוליו לא ישתתף בולידציה
- 0.00 - ערך תקין, Bid מינימלי
- 999.99 - ערך תקין, Bid מקסימלי

### Target CPA
- ריק - תקין, אין יעד
- 0.00 - תקין, יעד אפס
- 9999.99 - תקין, יעד מקסימלי

## 8. שימוש באופטימיזציות

### Zero Sales
- משתמש רק בלשונית Port Values
- מתעלם מ-Top ASINs
- דורש Base Bid תקין

### אופטימיזציות עתידיות
- חלק ישתמשו ב-Top ASINs
- יוגדר בהמשך לכל אופטימיזציה

## 9. יצירת Template ריק

### הורדה
כפתור "Download Template" יוצר קובץ עם:
- 2 לשוניות ריקות
- כותרות עמודות בלבד
- ללא נתונים

### תוכן
```python
# Port Values sheet
Portfolio Name | Base Bid | Target CPA
(empty rows)

# Top ASINs sheet  
ASIN
(empty rows)
```

## 10. תאימות

### Excel
- Excel 2010 ומעלה
- Google Sheets
- LibreOffice Calc

### CSV
- אם נשמר כ-CSV, רק לשונית אחת
- צריך 2 קבצי CSV נפרדים