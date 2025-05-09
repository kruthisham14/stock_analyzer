Stock Analyzer

This file contains instructions to be followed to execute the stock analyzer application. 

Console Interface instructions:
1. Run `stocks.py` and choose **Console Mode**.
2. From the main menu, you can:
  - Add/Delete Stocks
  - Buy/Sell shares with validated decimal or integer input
   - Import historical data:
   - 📁 **CSV Import**: Opens file dialog to select `.csv` file
   - 🌐 **Web Scrape**: Prompts for ticker, start and end date (`MM/DD/YYYY`)
3. Dates must be entered in this format: `01/01/25` (2-digit year)
4. Console prints confirmation or error messages after every action.

GUI Instructions

1. Run `stocks.py` and choose **GUI Mode**.
2. Use the left list to select a stock.
3. Use the tabs and buttons to:
   - Add/Buy/Sell shares
   - Import historical data:
     - 📁 **Import CSV from Yahoo** (file dialog opens)
     - 🌐 **Scrape from Yahoo** (uses ChromeDriver)
   - View history and charts with dropdown selection
4. Errors show in popups if input is missing or invalid.


CSV Format for Manual Upload:
Download a CSV file from Yahoo Finance, formatted like:
“
Date,Open,High,Low,Close,Adj Close,Volume2024-01-01,145.30,147.00,144.50,146.75,146.75,30480000
”
Select this file when prompted in Console or GUI.

Requirements:
•	Install matplotlib, NumPy, pandas requests selenium beautifulsoup4
•	Also install [ChromeDriver](https://sites.google.com/chromium.org/driver/) and add it to the system PATH for web scraping to work.
