Here are 3 critical Playwright practices I apply:

  - only launch like this: kill all old Chromium windows > launch > wait for 3 > only then procceed
  
  - Wait for elements before interacting with them - Use explicit waits to
  ensure elements are ready
  
  - Use JavaScript evaluate for stubborn UI elements - Bypass accessibility tree
   issues with DOM manipulation
  - Click label containers instead of radio buttons - Avoid overlay interception
   by targeting parent elements