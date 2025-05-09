# stock_analyzer
The Stock Analyzer is a Python-based application developed for managing and analyzing stock portfolios. It enables users to track stock prices, import historical data from Yahoo Finance (via scraping or CSV), and visualize performance through charts. The project meets the objectives of integrating GUI and Console interfaces, ensuring ease of use and robust data handling

#### Project Details:
This is an implementation of the stock analysis system. It includes a console interface and a Graphical User Interface (GUI) to manage stocks portfolio, retrieve data via web scraping and import CSV files manually from Yahoo Finance.
1.	A Graphical User Interface (GUI) for intuitive point-and-click interaction
2.	A Console interface for keyboard-driven workflows
Both modes allow users to:
3.	Add and manage stock symbols
4.	Buy or sell fractional and whole shares
5.	Import historical price data
6.	View price and volume charts
7.	Save and reload data from a SQLite database

#### Key Functionalities:
Buy/Sell Stocks
•	Validates integer/decimal input
•	Blocks invalid or negative values
•	Prevents selling more than owned
Data Import
•	CSV Import: Users can manually select CSV files downloaded from Yahoo Finance
•	Web Scraping: Pulls historical stock data directly from Yahoo using Selenium
Visualization
•	Users can generate charts to view:
o	Daily closing prices
o	Volume overlays
o	Moving averages
Persistence
•	Stock and daily price data are stored in a local SQLite database
•	Data can be saved or loaded using the GUI/Console

#### Features:
•	Add, delete, buy, and sell stocks (float and integer support)
•	Save/load portfolio data using SQLite
•	Web scrape historical data from Yahoo Finance
•	Manually import CSV files (no auto-downloads)
•	View stock data history and charts with price, volume, and moving average overlays
•	Input validation and error handling for user-friendly experience

#### Conclusion
The Stock Analyzer application provides a versatile, user-friendly platform for managing stock data while incorporating robust error handling and multiple methods of data input. The code is modular, maintainable, and ready for future enhancements such as real-time APIs or extended analytics.
