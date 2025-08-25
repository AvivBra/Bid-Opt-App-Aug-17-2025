# מיפוי מדויק בין PRD לקוד - Bids 60 Days
**תאריך: 25/12/2024 09:00**

## 1. דרישות קבצי קלט (bids_60_inputs_spec.md)

| דרישה PRD | קובץ קוד למימוש | פונקציה/מתודה |
|-----------|----------------|----------------|
| העלאת Template (זהה ל-Zero Sales) | `app/ui/shared/upload_section.py` | `_render_template_section()` |
| העלאת Bulk 60 Days | `app/ui/shared/upload_section.py` | `_render_bulk_section()` - שורה 108 |
| הפעלת כפתור Bulk 60 בבחירת האופטימיזציה | `app/ui/components/checklist.py` | `render()` - הוספת לוגיקה להפעלה מותנית |
| שמירת Bulk 60 בסשן | `app/state/bid_state.py` | `save_bulk('60_bids', file, df)` |
| ניקוי נתוני Bulk בהחלפת אופטימיזציה | `app/state/bid_state.py` | `reset_validation()` - שורה 95 |

## 2. דרישות ולידציה (bids_60_validation_spec.md)

| דרישה PRD | קובץ קוד למימוש | פונקציה/מתודה |
|-----------|----------------|----------------|
| שימוש בוולידציה גלובלית בלבד | `data/validators/bulk_validator.py` | הקובץ הקיים |
| בדיקת עמודות נדרשות | `data/validators/bulk_validator.py` | `validate_columns()` |
| בדיקת התאמת פורטפוליו | `data/validators/portfolio_validator.py` | `validate_portfolios()` |
| בדיקת נתונים לעיבוד | `data/validators/template_validator.py` | `validate()` |

## 3. דרישות ניקוי (bids_60_cleaning_criteria.md)

| דרישה PRD | קובץ קוד למימוש | פונקציה/מתודה |
|-----------|----------------|----------------|
| חלוקה לפי Entity type | `business/bid_optimizations/bids_60_days/cleaner.py` | `_split_by_entity()` |
| סינון units > 0 | `business/bid_optimizations/bids_60_days/cleaner.py` | `_filter_bids_60_criteria()` |
| הסרת 10 פורטפוליו Flat | `business/bid_optimizations/bids_60_days/cleaner.py` | `_remove_excluded_portfolios()` |
| הסרת פורטפוליו עם Ignore | `business/bid_optimizations/bids_60_days/cleaner.py` | `_remove_ignored_portfolios()` |
| מחיקת IDs מ-Delete for 60 | `business/bid_optimizations/bids_60_days/cleaner.py` | `_remove_delete_for_60_ids()` |
| סינון State = enabled | `business/bid_optimizations/bids_60_days/cleaner.py` | `_filter_by_state()` |

## 4. דרישות עיבוד (bids_60_processing_spec.md)

| דרישה PRD | קובץ קוד למימוש | פונקציה/מתודה |
|-----------|----------------|----------------|
| **שלב 0:** יצירת עמודות עזר | `business/bid_optimizations/bids_60_days/processor.py` | `_create_helper_columns()` |
| **שלב 1:** מילוי עמודות בסיס | `business/bid_optimizations/bids_60_days/processor.py` | `_fill_base_columns()` |
| **שלב 2:** העברת NULL ל-For Harvesting | `business/bid_optimizations/bids_60_days/processor.py` | `_separate_null_target_cpa()` |
| **שלב 3:** חישוב calc1, calc2 | `business/bid_optimizations/bids_60_days/processor.py` | `_calculate_calc_values()` |
| **שלב 4:** קביעת Temp Bid | `business/bid_optimizations/bids_60_days/processor.py` | `_determine_temp_bid()` |
| **שלב 5:** חישוב Max Bid | `business/bid_optimizations/bids_60_days/processor.py` | `_calculate_max_bid()` |
| **שלב 6:** חישוב calc3 | `business/bid_optimizations/bids_60_days/processor.py` | `_calculate_calc3()` |
| **שלב 7:** חישוב Bid סופי | `business/bid_optimizations/bids_60_days/processor.py` | `_calculate_final_bid()` |
| **שלב 8:** סימון שורות לצביעה | `business/bid_optimizations/bids_60_days/processor.py` | `_mark_rows_for_coloring()` |

## 5. דרישות פורמט פלט (excel_dataframe_mapping.md)

| דרישה PRD | קובץ קוד למימוש | פונקציה/מתודה |
|-----------|----------------|----------------|
| יצירת גיליון Targeting (58 עמודות) | `business/bid_optimizations/bids_60_days/output_formatter_60_days.py` | `_format_targeting_sheet()` |
| יצירת גיליון Bidding Adjustment (48 עמודות) | `business/bid_optimizations/bids_60_days/output_formatter_60_days.py` | `_format_bidding_sheet()` |
| יצירת גיליון For Harvesting | `business/bid_optimizations/bids_60_days/output_formatter_60_days.py` | `_format_harvesting_sheet()` |
| צביעת שורות בוורוד | `data/writers/excel_writer.py` | `_highlight_error_rows()` - שורה 167 |
| צביעת כותרות בתכלת | `business/bid_optimizations/bids_60_days/output_formatter_60_days.py` | `_highlight_column_headers()` |
| סידור עמודות עזר | `business/bid_optimizations/bids_60_days/output_formatter_60_days.py` | `_arrange_helper_columns()` |

## 6. דרישות מקרי קצה (bids_60_edge_cases.md)

| דרישה PRD | קובץ קוד למימוש | פונקציה/מתודה |
|-----------|----------------|----------------|
| טיפול בשגיאת חישוב | `business/bid_optimizations/bids_60_days/processor.py` | `_handle_calculation_error()` |
| טיפול בערך חסר | `business/bid_optimizations/bids_60_days/processor.py` | `_handle_missing_value()` |
| טיפול ב-CVR < 8% | `business/bid_optimizations/bids_60_days/processor.py` | `_check_conversion_rate()` |
| כתיבת הודעות שגיאה ב-Bid | `business/bid_optimizations/bids_60_days/processor.py` | `_write_error_message()` |

## 7. דרישות ממשק משתמש (multiple_optimization_spec_60.md)

| דרישה PRD | קובץ קוד למימוש | פונקציה/מתודה |
|-----------|----------------|----------------|
| בחירת אופטימיזציה אחת בלבד | `app/ui/components/checklist.py` | `render()` - לוגיקת radio button |
| השבתת אופטימיזציות אחרות | `app/ui/components/checklist.py` | `_disable_other_optimizations()` |
| הפעלת/השבתת כפתורי Bulk | `app/ui/shared/upload_section.py` | `_toggle_bulk_buttons()` |
| ניקוי נתוני סשן בהחלפה | `app/state/bid_state.py` | `clear_bulk_data()` |
| הצגת חיוויים על המסך | `app/ui/shared/output_section.py` | `_display_processing_stats()` |

## 8. דרישות קונפיגורציה

| דרישה PRD | קובץ קוד למימוש | פונקציה/מתודה |
|-----------|----------------|----------------|
| הגדרת קבועים לאופטימיזציה | `business/bid_optimizations/bids_60_days/constants.py` | קבועי CLASS |
| רישום האופטימיזציה במערכת | `config/optimization_config.py` | `BIDS_60_DAYS_CONFIG` |
| הוספה לרשימת אופטימיזציות | `app/ui/components/checklist.py` | `OPTIMIZATIONS` list |

## 9. דרישות אורכסטרציה

| דרישה PRD | קובץ קוד למימוש | פונקציה/מתודה |
|-----------|----------------|----------------|
| תיאום תהליך האופטימיזציה | `business/bid_optimizations/bids_60_days/orchestrator.py` | `Bids60DaysOptimization` class |
| ירושה מ-BaseOptimization | `business/bid_optimizations/bids_60_days/orchestrator.py` | `__init__()` |
| הפעלת validate, clean, process | `business/bid_optimizations/bids_60_days/orchestrator.py` | `run_optimization()` |
| איסוף סטטיסטיקות | `business/bid_optimizations/bids_60_days/orchestrator.py` | `get_statistics()` |

## 10. דרישות אינטגרציה ראשית

| דרישה PRD | קובץ קוד למימוש | פונקציה/מתודה |
|-----------|----------------|----------------|
| זיהוי בחירת Bids 60 Days | `app/pages/bid_optimizer.py` | בדיקת `selected_optimizations` |
| טעינת מודול האופטימיזציה | `app/pages/bid_optimizer.py` | `import Bids60DaysOptimization` |
| הפעלת האופטימיזציה | `app/pages/bid_optimizer.py` | תוך `process_files()` |
| יצירת קובץ Excel | `data/writers/excel_writer.py` | `create_working_file()` |
| הצגת תוצאות | `app/ui/shared/output_section.py` | `_display_statistics()` |

## הערות חשובות למימוש

1. **שימוש חוזר בקוד:** רוב הולידציה והניקוי זהים ל-Bids 30 Days - ניתן לרשת או לקרוא לאותן פונקציות
2. **עמודות עזר:** יש להוסיף 10 עמודות עזר חדשות בסדר הנכון (לפני ואחרי Bid)
3. **גיליון For Harvesting:** גיליון חדש שלא קיים ב-Zero Sales
4. **צביעת כותרות:** דרישה חדשה לצבוע כותרות עמודות משתתפות בתכלת
5. **Conversion Rate:** נתון מעמודה 55 בבאלק המקורי - יש לוודא מיפוי נכון
6. **Delete for 60:** דרישה ייחודית ל-60 יום - מחיקת IDs מגיליון Delete for 60 בטמפלט