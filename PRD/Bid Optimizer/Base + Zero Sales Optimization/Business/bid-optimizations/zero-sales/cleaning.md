# אופטימיזציית Zero Sales - ניקוי וסינון

## סדר פעולות הניקוי

### שלב 1: חלוקה לפי Entity Type
- **Targeting sheet:** שורות עם Entity = Keyword או Product Targeting (יעברו ניקוי)
- **Bidding Adjustment sheet:** שורות עם Entity = Bidding Adjustment (נשארות ללא שינוי)
- **כל Entity אחר:** השורה נמחקת (למשל Product Ad)

### שלב 2: סינון ב-Targeting בלבד

#### סינון לפי Units
- כל שורה שאינה Units = 0 נמחקת

#### סינון פורטפוליוז מוחרגים
הסרת 10 הפורטפוליוז הבאים (השוואה Case Sensitive):
- Flat 30, Flat 25, Flat 40
- Flat 25 | Opt, Flat 30 | Opt
- Flat 20, Flat 15
- Flat 40 | Opt, Flat 20 | Opt, Flat 15 | Opt

#### סינון פורטפוליוז עם Ignore
- הסרת פורטפוליוז שב-Template מסומנים עם Base Bid = "Ignore"

#### סינון לפי State
כל שורה שלא מכילה "enabled" באחת מהעמודות הבאות נמחקת:
- State
- Campaign State (Informational only)
- Ad Group State (Informational only)

## בדיקת ערכים מספריים

כל שורה שאינה מכילה ערך מספרי תקין בעמודות הבאות:
- **Bid**
- **Clicks**
- **Units**
- **Percentage**

התוצאה: הכתיבה "Error" בעמודת Bid וצביעת השורה בורוד

## טיפול בערכים חסרים

### עמודות קריטיות
אם חסר ערך באחת מהעמודות הבאות:
- Entity
- Portfolio Name
- Campaign ID

התוצאה: הכתיבה "Error" בעמודת Bid וצביעת השורה בורוד

## הודעות שגיאה בשלב הניקוי

### שגיאות שגורמות לסימון השורה בורוד ו-"Error" ב-Bid:
- **"Missing Entity"** - העמודה Entity ריקה
- **"Missing Portfolio"** - העמודה Portfolio Name ריקה
- **"Missing Campaign ID"** - העמודה Campaign ID ריקה
- **"Invalid Bid Value"** - ערך לא מספרי בעמודת Bid
- **"Invalid Clicks Value"** - ערך לא מספרי בעמודת Clicks
- **"Invalid Units Value"** - ערך לא מספרי בעמודת Units
- **"Invalid Percentage Value"** - ערך לא מספרי בעמודת Percentage
- **"Portfolio Not Found"** - הפורטפוליו לא קיים ב-Template
- **"Multiple Errors"** - יותר משגיאה אחת באותה שורה

### מאפיינים שגורמים למחיקת השורה:
- Entity שאינו Keyword/Product Targeting/Bidding Adjustment
- Units שאינו 0
- פורטפוליו מרשימת ה-Flat portfolios
- פורטפוליו עם Base Bid = "Ignore"
- State שאינו "enabled" (באחת מ-3 העמודות)

## מה נשמר ללא שינוי
- כל שורות Bidding Adjustment
- כל 48 כותרות העמודות (כולל Informational)
- סדר העמודות המקורי

## בדיקות אחרי ניקוי
- נשארה לפחות שורה אחת לעיבוד
- כל הפורטפוליוז שנשארו קיימים ב-Template
- כל השורות ב-Targeting עם Units = 0
- רק Keyword ו-Product Targeting ב-Targeting
- אין פורטפוליוז מוחרגים בנתונים הסופיים