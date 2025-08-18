# פריסת מסך מינימליסטית - Bid Optimizer (shadcn style)

## מסך ראשי - Dark Mode, Minimal Design

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│                                                                      │
│                      BID OPTIMIZER                                  │
│                    Automated Bid Management                         │
│                                                                      │
│                                                                      │
│     ┌──────────────────────────────────────────────────────┐       │
│     │                 Select Optimizations                  │       │
│     ├──────────────────────────────────────────────────────┤       │
│     │                                                        │       │
│     │     [✓] Zero Sales                                   │       │
│     │     [ ] Portfolio Bid                                │       │
│     │     [ ] Budget Optimization                          │       │
│     │     [ ] Keyword Optimization                         │       │
│     │     [ ] ASIN Targeting                               │       │
│     │     [ ] Negative Targeting                           │       │
│     │     [ ] Campaign Structure Optimization              │       │
│     │     [ ] Dayparting Optimization                      │       │
│     │     [ ] Placement Optimization                       │       │
│     │     [ ] Search Term Optimization                     │       │
│     │     [ ] Product Attribute Targeting                  │       │
│     │     [ ] Bid Adjustment Optimization                  │       │
│     │     [ ] Match Type Optimization                      │       │
│     │     [ ] Geographic Optimization                      │       │
│     │                                                        │       │
│     └──────────────────────────────────────────────────────┘       │
│                                                                      │
│     ┌──────────────────────────────────────────────────────┐       │
│     │                    Upload Files                       │       │
│     ├──────────────────────────────────────────────────────┤       │
│     │                                                        │       │
│     │            ┌─────────────────────────┐               │       │
│     │            │   Download Template     │               │       │
│     │            └─────────────────────────┘               │       │
│     │                                                        │       │
│     │     ┌──────────────┐  ┌──────────────┐              │       │
│     │     │   Template    │  │   Bulk 30    │              │       │
│     │     │              │  │              │              │       │
│     │     │  Choose file │  │  Choose file │              │       │
│     │     └──────────────┘  └──────────────┘              │       │
│     │     template.xlsx      Not uploaded                  │       │
│     │     125 KB                                           │       │
│     │                                                        │       │
│     │     ┌──────────────┐  ┌──────────────┐              │       │
│     │     │   Bulk 60    │  │   Bulk 7     │              │       │
│     │     │              │  │              │              │       │
│     │     │  Choose file │  │  Choose file │              │       │
│     │     └──────────────┘  └──────────────┘              │       │
│     │     bulk_60.xlsx       Not uploaded                  │       │
│     │     2.3 MB                                           │       │
│     │                                                        │       │
│     │            ┌──────────────┐                          │       │
│     │            │   Data Rova   │                          │       │
│     │            │              │                          │       │
│     │            │  Choose file │                          │       │
│     │            └──────────────┘                          │       │
│     │            Not uploaded                              │       │
│     │                                                        │       │
│     └──────────────────────────────────────────────────────┘       │
│                                                                      │
│     ┌──────────────────────────────────────────────────────┐       │
│     │                 Validation Results                    │       │
│     ├──────────────────────────────────────────────────────┤       │
│     │                                                        │       │
│     │     Zero Sales           Ready to process            │       │
│     │     Portfolio Bid        Missing Bulk 30 file        │       │
│     │     Budget Optimization  Missing Bulk 7 file         │       │
│     │                                                        │       │
│     │            ┌─────────────────────────┐               │       │
│     │            │     Process Files       │               │       │
│     │            └─────────────────────────┘               │       │
│     │                                                        │       │
│     └──────────────────────────────────────────────────────┘       │
│                                                                      │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

## מצב Processing - Minimal

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│     ┌──────────────────────────────────────────────────────┐       │
│     │                    Processing                         │       │
│     ├──────────────────────────────────────────────────────┤       │
│     │                                                        │       │
│     │     Processing Zero Sales                            │       │
│     │                                                        │       │
│     │     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░  65%           │       │
│     │                                                        │       │
│     │     Elapsed: 00:03    Remaining: 00:02               │       │
│     │                                                        │       │
│     └──────────────────────────────────────────────────────┘       │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

## מצב Complete - Minimal

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│     ┌──────────────────────────────────────────────────────┐       │
│     │                 Processing Complete                   │       │
│     ├──────────────────────────────────────────────────────┤       │
│     │                                                        │       │
│     │   ┌────────────────────┐  ┌────────────────────┐    │       │
│     │   │ Download Working    │  │ Download Clean     │    │       │
│     │   └────────────────────┘  └────────────────────┘    │       │
│     │                                                        │       │
│     │   Working File                Clean File             │       │
│     │   3.2 MB · 2 sheets          2.8 MB · 1 sheet       │       │
│     │                                                        │       │
│     │   ┌──────────────────────────────────────────────┐  │       │
│     │   │                  Note                         │  │       │
│     │   │  12 calculation errors found                 │  │       │
│     │   │  · 5 rows below 0.02                        │  │       │
│     │   │  · 3 rows above 1.25                        │  │       │
│     │   │  · 4 calculation errors                     │  │       │
│     │   └──────────────────────────────────────────────┘  │       │
│     │                                                        │       │
│     │            ┌─────────────────────────┐               │       │
│     │            │     New Processing      │               │       │
│     │            └─────────────────────────┘               │       │
│     │                                                        │       │
│     └──────────────────────────────────────────────────────┘       │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

## מצב Missing Portfolios - Minimal

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│     ┌──────────────────────────────────────────────────────┐       │
│     │           Missing Portfolios Found                    │       │
│     ├──────────────────────────────────────────────────────┤       │
│     │                                                        │       │
│     │     The following portfolios exist in Bulk            │       │
│     │     but not in Template:                             │       │
│     │                                                        │       │
│     │     · Portfolio_ABC                                  │       │
│     │     · Portfolio_DEF                                  │       │
│     │     · Portfolio_GHI                                  │       │
│     │                                                        │       │
│     │     Add these portfolios to your Template file        │       │
│     │     and upload again to continue.                    │       │
│     │                                                        │       │
│     │            ┌─────────────────────────┐               │       │
│     │            │   Upload New Template   │               │       │
│     │            └─────────────────────────┘               │       │
│     │                                                        │       │
│     └──────────────────────────────────────────────────────┘       │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

## עקרונות עיצוב מינימליסטיים (shadcn style)

### טיפוגרפיה
```
Title:          Inter 500, 24px, #FAFAFA
Section Header: Inter 500, 14px, #FAFAFA  
Body:           Inter 400, 14px, #B0B5BD
Small:          Inter 400, 12px, #6C757D
Button:         Inter 500, 14px, #FAFAFA
```

### צבעים
```
Background:     #0E1117 (main)
Card:           #1A1D23
Border:         #2E3138 (1px solid)
Primary:        #9B6BFF (violet)
Text Primary:   #FAFAFA
Text Secondary: #B0B5BD
Text Muted:     #6C757D
```

### מרווחים
```
Page Padding:   48px
Card Padding:   24px
Section Gap:    32px
Element Gap:    16px
Button Height:  36px
Border Radius:  4px
```

### כפתורים
```
┌─────────────────────┐
│    Button Text      │  Height: 36px
└─────────────────────┘  Padding: 12px 24px
                        Border: 1px solid
                        Radius: 4px
```

### Checkboxes
```
[ ] Unchecked - Border: #2E3138
[✓] Checked   - Background: #9B6BFF
                Size: 16x16px
                Gap to text: 12px
```

### Progress Bar
```
▓▓▓▓▓▓▓▓░░░░░░  - Height: 8px
                  Background: #2E3138
                  Fill: #9B6BFF
                  Radius: 4px
```

### מבנה כרטיס
```
┌──────────────────────────────┐
│         Header               │  Font: Inter 500, 14px
├──────────────────────────────┤  Border: 1px solid #2E3138
│                              │  
│         Content              │  Padding: 24px
│                              │  
└──────────────────────────────┘  Radius: 4px
```

## הערות חשובות

1. **ללא אייקונים** - כל הטקסט נקי, ללא אימוג'י
2. **מרכוז מלא** - כל האלמנטים ממורכזים, רוחב מקסימלי 800px
3. **כפתורים זה לצד זה** - בשורה אחת עם מרווח ביניהם
4. **מינימום צבעים** - רק violet, שחור ואפור
5. **גבולות דקים** - 1px בלבד
6. **ללא צללים** - עיצוב שטוח לחלוטין
7. **רדיוסים קטנים** - 4px מקסימום