# איפיון לוגיקת Zero Sales Optimization

## 1. סקירה כללית

### מטרה
אופטימיזציה של Bids עבור מוצרים ללא מכירות (Units = 0). האופטימיזציה מחשבת Bid חדש על סמך Portfolio settings, Target CPA, ונתוני ביצועים.

### עקרון פעולה
- סינון שורות עם Units = 0
- חישוב Bid חדש לפי 4 מקרים שונים
- הוספת עמודות עזר לניתוח
- סימון שגיאות וערכים חריגים

## 2. תהליך האופטימיזציה - 5 שלבים

### שלב 1: Validation (בתוך המודול)
```python
def validate_data(bulk_df, template_df):
    # בדיקת עמודות נדרשות
    required_columns = ['Units', 'Clicks', 'Percentage', 'Entity', 
                       'Portfolio Name (Informational only)', 
                       'Campaign Name (Informational only)']
    
    # בדיקת קיום Portfolio בTemplate
    # בדיקת ערכי Base Bid
    # בדיקת Ignore portfolios
```

### שלב 2: ניקוי הנתונים

#### תנאי סינון
משאירים רק שורות שעונות על **כל** התנאים הבאים:

1. **Units = 0**  
   רק שורות שלא נמכרו בהן יחידות כלל

2. **Portfolio לא בשימוש Flat**  
   השדה `Portfolio Name (Informational only)` **לא** שווה לאף אחד מהערכים:
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

3. **Entity Types מותרים**
   - Entity = Keyword
   - Entity = Product Targeting  
   - Entity = Product Ad
   - Entity = Bidding Adjustment

### שלב 3: חלוקה ללשוניות

```python
# הפרדה לפי Entity Type
keywords_pt_df = df[df['Entity'].isin(['Keyword', 'Product Targeting'])]
bidding_adj_df = df[df['Entity'] == 'Bidding Adjustment']
product_ad_df = df[df['Entity'] == 'Product Ad']
```

### שלב 4: הוספת עמודות עזר וחישובן

#### עמודות עזר (משמאל לעמודה Bid)
רק בלשונית הראשית (Keyword + Product Targeting):

1. **Old Bid** = Bid (שמירת הערך המקורי)
2. **calc1** - חישוב ביניים
3. **calc2** - חישוב ביניים  
4. **Target CPA** - מ-Template לפי Portfolio Name
5. **Base Bid** - מ-Template לפי Portfolio Name
6. **Adj. CPA** = Target CPA × (1 + Max BA/100)
7. **Max BA** - חישוב מ-Percentage

#### חישוב Max BA
```python
def calculate_max_ba(row, bidding_adj_df):
    campaign_id = row['Campaign ID']
    
    # חיפוש Bidding Adjustments לקמפיין
    campaign_ba = bidding_adj_df[
        bidding_adj_df['Campaign ID'] == campaign_id
    ]
    
    if len(campaign_ba) > 0:
        return campaign_ba['Percentage'].max()
    else:
        return 1  # ברירת מחדל
```

### שלב 5: חישוב ה-Bid החדש

#### מקרה א: Target CPA חסר + "up and" בשם
```python
if pd.isna(target_cpa) and "up and" in campaign_name:
    new_bid = base_bid * 0.5
```

#### מקרה ב: Target CPA חסר + אין "up and"
```python
if pd.isna(target_cpa) and "up and" not in campaign_name:
    new_bid = base_bid
```

#### מקרה ג: Target CPA קיים + "up and" בשם
```python
if not pd.isna(target_cpa) and "up and" in campaign_name:
    calc1 = adj_cpa * 0.5 / (clicks + 1)
    calc2 = calc1 - base_bid * 0.5
    
    if calc1 <= 0:
        new_bid = calc2
    else:
        new_bid = base_bid * 0.5
```

#### מקרה ד: Target CPA קיים + אין "up and"
```python
if not pd.isna(target_cpa) and "up and" not in campaign_name:
    calc1 = adj_cpa / (clicks + 1)
    calc2 = calc1 - base_bid / (1 + max_ba / 100)
    
    if calc1 <= 0:
        new_bid = calc2
    else:
        new_bid = base_bid / (1 + max_ba / 100)
```

## 3. סימון שגיאות וערכים חריגים

### סימון בצבע ורוד
```python
def mark_errors(df):
    error_conditions = [
        df['Bid'] < 0.02,     # Below minimum
        df['Bid'] > 1.25,     # Above maximum
        df['Bid'].isna()      # Calculation failed
    ]
    
    df['has_error'] = np.any(error_conditions, axis=0)
    return df
```

### הודעות למשתמש
```python
low_bids = len(df[df['Bid'] < 0.02])
high_bids = len(df[df['Bid'] > 1.25])
calc_errors = len(df[df['Bid'].isna()])

message = f"{low_bids} rows below 0.02, {high_bids} rows above 1.25, {calc_errors} rows with calculation errors"
```

## 4. מבנה קבצי הפלט

### Working File
```python
sheets = {
    'Clean Zero Sales': keywords_pt_df,      # עם עמודות עזר
    'Bidding Adjustment Zero Sales': bidding_adj_df,  # ללא עמודות עזר
    'Product Ad Zero Sales': product_ad_df    # ללא עמודות עזר
}
```

### Clean File
כרגע זהה ל-Working File. בעתיד Clean לא יכלול עמודות עזר.

## 5. טיפול במקרי קצה

### Portfolio עם Ignore
```python
if base_bid == 'Ignore':
    # דילוג על כל השורות של Portfolio זה
    continue
```

### חלוקה באפס
```python
# תמיד מוסיפים 1 ל-Clicks
calc1 = adj_cpa / (clicks + 1)
```

### ערכי null
```python
# בדיקה לפני חישוב
if pd.isna(base_bid) or pd.isna(clicks):
    new_bid = np.nan  # סימון כשגיאה
```

## 6. ביצועים

### אופטימיזציות
- עיבוד וקטורי עם pandas
- אין loops על שורות בודדות
- חישובים בבלוקים

### זמני עיבוד צפויים
| מספר שורות | זמן עיבוד |
|------------|-----------|
| 1,000 | < 1 שנייה |
| 10,000 | 2-3 שניות |
| 100,000 | 10-15 שניות |
| 500,000 | 30-45 שניות |

## 7. דוגמת קוד

```python
class ZeroSalesOptimization(BaseOptimization):
    
    def process(self, bulk_df: pd.DataFrame, template_df: pd.DataFrame) -> pd.DataFrame:
        # 1. Validation
        self.validate(bulk_df, template_df)
        
        # 2. Cleaning
        cleaned_df = self.clean(bulk_df)
        
        # 3. Split by Entity
        dfs = self.split_by_entity(cleaned_df)
        
        # 4. Add helper columns
        dfs['keywords_pt'] = self.add_helper_columns(
            dfs['keywords_pt'], 
            template_df
        )
        
        # 5. Calculate new bids
        dfs['keywords_pt'] = self.calculate_bids(dfs['keywords_pt'])
        
        # 6. Mark errors
        dfs['keywords_pt'] = self.mark_errors(dfs['keywords_pt'])
        
        return dfs
```