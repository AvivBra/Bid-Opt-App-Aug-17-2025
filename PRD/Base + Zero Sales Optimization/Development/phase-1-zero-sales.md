# Phase 1: Zero Sales Implementation

## סקירה כללית

Phase 1 מתמקד בפיתוח אופטימיזציית Zero Sales בלבד. זו האופטימיזציה הראשונה והיחידה שתפותח בשלב זה.

## היקף Phase 1

### מה כלול
- ממשק משתמש מלא (Sidebar Navigation)
- העלאת Template ו-Bulk 60
- אופטימיזציית Zero Sales
- יצירת Working File
- צביעה ורודה לשגיאות חישוב

### מה לא כלול (TBC)
- 13 האופטימיזציות הנוספות
- Campaigns Optimizer
- Clean File
- Data Rova
- Bulk 7/30

## רכיבי הפיתוח

### UI - ממשק משתמש

#### Sidebar Navigation
- 2 עמודים: Bid Optimizer, Campaigns Optimizer
- Bid Optimizer פעיל
- Campaigns Optimizer מוצג אך לא פעיל

#### Upload Panel
- כפתור Download Template
- 4 כפתורי Upload (Template, Bulk 7/30/60)
- כפתור Data Rova (Coming Soon)
- רק Template ו-Bulk 60 פעילים

#### Validation Panel
- בדיקת התאמה בין Template ל-Bulk
- הצגת portfolios חסרים
- הצגת מספר שורות לעיבוד
- כפתור Process Files

#### Output Panel
- Progress bar בזמן עיבוד
- הודעת סיום עם סטטיסטיקות
- כפתור Download Working File
- כפתור Reset

### Business Logic - Zero Sales

#### תהליך האופטימיזציה
1. **סינון:** שורות עם Units = 0
2. **ניקוי:** הסרת 10 Flat Portfolios
3. **חלוקה:** Keywords/Product Targeting vs Bidding Adjustment
4. **חישוב:** 4 מקרים לפי Target CPA ושם קמפיין
5. **עדכון:** Bid חדש בטווח 0.02-1.25

#### 4 מקרי החישוב
- **מקרה A:** אין Target CPA + "up and" בשם
- **מקרה B:** אין Target CPA + אין "up and" בשם
- **מקרה C:** יש Target CPA + "up and" בשם
- **מקרה D:** יש Target CPA + אין "up and" בשם

### Data Processing

#### קריאת קבצים
- Template: 2 לשוניות (Port Values, Top ASINs)
- Bulk 60: 48 עמודות, עד 500,000 שורות
- וולידציה של מבנה ונתונים

#### יצירת Working File
- 2 לשוניות: Targeting, Bidding Adjustment
- 7 עמודות עזר ב-Targeting
- צביעה ורודה לערכים מחוץ לטווח
- שמירת כל הנתונים המקוריים

## מגבלות וביצועים

### מגבלות גודל
- Template: עד 1MB
- Bulk: עד 40MB
- מספר שורות: עד 500,000

### ביצועים צפויים
- 10,000 שורות: עד 10 שניות
- 100,000 שורות: עד 30 שניות
- 500,000 שורות: עד 120 שניות

## טכנולוגיות

### סטאק טכנולוגי
- Python 3.8+
- Streamlit (UI)
- pandas (עיבוד נתונים)
- openpyxl (קבצי Excel)

### סביבת הרצה
- Desktop application
- Windows/Mac/Linux
- ללא תלות באינטרנט

## בדיקות

### בדיקות יחידה
- חישובי Zero Sales
- קריאת וכתיבת קבצים
- וולידציות

### בדיקות אינטגרציה
- תהליך מלא מקצה לקצה
- טיפול בשגיאות
- מקרי קצה

### בדיקות ביצועים
- קבצים גדולים (500K שורות)
- זמני תגובה
- ניהול זיכרון

## לוח זמנים

### שבוע 1: UI Development
- יום 1-2: Setup והגדרות פרויקט
- יום 3-4: Upload Panel
- יום 5: Validation Panel

### שבוע 2: Business Logic
- יום 6-7: Zero Sales implementation
- יום 8-9: File generation
- יום 10: Integration ובדיקות

## Definition of Done

### קריטריונים להשלמה
- כל הבדיקות עוברות
- UI עובד ללא באגים
- חישובים מדויקים
- קבצי פלט תקינים
- ביצועים בטווח המוגדר

### Deliverables
- קוד מקור מלא
- קובץ הרצה
- תיעוד למשתמש
- תיעוד טכני

## הערות לפיתוח

- להתחיל עם UI ואז להוסיף לוגיקה
- לבדוק עם קבצי דוגמה קטנים תחילה
- לשמור על קוד מודולרי להרחבות עתידיות
- לתעד כל פונקציה וחישוב

---

**עדכון אחרון:** 18 באוגוסט 2025, 20:00