# מפרט אזור העלאה - Bid Optimizer

## 1. סקירה כללית

### מטרה
אזור העלאת הקבצים מאפשר למשתמש להעלות עד 5 קבצים שונים ולבחור אילו אופטימיזציות להריץ.

### רכיבים
- כפתור הורדת Template
- 5 כפתורי העלאה נפרדים
- רשימת אופטימיזציות לבחירה
- הודעות סטטוס לכל קובץ

## 2. פריסת האזור

```
┌─────────────────────────────────────────┐
│         UPLOAD YOUR FILES               │
├─────────────────────────────────────────┤
│                                         │
│  Template File:                        │
│  [📥 Download Template]                │
│  [📤 Upload Template]                  │
│  Status: ✓ template.xlsx (125 KB)      │
│                                         │
│  ─────────────────────────────          │
│                                         │
│  Bulk 30 File:                         │
│  [📤 Upload Bulk 30]                   │
│  Status: ✗ Not uploaded                │
│                                         │
│  ─────────────────────────────          │
│                                         │
│  Bulk 60 File:                         │
│  [📤 Upload Bulk 60]                   │
│  Status: ✓ bulk_60.xlsx (2.3 MB)       │
│                                         │
│  ─────────────────────────────          │
│                                         │
│  Bulk 7 File:                          │
│  [📤 Upload Bulk 7]                    │
│  Status: ✗ Not uploaded                │
│                                         │
│  ─────────────────────────────          │
│                                         │
│  Data Rova File:                       │
│  [📤 Upload Data Rova]                 │
│  Status: ✗ Not uploaded                │
│                                         │
└─────────────────────────────────────────┘
```

## 3. כפתור Download Template

### מאפיינים
- טקסט: "📥 Download Template"
- צבע: אדום (#FF0000)
- פעולה: הורדת קובץ Excel ריק

### Template מוּרד
```python
# 2 לשוניות:
1. "Port Values" - Portfolio Name | Base Bid | Target CPA
2. "Top ASINs" - ASIN
```

## 4. כפתורי העלאה

### מאפיינים משותפים
- צבע: אדום (#FF0000)
- טקסט לבן
- אייקון: 📤
- גובה: 40px
- מגבלה: 40MB

### 5 הכפתורים
1. Upload Template
2. Upload Bulk 30
3. Upload Bulk 60
4. Upload Bulk 7
5. Upload Data Rova

## 5. הודעות סטטוס

### מצבים אפשריים
```python
# לא הועלה
"✗ Not uploaded"

# הועלה בהצלחה
"✓ filename.xlsx (2.3 MB)"

# שגיאה
"❌ File exceeds 40MB limit"
"❌ Invalid file format"
"❌ Cannot read file"
```

### צבעים
- אפור: לא הועלה
- ירוק: הועלה בהצלחה
- אדום: שגיאה

## 6. Optimization Checklist

### פריסה
```
SELECT OPTIMIZATIONS TO APPLY:

☐ Zero Sales
☐ Portfolio Bid
☐ Budget Optimization
☐ Keyword Optimization
☐ ASIN Targeting
☐ Negative Targeting
☐ Campaign Structure
☐ Dayparting
☐ Placement Optimization
☐ Search Term Optimization
☐ Product Attribute Targeting
☐ Bid Adjustment Optimization
☐ Match Type Optimization
☐ Geographic Optimization
```

### התנהגות
- ברירת מחדל: כלום לא מסומן
- ניתן לבחור מרובים
- כל בחירה נשמרת ב-Session State

## 7. התנהגות בזמן העלאה

### תהליך
1. משתמש לוחץ על כפתור העלאה
2. נפתח file dialog
3. משתמש בוחר קובץ
4. מוצג spinner "Uploading..."
5. בדיקות בסיסיות (גודל, פורמט)
6. קריאת הקובץ
7. הצגת סטטוס

### בדיקות מיידיות
- גודל < 40MB
- פורמט .xlsx או .csv
- קובץ קריא

## 8. שמירה ב-Session State

```python
st.session_state['files'] = {
    'template': {
        'file': BytesIO,
        'name': 'template.xlsx',
        'size': 125000,
        'df': DataFrame
    },
    'bulk_30': None,  # לא הועלה
    'bulk_60': {
        'file': BytesIO,
        'name': 'bulk_60.xlsx',
        'size': 2300000,
        'df': DataFrame
    },
    'bulk_7': None,
    'data_rova': None
}

st.session_state['selected_optimizations'] = [
    'zero_sales',
    'portfolio_bid'
]
```

## 9. עיצוב ויזואלי

### כפתורים
```css
.upload-button {
    background-color: #FF0000;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    height: 40px;
    min-width: 150px;
}

.upload-button:hover {
    background-color: #CC0000;
}

.upload-button:disabled {
    background-color: #6c757d;
    cursor: not-allowed;
}
```

### הפרדה בין קבצים
- קו אופקי דק (#E0E0E0)
- מרווח 20px

### כרטיס קובץ
```css
.file-card {
    border: 1px solid #E0E0E0;
    padding: 15px;
    margin: 10px 0;
    border-radius: 4px;
    background: #FAFAFA;
}
```

## 10. הודעות שגיאה

### סוגי שגיאות
```python
# גודל
"❌ File exceeds 40MB limit (your file: 45.2MB)"

# פורמט
"❌ File must be Excel (.xlsx) or CSV format"

# מבנה
"❌ Template must have 'Port Values' sheet"
"❌ Bulk file must have 'Sponsored Products Campaigns' sheet"

# קריאה
"❌ Cannot read file - it may be corrupted"
```

### תצוגה
- תיבה אדומה
- טקסט ברור
- הנחיות לתיקון

## 11. אינטראקציות

### Hover States
- כפתורים: החשכה קלה
- Checkboxes: הדגשה

### Loading States
- Spinner בזמן העלאה
- כפתור מושבת
- טקסט "Uploading..."

### Success Feedback
- הודעה ירוקה
- צליל (אופציונלי)
- אנימציית checkmark

## 12. מקרי קצה

### החלפת קובץ
- העלאה חדשה מחליפה את הקודם
- אזהרה אם קובץ קיים

### קבצים ריקים
- הודעה: "File is empty"
- לא נשמר ב-State

### שמות קבצים ארוכים
- חיתוך ל-30 תווים
- Tooltip עם שם מלא