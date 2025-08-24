# איפיון Validation Panel

## סקירה כללית

פאנל הוולידציה מופיע אוטומטית לאחר העלאת Template ו-Bulk 60. הפאנל מציג את תוצאות בדיקת התאימות בין הקבצים ומאפשר למשתמש להמשיך לעיבוד או לתקן שגיאות.

## מתי הפאנל מופיע

• אחרי העלאת Template + Bulk 60 בהצלחה
• לא מופיע אם חסר אחד הקבצים
• לא מופיע אם יש שגיאות קריאה בקבצים
• מתעדכן אוטומטית בכל העלאת Template חדש

## מצבי הפאנל

### מצב 1: Valid - הכל תקין

**תצוגה:**
• כותרת: DATA VALIDATION
• הודעת הצלחה עם נקודה ירוקה (#10B981)
• טקסט: "All portfolios valid"
• מספר שורות: "234,567 rows ready for processing"
• אופטימיזציה: "Zero Sales optimization selected"
• רקע הודעות: #404040
• טקסט הודעות: #E5E5E5

**כפתור Process Files:**
• מצב: Enabled
• רקע: #8B5CF6 (ויולט)
• טקסט: #E5E5E5
• מיקום: ממורכז
• רוחב: 200px
• גובה: 44px

### מצב 2: Missing Portfolios - חסרים פורטפוליוז

**תצוגה:**
• כותרת: DATA VALIDATION
• הודעת שגיאה עם נקודה אדומה (#EF4444)
• טקסט: "Missing portfolios found"
• הסבר: "The following portfolios are in the Bulk file but not in Template:"
• רשימת פורטפוליוז חסרים (כל אחד בשורה נפרדת עם bullet point)
• רקע הודעות: #404040
• טקסט הודעות: #E5E5E5

**כפתור Upload New Template:**
• מצב: Enabled
• רקע: #8B5CF6 (ויולט)
• טקסט: #E5E5E5
• מיקום: ממורכז
• טקסט נוסף: "(Bulk file will be kept in memory)"

**כפתור Process Files:**
• לא מוצג כלל

### מצב 3: Some Ignored - חלק מהפורטפוליוז ב-Ignore

**תצוגה:**
• כותרת: DATA VALIDATION
• הודעת מידע עם נקודה אפורה (#A1A1A1)
• טקסט: "Validation complete with notes"
• פירוט: "3 portfolios marked as Ignore"
• פירוט: "2 portfolios ready for processing"
• פירוט: "845 rows will be processed"
• רקע הודעות: #404040
• טקסט הודעות: #E5E5E5

**כפתור Process Files:**
• מצב: Enabled
• רקע: #8B5CF6 (ויולט)
• טקסט: #E5E5E5
• מיקום: ממורכז

### מצב 4: All Ignored - כל הפורטפוליוז ב-Ignore

**תצוגה:**
• כותרת: DATA VALIDATION
• הודעת שגיאה עם נקודה אדומה (#EF4444)
• טקסט: "All portfolios marked as Ignore"
• הסבר: "Cannot process - at least one portfolio must have numeric Base Bid"
• רקע הודעות: #404040
• טקסט הודעות: #E5E5E5

**כפתור Upload New Template:**
• מצב: Enabled
• רקע: #8B5CF6 (ויולט)
• טקסט: #E5E5E5

**כפתור Process Files:**
• לא מוצג כלל

## פורטפוליוז מותרים להיות חסרים

10 הפורטפוליוז הבאים מותר שיחסרו ב-Template (Case Sensitive):
• Flat 30
• Flat 25
• Flat 40
• Flat 25 | Opt
• Flat 30 | Opt
• Flat 20
• Flat 15
• Flat 40 | Opt
• Flat 20 | Opt
• Flat 15 | Opt

אם רק פורטפוליוז מהרשימה הזו חסרים, הוולידציה עוברת בהצלחה.

## בדיקות שמתבצעות

### בדיקת מבנה Template
• קיום לשונית Port Values
• 3 עמודות בסדר הנכון
• אין Portfolio Names כפולים

### בדיקת מבנה Bulk
• קיום Sheet "Sponsored Products Campaigns"
• בדיוק 48 עמודות
• לא יותר מ-500,000 שורות

### בדיקת התאמה
• כל Portfolio Name מ-Bulk (חוץ מ-Flat) קיים ב-Template
• לפחות פורטפוליו אחד עם Base Bid מספרי
• סינון שורות עם Units = 0

### ספירת שורות
• ספירה אחרי סינון Units = 0
• ספירה אחרי סינון Flat Portfolios
• ספירה אחרי סינון Ignore portfolios

## התנהגות מיוחדת

### העלאת Template חדש
• הוולידציה רצה מחדש אוטומטית
• ה-Bulk נשמר בזיכרון
• הודעות קודמות נמחקות
• אם התיקון מוצלח - עוברים למצב Valid

### ריענון אוטומטי
• כל שינוי בקבצים מריץ וולידציה מחדש
• אין צורך בלחיצה על כפתור refresh
• התוצאות מתעדכנות בזמן אמת

## אינטראקציה עם פאנלים אחרים

### השפעה על Output Panel
• לחיצה על Process Files מסתירה את Validation Panel
• מופיע Output Panel במקומו
• אין אפשרות לחזור לוולידציה בלי Reset

### השפעה על Upload Panel
• לחיצה על Upload New Template מחזירה ל-Upload Panel
• שומרת את ה-Bulk בזיכרון
• מאפסת את הוולידציה

## עיצוב

### מבנה
• רקע: #171717
• ללא גבולות
• ריפוד: 32px
• רווח מסקציות אחרות: 48px

### טיפוגרפיה
• כותרת: Inter Regular 400, 18px, UPPERCASE
• טקסט רגיל: Inter Regular 400, 14px
• רשימות: bullet points עם #E5E5E5

### צבעי הודעות
• כל ההודעות על רקע #404040
• נקודה ירוקה: #10B981 (תקין)
• נקודה אדומה: #EF4444 (שגיאה)
• נקודה אפורה: #A1A1A1 (מידע)
• טקסט: #E5E5E5

## הודעות מדויקות

### הודעות הצלחה
• "All portfolios valid"
• "X rows ready for processing"
• "Zero Sales optimization selected"

### הודעות שגיאה
• "Missing portfolios found"
• "All portfolios marked as Ignore"
• "No rows with Units = 0 found"

### הודעות מידע
• "X portfolios marked as Ignore"
• "Y portfolios ready for processing"
• "Z rows will be processed"

## הערות חשובות

• אין צביעה ורודה ב-UI
• הוולידציה רצה בתוך האופטימיזציה, לא לפניה
• 10 ה-Flat Portfolios תמיד מותרים לחסור
• Base Bid = "Ignore" הוא Case Sensitive