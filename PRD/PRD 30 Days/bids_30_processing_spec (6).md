# מסמך עיבוד - Bids 30 Days
**תאריך: 08:00**

## לוגיקת IF-THEN

### שלב 0: יצירת עמודות עזר ריקות (סדר הופעה בפלט)
```
Create empty columns:
- Old Bid
- calc1
- calc2
- Target CPA
- Base Bid
- Adj. CPA
- Max BA
- Temp Bid
- Max_Bid
- calc3
```

### צביעת כותרות עמודות שקיימות בבאלק המקורי ומשתתפות בעיבוד בתכלת
```
Highlight in blue:
- Bid
- Portfolio Name (Informational only)
- Campaign ID
- Campaign Name (Informational only)
- Percentage
- clicks
- units
- Match Type
- Product Targeting Expression
- Conversion Rate
- Entity
- State
- Campaign State (Informational only)
- Ad Group State (Informational only)
```

### שלב 1: מילוי עמודות בסיס
```
Old_Bid = Copy current Bid value
Target_CPA = VLOOKUP(Portfolio_Name from Template Port_Values)
Base_Bid = VLOOKUP(Portfolio_Name from Template Port_Values)
Max_BA = MAX(Percentage) per Campaign_ID
Adj_CPA = Target_CPA / (1 + Max_BA/100)
```

### שלב 2: חלוקה לפי Target CPA
```
IF (Target CPA = NULL)
    THEN:
        - Create new sheet "For Harvesting"
        - Move these rows to the new sheet
        - Remove from current sheet
   
ELSE IF (Target CPA EXISTS)
    THEN → Continue to Step 3
```

### שלב 3: חישוב Calc
```
IF ("Campaign Name (Informational only)" contains "up and")
    THEN:
        calc1 = Adj.CPA * 0.5 / (clicks/units)
        calc2 = calc1 / Old Bid
ELSE
    THEN:
        calc1 = Adj.CPA / (clicks/units)
        calc2 = calc1 / Old Bid
```

### שלב 4: קביעת Temp Bid
```
IF (calc2 < 1.1)
    THEN:
        Bid = calc1  [FINAL - Skip to next row]
        
ELSE IF (calc2 >= 1.1)
    THEN:
        IF (Match Type = "Exact" OR Product Targeting Expression CONTAINS "asin=B0")
            THEN:
                Temp_Bid = calc1  [Continue to Step 5]
        ELSE
            THEN:
                Bid = Old Bid * 1.1  [FINAL - Skip to next row]
```

### שלב 5: חישוב Max Bid
```
IF (calc2 >= 1.1 
    AND 
    ((Product Targeting Expression CONTAINS "asin=B0") OR (Match Type = "Exact")))
    THEN:
        IF (units < 3)
            THEN:
                Max_Bid = 0.8 / (1 + Max_BA/100)
        ELSE
            THEN:
                Max_Bid = 1.25 / (1 + Max_BA/100)
```

### שלב 6: חישוב calc3
```
IF (Max_Bid EXISTS)
    THEN:
        calc3 = Temp_Bid - Max_Bid
```

### שלב 7: חישוב Bid עבור שורות עם Max Bid
```
IF (calc3 < 0)
    THEN:
        Bid = Max_Bid
ELSE
    THEN:
        Bid = Temp_Bid
```

### שלב 8: צביעת שורות בוורוד (רק בגיליון Targeting)
```
IF (value in "Conversion Rate" column < 0.08
    OR
    Error in any calculation
    OR
    Bid < 0.02
    OR
    Bid > 1.25)
    THEN:
        Mark row for pink highlighting
        Continue processing remaining rows
        Include in output file
        
Note: No pink highlighting in "Bidding Adjustment" sheet
```

### שלב 9: חיווים על המסך (במקביל להצגת כפתור הורדה)
```
IF (COUNT(Conversion Rate < 0.08) > 0)
    THEN:
        Display: "[count] rows with CVR < 8%"
        
IF (COUNT(Error rows) > 0)
    THEN:
        Display: "[count] errored rows"
        
IF (COUNT(Bid < 0.02) > 0)
    THEN:
        Display: "[count] rows with Bid < 0.02"
        
IF (COUNT(Bid > 1.25) > 0)
    THEN:
        Display: "[count] rows with Bid > 1.25"
```