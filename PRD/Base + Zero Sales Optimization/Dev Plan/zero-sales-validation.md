# בדיקת לוגיקת Zero Sales - Pre-Development Validation
**תאריך: דצמבר 2024**  
**מטרה: אימות הלוגיקה העסקית לפני כתיבת קוד**

---

## שלב 1: הכנת קובץ Excel לבדיקה

### יצירת המבנה
1. פתח Excel חדש
2. שמור בשם: `zero_sales_test_cases.xlsx`
3. צור 2 לשוניות:
   - `Test Data` - נתוני בדיקה
   - `Template` - ערכי פורטפוליו

### עמודות נדרשות ב-Test Data
צור את 48 העמודות הבאות (רשום רק את הרלוונטיות לחישוב):
- **A:** Entity (מלא: "Keyword" או "Product Targeting")
- **B:** Campaign Name (Informational only)
- **C:** Portfolio Name
- **D:** Units (מלא: תמיד 0 לבדיקה זו)
- **E:** Clicks (מלא: מספרים שונים)
- **F:** Bid (מלא: ערך נוכחי)
- **G:** Bidding Adjustment
- **H-AV:** שאר העמודות (מלא כותרות בלבד)

### עמודות נדרשות ב-Template
- **A:** Portfolio Name
- **B:** Base Bid
- **C:** Target CPA

---

## שלב 2: יצירת 20 שורות בדיקה

### Case A: Target CPA ריק + "up and" בשם (5 שורות)
```
Portfolio: Port_A
Base Bid: 1.00
Target CPA: (ריק)
Campaign Name: "Campaign up and running"
Entity: "Keyword"
Units: 0
Clicks: 10
Current Bid: 0.80

חישוב צפוי: 1.00 × 0.5 = 0.50
```

### Case B: Target CPA ריק ללא "up and" (5 שורות)
```
Portfolio: Port_B
Base Bid: 2.00
Target CPA: (ריק)
Campaign Name: "Regular Campaign"
Entity: "Keyword"
Units: 0
Clicks: 15
Current Bid: 1.50

חישוב צפוי: 2.00 (ללא שינוי)
```

### Case C: יש Target CPA, Entity = Keyword (5 שורות)
```
Portfolio: Port_C
Base Bid: 1.50
Target CPA: 20.00
Campaign Name: "Test Campaign"
Entity: "Keyword"
Units: 0
Clicks: 8
Current Bid: 1.20
Max BA בקמפיין: 1.30

חישוב צפוי:
1. Adj CPA = 20.00 × 0.7 = 14.00
2. Temp Bid = 14.00 × 0.09 = 1.26
3. Final = MIN(1.26, 1.50, 1.30×1.4) = 1.26
```

### Case D: יש Target CPA, Entity = Product Targeting (5 שורות)
```
Portfolio: Port_D
Base Bid: 0.75
Target CPA: 15.00
Campaign Name: "Product Campaign"
Entity: "Product Targeting"
Units: 0
Clicks: 20
Current Bid: 0.60
Max BA בקמפיין: 0.70

חישוב צפוי:
1. Adj CPA = 15.00 × 0.5 = 7.50
2. Temp Bid = 7.50 × 0.09 = 0.675
3. Final = MIN(0.675, 0.75, 0.70×1.4) = 0.675
```

### שורת Bidding Adjustment (1 שורה)
```
Entity: "Bidding Adjustment"
Campaign Name: זהה לאחד הקמפיינים למעלה
Bidding Adjustment: 30%
Current Bid: ריק

פעולה צפויה: העתקה ללא שינוי
```

---

## שלב 3: הוספת נוסחאות Excel לבדיקה

### עמודה חדשה: Calculated New Bid (עמודה AW)
הוסף נוסחה שמחשבת את ה-Bid החדש לפי הלוגיקה:

```
=IF(Units<>0, "Skip",
  IF(Entity="Bidding Adjustment", Current_Bid,
    IF(Target_CPA="",
      IF(ISNUMBER(SEARCH("up and",Campaign_Name)),
        Base_Bid*0.5,
        Base_Bid),
      חישוב_מורכב_לפי_Entity)))
```

### עמודה חדשה: Validation Status (עמודה AX)
```
=IF(ABS(Calculated_New_Bid - Expected_Bid) < 0.01, "PASS", "FAIL")
```

### עמודה חדשה: Expected Bid (עמודה AY)
מלא ידנית את התוצאות הצפויות מהחישובים למעלה

---

## שלב 4: הרצת הבדיקה

### ביצוע
1. מלא את כל הנתונים ב-20 השורות
2. הוסף את הנוסחאות
3. בדוק שכל השורות מקבלות "PASS"

### תיעוד תוצאות
צור טבלת סיכום:
| Case | שורות | עברו | נכשלו | הערות |
|------|--------|------|-------|--------|
| A    | 5      |      |       |        |
| B    | 5      |      |       |        |
| C    | 5      |      |       |        |
| D    | 5      |      |       |        |

---

## שלב 5: מקרי קצה לבדיקה

### ערכים קיצוניים
1. **Bid = 0.01** - מתחת למינימום (0.02)
2. **Bid = 5.00** - מעל למקסימום (4.00)
3. **Target CPA = "Ignore"** - טקסט במקום מספר
4. **Clicks = 0** - אין קליקים
5. **Portfolio חסר ב-Template** - התאמה חסרה

### תוצאות צפויות
- Bid < 0.02 → 0.02
- Bid > 4.00 → 4.00
- Target CPA = "Ignore" → דלג על השורה
- Portfolio חסר → שגיאה

---

## שלב 6: תיקוף עם המשתמשת

### מה לשלוח למשתמשת
1. קובץ Excel עם 20 שורות הבדיקה
2. טבלת תוצאות צפויות
3. רשימת מקרי קצה

### שאלות לאימות
1. האם החישובים נכונים?
2. האם יש מקרים נוספים?
3. האם הקבועים (0.7, 0.5, 0.09) נכונים?
4. האם המכפיל 1.4 ל-Max BA נכון?

---

## שלב 7: הכנת Fixtures לפיתוח

### לאחר אישור הלוגיקה
1. שמור את הקובץ כ-`valid_zero_sales_test.xlsx`
2. צור קובץ JSON עם התוצאות הצפויות
3. תעד את כל החריגים שנמצאו

### מבנה קובץ התוצאות
```
test_results.json:
{
  "case_a": {
    "input": {...},
    "expected": 0.50,
    "formula": "base_bid * 0.5"
  },
  ...
}
```

---

## נקודות קריטיות לבדיקה

⚠️ **חובה לבדוק:**
1. כל 4 המקרים עובדים נכון
2. סינון Units=0 תקין
3. Bidding Adjustment מועתק ללא שינוי
4. טווח 0.02-4.00 נאכף
5. Ignore ב-Target CPA מדלג

✅ **סימן שהלוגיקה נכונה:**
- 20/20 שורות עוברות
- אין חריגה מהטווח המותר
- Portfolio matching עובד
- Entity types מזוהים נכון

---

## המשך לאחר הבדיקה

**אם כל הבדיקות עוברות:**
→ להתחיל פיתוח לפי תוכנית הפיתוח

**אם יש כשלונות:**
→ לעדכן את האיפיון
→ לתקן את הנוסחאות
→ לבדוק שוב

---

**הערה:** קובץ זה הוא המפתח להצלחת הפרויקט. אל תדלגו על השלב הזה!