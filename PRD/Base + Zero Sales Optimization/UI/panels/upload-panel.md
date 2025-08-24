# איפיון Upload Panel

## סקירה כללית

פאנל העלאת הקבצים מאפשר למשתמש להעלות את קבצי הנתונים הנדרשים לביצוע אופטימיזציות. הפאנל כולל כפתורי העלאה לסוגי קבצים שונים ומציג סטטוס של הקבצים שהועלו.

## מבנה הפאנל

### כותרת
• טקסט: UPLOAD FILES
• פונט: Inter Regular 400, 18px, UPPERCASE
• צבע: #E5E5E5
• יישור: מרכז

### אזור בחירת אופטימיזציות
• כותרת משנה: SELECT OPTIMIZATIONS
• Checkbox יחיד: "Zero Sales" (מסומן כברירת מחדל)
• טקסט נוסף: "(13 additional optimizations coming soon)"
• צבע טקסט: #E5E5E5
• רקע: #171717
• ללא גבולות

## כפתורי העלאה

### סידור הכפתורים
• שורה ראשונה: UPLOAD TEMPLATE | BULK 60 DAYS
• שורה שנייה: BULK 30 DAYS | BULK 7 DAYS
• שורה שלישית: DATA ROVA (ממורכז)

### מצבי כפתורים

**כפתורים פעילים:**
• UPLOAD TEMPLATE - enabled
• BULK 60 DAYS - enabled
• רקע: #8B5CF6 (ויולט)
• טקסט: #E5E5E5
• Hover: #7C3AED

**כפתורים מושבתים:**
• BULK 30 DAYS - disabled עם "[Coming Soon]"
• BULK 7 DAYS - disabled עם "[Coming Soon]"
• DATA ROVA - disabled עם "[Coming Soon]"
• רקע: #171717
• טקסט: #171717 (אפור כהה)
• אין Hover

### מידות כפתורים
• רוחב: 200px
• גובה: 44px
• ריווח: 16px בין כפתורים
• Border radius: 4px

## תהליך העלאה

### לחיצה על כפתור פעיל
1. נפתח דיאלוג בחירת קובץ
2. סוגי קבצים מותרים: .xlsx, .csv
3. לאחר בחירה - הקובץ נקרא ומאומת

### וולידציה מיידית

**Template:**
• גודל מקסימלי: 1MB
• חייב להכיל 2 לשוניות: "Port Values", "Top ASINs"
• 3 עמודות ב-Port Values: Portfolio Name, Base Bid, Target CPA

**Bulk 60:**
• גודל מקסימלי: 40MB
• חייב להכיל Sheet: "Sponsored Products Campaigns"
• בדיוק 48 עמודות
• עד 500,000 שורות

## הודעות סטטוס

### לפני העלאה
• Template: Not uploaded
• Bulk 60: Not uploaded
• צבע: #171717 (טקסט משני)

### אחרי העלאה מוצלחת
• Template: template_name.xlsx (125 KB)
• Bulk 60: bulk_60_days.xlsx (12.3 MB)
• צבע: #E5E5E5 עם נקודה ירוקה (#10B981)

### שגיאות העלאה

**גודל חורג:**
• הודעה: "File exceeds 40MB limit" (Bulk) או "File exceeds 1MB limit" (Template)
• רקע: #404040
• נקודה: אדומה (#EF4444)
• טקסט: #E5E5E5

**פורמט שגוי:**
• הודעה: "File must be Excel (.xlsx) or CSV"
• רקע: #404040
• נקודה: אדומה (#EF4444)
• טקסט: #E5E5E5

**קובץ פגום:**
• הודעה: "Cannot read file - may be corrupted"
• רקע: #404040
• נקודה: אדומה (#EF4444)
• טקסט: #E5E5E5

**מבנה שגוי:**
• Template: "Missing 'Port Values' sheet" או "Template must have 3 columns"
• Bulk: "Missing 'Sponsored Products Campaigns' sheet" או "File must have 48 columns"
• רקע: #404040
• נקודה: אדומה (#EF4444)
• טקסט: #E5E5E5

## התנהגות מיוחדת

### שמירת קבצים בזיכרון
• קבצים שהועלו נשמרים ב-Session State
• החלפת קובץ מאפסת את תהליך הוולידציה
• Bulk נשמר גם אם מעלים Template חדש

### הגבלות
• אפשר להעלות רק Bulk 60 אחד בכל פעם
• אפשר להעלות רק Template אחד בכל פעם
• אין אפשרות להעלות מספר קבצים במקביל

## אינטראקציה עם פאנלים אחרים

### השפעה על Validation Panel
• העלאת Template + Bulk 60 מפעילה את Validation Panel
• העלאת Template בלבד לא מפעילה וולידציה
• העלאת Bulk בלבד לא מפעילה וולידציה

### השפעה על כפתור Process
• כפתור Process נשאר disabled עד שיש Template + Bulk תקינים
• כפתור Process נשאר disabled אם כל הפורטפוליוז ב-Ignore

## עיצוב

### צבעים
• רקע פאנל: #171717
• רקע ראשי: #0A0A0A
• טקסט ראשי: #E5E5E5
• טקסט משני: #171717
• הודעות: רקע #404040
• ללא גבולות (transparent borders)

### Typography
• כותרות: Inter Regular 400, 18px, UPPERCASE
• טקסט רגיל: Inter Regular 400, 14px
• סטטוס: Inter Regular 400, 12px

## הערות חשובות

• אין להציג שמות של 13 האופטימיזציות הנוספות
• רק Zero Sales checkbox מוצג
• כפתורי Coming Soon נראים אבל מושבתים
• אין צביעה ורודה ב-UI (רק בקובץ Excel)
• כל ההודעות עם רקע אפור כהה אחיד