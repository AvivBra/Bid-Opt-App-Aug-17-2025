# שלב 2: Sidebar Navigation
**משך: 1 יום**

## מטרת השלב
בניית Sidebar עם ניווט בין 2 עמודים - Bid Optimizer (פעיל) ו-Campaigns Optimizer (מושבת). בסוף השלב יהיה ניווט עובד עם עיצוב Dark Mode.

## רשימת קבצים לפיתוח (3 קבצים)

### 1. app/navigation.py
**פונקציות:**
- `render_navigation()` - מציג את אפשרויות הניווט ב-sidebar
- `get_current_page()` - מחזיר את העמוד הנוכחי הנבחר
- `set_page()` - מעדכן את העמוד הנוכחי ב-state
- `is_page_enabled()` - בודק אם עמוד מסוים פעיל או מושבת

### 2. app/ui/sidebar.py
**פונקציות:**
- `render_sidebar()` - בונה את כל ה-sidebar עם כפתורים
- `create_nav_button()` - יוצר כפתור ניווט בודד עם סטיילינג
- `apply_sidebar_styles()` - מחיל CSS לעיצוב ה-sidebar
- `set_sidebar_width()` - קובע רוחב קבוע של 200px

### 3. app/ui/layout.py
**פונקציות:**
- `setup_page_layout()` - מגדיר את מבנה הדף הכללי
- `apply_dark_theme()` - מחיל עיצוב dark mode על כל הדף
- `set_content_margins()` - קובע מרווחים לתוכן הראשי
- `inject_custom_css()` - מזריק CSS מותאם אישית לדף

## בדיקות משתמש

1. **הופעת Sidebar**
   - Sidebar מופיע בצד שמאל
   - רוחב קבוע 200 פיקסלים
   - רקע כהה יותר מהדף הראשי

2. **כפתורי ניווט**
   - BID OPTIMIZER כפתור פעיל וניתן ללחיצה
   - CAMPAIGNS OPTIMIZER מושבת עם Coming Soon
   - צבע ויולט לכפתור פעיל

3. **תגובה ללחיצות**
   - לחיצה על BID OPTIMIZER לא משנה כלום
   - לחיצה על CAMPAIGNS מושבת לא עושה כלום

## בדיקות מתכנת

1. **בדיקת state**
   - current_page מאותחל ל-bid_optimizer
   - navigation לא מאפשר מעבר לעמוד מושבת
   - state נשמר בין רענונים

2. **בדיקת CSS**
   - sidebar width מוגדר ל-200px
   - background-color של sidebar הוא #171717
   - כפתורים מושבתים עם opacity נמוך

3. **בדיקת פונקציונליות**
   - render_navigation מחזיר ערך נכון
   - is_page_enabled מחזיר False ל-campaigns
   - כפתורים מעדכנים state בלחיצה

## מה המשתמש רואה

### מה עובד:
- Sidebar עם 2 כפתורים
- עיצוב Dark Mode
- כפתור אחד פעיל
- Layout נכון

### מה עדיין משובש:
- אין תוכן בעמוד הראשי
- אין Upload Panel
- אין פונקציונליות
- כפתורים לא עושים כלום מעשי
- רק מבנה ויזואלי

---
**תאריך: דצמבר 2024, 12:45**