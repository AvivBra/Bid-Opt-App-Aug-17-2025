# תרחישי בדיקה - Bid Optimizer

## 1. תרחיש Happy Path

### תיאור
משתמש עם קבצים תקינים מריץ Zero Sales

### צעדים
1. **הורדת Template**
   - לחץ "Download Template"
   - מלא 3 פורטפוליוז ב-Port Values
   - שמור

2. **העלאת קבצים**
   - העלה Template (125KB)
   - העלה Bulk 60 (2.3MB)
   - ודא: ✓ על שני הקבצים

3. **בחירת אופטימיזציה**
   - סמן: Zero Sales
   - ודא: הודעה "✅ Ready to process"

4. **עיבוד**
   - לחץ: Process Files
   - ודא: Progress bar
   - ודא: "Processing complete"

5. **הורדה**
   - הורד Working File
   - הורד Clean File
   - פתח ב-Excel

### תוצאה צפויה
- 2 קבצים תקינים
- Working: לשונית עם עמודות עזר
- Clean: רק 48 עמודות
- Operation="Update" בכל השורות

---

## 2. תרחיש Missing Portfolios

### תיאור
Template חסרים בו פורטפוליוז מ-Bulk 60

### צעדים
1. **העלאת קבצים**
   - Template עם 2 פורטפוליוז
   - Bulk 60 עם 4 פורטפוליוז

2. **ראה שגיאה**
   ```
   ❌ Missing portfolios found - Processing Blocked
   Missing: Portfolio_C, Portfolio_D
   ```

3. **תיקון**
   - הכן Template עם כל 4
   - לחץ "Upload New Template"
   - העלה מחדש

4. **המשך**
   - ודא: "✅ All portfolios valid"
   - Process עובד

### תוצאה צפויה
- חסימה ראשונית
- אפשרות תיקון
- המשך רגיל

---

## 3. תרחיש Multiple Files

### תיאור
העלאת מספר קבצי Bulk

### צעדים
1. **העלאת קבצים**
   - Template ✓
   - Bulk 30 ✓
   - Bulk 60 ✓
   - Bulk 7 ✗
   - Data Rova ✗

2. **בחירת אופטימיזציות**
   - Zero Sales (דורש Bulk 60) ✓
   - Portfolio Bid (דורש Bulk 30) ✓
   - Budget Opt (דורש Bulk 7) ✗

3. **ולידציה**
   ```
   Zero Sales: ✅ Ready
   Portfolio Bid: ✅ Ready
   Budget Opt: ❌ Missing Bulk 7
   ```

4. **עיבוד**
   - רק 2 הראשונות רצות

### תוצאה צפויה
- רק אופטימיזציות עם קבצים רצות
- הודעות ברורות לכל אחת

---

## 4. תרחיש File Too Large

### תיאור
ניסיון העלאת קובץ 41MB

### צעדים
1. **העלה Bulk 60 גדול**
   - בחר קובץ 41MB
   - ודא: "❌ File exceeds 40MB limit"

2. **הקובץ לא נטען**
   - Status: "✗ Not uploaded"
   - אין Progress

3. **העלה קובץ קטן**
   - Bulk 60 של 35MB
   - ודא: "✓ Uploaded"

### תוצאה צפויה
- דחייה מיידית
- הודעה ברורה
- אפשרות להעלות אחר

---

## 5. תרחיש Calculation Errors

### תיאור
Zero Sales עם שגיאות חישוב

### צעדים
1. **הכן נתונים בעייתיים**
   - Portfolio עם Base Bid = "Ignore"
   - שורות עם Clicks = NULL
   - שורות עם Units = 0

2. **הרץ Zero Sales**
   - העיבוד מצליח
   - Pink notice מופיע

3. **בדוק הודעות**
   ```
   ⚠️ Please note:
   - 5 rows below $0.02
   - 3 rows above $1.25
   - 7 calculation errors
   ```

### תוצאה צפויה
- עיבוד לא נכשל
- שורות בעייתיות מסומנות
- הודעה ברורה

---

## 6. תרחיש Template Sheets

### תיאור
בדיקת 2 הלשוניות בTemplate

### צעדים
1. **הורד Template**
   - ודא: 2 לשוניות
   - Port Values (3 עמודות)
   - Top ASINs (1 עמודה)

2. **מלא נתונים**
   - Port Values: 5 פורטפוליוז
   - Top ASINs: 10 ASINs

3. **העלה ועבד**
   - Zero Sales משתמש רק ב-Port Values
   - אופטימיזציות עתידיות ישתמשו ב-Top ASINs

### תוצאה צפויה
- 2 לשוניות נשמרות
- Zero Sales עובד רגיל
- Top ASINs מוכן לעתיד

---

## 7. תרחיש Reset Flow

### תיאור
התחלה מחדש אחרי עיבוד

### צעדים
1. **השלם תהליך מלא**
   - Upload → Process → Download

2. **לחץ New Processing**
   - כל הקבצים נמחקים
   - Checkboxes מתאפסים
   - חזרה למצב התחלתי

3. **העלה קבצים חדשים**
   - תהליך חדש לגמרי

### תוצאה צפויה
- ניקוי מלא
- אין "זיכרון"
- מוכן לתהליך חדש

---

## 8. תרחיש Flat Portfolios

### תיאור
בדיקת התעלמות מ-Flat portfolios

### צעדים
1. **הכן Bulk עם Flat**
   - Portfolio רגיל: Kids-Brand
   - Flat portfolio: Flat 30
   - Units = 0 לשניהם

2. **הרץ Zero Sales**
   - Kids-Brand מעובד
   - Flat 30 מתעלם

3. **בדוק תוצאות**
   - רק Kids-Brand בפלט
   - אין Flat 30

### תוצאה צפויה
- Flat portfolios לא מעובדים
- אין הודעת שגיאה
- עיבוד רגיל לאחרים

---

## 9. תרחיש Empty Files

### תיאור
העלאת קבצים ריקים

### צעדים
1. **העלה Template ריק**
   - 0 שורות data
   - ודא: "❌ Template has no data"

2. **העלה Bulk ריק**
   - Headers בלבד
   - ודא: "❌ No valid rows"

### תוצאה צפויה
- זיהוי מיידי
- הודעות ברורות
- חסימת עיבוד

---

## 10. תרחיש Performance

### תיאור
עיבוד 100K שורות

### צעדים
1. **העלה Bulk 60 גדול**
   - 100,000 שורות
   - 35MB

2. **הרץ Zero Sales**
   - Progress bar חלק
   - עדכוני אחוזים

3. **מדוד זמנים**
   - העלאה: < 5 שניות
   - ולידציה: < 2 שניות
   - עיבוד: < 10 שניות
   - סה"כ: < 20 שניות

### תוצאה צפויה
- ביצועים סבירים
- אין קריסות
- Progress bar informatif

---

## סיכום בדיקות קריטיות

| תרחיש | קריטי | מטרה |
|--------|-------|-------|
| Happy Path | ✅ | תהליך מלא עובד |
| Missing Portfolios | ✅ | ולידציה תקינה |
| File Too Large | ✅ | מגבלות גודל |
| Calculation Errors | ✅ | טיפול בשגיאות |
| Reset | ✅ | ניקוי State |
| Multiple Files | ⚠️ | גמישות |
| Performance | ⚠️ | ביצועים |
| Empty Files | ⚠️ | קלט לא תקין |