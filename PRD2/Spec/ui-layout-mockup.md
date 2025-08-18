### Layout
```
Container:     max-width: 800px, centered
Card Padding:  32px
Section Gap:   48px
Element# סימולציית פריסת עמוד - Bid Optimizer

## עיצוב כללי
- **רקע:** Dark mode (#0F0F0F)
- **צבע ראשי:** Violet (#8B5CF6)
- **פונט:** Inter Regular 400
- **סגנון:** Minimalist, Centered, No icons

---

## מבנה כללי

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  ┌────────┐                                                 │
│  │        │         MAIN CONTENT AREA                       │
│  │  SIDE  │    ┌─────────────────────────────┐             │
│  │  BAR   │    │                             │             │
│  │        │    │    Centered Content         │             │
│  │        │    │                             │             │
│  │        │    └─────────────────────────────┘             │
│  └────────┘                                                 │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Sidebar - שלב ראשון
```
┌──────────────┐
│              │
│     BID      │
│  OPTIMIZER   │ ← Violet BG (Active)
│              │   
│──────────────│
│              │
│  CAMPAIGNS   │ ← Dark BG (Disabled - Phase 5)
│  OPTIMIZER   │   Grayed out
│              │
└──────────────┘
```

---

## Main Content - Bid Optimizer Page

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│                                                              │
│                      BID OPTIMIZER                          │
│                    ─────────────────                        │
│                                                              │
│     ┌──────────────────────────────────────────────┐       │
│     │                                                │       │
│     │            SELECT OPTIMIZATIONS                │       │
│     │                                                │       │
│     │  ┌────────────────────────────────────────┐  │       │
│     │  │                                         │  │       │
│     │  │ □ Zero Sales                           │  │       │
│     │  │                                         │  │       │
│     │  │ (13 more optimizations - Phase 3)      │  │       │
│     │  │                                         │  │       │
│     │  └────────────────────────────────────────┘  │       │
│     │                                                │       │
│     └──────────────────────────────────────────────┘       │
│                                                              │
│     ┌──────────────────────────────────────────────┐       │
│     │                                                │       │
│     │               UPLOAD FILES                    │       │
│     │                                                │       │
│     │  ┌──────────────────┐ ┌──────────────────┐  │       │
│     │  │Download Template │ │   Bulk 7 Days    │  │       │
│     │  └──────────────────┘ └──────────────────┘  │       │
│     │                                                │       │
│     │  ┌──────────────────┐ ┌──────────────────┐  │       │
│     │  │  Bulk 30 Days    │ │   Bulk 60 Days   │  │       │
│     │  └──────────────────┘ └──────────────────┘  │       │
│     │                                                │       │
│     │         ┌──────────────────────┐             │       │
│     │         │      Data Rova        │             │       │
│     │         └──────────────────────┘             │       │
│     │                                                │       │
│     │  Template: Not uploaded                       │       │
│     │  Bulk: Not uploaded                           │       │
│     │                                                │       │
│     └──────────────────────────────────────────────┘       │
│                                                              │
│     ┌──────────────────────────────────────────────┐       │
│     │                                                │       │
│     │            DATA VALIDATION                    │       │
│     │                                                │       │
│     │  [Hidden until files uploaded]                │       │
│     │                                                │       │
│     └──────────────────────────────────────────────┘       │
│                                                              │
│     ┌──────────────────────────────────────────────┐       │
│     │                                                │       │
│     │             OUTPUT FILES                      │       │
│     │                                                │       │
│     │  [Hidden until processing complete]           │       │
│     │                                                │       │
│     └──────────────────────────────────────────────┘       │
│                                                              │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## מצבי תצוגה

### State 1: Initial (Upload)
```
┌──────────────────────────────────────────────┐
│           SELECT OPTIMIZATIONS                │
│  ┌────────────────────────────────────────┐  │
│  │ □ Zero Sales                           │  │
│  └────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│              UPLOAD FILES                     │
│                                               │
│        ┌──────────────────────┐              │
│        │  Download Template    │              │
│        └──────────────────────┘              │
│                                               │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│ │ Bulk 7   │ │ Bulk 30  │ │ Bulk 60  │     │
│ └──────────┘ └──────────┘ └──────────┘     │
│                                               │
│        ┌──────────────────────┐              │
│        │  Data Rova           │              │
│        └──────────────────────┘              │
│                                               │
│ Template: Not uploaded                        │
│ Bulk: Not uploaded                            │
└──────────────────────────────────────────────┘
```

### State 2: Files Uploaded - Validation Running
```
┌──────────────────────────────────────────────┐
│              UPLOAD FILES                     │
│                                               │
│ Template: template.xlsx (125 KB)             │
│ Bulk: bulk_30.xlsx (2.3 MB)                  │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│           DATA VALIDATION                     │
│                                               │
│         Validating portfolios...              │
│         ━━━━━━━━━━━━━━━━━━━━━                │
│                                               │
└──────────────────────────────────────────────┘
```

### State 3: Validation Complete - Ready
```
┌──────────────────────────────────────────────┐
│           DATA VALIDATION                     │
│                                               │
│    All portfolios valid                       │
│    234 rows ready for processing              │
│                                               │
│         ┌──────────────────────┐             │
│         │    Process Files     │             │
│         └──────────────────────┘             │
└──────────────────────────────────────────────┘
```

### State 4: Processing
```
┌──────────────────────────────────────────────┐
│            OUTPUT FILES                       │
│                                               │
│    Processing Zero Sales optimization...      │
│    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━             │
│                65%                            │
│                                               │
└──────────────────────────────────────────────┘
```

### State 5: Complete
```
┌──────────────────────────────────────────────┐
│            OUTPUT FILES                       │
│                                               │
│    Processing complete                        │
│                                               │
│    Files generated:                          │
│    Working File: 2.4 MB (3 sheets)          │
│    Clean File: 1.8 MB (2 sheets)            │
│                                               │
│  ┌──────────────────┐ ┌──────────────────┐ │
│  │ Download Working │ │  Download Clean  │ │
│  └──────────────────┘ └──────────────────┘ │
│                                               │
│        ┌──────────────────────┐             │
│        │        Reset          │             │
│        └──────────────────────┘             │
└──────────────────────────────────────────────┘
```

---

## Validation Messages Examples

### Success
```
┌──────────────────────────────────────────────┐
│           DATA VALIDATION                     │
│                                               │
│    All portfolios valid                       │
│    5 portfolios found                        │
│    1,234 rows ready for processing           │
│                                               │
│         ┌──────────────────────┐             │
│         │    Process Files     │             │
│         └──────────────────────┘             │
└──────────────────────────────────────────────┘
```

### Missing Portfolios
```
┌──────────────────────────────────────────────┐
│           DATA VALIDATION                     │
│                                               │
│    Missing portfolios found                   │
│                                               │
│    The following portfolios are in the       │
│    Bulk file but not in Template:            │
│    • Portfolio_ABC                           │
│    • Portfolio_DEF                           │
│                                               │
│         ┌──────────────────────┐             │
│         │  Upload New Template  │             │
│         └──────────────────────┘             │
└──────────────────────────────────────────────┘
```

### Some Ignored
```
┌──────────────────────────────────────────────┐
│           DATA VALIDATION                     │
│                                               │
│    Validation complete with notes             │
│                                               │
│    3 portfolios marked as Ignore             │
│    2 portfolios ready for processing         │
│    845 rows will be processed                │
│                                               │
│         ┌──────────────────────┐             │
│         │    Process Files     │             │
│         └──────────────────────┘             │
└──────────────────────────────────────────────┘
```

---

## עיצוב מינימליסטי

### Elements
- Text only - no icons/emojis
- Clean 1px borders
- No shadows or gradients
- Simple checkboxes
- Plain progress bars
- Centered layout
- **All buttons same size**

### Colors
```
Background:    #0F0F0F
Card BG:       #1A1A1A  
Border:        #2D2D2D
Text:          #FFFFFF
Secondary:     #A1A1A1
Accent:        #8B5CF6
Success:       #10B981
Error:         #EF4444
```

### Typography
```
Page Title:    Inter 400, 28px, centered
Section Title: Inter 400, 18px, uppercase
Body Text:     Inter 400, 14px
Button Text:   Inter 400, 14px, uppercase
Status Text:   Inter 400, 12px
```

### Layout
```
Container:     max-width: 800px, centered
Card Padding:  32px
Section Gap:   48px
Element Gap:   16px
Button Height: 44px
Button Width:  200px (all buttons)
Border Radius: 4px
```