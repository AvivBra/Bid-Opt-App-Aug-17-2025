# Q&A Log - שאלות ותשובות לאיפיון UI Panels

**תאריך:** 18 באוגוסט 2025, 14:00  
**נושא:** הבהרות לכתיבת UI Panels ו-Overview Documents  
**מיועד ל:** מנהלי איפיון ומפתחים עתידיים

---

## שאלות לגבי Upload Panel

### ש: כמה כפתורי Upload צריכים להיות בפאנל?
**ת:** 5 כפתורים בסך הכל:
1. **Template** - פעיל (enabled)
2. **Bulk 60** - פעיל (enabled)  
3. **Bulk 30** - מושבת עם "Coming Soon" (disabled)
4. **Bulk 7** - מושבת עם "Coming Soon" (disabled)
5. **Data Rova** - מושבת עם "Coming Soon" (disabled)

### ש: האם כפתורי Bulk 7/30 צריכים להיות מוסתרים או מוצגים?
**ת:** מוצגים אך מושבתים (disabled). כל הכפתורים נראים מהיום הראשון, רק הפונקציונליות משתנה. זה מונע שינויי UI בעתיד.

### ש: מה ההודעות המדויקות להצלחה/כישלון בהעלאת קבצים?
**ת:** 
- הצלחה: "Template uploaded successfully" / "Bulk 60 uploaded successfully"
- כישלון גודל: "File exceeds 40MB limit" (Bulk) / "File exceeds 1MB limit" (Template)
- כישלון פורמט: "File must be Excel (.xlsx) or CSV"
- קובץ פגום: "Cannot read file - may be corrupted"

---

## שאלות לגבי Validation Panel

### ש: אילו מצבים אפשריים יש לפאנל הוולידציה?
**ת:** 3 מצבים עיקריים:
1. **Valid:** "✓ All portfolios valid" - כפתור Process Files פעיל
2. **Missing:** "Missing portfolios found - Reupload Full Template: [רשימה]" - כפתור Process Files מושבת
3. **Ignored:** "ℹ️ Some portfolios marked as Ignore: [מספר]" - כפתור Process Files פעיל

### ש: מתי כפתור "Process Files" הופך לפעיל?
**ת:** רק כאשר:
- יש Template תקין
- יש Bulk 60 תקין
- אין פורטפוליוז חסרים (או רק מהרשימה המותרת)
- יש לפחות פורטפוליו אחד עם Base Bid מספרי (לא "Ignore")

### ש: מה קורה כשמעלים Template חדש באמצע התהליך?
**ת:** כל תהליך הוולידציה מתאפס. הבאלק נשמר בזיכרון, אבל הוולידציה רצה מחדש עם הטמפלייט החדש.

---

## שאלות לגבי Output Panel

### ש: כמה כפתורי Download צריכים להופיע?
**ת:** 2 כפתורים:
1. **Download Working File** - פעיל אחרי עיבוד מוצלח
2. **Download Clean File** - מושבת תמיד עם "Coming Soon"

### ש: מה מוצג ב-Progress Bar במהלך עיבוד?
**ת:** 
- טקסט: "Processing Zero Sales optimization..."
- אחוזי התקדמות: 0-100%
- עדכון כל 500ms (המלצה, המפתח יחליט)
- ללא אפשרות ביטול

### ש: איך מסמנים שורות עם שגיאות חישוב?
**ת:** צבע רקע ורוד (#FFE4E1) לכל השורה. הצבע נשמר בקובץ Excel הסופי. הודעה מסכמת: "Please note: [X] calculation errors in Zero Sales optimization"

---

## שאלות לגבי ארכיטקטורה

### ש: האם יש Stepper או Sidebar Navigation?
**ת:** **Sidebar Navigation בלבד!** אין Stepper של 3 שלבים. יש Sidebar קבוע בצד שמאל עם 2 עמודים:
1. **Bid Optimizer** - פעיל
2. **Campaigns Optimizer** - מושבת עם "Coming Soon"

### ש: האם יש וולידציה גלובלית או לכל אופטימיזציה בנפרד?
**ת:** **אין וולידציה גלובלית.** כל אופטימיזציה מבצעת וולידציה וניקוי עצמאיים. זה מאפשר גמישות והוספת אופטימיזציות בעתיד.

### ש: כמה אופטימיזציות מופיעות ב-Checkbox List?
**ת:** 14 אופטימיזציות בסך הכל:
1. **Zero Sales** - פעיל, ניתן לסימון
2. **13 אופטימיזציות נוספות** - מושבתות עם "Coming Soon"

---

## שאלות לגבי קבצי פלט

### ש: איזה קבצים נוצרים בפועל?
**ת:** כרגע רק **Working File** עם השם:
`Auto Optimized Bulk | Working | YYYY-MM-DD | HH-MM.xlsx`

Clean File לא נוצר בשלב הנוכחי (TBC).

### ש: מה מבנה ה-Working File?
**ת:** 2 לשוניות:
1. **Targeting** - Keywords + Product Targeting עם 48 עמודות + 7 עמודות עזר
2. **Bidding Adjustment** - רק 48 העמודות המקוריות, ללא עמודות עזר

---

## שאלות לגבי פורטפוליוז

### ש: אילו פורטפוליוז מותר שיחסרו בטמפלייט?
**ת:** 10 פורטפוליוז בדיוק (Case Sensitive):
- Flat 30, Flat 25, Flat 40
- Flat 25 | Opt, Flat 30 | Opt
- Flat 20, Flat 15
- Flat 40 | Opt, Flat 20 | Opt, Flat 15 | Opt

### ש: מה קורה עם פורטפוליו שה-Base Bid שלו "Ignore"?
**ת:** הפורטפוליו לא מעובד כלל. השורות שלו נשארות בקובץ אבל לא עוברות אופטימיזציה.

---

## שאלות לגבי גבולות המערכת

### ש: מה הגבולות של גודל קבצים ומספר שורות?
**ת:**
- **Template:** עד 1MB
- **Bulk:** עד 40MB
- **מספר שורות:** עד 500,000
- **זמן עיבוד מקסימלי:** 60 שניות (המלצה: timeout של 5 דקות)

### ש: מה טווח הערכים התקין ל-Bid?
**ת:** 
- **מינימום:** 0.02
- **מקסימום:** 1.25
- שורות מחוץ לטווח מסומנות בורוד

---

## שאלות לגבי 48 העמודות

### ש: איפה בדיוק נוספות 7 עמודות העזר?
**ת:** משמאל לעמודת Bid המקורית (עמודה 28). אחרי ההוספה:
- עמודות 1-27: המקוריות
- עמודות 28-34: עמודות העזר (Old Bid, calc1, calc2, Target CPA, Base Bid, Adj. CPA, Max BA)
- עמודה 35: Bid (המקורית 28)
- עמודות 36-55: שאר המקוריות (29-48)

### ש: אילו עמודות הן Informational Only?
**ת:** עמודות 12, 13, 14, 19, 20, 24, 25, 27, 37. הן לא משתתפות בחישובים אבל חובה לשמור אותן בפלט.

---

## הנחיות כלליות

### עיקרון מנחה
**הצג את כל הרכיבים מהיום הראשון, גם אם לא פעילים.** זה מונע שינויי UI בעתיד ונותן למשתמש תמונה מלאה של היכולות העתידיות.

### מה TBC (To Be Completed)
- 13 אופטימיזציות נוספות
- Campaigns Optimizer
- Clean File
- Data Rova Integration
- Bulk 7/30 support

### למי לפנות בשאלות נוספות
בדוק קודם ב:
1. `PRD/Dev Log/faq-developers.md`
2. `PRD/Dev Log/faq-answers-updated.md`
3. `PRD/Dev Log/project-handover-letter (1).md`

---

*מסמך זה נכתב ב-18 באוגוסט 2025, 14:00*