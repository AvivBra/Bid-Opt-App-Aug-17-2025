# תרשים זרימה מלא - Bids 30 Days Optimization

## 🎯 תהליך ראשי

```mermaid
graph TB
    Start([התחלה]) --> SelectOpt[בחירת אופטימיזציה - רק אחת מותרת]
    
    SelectOpt --> CheckBids30{Bids 30 Days נבחר?}
    CheckBids30 -->|כן| DisableAll[השבת כל האופטימיזציות האחרות<br/>ניקוי נתוני Bulk קודמים מהסשן<br/>השבת Bulk 60<br/>הפעל Bulk 30]
    CheckBids30 -->|לא| CheckZeroSales{Zero Sales נבחר?}
    
    CheckZeroSales -->|כן| DisableBids30[השבת Bids 30 Days<br/>ניקוי נתוני Bulk קודמים מהסשן<br/>השבת Bulk 30<br/>הפעל Bulk 60]
    CheckZeroSales -->|לא| AllDisabled[כל כפתורי Bulk מושבתים]
    
    DisableAll --> UploadFiles[העלאת קבצים חדשים - חובה]
    DisableBids30 --> UploadFiles[העלאת קבצים חדשים - חובה]
    AllDisabled --> WaitSelection[המתן לבחירה]
```

## 📁 שלב 1: העלאת קבצים

```mermaid
graph LR
    UploadFiles --> UploadTemplate[העלאת Template]
    UploadFiles --> UploadBulk30[העלאת Bulk 30 Days]
    
    UploadTemplate --> ValidateTemplate{תקינות Template?}
    ValidateTemplate -->|כן| SaveTemplate[שמירה בסשן]
    ValidateTemplate -->|לא| ErrorTemplate[הודעת שגיאה]
    
    UploadBulk30 --> ValidateBulk{תקינות Bulk?}
    ValidateBulk -->|כן| SaveBulk[שמירה בסשן]
    ValidateBulk -->|לא| ErrorBulk[הודעת שגיאה]
    
    SaveTemplate --> ReadyToProcess
    SaveBulk --> ReadyToProcess[מוכן לעיבוד]
```

## ✅ שלב 2: ולידציה

```mermaid
graph TB
    ReadyToProcess --> Validation[תהליך ולידציה]
    
    Validation --> CheckColumns{בדיקת עמודות נדרשות}
    CheckColumns -->|חסרות| ValidationFail[כישלון ולידציה]
    CheckColumns -->|קיימות| CheckPortfolios
    
    CheckPortfolios{בדיקת התאמת פורטפוליו}
    CheckPortfolios -->|לא תואם| ValidationFail
    CheckPortfolios -->|תואם| CheckData
    
    CheckData{בדיקת נתונים}
    CheckData -->|לא תקין| ValidationFail
    CheckData -->|תקין| ValidationPass[ולידציה עברה בהצלחה]
    
    ValidationPass --> ProcessButton[הפעלת כפתור Process Files]
```

## 🧹 שלב 3: ניקוי נתונים

```mermaid
graph TB
    ProcessButton --> Cleaning[תהליך ניקוי]
    
    Cleaning --> SplitEntity[חלוקה לפי Entity Type]
    SplitEntity --> Targeting[Targeting Sheet]
    SplitEntity --> BiddingAdj[Bidding Adjustment Sheet]
    SplitEntity --> ProductAd[Product Ad Sheet]
    
    Targeting --> FilterUnits{סינון: units > 0 AND<br/>units > 2 OR clicks > 30}
    FilterUnits -->|עובר| RemoveFlat[הסרת 10 פורטפוליו Flat]
    FilterUnits -->|לא עובר| RemoveRow[הסרת שורה]
    
    RemoveFlat --> RemoveIgnore[הסרת פורטפוליו עם Ignore]
    RemoveIgnore --> FilterEnabled{State = enabled?}
    FilterEnabled -->|כן| CleanedData[נתונים נקיים]
    FilterEnabled -->|לא| RemoveRow
```

## 🔢 שלב 4: עיבוד חישובים - חלק א'

```mermaid
graph TB
    CleanedData --> Processing[תהליך עיבוד]
    
    Processing --> Step0[שלב 0: יצירת עמודות עזר ריקות]
    Step0 --> Step1[שלב 1: מילוי עמודות בסיס]
    
    Step1 --> FillOldBid[Old Bid = העתק Bid נוכחי]
    Step1 --> FillTargetCPA[Target CPA = VLOOKUP מ-Template]
    Step1 --> FillBaseBid[Base Bid = VLOOKUP מ-Template]
    Step1 --> CalcMaxBA[Max BA = MAX Percentage per Campaign ID]
    Step1 --> CalcAdjCPA[Adj CPA = Target CPA / 1 + Max BA/100]
    
    CalcAdjCPA --> Step2{שלב 2: Target CPA קיים?}
    Step2 -->|NULL| MoveToHarvesting[העבר לגיליון For Harvesting]
    Step2 -->|קיים| Step3
```

## 🔢 שלב 4: עיבוד חישובים - חלק ב'

```mermaid
graph TB
    Step3[שלב 3: חישוב Calc] --> CheckUpAnd{Campaign Name מכיל 'up and'?}
    
    CheckUpAnd -->|כן| CalcWithUpAnd[calc1 = Adj.CPA * 0.5 / clicks/units<br/>calc2 = calc1 / Old Bid]
    CheckUpAnd -->|לא| CalcNoUpAnd[calc1 = Adj.CPA / clicks/units<br/>calc2 = calc1 / Old Bid]
    
    CalcWithUpAnd --> Step4
    CalcNoUpAnd --> Step4
    
    Step4{שלב 4: calc2 < 1.1?}
    Step4 -->|כן| SetBidCalc1[Bid = calc1<br/>סיום עיבוד שורה]
    Step4 -->|לא| CheckMatchType
    
    CheckMatchType{Match Type = Exact<br/>OR<br/>Product Targeting<br/>contains asin=B0?}
    CheckMatchType -->|כן| SetTempBid[Temp Bid = calc1<br/>המשך לשלב 5]
    CheckMatchType -->|לא| SetBidMultiply[Bid = Old Bid * 1.1<br/>סיום עיבוד שורה]
```

## 🔢 שלב 4: עיבוד חישובים - חלק ג'

```mermaid
graph TB
    SetTempBid --> Step5[שלב 5: חישוב Max Bid]
    
    Step5 --> CheckUnits{units < 3?}
    CheckUnits -->|כן| MaxBid08[Max_Bid = 0.8 / 1 + Max BA/100]
    CheckUnits -->|לא| MaxBid125[Max_Bid = 1.25 / 1 + Max BA/100]
    
    MaxBid08 --> Step6
    MaxBid125 --> Step6
    
    Step6[שלב 6: calc3 = Temp Bid - Max Bid]
    
    Step6 --> Step7{שלב 7: calc3 < 0?}
    Step7 -->|כן| FinalBidMax[Bid = Max_Bid]
    Step7 -->|לא| FinalBidTemp[Bid = Temp_Bid]
    
    FinalBidMax --> Step8
    FinalBidTemp --> Step8
```

## 🎨 שלב 5: סימון וצביעה

```mermaid
graph TB
    Step8[שלב 8: בדיקת תנאי צביעה] --> CheckCVR{Conversion Rate < 0.08?}
    CheckCVR -->|כן| MarkPink1[סמן לצביעה ורודה]
    CheckCVR -->|לא| CheckBidRange
    
    CheckBidRange{Bid < 0.02 OR Bid > 1.25?}
    CheckBidRange -->|כן| MarkPink2[סמן לצביעה ורודה]
    CheckBidRange -->|לא| CheckError
    
    CheckError{שגיאה בחישוב?}
    CheckError -->|כן| MarkPink3[סמן לצביעה ורודה]
    CheckError -->|לא| NoMark[ללא סימון]
    
    MarkPink1 --> CollectStats
    MarkPink2 --> CollectStats
    MarkPink3 --> CollectStats
    NoMark --> CollectStats[איסוף סטטיסטיקות]
```

## 📊 שלב 6: יצירת פלט

```mermaid
graph TB
    CollectStats --> CreateOutput[יצירת קובץ פלט]
    
    CreateOutput --> Sheet1[גיליון Targeting<br/>58 עמודות - 48 מקוריות + 10 עזר]
    CreateOutput --> Sheet2[גיליון Bidding Adjustment<br/>48 עמודות מקוריות בלבד]
    CreateOutput --> Sheet3[גיליון For Harvesting<br/>שורות עם Target CPA = NULL]
    
    Sheet1 --> ApplyPink[החלת צביעה ורודה על שורות מסומנות]
    Sheet1 --> ApplyBlue[צביעת כותרות עמודות משתתפות בתכלת]
    
    ApplyPink --> FinalFile
    ApplyBlue --> FinalFile
    Sheet2 --> FinalFile
    Sheet3 --> FinalFile[קובץ Excel סופי]
```

## 📈 שלב 7: הצגת תוצאות

```mermaid
graph TB
    FinalFile --> DisplayStats[הצגת סטטיסטיקות]
    
    DisplayStats --> ShowCVR[rows with CVR < 8%]
    DisplayStats --> ShowErrors[errored rows]
    DisplayStats --> ShowLowBid[rows with Bid < 0.02]
    DisplayStats --> ShowHighBid[rows with Bid > 1.25]
    
    ShowCVR --> DownloadButton
    ShowErrors --> DownloadButton
    ShowLowBid --> DownloadButton
    ShowHighBid --> DownloadButton[כפתור הורדה]
    
    DownloadButton --> End([סיום])
```

## 📋 סיכום עמודות עזר

| עמודה | מיקום | חישוב |
|--------|--------|--------|
| Old Bid | לפני Bid | העתק Bid מקורי |
| calc1 | אחרי Bid | Adj.CPA × מכפיל / (clicks/units) |
| calc2 | אחרי calc1 | calc1 / Old Bid |
| Target CPA | לפני Base Bid | VLOOKUP מ-Template |
| Base Bid | לפני Adj. CPA | VLOOKUP מ-Template |
| Adj. CPA | לפני Max BA | Target CPA / (1 + Max BA/100) |
| Max BA | לפני Old Bid | MAX(Percentage) per Campaign ID |
| Temp Bid | אחרי Old Bid | calc1 (בתנאים מסוימים) |
| Max_Bid | אחרי Bid | 0.8 או 1.25 / (1 + Max BA/100) |
| calc3 | אחרי Max_Bid | Temp Bid - Max_Bid |

## 🚫 כללי הדרה

### פורטפוליו מוחרגים (10):
- Flat 30
- Flat 25
- Flat 40
- Flat 25 | Opt
- Flat 30 | Opt
- Flat 20
- Flat 15
- Flat 40 | Opt
- Flat 20 | Opt
- Flat 15 | Opt

### תנאי סינון:
- ✅ units > 0
- ✅ units > 2 OR clicks > 30
- ✅ State = enabled
- ✅ Campaign State = enabled
- ✅ Ad Group State = enabled
- ❌ Base Bid = "Ignore"
- ❌ Target CPA = NULL → העברה ל-"For Harvesting"

## 🎨 קודי צבע

- **ורוד** 🟪: שורות עם שגיאה/CVR נמוך/Bid מחוץ לטווח
- **תכלת** 🟦: כותרות עמודות משתתפות בעיבוד
- **ללא צבע**: שורות תקינות ועמודות לא משתתפות