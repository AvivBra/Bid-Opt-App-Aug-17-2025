# מסמך עיבוד - Bids 30 Days
**תאריך: 08:00**

## שלב 1: עיבוד ראשוני (זהה ל-Zero Sales)
1. חישוב Max BA לכל Campaign ID
2. מיזוג עם Port Values מהטמפלייט
3. חישוב Adj. CPA = Target CPA / (1 + Max BA/100)

## שלב 2: חלוקה לפי Target CPA

### מקרה A - אין Target CPA:
- העברת כל השורות לגיליון חדש: **"For Harvesting"**
- אין חישובי Bid לשורות אלו

### שורות עם Target CPA - ממשיכים לשלב 3

## שלב 3: חישובי Calc (רק לשורות עם Target CPA)

### מקרה B - יש "up and" ב-Campaign Name (Informational only):
```
calc1 = Adj. CPA * 0.5 / (clicks/units)
calc2 = calc1 / Old Bid
```

### מקרה C - אין "up and" ב-Campaign Name (Informational only):
```
calc1 = Adj. CPA / (clicks/units)
calc2 = calc1 / Old Bid
```

## שלב 4: חישוב Bid זמני

### תת-מקרה 1: כאשר calc2 < 1
```
Bid = calc2
```

### תת-מקרה 2: כאשר calc2 > 1

#### תנאי:
```
IF (Match Type = "Exact") 
   OR (Product Targeting Expression contains "asin=B0")
```

#### תוצאה:
```
THEN: Bid = calc1
ELSE: Bid = Old Bid * 1.1
```

## שלב 5: הוספת עמודת Max Bid

### כאשר units < 3:
```
Max Bid = 0.8 / (1 + Max BA/100)
```

### כאשר units >= 3:
```
Max Bid = 1.25 / (1 + Max BA/100)
```

## שלב 6: הוספת עמודת calc3
```
calc3 = Bid - Max Bid
```

## שלב 7: תיקון עמודת Bid

### כאשר calc3 < 0:
```
Bid = Max Bid
```

### כאשר calc3 >= 0:
```
Bid remains unchanged
```

---

## לוגיקת IF-THEN

### שלב 1: עיבוד ראשוני
```
Max_BA = MAX(Percentage) per Campaign_ID
Adj_CPA = Target_CPA / (1 + Max_BA/100)
```

### שלב 2: חלוקה לפי Target CPA
```
IF (Target CPA = NULL)
    THEN → For Harvesting sheet
   
ELSE IF (Target CPA EXISTS)
    THEN → Continue to Step 3
```

### שלב 3: חישוב Calc
```
IF ("up and" IN Campaign Name)
    THEN:
        calc1 = Adj.CPA * 0.5 / (clicks/units)
        calc2 = calc1 / Old Bid
ELSE
    THEN:
        calc1 = Adj.CPA / (clicks/units)
        calc2 = calc1 / Old Bid
```

### שלב 4: קביעת Bid זמני
```
IF (calc2 < 1)
    THEN:
        Bid = calc2
ELSE IF (calc2 >= 1)
    THEN:
        IF (Match Type = "Exact" OR Product Targeting Expression CONTAINS "asin=B0")
            THEN:
                Bid = calc1
        ELSE
            THEN:
                Bid = Old Bid * 1.1
```

### שלב 5: חישוב Max Bid
```
IF (units < 3)
    THEN:
        Max_Bid = 0.8 / (1 + Max_BA/100)
ELSE
    THEN:
        Max_Bid = 1.25 / (1 + Max_BA/100)
```

### שלב 6: חישוב calc3
```
calc3 = Bid - Max_Bid
```

### שלב 7: תיקון Bid סופי
```
IF (calc3 < 0)
    THEN:
        Bid = Max_Bid
ELSE
    THEN:
        Bid = No Change
```