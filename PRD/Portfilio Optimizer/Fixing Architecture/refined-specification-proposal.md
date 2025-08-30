# הצעת איפיון מתוקנת - 3 קבצים בלבד
## תאריך: 30 באוגוסט 2025 | שעה: 13:00

## 1. **optimization_contract.md**
1. פונקציית `run(all_sheets) -> OptimizationResult`
2. שדות חובה: result_type, merge_keys, patch
3. patch = שורות לעדכון בלבד
4. אין שינוי in-place במקור
5. metrics + messages לסטטוס ואזהרות

## 2. **results_manager_contract.md**
1. טבלת result_type → sheet יעד
2. אלגוריתם merge_patch בפסאודו-קוד קצר
3. טיפול בקונפליקטים: האחרון גובר + לוג
4. אסור לעדכן עמודות לא מותרות
5. יצירת Run Report עם metrics

## 3. **migration_steps.md**
1. **חילוץ לוגיקה מ-campaign_optimizer.py לשירות**
2. תיקון result_type שגוי בקוד
3. מעבר להחזרת patch בלבד
4. כתיבת בדיקות חוזה מינימליות
5. בדיקת merge_patch עם דוגמאות קטנות
6. הפקת קובץ יצוא מבוקר

---

## הערות:
- כל סעיף עד 6 מילים
- החוזים מגדירים ממשק ברור ללא מקום לפרשנות
- סעיף 1 ב-migration_steps הוא קריטי - בלעדיו כל החוזים לא רלוונטיים