# Campaign Optimizer 1 - תהליך ניקוי

**תאריך ושעה:** 07:20

## תהליך ניקוי

### שלב 1
הולכת ללשונית Sponsored Products Campaigns
ומשם מעבירה את כל השורות שבהן Entity = Campaign
ללשונית חדשה שקוראת לה Campaign

### שלב 2
המערכת מוחקת את כל הלשוניות שאינן Campaign

### שלב 3
המערכת מוחקת כל שורה שבה מתקיים אחד מהתנאים הבאים לפחות:
- State = paused
- Campaign State (Informational only) = paused
- Ad Group State (Informational only) = paused