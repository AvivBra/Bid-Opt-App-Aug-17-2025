# איפיון Product Targeting - Campaign Creator

**תאריך:** 28.08.2025  
**שעה:** 15:50

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

## טבלת Product Targeting

| # | עמודה | Testing PT | Expanded | Halloween Testing PT | Halloween Expanded |
|---|--------|------------|----------|---------------------|-------------------|
| 1 | My ASIN | From template | From template | From template | From template |
| 2 | Product Type | From template | From template | From template | From template |
| 3 | Niche | From template | From template | From template | From template |
| 4 | Target | From Data Dive (ASINs only, not keywords) | From Data Dive (ASINs only, not keywords) | From Data Dive (ASINs only, not keywords) | From Data Dive (ASINs only, not keywords) |
| 5 | Product | Sponsored Products | Sponsored Products | Sponsored Products | Sponsored Products |
| 6 | Entity | Campaign / Ad Group / Product Ad / Product Targeting | Campaign / Ad Group / Product Ad / Product Targeting | Campaign / Ad Group / Product Ad / Product Targeting | Campaign / Ad Group / Product Ad / Product Targeting |
| 7 | Operation | Create | Create | Create | Create |
| 8 | Campaign ID | Testing \| PT \| {ASIN} \| {product targeting} \| {niche} | Expanded \| {ASIN} \| {product targeting} \| {niche} | Halloween \| Testing \| PT \| {ASIN} \| {product targeting} \| {niche} | Expanded \| {ASIN} \| {product targeting} \| {niche} |
| 9 | Ad Group ID | {ASIN} | {ASIN} | {ASIN} | {ASIN} |
| 10 | Portfolio ID | Empty | Empty | Empty | Empty |
| 11 | Ad ID | Empty | Empty | Empty | Empty |
| 12 | Keyword ID | Empty | Empty | Empty | Empty |
| 13 | Product Targeting ID | Empty | Empty | Empty | Empty |
| 14 | Campaign Name | {Campaign ID} | {Campaign ID} | {Campaign ID} | {Campaign ID} |
| 15 | Ad Group Name | {Ad Group ID} | {Ad Group ID} | {Ad Group ID} | {Ad Group ID} |
| 16 | Start Date | {yyyymmdd} | {yyyymmdd} | {yyyymmdd} | {yyyymmdd} |
| 17 | End Date | Empty | Empty | Empty | Empty |
| 18 | Targeting Type | MANUAL | MANUAL | MANUAL | MANUAL |
| 19 | State | enabled | enabled | enabled | enabled |
| 20 | Daily Budget | 1 | 1 | 1 | 1 |
| 21 | SKU | Empty | Empty | Empty | Empty |
| 22 | ASIN | {ASIN} | {ASIN} | {ASIN} | {ASIN} |
| 23 | Ad Group Default Bid | 0.15 | 0.15 | 0.15 | 0.15 |
| 24 | Bid | [Variable by campaign - from template] | [Variable by campaign - from template] | [Variable by campaign - from template] | [Variable by campaign - from template] |
| 25 | Keyword Text | ריק | ריק | ריק | ריק |
| 26 | Native Language Keyword | Empty | Empty | Empty | Empty |
| 27 | Native Language Locale | Empty | Empty | Empty | Empty |
| 28 | Match Type | ריק | ריק | ריק | ריק |
| 29 | Bidding Strategy | Dynamic bids - down only | Dynamic bids - down only | Dynamic bids - down only | Dynamic bids - down only |
| 30 | Placement | Empty | Empty | Empty | Empty |
| 31 | Percentage | Empty | Empty | Empty | Empty |
| 32 | Product Targeting Expression | asin="{ASIN from the target from the template}" | asin-expanded="{ASIN from the target from the template}" | asin="{ASIN from the target from the template}" | asin-expanded="{ASIN from the target from the template}" |

## Template Bid Column Mapping

### Product Targeting Campaign Bid Columns

| Campaign Type | Template Bid Column |
|---------------|-------------------|
| Testing PT | Testing PT Bid |
| Expanded | Expanded Bid |
| Halloween Testing PT | Halloween Testing PT Bid |
| Halloween Expanded | Halloween Expanded Bid |

### Bid Column Usage Notes:
- Each campaign type reads its bid value from its specific template column
- Bid values must be between MIN_BID (0.02) and MAX_BID (1.5)

## Session Table ASIN Structure

### ASIN Target Data Format

**Session Table Structure for Product Targeting:**
```
target          | ASIN          | Product Type | Niche        | Campaign type        | Bid  | kw cvr | kw sales
B0ABC123DEF     | B09XYZ456GHI  | Books        | Fiction      | Testing PT           | 0.30 | None   | None
B0ABC123DEF     | B09XYZ456GHI  | Books        | Fiction      | Expanded             | 0.25 | None   | None
```

### Key Data Points:

**ASIN Identification:**
- ASINs in `target` column are identified by starting with "B0"
- ASINs are extracted from Data Dive file column headers
- Example: Column "B0ABC123DEF Sales Rank" → ASIN "B0ABC123DEF"

**Session Table Columns:**
- `target`: The ASIN being targeted (from Data Dive headers)
- `ASIN`: Template ASIN (the product being advertised) 
- `Product Type`: From template
- `Niche`: From template
- `Campaign type`: PT campaign type (Testing PT, Expanded, etc.)
- `Bid`: Bid value from template bid column
- `kw cvr`: Always None for ASINs (keyword-only field)
- `kw sales`: Always None for ASINs (keyword-only field)

### ASIN Processing Logic:

**Data Source:** ASINs extracted from Data Dive column headers starting with "B0"
**Filtering:** Product Targeting campaigns only process targets where `str(target).startswith('B0')`
**No Data Rova Required:** ASINs don't need CVR/sales thresholds like keywords do
**Product Targeting Expression:** 
- Testing PT / Halloween Testing PT: `asin="B0ABC123DEF"`  
- Expanded / Halloween Expanded: `asin-expanded="B0ABC123DEF"`