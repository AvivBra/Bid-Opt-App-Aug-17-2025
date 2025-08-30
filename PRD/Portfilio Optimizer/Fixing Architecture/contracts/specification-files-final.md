# קבצי איפיון סופיים לתהליך
## תאריך: 30 באוגוסט 2025 | שעה: 13:15

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
1. חילוץ לוגיקה מ-campaign_optimizer.py לשירות
2. תיקון result_type שגוי בקוד
3. מעבר להחזרת patch בלבד
4. כתיבת בדיקות חוזה מינימליות
5. בדיקת merge_patch עם דוגמאות קטנות
6. הפקת קובץ יצוא מבוקר

## 4. **strategies_implementation.md**
1. העתק process() מ-empty_portfolios/processor.py
2. העתק process() מ-campaigns_without_portfolios/processor.py
3. מחק validate(), clean() - נשארים ב-orchestrator
4. מחק get_updated_indices() - מוחלף ב-patch
5. שמור רק לוגיקה ייחודית (~50 שורות)
6. הוסף @contract decorator לכל strategy