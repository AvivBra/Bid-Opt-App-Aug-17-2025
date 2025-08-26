# מסמך איפיון UI - Campaign Optimizer

## ⚠️ הערה חשובה מאוד
**בכל האפליקציה - לא להשתמש באייקונים/אימוג'י בכלל!**
- לא בתפריטים
- לא בכפתורים  
- לא בהודעות
- לא בכותרות
- **שום אייקון בשום מקום**

---

## דרישות כלליות
- העמוד זהה במראה ל-Bid Optimizer הקיים
- Layout: 6 עמודות [1, 7, 1, 1, 6, 2]
- כותרת בעמודה השנייה משמאל
- כל התוכן בעמודה החמישית (השנייה מימין)

---

## 1. Top Navigation Bar
### מיקום: 
- **position="top"** 

### תוכן:
- **Bids**
- **Campaigns**

### התנהגות:
- לחיצה מעבירה בין העמודים
- העמוד הנוכחי מודגש
- **ללא אייקונים**

---

## 2. Header (כותרת)
### מיקום:
- עמודה 2 (השנייה משמאל)

### טקסט:
```
Campaign Optimizer
```
- יישור לשמאל
- **שורה אחת**

---

## 3. תוכן העמוד (בעמודה 5)

### Section 1: Select Optimization
```html
<h3>1. Select Optimization</h3>
```
- **Radio button אחד בלבד:**
  - Campaign Creator (מסומן כברירת מחדל)
- בעתיד יהיו עוד אופציות

### רווח
```html
<div style='height: 150px;'></div>
```

### Section 2: Upload Files
```html
<h3>2. Upload Files</h3>
```

#### כפתורים:
1. **Download Template**
   - רוחב מלא
   - צבע: אפור (#DDDDDD)

2. **Upload Template** 
   - File uploader
   - מקבל רק xlsx

3. **Data Rova**
   - File uploader
   - פעיל

4. **Data Dive**
   - File uploader  
   - פעיל

### Section 3: Data Validation
- **מופיע רק אחרי העלאת Template**
```html
<h3>3. Data Validation</h3>
```
- הודעת success: "Template loaded"
- הודעת info: "Ready for processing!"

### Section 4: Process
- **כפתור Process Files**
  - רוחב מלא
  - צבע: אפור (#DDDDDD)
  - מופעל רק אחרי העלאת Template

### Section 5: Output Files
- **מופיע רק אחרי Process**
```html
<h3>5. Output Files</h3>
```
- **Download Campaign Bulk File**
  - רוחב מלא
  - צבע: אפור (#DDDDDD)

---

## מצבי UI

### מצב התחלתי:
- Campaign Creator מסומן
- Template לא הועלה
- Data Rova לא הועלה
- Data Dive לא הועלה
- Process disabled
- Validation לא מוצג
- Output לא מוצג

### אחרי העלאת Template:
- Validation section מופיע
- Process enabled (אם גם Data Rova ו-Data Dive הועלו)

### אחרי Process:
- Output section מופיע
- Download button enabled

---

## הערות למפתח:
1. **UI בלבד** - בלי לוגיקה אמיתית
2. Process יציג progress bar למשך 2 שניות (mock)
3. **לא להשתמש באייקונים בשום מקום**
4. להעתיק את המבנה מ-BidOptimizerPage
5. לשנות רק טקסטים וכפתורים רלוונטיים
6. **להשתמש רק ב-`apply_custom_css()` הקיים - לא להוסיף CSS חדש!**
7. כל הצבעים יבואו מההגדרות הגלובליות בלבד