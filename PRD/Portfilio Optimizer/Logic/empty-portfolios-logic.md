# Empty Portfolios Logic
**תאריך ושעה:** 07:15

## שלב 1
- בלשונית Portfolios יוצרים עמודה נוספת בשם Camp Count

## שלב 2
- כל שורה בלשונית פורטפוליוז מייצגת פורטפוליו מסוים
- בכל שורה בעמודה החדשה Camp Count מיישמים פעולה מקבילה ל-countifs ורושמים בשורה הזאת כמה קמפיינים קיימים בלשונית Campaigns שהערך שלהם בעמודה Portfolio ID שווה לערך של הפורטפוליו בלשונית Portfolios בעמודה Portfolio ID
- כך ממלאים את עמודת Camp Count בכל שורה שמייצגת כמה קמפיינים יש באותו פורטפוליו

## שלב 3
- לימין עמודה Portfolio Name בלשונית Portfolios יוצרים עמודה בשם Old Portfolio Name ומעתיקים אליה את כל השמות של הפורטפוליוז

## שלב 4
- בלשונית Portfolios מוצאים את השורות שעונות על התנאים:
  1. Camp Count = 0
  2. Portfolio Name is not either: "Paused", "Terminal", "Top Terminal", or a number.
- עבור השורות האלה בעמודה Portfolio Name משנים את הערך למספר הכי נמוך שלא קיים עדיין בעמודה הזאת

## שלב 5
- עבור השורות שעברו שינוי מוסיפים את הערך update בעמודה Operation

## שלב 6
- עבור השורות שעברו שינוי מוחקים את הערכים שבעמודות Budget Amount ו-Budget Start Date אם יש משהו בעמודות האלה
- משנים את הערך בעמודה Budget Policy = No Cap