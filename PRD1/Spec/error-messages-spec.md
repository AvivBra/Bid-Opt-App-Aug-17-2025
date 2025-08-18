# הודעות שגיאה - Bid Optimizer

## 1. שגיאות העלאת קבצים

### גודל קובץ
```
❌ File exceeds 40MB limit
   Your file: {size}MB
   Maximum allowed: 40MB
```

### פורמט קובץ
```
❌ Invalid file format
   Expected: Excel (.xlsx) or CSV (.csv)
   Received: {extension}
```

### קובץ פגום
```
❌ Cannot read file
   The file may be corrupted or password protected.
   Please check the file and try again.
```

### קובץ ריק
```
❌ File is empty
   The uploaded file contains no data.
   Please upload a file with content.
```

## 2. שגיאות מבנה Template

### לשוניות חסרות
```
❌ Missing required sheet 'Port Values'
   Template must contain 'Port Values' sheet.
```

```
❌ Missing required sheet 'Top ASINs'
   Template must contain 'Top ASINs' sheet.
```

### עמודות שגויות
```
❌ Invalid column structure in 'Port Values'
   Expected columns: Portfolio Name, Base Bid, Target CPA
   Found: {actual_columns}
```

### סדר עמודות
```
❌ Wrong column order
   Columns must be in exact order:
   Portfolio Name | Base Bid | Target CPA
```

## 3. שגיאות נתוני Template

### Portfolio Name
```
❌ Empty Portfolio Name in row {n}
   Portfolio Name cannot be empty.
```

```
❌ Duplicate portfolio name: {name}
   Each portfolio must have a unique name.
```

### Base Bid
```
❌ Invalid Base Bid in row {n}
   Value: {value}
   Expected: Number (0.00-999.99) or "Ignore"
```

```
❌ All portfolios marked as 'Ignore'
   At least one portfolio must have a numeric Base Bid.
```

### Target CPA
```
❌ Invalid Target CPA in row {n}
   Value: {value}
   Expected: Number (0.00-9999.99) or empty
```

## 4. שגיאות מבנה Bulk

### Sheet חסר
```
❌ Required sheet not found
   Missing: 'Sponsored Products Campaigns'
   This sheet must exist in all Bulk files.
```

### עמודות חסרות
```
❌ Missing required columns
   Expected: 48 columns
   Found: {count} columns
   Missing: {column_names}
```

### מספר שורות
```
❌ File exceeds row limit
   Maximum: 500,000 rows
   Found: {count} rows
```

## 5. שגיאות ולידציה Zero Sales

### קבצים חסרים
```
❌ Missing required files for Zero Sales
   Required: Template, Bulk 60
   Missing: {file_names}
```

### עמודות קריטיות
```
❌ Missing critical column 'Units'
   Zero Sales requires 'Units' column in Bulk 60.
```

```
❌ Missing critical column 'Clicks'
   Zero Sales requires 'Clicks' column for calculations.
```

### פורטפוליוז חסרים
```
❌ Missing portfolios - Processing Blocked
   
   The following portfolios exist in Bulk but not in Template:
   • {portfolio_1}
   • {portfolio_2}
   • {portfolio_3}
   
   Add these portfolios to Template to continue.
```

## 6. שגיאות עיבוד

### כישלון חישוב
```
❌ Calculation error in row {n}
   Unable to calculate new bid value.
   Check data integrity in this row.
```

### ערכים לא תקינים
```
❌ Invalid data type in column '{column}'
   Expected: {expected_type}
   Found: {actual_type}
```

### זיכרון
```
❌ Memory error
   The file is too large to process.
   Try reducing the file size or contact support.
```

## 7. אזהרות (Warnings)

### ערכי Bid
```
⚠️ Bid adjustments out of range
   • {n} rows below minimum ($0.02)
   • {n} rows above maximum ($1.25)
   Values will be capped to valid range.
```

### פורטפוליוז מתעלמים
```
⚠️ Ignored portfolios
   {n} portfolios marked as 'Ignore' will be skipped.
```

### נתונים חסרים
```
⚠️ Missing data in {n} rows
   Rows with missing values will be skipped.
```

### ביצועים
```
⚠️ Large file detected
   Processing {n} rows may take several minutes.
```

## 8. הודעות מידע

### ולידציה
```
ℹ️ Validating files...
   This may take a moment for large files.
```

### עיבוד
```
ℹ️ Processing {optimization_name}
   {current}/{total} optimizations
```

### השלמה
```
ℹ️ Processing complete
   • Optimizations run: {n}
   • Rows processed: {count}
   • Time taken: {time} seconds
```

## 9. הודעות הצלחה

### העלאה
```
✅ File uploaded successfully
   {filename} ({size})
```

### ולידציה
```
✅ All validations passed
   Ready to process {n} optimizations.
```

### עיבוד
```
✅ {optimization_name} completed
   Modified {n} rows.
```

### הורדה
```
✅ Files ready for download
   • Working File: {size}MB
   • Clean File: {size}MB
```

## 10. הודעות Pink Notice

### סיכום בעיות
```
⚠️ Please note:
   
   Processing completed with the following issues:
   • {n} calculation errors
   • {n} rows below minimum bid
   • {n} rows above maximum bid
   • {n} portfolios ignored
   
   Review Working File for details.
```

## 11. הודעות דיאלוג

### אישור Reset
```
🔄 Start New Processing?
   
   This will clear all uploaded files and results.
   
   [Cancel] [Confirm]
```

### אישור החלפת קובץ
```
📤 Replace existing file?
   
   {filename} is already uploaded.
   Upload new file to replace it?
   
   [Cancel] [Replace]
```

## 12. טיפול בשגיאות לא צפויות

### שגיאה כללית
```
❌ Unexpected error occurred
   
   Error code: {code}
   Please try again or contact support.
   
   [Copy Error Details] [Report Issue]
```

### תקלת שרת
```
❌ Server error
   
   Unable to process request.
   Please try again in a few moments.
```

### תקלת רשת
```
❌ Connection error
   
   Check your internet connection and try again.
   
   [Retry]
```

## 13. עיצוב הודעות

### מבנה סטנדרטי
```
[ICON] [TITLE]
[MAIN MESSAGE]
[DETAILS/LIST]
[ACTION BUTTONS]
```

### צבעים
- **אדום** (#dc3545): שגיאות
- **כתום** (#ffc107): אזהרות
- **כחול** (#17a2b8): מידע
- **ירוק** (#28a745): הצלחה
- **ורוד** (#FFE4E1): Pink notices

## 14. טונים וניסוחים

### עקרונות
- ברור ותמציתי
- מכיל פתרון/הנחיה
- לא טכני מדי
- ידידותי אך מקצועי

### דוגמאות טובות
✅ "Missing portfolios: ABC, DEF"
✅ "Upload Bulk 60 to continue"
✅ "Processing will take ~2 minutes"

### דוגמאות רעות
❌ "Error 0x80004005"
❌ "DataFrame concatenation failed"
❌ "Invalid dtype for column"