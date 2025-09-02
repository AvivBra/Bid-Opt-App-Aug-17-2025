# Campaign Optimizer 1 - לוגיקת עיבוד

**תאריך ושעה:** 09:00

## Step 1
if (
Units = 0
&
Daily Budget > 1
)

then set:
- Daily Budget = 1
- Operation = update

## Step 2
if (
Units > 0
&
ACOS > .17
&
Daily Budget > 1
)

then set:
- Daily Budget = 1
- Operation = update

## Step 3
if (
Units > 0
&
ACOS < .17
&
Daily Budget < 3
)

then set:
- Daily Budget = 3
- Operation = update

## Step 4
if (
Units > 2
&
ACOS < .17
&
Daily Budget < 5
)

then set:
- Daily Budget = 5
- Operation = update