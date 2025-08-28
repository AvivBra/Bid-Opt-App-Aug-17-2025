# איפיון Output Panel

## סקירה כללית

פאנל הפלט מופיע לאחר לחיצה על Process Files ומציג את התקדמות העיבוד, תוצאות הסופיות וכפתורי הורדה לקבצים שנוצרו.

## מתי הפאנל מופיע

• מיד אחרי לחיצה על Process Files ב-Validation Panel
• מחליף את Validation Panel
• נשאר גלוי עד ללחיצה על Reset

## מצבי הפאנל

### מצב 1: Processing - במהלך עיבוד

**תצוגה:**
• כותרת: OUTPUT FILES
• טקסט: "Processing Zero Sales optimization..."
• Progress bar עם אחוזים (0-100%)
• צבע Progress bar: #8B5CF6 (ויולט)
• רקע Progress bar: #171717
• זמן שחלף: "Time elapsed: 00:45"
• זמן משוער: "Estimated remaining: 00:24"

**התנהגות Progress Bar:**
• עדכון כל 500ms
• אנימציה חלקה
• אין אפשרות לביטול
• אם תקוע על 100% יותר מ-5 שניות - הודעת שגיאה

### מצב 2: Complete - עיבוד הושלם בהצלחה

**תצוגה:**
• כותרת: OUTPUT FILES
• הודעת הצלחה עם נקודה ירוקה (#10B981)
• טקסט: "Processing complete"
• רקע הודעה: #404040
• טקסט הודעה: #E5E5E5

**סטטיסטיקות:**
• Rows processed: 234,567
• Rows modified: 45,678
• Processing time: 1:09
• צבע טקסט: #E5E5E5

**הודעה על שגיאות חישוב:**
• אם יש שגיאות: "234 calculation errors found (marked in Excel file)"
• נקודה כתומה (#F59E0B)
• רקע: #404040
• טקסט: #E5E5E5
• ללא קופסה ורודה ב-UI

**פרטי קבצים שנוצרו:**
• Working File: 14.2 MB (2 sheets)
• Clean File: [Coming Soon]
• צבע טקסט: #E5E5E5

**כפתורי הורדה:**
• DOWNLOAD WORKING FILE - Enabled
• DOWNLOAD CLEAN - Disabled עם "[Coming Soon]"
• רקע כפתור פעיל: #8B5CF6
• רקע כפתור מושבת: #171717
• טקסט פעיל: #E5E5E5
• טקסט מושבת: #171717
• מיקום: 2 כפתורים זה לצד זה
• רוחב: 200px כל אחד
• גובה: 44px

**כפתור Reset:**
• מיקום: ממורכז מתחת לכפתורי ההורדה
• רקע: #171717
• טקסט: #E5E5E5
• רוחב: 200px
• גובה: 44px

### מצב 3: Error - שגיאה בעיבוד

**תצוגה:**
• כותרת: OUTPUT FILES
• הודעת שגיאה עם נקודה אדומה (#EF4444)
• טקסט: "Processing failed"
• סיבה: הודעה ספציפית לשגיאה
• רקע הודעה: #404040
• טקסט הודעה: #E5E5E5

**כפתורי פעולה:**
• RETRY - לנסות שוב את העיבוד
• RESET - לחזור להתחלה
• רקע: #8B5CF6
• טקסט: #E5E5E5
• מיקום: זה לצד זה

## שמות קבצי הפלט

### Working File
פורמט: `Auto Optimized Bulk | Working | YYYY-MM-DD | HH-MM.xlsx`
דוגמה: `Auto Optimized Bulk | Working | 2025-08-18 | 14-30.xlsx`

### Clean File (TBC)
פורמט: `Auto Optimized Bulk | Clean | YYYY-MM-DD | HH-MM.xlsx`
כרגע מושבת - Coming Soon

## מבנה קבצי הפלט

### Working File - 2 לשוניות
• **Targeting:** Keywords + Product Targeting עם 48 עמודות + 7 עמודות עזר
• **Bidding Adjustment:** 48 עמודות בלבד, ללא עמודות עזר

### עמודות העזר (רק ב-Targeting)
• Old Bid
• calc1
• calc2
• Target CPA
• Base Bid
• Adj. CPA
• Max BA

### צביעה בקובץ Excel
• שורות עם Bid < 0.02 - רקע ורוד (#FFE4E1)
• שורות עם Bid > 1.25 - רקע ורוד (#FFE4E1)
• שורות עם Clicks > 15 ו-Units = 0 - רקע ורוד (#FFE4E1)
• שגיאות חישוב (NaN) - רקע ורוד (#FFE4E1)

**חשוב:** הצביעה הורודה קיימת רק בקובץ Excel, לא ב-UI!

## זמני עיבוד צפויים

• עד 10,000 שורות: 5-10 שניות
• 10,000-50,000 שורות: 10-30 שניות
• 50,000-200,000 שורות: 30-60 שניות
• 200,000-500,000 שורות: 60-120 שניות

אם העיבוד חורג מ-3 דקות, מופיעה אזהרה.

## התנהגות מיוחדת

### הורדת קבצים
• לחיצה על Download פותחת דיאלוג שמירה
• שם ברירת מחדל כולל תאריך ושעה
• אפשר להוריד כמה פעמים
• הקבצים נשמרים בזיכרון עד Reset

### כפתור Reset
• מאפס את כל המערכת
• חוזר ל-Upload Panel
• מוחק את כל הקבצים מהזיכרון
• דורש אישור: "Are you sure? All data will be lost"

### טיפול בשגיאות
• Timeout אחרי 5 דקות
• שגיאת זיכרון אם הקובץ גדול מדי
• שגיאת חישוב אם יש בעיה בנוסחאות

## אינטראקציה עם פאנלים אחרים

### חזרה ל-Upload Panel
• רק דרך כפתור Reset
• אין אפשרות לחזור אחורה בלי לאבד נתונים

### שמירת מצב
• התוצאות נשמרות ב-Session State
• אפשר לרענן את הדף בלי לאבד תוצאות
• נמחק רק ב-Reset או סגירת הדפדפן

## עיצוב

### מבנה
• רקע: #171717
• ללא גבולות
• ריפוד: 32px
• רווח מסקציות אחרות: 48px

### Progress Bar
• גובה: 8px
• רוחב: 100%
• Border radius: 4px
• צבע מילוי: #8B5CF6
• צבע רקע: #171717

### טיפוגרפיה
• כותרת: Inter Regular 400, 18px, UPPERCASE
• סטטיסטיקות: Inter Regular 400, 14px
• זמנים: Inter Regular 400, 12px
• כל הטקסטים: #E5E5E5

## הודעות למשתמש

### הודעות במהלך עיבוד
• "Processing Zero Sales optimization..."
• "Filtering portfolios..."
• "Calculating new bids..."
• "Generating output files..."

### הודעות סיום
• "Processing complete"
• "Files generated successfully"

### הודעות שגיאה
• "Processing failed: Out of memory"
• "Processing failed: Timeout exceeded"
• "Processing failed: Invalid data format"

## הערות חשובות

• אין הודעה ורודה ב-UI - רק ציון מספר השגיאות
• Clean File כרגע לא זמין (TBC)
• אין אפשרות לעצור עיבוד באמצע
• כל השורות בפלט מקבלות Operation = "Update"
• הצביעה הורודה נשמרת בקובץ Excel עצמו