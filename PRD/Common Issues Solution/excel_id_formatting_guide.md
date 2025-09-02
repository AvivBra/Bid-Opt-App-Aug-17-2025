# Excel ID/Serial Number Formatting Guide

## CRITICAL: Prevent Scientific Notation in Excel

### Problem Pattern
Long IDs/serial numbers display as scientific notation (e.g., 1.23E+10) or with .0 suffix

### Required Solution Approach

#### 1. **ALWAYS modify BOTH files:**
- `service.py` - data processing layer
- `excel_writer.py` - Excel writing layer

#### 2. **In service.py:**
```python
# Convert ALL ID columns to strings
id_keywords = ['ID', 'ASIN', 'Campaign ID', 'Product ID', 'Ad Group ID', 
               'Keyword ID', 'Portfolio ID', 'Target ID', 'Ad ID']
for col in df.columns:
    if any(keyword in col for keyword in id_keywords):
        df[col] = df[col].astype(str).str.replace('.0', '', regex=False)
```

#### 3. **In excel_writer.py:**
```python
# Force text format for ID columns - ALL sheets, not just specific ones
if is_id_column:  # NO sheet name restrictions!
    cell.number_format = "@"  # Excel text format
    cell.value = str(cell.value).replace('.0', '')
```

### Common Mistakes to Avoid
❌ Only fixing service.py without excel_writer.py  
❌ Applying text format only to specific sheets (e.g., only 'Campaign')  
❌ Checking ID columns AFTER type detection  
❌ Using incomplete ID keyword lists  

### Verification Checklist
- [ ] ID columns converted to string in service.py
- [ ] excel_writer.py applies "@" format to ALL ID columns
- [ ] No sheet-specific restrictions for ID formatting
- [ ] ID check happens BEFORE other type checks
- [ ] Both files use same comprehensive ID keyword list

### Test Command
After changes, verify no scientific notation appears in output Excel for columns containing: Campaign ID, Product Targeting ID, ASIN, or any column with "ID" in name.