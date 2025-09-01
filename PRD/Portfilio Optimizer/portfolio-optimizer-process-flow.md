# תהליך Portfolio Optimizer - מעבר השרביט בין הקבצים

## שלב 1
**ממי למי:** המשתמש → main.py  
**מה מבצע:** מציג תפריט ראשי עם אפשרויות  
**מעביר ל:** navigation.py  
**Session State:** ריק

---

## שלב 2
**ממי למי:** main.py → navigation.py  
**מה מבצע:** מנתב לעמוד Portfolio Optimizer  
**מעביר ל:** portfolio_optimizer.py  
**Session State:** ריק

---

## שלב 3
**ממי למי:** navigation.py → portfolio_optimizer.py  
**מה מבצע:** מציג ממשק עם כותרת וצ'קבוקסים  
**מעביר ל:** factory.py  
**Session State:** ריק

---

## שלב 4
**ממי למי:** portfolio_optimizer.py → factory.py  
**מה מבצע:** מחזיר רשימת אופטימיזציות זמינות  
**מעביר ל:** portfolio_optimizer.py (חזרה)  
**Session State:** ריק

---

## שלב 5
**ממי למי:** המשתמש → portfolio_optimizer.py  
**מה מבצע:** המשתמש סימן צ'קבוקסים  
**מעביר ל:** portfolio_state.py  
**Session State:** 
- `selected_optimizations`: ["empty_portfolios", "campaigns_without_portfolios"]

---

## שלב 6
**ממי למי:** portfolio_optimizer.py → portfolio_state.py  
**מה מבצע:** שומר את הבחירות בזיכרון  
**מעביר ל:** portfolio_optimizer.py (חזרה)  
**Session State:**
- `selected_optimizations`: ["empty_portfolios", "campaigns_without_portfolios"]

---

## שלב 7
**ממי למי:** המשתמש → portfolio_optimizer.py  
**מה מבצע:** המשתמש העלה קובץ אקסל  
**מעביר ל:** excel_reader.py  
**Session State:**
- `selected_optimizations`: ["empty_portfolios", "campaigns_without_portfolios"]

---

## שלב 8
**ממי למי:** portfolio_optimizer.py → excel_reader.py  
**מה מבצע:** קורא את הקובץ ומפרק לגיליונות  
**מעביר ל:** bulk_validator.py  
**Session State:**
- `selected_optimizations`: ["empty_portfolios", "campaigns_without_portfolios"]
- `raw_data`: {שם_גיליון: DataFrame}

---

## שלב 9
**ממי למי:** excel_reader.py → bulk_validator.py  
**מה מבצע:** בודק שהקובץ תקין וכל הגיליונות קיימים  
**מעביר ל:** portfolio_state.py  
**Session State:**
- `selected_optimizations`: ["empty_portfolios", "campaigns_without_portfolios"]
- `raw_data`: {שם_גיליון: DataFrame}
- `validation_status`: "passed"

---

## שלב 10
**ממי למי:** bulk_validator.py → portfolio_state.py  
**מה מבצע:** שומר את הנתונים המאומתים  
**מעביר ל:** portfolio_optimizer.py (חזרה)  
**Session State:**
- `selected_optimizations`: ["empty_portfolios", "campaigns_without_portfolios"]
- `original_data`: {שם_גיליון: DataFrame}
- `validation_status`: "passed"
- `file_name`: "bulk_60.xlsx"
- `upload_time`: "2025-08-30 10:30:00"

---

## שלב 11
**ממי למי:** המשתמש → portfolio_optimizer.py  
**מה מבצע:** המשתמש לחץ על Process  
**מעביר ל:** orchestrator.py  
**Session State:** ללא שינוי מהשלב הקודם

---

## שלב 12
**ממי למי:** portfolio_optimizer.py → orchestrator.py  
**מה מבצע:** מתחיל תהליך עיבוד  
**מעביר ל:** cleaning.py  
**Session State:** ללא שינוי

---

## שלב 13
**ממי למי:** orchestrator.py → cleaning.py  
**מה מבצע:** מנקה רווחים מיותרים ומפצל גיליונות  
**מעביר ל:** orchestrator.py (חזרה)  
**Session State:**
- כל מה שהיה קודם
- `cleaned_data`: {
  - "Portfolios": DataFrame,
  - "Campaigns": DataFrame,
  - "Product Ad": DataFrame
}

---

## שלב 14
**ממי למי:** orchestrator.py → factory.py  
**מה מבצע:** יוצר אסטרטגיה ראשונה (empty_portfolios)  
**מעביר ל:** strategies.py  
**Session State:** ללא שינוי

---

## שלב 15
**ממי למי:** factory.py → strategies.py  
**מה מבצע:** מריץ EmptyPortfoliosStrategy.run()  
**מעביר ל:** orchestrator.py (חזרה)  
**Session State:**
- כל מה שהיה קודם
- `optimization_results[0]`: {
  - result_type: "portfolios",
  - patch: {שורות לעדכון},
  - metrics: {portfolios_updated: 5}
}

---

## שלב 16
**ממי למי:** orchestrator.py → factory.py  
**מה מבצע:** יוצר אסטרטגיה שנייה (campaigns_without_portfolios)  
**מעביר ל:** strategies.py  
**Session State:** ללא שינוי

---

## שלב 17
**ממי למי:** factory.py → strategies.py  
**מה מבצע:** מריץ CampaignsWithoutPortfoliosStrategy.run()  
**מעביר ל:** orchestrator.py (חזרה)  
**Session State:**
- כל מה שהיה קודם
- `optimization_results[1]`: {
  - result_type: "campaigns",
  - patch: {שורות לעדכון},
  - metrics: {campaigns_updated: 12}
}

---

## שלב 18
**ממי למי:** orchestrator.py → results_manager.py  
**מה מבצע:** ממזג את כל התוצאות לנתונים המקוריים  
**מעביר ל:** orchestrator.py (חזרה)  
**Session State:**
- כל מה שהיה קודם
- `merged_data`: {גיליונות מעודכנים}
- `updated_indices`: {Portfolios: [2,5,8], Campaigns: [1,3,7,9]}
- `conflicts`: []

---

## שלב 19
**ממי למי:** orchestrator.py → service.py  
**מה מבצע:** יוצר קובץ אקסל חדש  
**מעביר ל:** excel_writer.py  
**Session State:** ללא שינוי

---

## שלב 20
**ממי למי:** service.py → excel_writer.py  
**מה מבצע:** כותב אקסל עם צביעה צהובה  
**מעביר ל:** service.py (חזרה)  
**Session State:** ללא שינוי

---

## שלב 21
**ממי למי:** service.py → orchestrator.py  
**מה מבצע:** מחזיר BytesIO של הקובץ  
**מעביר ל:** portfolio_optimizer.py  
**Session State:**
- כל מה שהיה קודם
- `output_file`: BytesIO object

---

## שלב 22
**ממי למי:** orchestrator.py → portfolio_optimizer.py  
**מה מבצע:** מקבל קובץ ודוח סופי  
**מעביר ל:** portfolio_state.py  
**Session State:**
- כל מה שהיה קודם
- `run_report`: {
  - optimizations_run: 2,
  - rows_updated: 17,
  - time_elapsed: 3.2
}

---

## שלב 23
**ממי למי:** portfolio_optimizer.py → portfolio_state.py  
**מה מבצע:** שומר קובץ ודוח בזיכרון  
**מעביר ל:** portfolio_optimizer.py (חזרה)  
**Session State:**
- כל מה שהיה קודם
- `output_file`: BytesIO object
- `run_report`: דוח מלא
- `process_status`: "completed"

---

## שלב 24
**ממי למי:** portfolio_optimizer.py → download_buttons.py  
**מה מבצע:** מציג כפתור הורדה  
**מעביר ל:** filename_generator.py  
**Session State:** ללא שינוי

---

## שלב 25
**ממי למי:** download_buttons.py → filename_generator.py  
**מה מבצע:** יוצר שם קובץ עם תאריך  
**מעביר ל:** download_buttons.py (חזרה)  
**Session State:**
- כל מה שהיה קודם
- `output_filename`: "portfolio_optimized_20250830_103500.xlsx"

---

## שלב 26
**ממי למי:** המשתמש → download_buttons.py  
**מה מבצע:** המשתמש הוריד את הקובץ  
**מעביר ל:** אף אחד (סיום)  
**Session State:** נשאר כמו שהוא עד שהמשתמש יעבור עמוד