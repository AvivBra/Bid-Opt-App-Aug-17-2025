"""Inspect expected output format."""

import pandas as pd
from pathlib import Path

# Load expected output
expected_path = Path("PRD/Portfilio Optimizer/Excel Examples/Empty Port Output Bulk Example.xlsx")
expected_df = pd.read_excel(expected_path, sheet_name="Portfolios", dtype=str)

print("Expected output info:")
print(f"Shape: {expected_df.shape}")
print(f"Columns: {list(expected_df.columns)}")
print()

# Check a few specific rows to understand format
print("Sample of Operation column (first 10 rows):")
for i, val in enumerate(expected_df['Operation'].head(10)):
    print(f"  Row {i}: '{val}' (type: {type(val)})")
print()

print("Sample of Budget Amount column (first 10 rows):")
for i, val in enumerate(expected_df['Budget Amount'].head(10)):
    print(f"  Row {i}: '{val}' (type: {type(val)})")
print()

print("Sample of Camp Count column (first 10 rows):")
for i, val in enumerate(expected_df['Camp Count'].head(10)):
    print(f"  Row {i}: '{val}' (type: {type(val)})")
print()

# Look for the renamed portfolio
renamed_mask = expected_df['Portfolio Name'] == '1'
if renamed_mask.any():
    renamed_row = expected_df[renamed_mask].iloc[0]
    print("Renamed portfolio row:")
    for col in expected_df.columns:
        print(f"  {col}: '{renamed_row[col]}'")
    print()

# Check unique values in Operation column
print("Unique values in Operation column:")
print(expected_df['Operation'].value_counts())