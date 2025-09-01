# סדר זרימת הפעולות - Portfolio Optimizer
## תאריך: 30 באוגוסט 2025 | שעה: 15:10

## 🚀 **שלב 1: הצגת הדף**
1. **app/main.py** → בוחר לנווט ל-Portfolio Optimizer
2. **app/navigation.py** → טוען את הדף הנכון
3. **app/components/portfolio_optimizer.py** → מציג את הממשק
4. **business/portfolio_optimizations/factory.py** → מחזיר רשימת אופטימיזציות זמינות
5. **app/components/portfolio_optimizer.py** → מציג צ'קבוקסים דינמית

**📦 Session State:**
- ריק לחלוטין

---

## ✅ **שלב 2: בחירת אופטימיזציות**
6. **משתמש** → מסמן Empty Portfolios + Campaigns w/o Portfolios
7. **app/components/portfolio_optimizer.py** → אוסף את הבחירות
8. **app/state/portfolio_state.py** → שומר את הבחירות

**📦 Session State:**
- רשימת אופטימיזציות שנבחרו
- סטטוס המערכת: ממתינה לקובץ

---

## 📤 **שלב 3: העלאת קובץ**
9. **משתמש** → מעלה קובץ Bulk 60
10. **app/components/portfolio_optimizer.py** → מקבל את הקובץ
11. **data/readers/excel_reader.py** → קורא ומפרק לגיליונות
12. **data/validators/bulk_validator.py** → מאמת שהקובץ תקין
13. **app/state/portfolio_state.py** → שומר את הנתונים בסשן

**📦 Session State:**
- רשימת אופטימיזציות שנבחרו
- הקובץ המקורי שהועלה
- כל הגיליונות מפורקים לטבלאות
- שם הקובץ המקורי
- זמן ההעלאה
- סטטוס המערכת: מוכן לעיבוד

---

## ⚙️ **שלב 4: עיבוד - לחיצה על Process**
14. **משתמש** → לוחץ על כפתור Process Files
15. **app/components/portfolio_optimizer.py** → מתחיל תהליך
16. **app/components/portfolio_optimizer.py** → קורא ל-orchestrator

### 🔍 **תת-שלב 4.0: ולידציה וניקוי כללי**
17. **business/portfolio_optimizations/orchestrator.py** → קורא ל-validate_data (פונקציה פנימית)
18. **business/portfolio_optimizations/orchestrator.py** → קורא ל-clean_data (פונקציה פנימית)
19. **business/portfolio_optimizations/orchestrator.py** → בודק גיליונות (בדיקה פנימית)

**📦 Session State בסוף 4.0:**
- רשימת אופטימיזציות שנבחרו
- הקובץ המקורי
- הגיליונות המקוריים
- גיליונות מנוקים (ללא רווחים מיותרים)
- שם הקובץ המקורי
- זמן ההעלאה
- סטטוס: בעיבוד
- השלב הנוכחי: ולידציה

### 🔄 **תת-שלב 4.1: הפעלת אסטרטגיה ראשונה (Empty Portfolios)**
20. **business/portfolio_optimizations/orchestrator.py** → קורא ל-factory.create_strategy('empty_portfolios')
21. **business/portfolio_optimizations/factory.py** → טוען את קלאס EmptyPortfoliosStrategy
22. **business/portfolio_optimizations/factory.py** → מחזיר instance של האסטרטגיה
23. **business/portfolio_optimizations/orchestrator.py** → קורא ל-strategy.run(data)
24. **business/portfolio_optimizations/strategies.py** → מריץ EmptyPortfoliosStrategy.run()
25. **business/portfolio_optimizations/strategies.py** → מחזיר OptimizationResult
26. **business/portfolio_optimizations/orchestrator.py** → שולח תוצאה ל-results_manager.add_result()
27. **business/portfolio_optimizations/results_manager.py** → שומר את התוצאה

**📦 Session State בסוף 4.1:**
- רשימת אופטימיזציות שנבחרו
- הקובץ המקורי
- הגיליונות המקוריים
- גיליונות מנוקים
- תוצאות אופטימיזציה ראשונה (פאטץ׳ של פורטפוליוז ריקים)
- מטריקות: כמה פורטפוליוז עודכנו
- הודעות: מה נמצא ומה בוצע
- שם הקובץ המקורי
- זמן ההעלאה
- סטטוס: בעיבוד
- השלב הנוכחי: מריץ אופטימיזציית פורטפוליוז ריקים

### 🔄 **תת-שלב 4.2: הפעלת אסטרטגיה שנייה (Campaigns w/o Portfolios)**
28. **business/portfolio_optimizations/orchestrator.py** → קורא ל-factory.create_strategy('campaigns_without_portfolios')
29. **business/portfolio_optimizations/factory.py** → טוען את קלאס CampaignsWithoutPortfoliosStrategy
30. **business/portfolio_optimizations/factory.py** → מחזיר instance של האסטרטגיה
31. **business/portfolio_optimizations/orchestrator.py** → קורא ל-strategy.run(data)
32. **business/portfolio_optimizations/strategies.py** → מריץ CampaignsWithoutPortfoliosStrategy.run()
33. **business/portfolio_optimizations/strategies.py** → מחזיר OptimizationResult
34. **business/portfolio_optimizations/orchestrator.py** → שולח תוצאה ל-results_manager.add_result()
35. **business/portfolio_optimizations/results_manager.py** → שומר את התוצאה

**📦 Session State בסוף 4.2:**
- רשימת אופטימיזציות שנבחרו
- הקובץ המקורי
- הגיליונות המקוריים
- גיליונות מנוקים
- תוצאות אופטימיזציה ראשונה (פורטפוליוז ריקים)
- תוצאות אופטימיזציה שנייה (קמפיינים ללא פורטפוליו)
- מטריקות משתי האופטימיזציות
- הודעות משתי האופטימיזציות
- שם הקובץ המקורי
- זמן ההעלאה
- סטטוס: בעיבוד
- השלב הנוכחי: מריץ אופטימיזציית קמפיינים ללא פורטפוליו

### 🔀 **תת-שלב 4.3: מיזוג תוצאות**
36. **business/portfolio_optimizations/orchestrator.py** → קורא ל-results_manager.merge_all()
37. **business/portfolio_optimizations/results_manager.py** → קורא ל-merge_patch() לכל תוצאה
38. **business/portfolio_optimizations/results_manager.py** → מזהה קונפליקטים
39. **business/portfolio_optimizations/results_manager.py** → מיישם כלל "האחרון גובר"
40. **business/portfolio_optimizations/results_manager.py** → יוצר דוח עם conflicts_log
41. **business/portfolio_optimizations/results_manager.py** → מחזיר נתונים ממוזגים ל-orchestrator
42. **business/portfolio_optimizations/orchestrator.py** → מחזיר הכל ל-portfolio_optimizer.py

**📦 Session State בסוף 4.3:**
- רשימת אופטימיזציות שנבחרו
- הקובץ המקורי
- הגיליונות המקוריים
- גיליונות מנוקים
- תוצאות שתי האופטימיזציות
- נתונים ממוזגים סופיים (גיליונות קמפיינים ופורטפוליוז מעודכנים)
- רשימת אינדקסים של שורות שהשתנו בכל גיליון
- דוח ריצה כולל (כמה אופטימיזציות רצו, כמה שורות עודכנו, זמן ביצוע)
- לוג קונפליקטים (אם היו)
- שם הקובץ המקורי
- זמן ההעלאה
- סטטוס: עיבוד הושלם
- השלב הנוכחי: מיזוג הושלם

---

## 📝 **שלב 5: יצירת קובץ פלט**
43. **business/portfolio_optimizations/orchestrator.py** → קורא ל-service.create_output_file()
44. **business/portfolio_optimizations/service.py** → מקבל נתונים סופיים
45. **business/portfolio_optimizations/service.py** → קורא ל-excel_writer.write()
46. **data/writers/excel_writer.py** → יוצר קובץ אקסל
47. **data/writers/excel_writer.py** → מוסיף צבע צהוב לשורות שהשתנו
48. **data/writers/excel_writer.py** → מחזיר BytesIO ל-service
49. **business/portfolio_optimizations/service.py** → מחזיר BytesIO ל-orchestrator
50. **business/portfolio_optimizations/orchestrator.py** → מחזיר ל-portfolio_optimizer
51. **app/components/portfolio_optimizer.py** → קורא ל-portfolio_state.save_output()
52. **app/state/portfolio_state.py** → שומר קובץ בסשן

**📦 Session State:**
- כל האובייקטים הקודמים
- קובץ אקסל מוכן להורדה (בזיכרון)
- שם הקובץ החדש להורדה
- זמן יצירת הקובץ
- סטטוס: מוכן להורדה

---

## 💾 **שלב 6: הורדת הקובץ**
53. **app/components/portfolio_optimizer.py** → מציג כפתור הורדה
54. **app/components/portfolio_optimizer.py** → קורא ל-download_buttons.render()
55. **app/ui/components/download_buttons.py** → קורא ל-filename_generator
56. **utils/filename_generator.py** → יוצר שם עם תאריך
57. **utils/filename_generator.py** → מחזיר שם ל-download_buttons
58. **app/ui/components/download_buttons.py** → מטפל בהורדה
59. **משתמש** → מוריד את הקובץ

**📦 Session State:**
- ללא שינוי - כל האובייקטים נשארים כמו בשלב 5

---

## 📊 **שלב 7: הצגת דוח**
60. **app/components/portfolio_optimizer.py** → מציג סיכום
61. **app/ui/components/alerts.py** → מציג הודעות הצלחה

**📦 Session State:**
- ללא שינוי - כל האובייקטים נשארים כמו בשלב 5

---

## 🔁 **סיום או התחלה חדשה**
62. **משתמש** → מרענן את הדף או עובר לעמוד אחר
63. **Streamlit** → מוחק את כל ה-Session State אוטומטית

**📦 Session State:**
- נמחק לחלוטין - כל האובייקטים נעלמים
- אין שמירת מידע בין ריצות