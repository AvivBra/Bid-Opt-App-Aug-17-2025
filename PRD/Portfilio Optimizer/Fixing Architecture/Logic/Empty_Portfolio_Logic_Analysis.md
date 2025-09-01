# Empty Portfolio Logic Analysis
**Date:** August 31, 2025  
**Analysis:** PRD Specification vs Code Implementation  
**Focus:** "Empty Portfolio" identification and processing logic

---


**Step 1: Identification Method:** 
1. add a new column in the "Portfolios" tab, to the right of the column "In Budget (Informational only)" and call the new column "campaign count"
2. Use a COUNTIFS-like approach to add a campaign count to the "campaign count". Count matching Portfolio ID values between Portfolios and Campaigns sheets. Empty portfolios have Campaign_Count "0"


### **Step 3: Empty Portfolio Identification**
   - It's not in the excluded names list (`["Paused", "Terminal"]`)










