# תבנית בסיסית - מבנה עמודות לקמפיינים

## מבנה עמודות (זהה לכל הקמפיינים)

| # | עמודה | תוכן |
|---|--------|------|
| 1 | My ASIN | מהטמפלט |
| 2 | Product Type | מהטמפלט |
| 3 | Niche | מהטמפלט |
| 4 | Target | מ-Data Dive (Keywords בלבד, לא ASINs) |
| 5 | Product | **קבוע:** "Sponsored Products" |
| 6 | Entity | **לשונית 1:** Campaign<br>**לשונית 2:** Ad Group<br>**לשונית 3:** Product Ad<br>**לשונית 4:** Keyword |
| 7 | Operation | **קבוע:** "Create" |
| 8 | Campaign ID | **[משתנה לפי קמפיין]** |
| 9 | Ad Group ID | {ASIN} |
| 10 | Portfolio ID | ריק |
| 11 | Ad ID | ריק |
| 12 | Keyword ID | ריק |
| 13 | Product Targeting ID | ריק |
| 14 | Campaign Name | {Campaign ID} |
| 15 | Ad Group Name | {Ad Group ID} |
| 16 | Start Date | {yyyymmdd} |
| 17 | End Date | ריק |
| 18 | Targeting Type | **קבוע:** "MANUAL" |
| 19 | State | **קבוע:** "enabled" |
| 20 | Daily Budget | **קבוע: 1** |
| 21 | SKU | ריק |
| 22 | ASIN | {ASIN} |
| 23 | Ad Group Default Bid | **קבוע: 0.15** |
| 24 | Bid | **[משתנה לפי קמפיין - מהטמפלט]** |
| 25 | Keyword Text | מ-target (keywords בלבד) |
| 26 | Native Language Keyword | ריק |
| 27 | Native Language Locale | ריק |
| 28 | Match Type | **[משתנה לפי קמפיין]** |
| 29 | Bidding Strategy | **קבוע:** "Dynamic bids - down only" |
| 30 | Placement | ריק |
| 31 | Percentage | ריק |
| 32 | Product Targeting Expression | ריק |

## טבלת השדות המשתנים בלבד

| # | עמודה | Testing | Phrase | Broad | Halloween Testing | Halloween Phrase | Halloween Broad |
|---|--------|---------|--------|-------|-------------------|------------------|-----------------|
| 8 | Campaign ID | Testing \| {ASIN} \| {product type} \| {Niche} | Phrase \| {ASIN} \| {product type} \| {Niche} | Broad \| {ASIN} \| {product type} \| {Niche} | Testing \| Halloween \| {ASIN} \| {product type} \| {niche} | Halloween Phrase \| {ASIN} \| {product type} \| {Niche} | Halloween Broad \| {ASIN} \| {product type} \| {Niche} |
| 28 | Match Type | exact | phrase | broad | exact | phrase | broad |

## מבנה הלשוניות בקובץ הפלט

### לשונית 1: Campaign
- **Entity:** "Campaign"
- **שורות:** שורה אחת בלבד לכל קמפיין

### לשונית 2: Ad Group
- **Entity:** "Ad Group"
- **שורות:** שורה אחת בלבד לכל קמפיין

### לשונית 3: Product Ad
- **Entity:** "Product Ad"
- **שורות:** שורה אחת בלבד לכל קמפיין

### לשונית 4: Keyword
- **Entity:** "Keyword"
- **שורות:** שורה נפרדת לכל keyword