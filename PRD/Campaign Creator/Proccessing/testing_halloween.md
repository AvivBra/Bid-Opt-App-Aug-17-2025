# טמפלט קמפיין Halloween Testing - מבנה עמודות

**תאריך:** 27.08.2025  
**שעה:** 17:45

| # | עמודה | תוכן |
|---|--------|------|
| 1 | My ASIN | מהטמפלט |
| 2 | Product Type | מהטמפלט |
| 3 | Niche | מהטמפלט |
| 4 | Target | מ-Data Dive (Keywords + ASINs) |
| 5 | Product | **קבוע:** "Sponsored Products" |
| 6 | Entity | **לשונית 1:** Campaign<br>**לשונית 2:** Ad Group<br>**לשונית 3:** Product Ad<br>**לשונית 4:** Keyword |
| 7 | Operation | **קבוע:** "Create" |
| 8 | Campaign ID | Testing \| Halloween \| {ASIN} \| {product type} \| {niche} |
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
| 20 | Daily Budget | **קבוע:** 1 |
| 21 | SKU | ריק |
| 22 | ASIN | {ASIN} |
| 23 | Ad Group Default Bid | **קבוע:** 0.15 |
| 24 | Bid | מה-Bid המתאים |
| 25 | Keyword Text | מ-target (keywords בלבד) |
| 26 | Native Language Keyword | ריק |
| 27 | Native Language Locale | ריק |
| 28 | Match Type | **קבוע:** "exact" |
| 29 | Bidding Strategy | **קבוע:** "Dynamic bids - down only" |
| 30 | Placement | ריק |
| 31 | Percentage | ריק |
| 32 | Product Targeting Expression | ריק |

## איך בונים את הלשוניות השונות בקובץ הפלט

### לשונית 1: Campaign
- **Entity:** "Campaign"
- **שורות:** שורה אחת בלבד לכל קמפיין
- **דוגמה:** אם יש 20 keywords בקמפיין, תופיע רק שורה אחת עם keyword אחד מייצג

### לשונית 2: Ad Group
- **Entity:** "Ad Group"
- **שורות:** שורה אחת בלבד לכל קמפיין
- **דוגמה:** אם יש 20 keywords בקמפיין, תופיע רק שורה אחת עם keyword אחד מייצג

### לשונית 3: Product Ad
- **Entity:** "Product Ad"
- **שורות:** שורה אחת בלבד לכל קמפיין
- **דוגמה:** אם יש 20 keywords בקמפיין, תופיע רק שורה אחת עם keyword אחד מייצג

### לשונית 4: Keyword
- **Entity:** "Keyword"
- **שורות:** כל השורות - שורה נפרדת לכל keyword
- **דוגמה:** אם יש 20 keywords בקמפיין, יופיעו 20 שורות