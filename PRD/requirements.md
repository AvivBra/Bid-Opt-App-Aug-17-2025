# דרישות מערכת Bid Optimizer

## דרישות עסקיות

### מטרת המערכת
אוטומציה של תהליך אופטימיזציית Bids עבור קמפיינים ב-Amazon Ads, החלפת עבודה ידנית ב-Excel שלוקחת שעות בתהליך אוטומטי של דקות.

### משתמשי היעד
• מנהלי PPC בחברות ניהול קמפיינים
• מנהלי חשבונות Amazon Ads
• צוותים המנהלים מספר רב של פורטפוליוז

### ערך עסקי
• חיסכון של 90% בזמן עבודה
• הפחתת טעויות אנוש בחישובים
• סטנדרטיזציה של תהליכי אופטימיזציה
• יכולת לעבד קבצים גדולים (עד 500,000 שורות)

## דרישות פונקציונליות

### העלאת קבצים

**Template File:**
• פורמט: Excel (.xlsx) בלבד
• גודל מקסימלי: 1MB
• 2 לשוניות חובה: Port Values, Top ASINs
• 3 עמודות ב-Port Values: Portfolio Name, Base Bid, Target CPA
• Portfolio Names ייחודיים
• Base Bid: מספר 0.02-4 או "Ignore"
• Target CPA: מספר 0.01-4 או ריק

**Bulk Files:**
• פורמט: Excel (.xlsx) או CSV
• גודל מקסימלי: 40MB
• Sheet נדרש: "Sponsored Products Campaigns"
• בדיוק 48 עמודות בסדר קבוע
• עד 500,000 שורות
• כרגע רק Bulk 60 פעיל (Bulk 7/30 - TBC)

### אופטימיזציות

**Zero Sales (פעיל):**
• מזהה מוצרים עם Units = 0
• מחשב Bid חדש לפי 4 מקרים
• מסנן 10 Flat Portfolios
• מסנן פורטפוליוז עם Base Bid = "Ignore"
• מוסיף 7 עמודות עזר ב-Working File

**13 אופטימיזציות נוספות (TBC):**
• Portfolio Bid Optimization
• Budget Optimization
• Keyword Optimization
• ASIN Targeting
• ועוד 9 ללא שמות מוגדרים

### קבצי פלט

**Working File (פעיל):**
• שם: `Auto Optimized Bulk | Working | YYYY-MM-DD | HH-MM.xlsx`
• 2 לשוניות: Targeting, Bidding Adjustment
• 48 עמודות מקוריות + 7 עמודות עזר (רק ב-Targeting)
• שורות בעייתיות מסומנות בורוד בקובץ Excel

**Clean File (TBC):**
• ללא עמודות עזר
• מוכן להעלאה ישירה ל-Amazon

### וולידציה

**בדיקות Template:**
• מבנה נכון (לשוניות ועמודות)
• אין כפילויות ב-Portfolio Names
• ערכי Base Bid תקינים
• לפחות פורטפוליו אחד לא ב-Ignore

**בדיקות Bulk:**
• 48 עמודות בדיוק
• לא יותר מ-500,000 שורות
• Sheet נכון קיים

**בדיקות התאמה:**
• כל פורטפוליו מ-Bulk קיים ב-Template (חוץ מ-10 Flat Portfolios)
• יש שורות עם Units = 0

## דרישות לא-פונקציונליות

### ביצועים
• עיבוד עד 10,000 שורות: מקסימום 10 שניות
• עיבוד עד 100,000 שורות: מקסימום 30 שניות
• עיבוד עד 500,000 שורות: מקסימום 120 שניות
• זמן תגובה UI: מתחת ל-200ms

### זמינות
• אפליקציה Desktop בלבד (לא שרת)
• עבודה Offline מלאה
• אין תלות בשירותים חיצוניים (חוץ מ-Data Rova - TBC)

### אמינות
• שמירת נתונים ב-Session State
• התאוששות משגיאות ללא קריסה
• Timeout אחרי 5 דקות עיבוד

### שימושיות
• ממשק Dark Mode עם accent ויולט
• כל הטקסטים באנגלית
• הודעות שגיאה ברורות
• Progress bar בזמן עיבוד
• Desktop בלבד (מינימום 1024px רוחב)

### אבטחה
• אין שמירת נתונים על דיסק
• כל הנתונים בזיכרון בלבד
• ניקוי זיכרון ב-Reset
• אין שליחת נתונים לשרתים חיצוניים

## מגבלות טכניות

### מגבלות קבצים
• Template: עד 1MB
• Bulk: עד 40MB
• מספר שורות: עד 500,000
• מספר עמודות: בדיוק 48

### מגבלות ערכים
• Bid: 0.02 עד 1.25 (מחוץ לטווח = ורוד)
• Base Bid: 0.02 עד 4
• Target CPA: 0.01 עד 4
• Portfolio Name: עד 255 תווים

### מגבלות סביבה
• Python 3.8+
• RAM: מינימום 4GB
• מקום בדיסק: 100MB לאפליקציה
• רזולוציה: מינימום 1024x768

## דרישות ממשק משתמש

### עיצוב
• Dark Mode בהשראת shadcn UI
• צבעים: רקע #0A0A0A, כרטיסים #171717, טקסט #E5E5E5
• Accent color: ויולט #8B5CF6
• ללא אייקונים או אימוג'ים
• גבולות שקופים

### ניווט
• Sidebar Navigation (לא Stepper!)
• 2 עמודים: Bid Optimizer (פעיל), Campaigns Optimizer (TBC)
• רוחב Sidebar: 200px קבוע

### הודעות
• כל ההודעות על רקע #404040
• נקודה צבעונית לסוג ההודעה
• טקסט תמיד #E5E5E5
• אין הודעות ורודות ב-UI (רק ב-Excel)

## אינטגרציות

### Amazon Ads
• תאימות מלאה לפורמט Bulk Files
• שמירת כל 48 העמודות
• Operation = "Update" לכל השורות

### Data Rova (TBC)
• Benchmarking data
• API integration
• כרגע לא מיושם

## סדרי עדיפויות פיתוח

### Phase 1 (נוכחי)
• Bid Optimizer עם Zero Sales בלבד
• Working File בלבד
• Bulk 60 בלבד

### Phase 2-3 (TBC)
• 13 אופטימיזציות נוספות
• Clean File
• Bulk 7/30

### Phase 4-6 (TBC)
• Campaigns Optimizer
• Negation & Harvesting
• Data Rova Integration

## קריטריוני קבלה

### להשלמת Phase 1
• Zero Sales עובד נכון על קבצים עד 500K שורות
• זמני עיבוד בתוך היעדים
• Working File עם עמודות עזר נכונות
• שורות בעייתיות מסומנות בורוד ב-Excel
• UI עובד ללא תקלות

### בדיקות נדרשות
• בדיקת חישובים ב-4 המקרים
• בדיקת סינון 10 Flat Portfolios
• בדיקת Ignore portfolios
• בדיקת קבצים גדולים
• בדיקת שגיאות והתאוששות