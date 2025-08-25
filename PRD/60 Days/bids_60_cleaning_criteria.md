# קריטריונים לניקוי - Bids 60 Days
**תאריך: 18/08/2025 07:15**

## קריטריונים למחיקת שורות:

### 1. חלוקה לגיליונות לפי Entity type
   - **Targeting:** Entity = "Keyword" או "Product Targeting"
   - **Bidding Adjustment:** Entity = "Bidding Adjustment"
   - **Product Ad:** Entity = "Product Ad"

### 2. סינון על גיליון Targeting בלבד:

#### 2.1 מחיקת שורות עם units ≤ 0

#### 2.2 מחיקת שורות עם Portfolio Name המופיע ברשימה:
   - "Flat 30"
   - "Flat 25"
   - "Flat 40"
   - "Flat 25 | Opt"
   - "Flat 30 | Opt"
   - "Flat 20"
   - "Flat 15"
   - "Flat 40 | Opt"
   - "Flat 20 | Opt"
   - "Flat 15 | Opt"

#### 2.3 מחיקת שורות שהפורטפוליו שלהן מסומן כ-Ignore:
   - בודקים את הערך בעמודה **Portfolio Name (Informational only)** בקובץ Bulk
   - מחפשים את הפורטפוליו בגיליון **Port Values** בקובץ Template
   - אם הערך בעמודה **Base Bid** בטמפלט = "Ignore" - מוחקים את השורה

#### 2.4 מחיקת שורות לפי רשימת IDs מהטמפלט:
   - מוחקים שורות שהערך ב-**Keyword ID** או **Product Targeting ID** מופיע בגיליון **"Delete for 60"** בקובץ Template

#### 2.5 מחיקת שורות לפי מצב (State):
   - State ≠ "enabled"
   - Campaign State (Informational only) ≠ "enabled"
   - Ad Group State (Informational only) ≠ "enabled"

### 3. שמירת כל 48 העמודות המקוריות ללא שינוי