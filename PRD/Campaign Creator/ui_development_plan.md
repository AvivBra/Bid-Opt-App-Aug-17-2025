# תוכנית פיתוח UI בלבד - Campaign Optimizer

## שלב 1: הוספת העמוד לניווט
**מטרה:** להוסיף כניסה לעמוד החדש בתפריט  
**קבצים:**
- `app/navigation.py` - עדכון
- `app/main.py` - עדכון

**תוצאה:** תפריט עם 2 אופציות - Bid Optimizer ו-Campaign Optimizer

---

## שלב 2: יצירת העמוד עם כל ה-UI
**מטרה:** ליצור עמוד עם כל האלמנטים הויזואליים  
**קבצים:**
- `app/pages/campaign_optimizer.py` - חדש
- `config/ui_text.py` - עדכון

**תוצאה:** עמוד מלא עם כל הכפתורים והאזורים הנדרשים

---

## שלב 3: הוספת Sidebar מכווץ
**מטרה:** sidebar שמתחיל מכווץ  
**קבצים:**
- `app/main.py` - עדכון (הוספת initial_sidebar_state)

**תוצאה:** האפליקציה נפתחת עם sidebar מכווץ