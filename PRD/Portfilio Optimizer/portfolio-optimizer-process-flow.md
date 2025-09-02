# תהליך Portfolio Optimizer - מעבר השרביט בין הקבצים

## שלב 1
**ממי למי:** המשתמש → app/main.py  
**מה מבצע:** מציג תפריט ראשי עם אפשרויות  
**מעביר ל:** app/navigation.py  
**Session State:** ריק

---

## שלב 2
**ממי למי:** app/main.py → app/navigation.py  
**מה מבצע:** מנתב לעמוד Portfolio Optimizer  
**מעביר ל:** app/components/portfolio_optimizer.py  
**Session State:** ריק

---

## שלב 3
**ממי למי:** app/navigation.py → app/components/portfolio_optimizer.py  
**מה מבצע:** מציג ממשק עם כותרת וצ'קבוקסים  
**מעביר ל:** business/portfolio_optimizations/factory.py  
**Session State:** ריק

---

## שלב 4
**ממי למי:** app/components/portfolio_optimizer.py → business/portfolio_optimizations/factory.py  
**מה מבצע:** מחזיר רשימת אופטימיזציות זמינות  
**מעביר ל:** app/components/portfolio_optimizer.py (חזרה)  
**Session State:** ריק

---

## שלב 5
**ממי למי:** המשתמש → app/components/portfolio_optimizer.py  
**מה מבצע:** המשתמש סימן צ'קבוקסים  
**מעביר ל:** app/state/portfolio_state.py  
**Session State:** 
- `empty_portfolios_selected`: True/False
- `campaigns_without_portfolios_selected`: True/False
- `organize_top_campaigns_selected`: True/False
- `portfolio_selected_optimizations`: ["empty_portfolios", "campaigns_without_portfolios", "organize_top_campaigns"]

---

## שלב 6
**ממי למי:** app/components/portfolio_optimizer.py → app/state/portfolio_state.py  
**מה מבצע:** שומר את הבחירות בזיכרון  
**מעביר ל:** app/components/portfolio_optimizer.py (חזרה)  
**Session State:**
- `empty_portfolios_selected`: True/False
- `campaigns_without_portfolios_selected`: True/False
- `organize_top_campaigns_selected`: True/False
- `portfolio_selected_optimizations`: ["empty_portfolios", "campaigns_without_portfolios", "organize_top_campaigns"]

---

## שלב 7
**ממי למי:** המשתמש → app/components/portfolio_optimizer.py  
**מה מבצע:** המשתמש העלה קובץ אקסל ו/או טמפלט Top ASINs (אם נבחר organize_top_campaigns)  
**מעביר ל:** data/readers/excel_reader.py  
**Session State:**
- `portfolio_selected_optimizations`: ["empty_portfolios", "campaigns_without_portfolios", "organize_top_campaigns"]
- `portfolio_template_uploaded`: True (אם נבחר organize_top_campaigns)

---

## שלב 8
**ממי למי:** app/components/portfolio_optimizer.py → data/readers/excel_reader.py  
**מה מבצע:** קורא את הקובץ ומפרק לגיליונות  
**מעביר ל:** data/validators/bulk_validator.py  
**Session State:**
- `portfolio_selected_optimizations`: ["empty_portfolios", "campaigns_without_portfolios", "organize_top_campaigns"]
- `portfolio_bulk_60_df`: DataFrame
- `portfolio_sheets`: {שם_גיליון: DataFrame}

---

## שלב 9
**ממי למי:** data/readers/excel_reader.py → data/validators/bulk_validator.py  
**מה מבצע:** בודק שהקובץ תקין וכל הגיליונות קיימים  
**מעביר ל:** app/state/portfolio_state.py  
**Session State:**
- `portfolio_selected_optimizations`: ["empty_portfolios", "campaigns_without_portfolios", "organize_top_campaigns"]
- `portfolio_bulk_60_df`: DataFrame
- `portfolio_sheets`: {שם_גיליון: DataFrame}
- `portfolio_validation_passed`: True
- `portfolio_validation_result`: "success"

---

## שלב 10
**ממי למי:** data/validators/bulk_validator.py → app/state/portfolio_state.py  
**מה מבצע:** שומר את הנתונים המאומתים  
**מעביר ל:** app/components/portfolio_optimizer.py (חזרה)  
**Session State:**
- `portfolio_selected_optimizations`: ["empty_portfolios", "campaigns_without_portfolios", "organize_top_campaigns"]
- `portfolio_bulk_60_df`: DataFrame
- `portfolio_sheets`: {שם_גיליון: DataFrame}
- `portfolio_validation_passed`: True
- `portfolio_bulk_60_uploaded`: True
- `portfolio_filename`: "Input Bulk Example.xlsx"
- `portfolio_upload_time`: timestamp

---

## שלב 11
**ממי למי:** המשתמש → app/components/portfolio_optimizer.py  
**מה מבצע:** המשתמש לחץ על Process Optimizations  
**מעביר ל:** business/portfolio_optimizations/orchestrator.py  
**Session State:** ללא שינוי מהשלב הקודם

---

## שלב 12
**ממי למי:** app/components/portfolio_optimizer.py → business/portfolio_optimizations/orchestrator.py  
**מה מבצע:** מתחיל תהליך עיבוד  
**מעביר ל:** business/portfolio_optimizations/cleaning.py  
**Session State:** 
- `portfolio_processing_started`: True
- `portfolio_processing_status`: "processing"

---

## שלב 13
**ממי למי:** business/portfolio_optimizations/orchestrator.py → business/portfolio_optimizations/cleaning.py  
**מה מבצע:** מנקה רווחים מיותרים ומפצל גיליונות  
**מעביר ל:** business/portfolio_optimizations/orchestrator.py (חזרה)  
**Session State:**
- כל מה שהיה קודם
- `portfolio_merged_data`: {
  - "Portfolios": DataFrame,
  - "Campaign": DataFrame,
  - "Product Ad": DataFrame,
  - "Sheet3": DataFrame
}

---

## שלב 14
**ממי למי:** business/portfolio_optimizations/orchestrator.py → business/portfolio_optimizations/factory.py  
**מה מבצע:** יוצר אסטרטגיה ראשונה (empty_portfolios)  
**מעביר ל:** business/portfolio_optimizations/strategies/empty_portfolios_strategy.py  
**Session State:** ללא שינוי

---

## שלב 15
**ממי למי:** business/portfolio_optimizations/factory.py → business/portfolio_optimizations/strategies/empty_portfolios_strategy.py  
**מה מבצע:** מריץ EmptyPortfoliosStrategy.run()  
**מעביר ל:** business/portfolio_optimizations/orchestrator.py (חזרה)  
**Session State:**
- כל מה שהיה קודם
- `empty_portfolios_found`: מספר פורטפוליו ריקים שנמצאו
- `empty_portfolios_renamed`: מספר פורטפוליו שנשמו
- `empty_portfolios_results`: תוצאות האופטימיזציה

---

## שלב 16
**ממי למי:** business/portfolio_optimizations/orchestrator.py → business/portfolio_optimizations/factory.py  
**מה מבצע:** יוצר אסטרטגיה שנייה (campaigns_without_portfolios)  
**מעביר ל:** business/portfolio_optimizations/strategies/campaigns_without_portfolios_strategy.py  
**Session State:** ללא שינוי

---

## שלב 17
**ממי למי:** business/portfolio_optimizations/factory.py → business/portfolio_optimizations/strategies/campaigns_without_portfolios_strategy.py  
**מה מבצע:** מריץ CampaignsWithoutPortfoliosStrategy.run()  
**מעביר ל:** business/portfolio_optimizations/orchestrator.py (חזרה)  
**Session State:**
- כל מה שהיה קודם
- `campaigns_without_portfolios_found`: מספר קמפיינים בלי פורטפוליו
- `campaigns_without_portfolios_updated`: מספר קמפיינים שעודכנו
- `campaigns_without_portfolios_results`: תוצאות האופטימיזציה

---

## שלב 18
**ממי למי:** business/portfolio_optimizations/orchestrator.py → business/portfolio_optimizations/factory.py  
**מה מבצע:** יוצר אסטרטגיה שלישית (organize_top_campaigns)  
**מעביר ל:** business/portfolio_optimizations/strategies/organize_top_campaigns_strategy.py  
**Session State:** ללא שינוי

---

## שלב 19
**ממי למי:** business/portfolio_optimizations/factory.py → business/portfolio_optimizations/strategies/organize_top_campaigns_strategy.py  
**מה מבצע:** מריץ OrganizeTopCampaignsStrategy.run()  
**מעביר ל:** business/portfolio_optimizations/orchestrator.py (חזרה)  
**Session State:**
- כל מה שהיה קודם
- `organize_top_campaigns_results`: תוצאות האופטימיזציה
- `portfolio_template_uploaded`: True (אם הועלה טמפלט)
- גיליון Top נוסף לנתונים

---

## שלב 20
**ממי למי:** business/portfolio_optimizations/orchestrator.py → business/portfolio_optimizations/results_manager.py  
**מה מבצע:** ממזג את כל התוצאות לנתונים המקוריים  
**מעביר ל:** business/portfolio_optimizations/orchestrator.py (חזרה)  
**Session State:**
- כל מה שהיה קודם
- `portfolio_merged_data`: {גיליונות מעודכנים כולל Top sheet}
- `portfolio_updated_indices`: {מדדי השורות שעודכנו}
- `portfolio_run_report`: דוח מלא על התוצאות

---

## שלב 21
**ממי למי:** business/portfolio_optimizations/orchestrator.py → business/portfolio_optimizations/service.py  
**מה מבצע:** יוצר קובץ אקסל חדש  
**מעביר ל:** data/writers/excel_writer.py  
**Session State:** ללא שינוי

---

## שלב 22
**ממי למי:** business/portfolio_optimizations/service.py → data/writers/excel_writer.py  
**מה מבצע:** כותב אקסל עם צביעה צהובה  
**מעביר ל:** business/portfolio_optimizations/service.py (חזרה)  
**Session State:** ללא שינוי

---

## שלב 23
**ממי למי:** business/portfolio_optimizations/service.py → business/portfolio_optimizations/orchestrator.py  
**מה מבצע:** מחזיר BytesIO של הקובץ  
**מעביר ל:** app/components/portfolio_optimizer.py  
**Session State:**
- כל מה שהיה קודם
- `portfolio_output_file`: BytesIO object

---

## שלב 24
**ממי למי:** business/portfolio_optimizations/orchestrator.py → app/components/portfolio_optimizer.py  
**מה מבצע:** מקבל קובץ ודוח סופי  
**מעביר ל:** app/state/portfolio_state.py  
**Session State:**
- כל מה שהיה קודם
- `portfolio_run_report`: {
  - total_optimizations: 3,
  - total_rows_updated: מספר שורות שעודכנו,
  - execution_time_seconds: זמן ביצוע,
  - successful_optimizations: 3,
  - failed_optimizations: []
}

---

## שלב 25
**ממי למי:** app/components/portfolio_optimizer.py → app/state/portfolio_state.py  
**מה מבצע:** שומר קובץ ודוח בזיכרון  
**מעביר ל:** app/components/portfolio_optimizer.py (חזרה)  
**Session State:**
- כל מה שהיה קודם
- `portfolio_output_file`: BytesIO object
- `portfolio_run_report`: דוח מלא
- `portfolio_processing_status`: "complete"
- `portfolio_output_generated`: True

---

## שלב 26
**ממי למי:** app/components/portfolio_optimizer.py → app/ui/components/download_buttons.py  
**מה מבצע:** מציג כפתור הורדה  
**מעביר ל:** utils/filename_generator.py  
**Session State:** ללא שינוי

---

## שלב 27
**ממי למי:** app/ui/components/download_buttons.py → utils/filename_generator.py  
**מה מבצע:** יוצר שם קובץ עם תאריך  
**מעביר ל:** app/ui/components/download_buttons.py (חזרה)  
**Session State:**
- כל מה שהיה קודם
- `portfolio_output_filename`: "portfolio_optimized_20250902_164017.xlsx"

---

## שלב 28
**ממי למי:** המשתמש → app/ui/components/download_buttons.py  
**מה מבצע:** המשתמש הוריד את הקובץ  
**מעביר ל:** אף אחד (סיום)  
**Session State:** נשאר כמו שהוא עד שהמשתמש יעבור עמוד