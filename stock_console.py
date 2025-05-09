# Summary: This module contains the user interface and logic for a console-based version of the stock manager program.

from datetime import datetime
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart
from os import path
from io import StringIO
import stock_data
import time
import csv
import requests


# Main Menu
def main_menu(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Stock Analyzer ---")
        print("1 - Manage Stocks (Add, Update, Delete, List)")
        print("2 - Add Daily Stock Data (Date, Price, Volume)")
        print("3 - Show Report")
        print("4 - Show Chart")
        print("5 - Manage Data (Save, Load, Retrieve)")
        print("0 - Exit Program")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","5","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("Stock Analyzer ---")
            print("1 - Manage Stocks (Add, Update, Delete, List)")
            print("2 - Add Daily Stock Data (Date, Price, Volume)")
            print("3 - Show Report")
            print("4 - Show Chart")
            print("5 - Manage Data (Save, Load, Retrieve)")
            print("0 - Exit Program")
            option = input("Enter Menu Option: ")
        if option == "1":
            manage_stocks(stock_list)
        elif option == "2":
            add_stock_data(stock_list)
        elif option == "3":
            display_report(stock_list)
        elif option == "4":
            display_chart(stock_list)
        elif option == "5":
            manage_data(stock_list)
        else:
            clear_screen()
            print("Goodbye")

# Manage Stocks
def manage_stocks(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Stocks ---")
        print("1 - Add Stock")
        print("2 - Update Shares")
        print("3 - Delete Stock")
        print("4 - List Stocks")
        print("0 - Exit Manage Stocks")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("1 - Add Stock")
            print("2 - Update Shares")
            print("3 - Delete Stock")
            print("4 - List Stocks")
            print("0 - Exit Manage Stocks")
            option = input("Enter Menu Option: ")
        if option == "1":
            add_stock(stock_list)
        elif option == "2":
            update_shares(stock_list)
        elif option == "3":
            delete_stock(stock_list)
        elif option == "4":
            list_stocks(stock_list)
        else:
            print("Returning to Main Menu")

# Add new stock to track (Updated function- Kruthi)
def add_stock(stock_list):
    clear_screen()
    symbol = input("Enter Ticker Symbol: ").upper()
    for stock in stock_list:
        if stock.symbol == symbol:
            print("Stock already exists.")
            input("Press Enter to continue...")
            return
    name = input("Enter Company Name: ")
    try:
        shares = float(input("Enter Number of Shares: "))
        if shares <= 0:
            print("Error: Shares must be greater than 0.")
            input("Press Enter to continue...")
            return
    except ValueError:
        print("Invalid number.")
        input("Press Enter to continue...")
        return
    new_stock = Stock(symbol, name, shares)
    stock_list.append(new_stock)
    print("Stock Added.")
    input("Press Enter to continue...")
        
# Buy or Sell Shares Menu (Updated function- Kruthi)
def update_shares(stock_list):
    clear_screen()
    print("Update Shares")

    symbol = input("Enter Ticker Symbol to Update: ").upper()
    for stock in stock_list:
        if stock.symbol == symbol:
            option = input("Enter 1 to Buy or 2 to Sell: ")
            try:
                amount = float(input("Enter number of shares: "))
                if option == "1":
                    stock.buy(amount)
                    print(f"Bought {amount} shares of {symbol}.")
                elif option == "2":
                    stock.sell(amount)
                    print(f"Sold {amount} shares of {symbol}.")
                else:
                    print("Invalid option.")
            except ValueError as ve:
                print(f"Error: {ve}")
            except Exception:
                print("Invalid input. Please enter a valid number.")
            input("Press Enter to continue...")
            return

    print(f"Stock {symbol} not found.")
    input("Press Enter to continue...")


# Buy Stocks (add to shares)
def buy_stock(stock_list):
    clear_screen()
    print("Buy Shares")

    symbol = input("Enter Ticker Symbol to Buy: ").upper()
    for stock in stock_list:
        if stock.symbol == symbol:
            value = input("Enter number of shares to buy: ").strip()
            if not value:
                print("Error: Share amount cannot be empty.")
                input("Press Enter to continue...")
                return

            try:
                amount = float(value)
                if amount <= 0:
                    raise ValueError("Shares must be greater than 0.")
                stock.buy(amount)
                print(f"Bought {amount} shares of {symbol}.")
            except ValueError as ve:
                print(f"Error: {ve}")
            input("Press Enter to continue...")
            return

    print("Stock not found.")
    input("Press Enter to continue...")

# Sell Stocks (subtract from shares)
def sell_stock(stock_list):
    clear_screen()
    print("Sell Shares")

    symbol = input("Enter Ticker Symbol to Sell: ").upper()
    for stock in stock_list:
        if stock.symbol == symbol:
            value = input("Enter number of shares to sell: ").strip()
            if not value:
                print("Error: Share amount cannot be empty.")
                input("Press Enter to continue...")
                return

            try:
                amount = float(value)
                if amount <= 0:
                    raise ValueError("Shares must be greater than 0.")
                stock.sell(amount)
                print(f"Sold {amount} shares of {symbol}.")
            except ValueError as ve:
                print(f"Error: {ve}")
            input("Press Enter to continue...")
            return

    print("Stock not found.")
    input("Press Enter to continue...")

# Remove stock and all daily data ()
def delete_stock(stock_list):
    clear_screen()
    symbol = input("Enter Ticker Symbol to Delete: ").upper()
    for stock in stock_list:
        if stock.symbol == symbol:
            stock_list.remove(stock)
            print("Stock Deleted.")
            break
    else:
        print("Stock not found.")
    input("Press Enter to continue...")


# List stocks being tracked ()
def list_stocks(stock_list):
    clear_screen()
    print("Stocks Being Tracked:")
    for stock in stock_list:
        print(f"{stock.symbol} - {stock.name} ({stock.shares} shares)")
    input("Press Enter to continue...")

# Add Daily Stock Data ()
def add_stock_data(stock_list):
    from datetime import datetime
    clear_screen()
    symbol = input("Enter Ticker Symbol: ").upper()
    for stock in stock_list:
        if stock.symbol == symbol:
            try:
                date = datetime.strptime(input("Enter Date (m/d/yy): "), "%m/%d/%y")
                if any(d.date == date for d in stock.DataList):
                    print("Data for this date already exists.")
                    input("Press Enter to continue...")
                    return
                close = float(input("Enter Closing Price: "))
                volume = float(input("Enter Volume: "))
                daily = DailyData(date, close, volume)
                stock.add_data(daily)
                print("Daily Data Added.")
            except ValueError:
                print("Invalid input. Please check the date and numbers.")
            break
    else:
        print("Stock not found.")
    input("Press Enter to continue...")

# Display Report for All Stocks ()
def display_report(stock_list):
    clear_screen()
    for stock in stock_list:
        print(f"Symbol: {stock.symbol} | Name: {stock.name} | Shares: {stock.shares}")
        print("- Date -   - Price -   - Volume -")
        for daily in stock.DataList:
            print(f"{daily.date.strftime('%m/%d/%y')}   ${daily.close:.2f}   {int(daily.volume)}")
        print("="*40)
    input("Press Enter to continue...")

# Display Chart ()
def display_chart(stock_list):
    clear_screen()
    symbol = input("Enter Ticker Symbol for Chart: ").upper()
    display_stock_chart(stock_list, symbol)
    input("Press Enter to continue...")

# Manage Data Menu ()
def manage_data(stock_list):
    while True:
        clear_screen()
        print("Manage Data ---")
        print("1 - Save to Database")
        print("2 - Load from Database")
        print("3 - Retrieve from Web")
        print("4 - Import from CSV")
        print("0 - Exit")
        option = input("Enter Menu Option: ")
        if option == "1":
            stock_data.save_stock_data(stock_list)
            print("Data Saved.")
            input("Press Enter to continue...")
        elif option == "2":
            stock_data.load_stock_data(stock_list)
            print("Data Loaded.")
            input("Press Enter to continue...")
        elif option == "3":
            retrieve_from_web(stock_list)
        elif option == "4":
            import_csv(stock_list)
        elif option == "0":
            break


# Get stock price and volume history from Yahoo! Finance using Web Scraping
def retrieve_from_web(stock_list):
    clear_screen()
    print("Retrieve Stock Data from Web")

    symbol = input("Enter Ticker Symbol to Retrieve: ").upper()
    dateFrom = input("Enter Start Date (m/d/yy): ")
    dateTo = input("Enter End Date (m/d/yy): ")

    # Find the stock by symbol
    selected_stock = [stock for stock in stock_list if stock.symbol == symbol]
    if not selected_stock:
        print(f"Error: Stock {symbol} not found in your portfolio.")
        input("Press Enter to continue...")
        return

    try:
        recordCount = stock_data.retrieve_stock_web(dateFrom, dateTo, selected_stock)
        print(f"{recordCount} records retrieved for {symbol} successfully.")
    except Exception as e:
        print(f"Error: Could not retrieve data. Reason: {str(e)}")

    input("Press Enter to continue...")



# Import stock price and volume history from Yahoo! Finance using CSV Import
def import_csv(stock_list):
    clear_screen()
    print("Import CSV Stock Data")

    symbol = input("Enter Ticker Symbol to Import Data For: ").upper()
    matching_stock = [stock for stock in stock_list if stock.symbol == symbol]
    if not matching_stock:
        print(f"Error: Stock {symbol} not found in your portfolio.")
        input("Press Enter to continue...")
        return

    try:
        from tkinter import filedialog, Tk
        Tk().withdraw()
        filename = filedialog.askopenfilename(
            title=f"Select CSV File for {symbol}",
            filetypes=[("CSV Files", "*.csv")]
        )
    except Exception as e:
        print(f"File dialog error: {e}")
        filename = input("Enter full path to .csv file: ").strip()

    if not filename:
        print("No file selected.")
    elif not path.exists(filename):
        print("Error: File not found.")
    else:
        try:
            stock_data.import_stock_web_csv(matching_stock, symbol, filename)
            print(f"CSV Data Imported Successfully for {symbol}.")
        except Exception as e:
            print(f"Error: Import failed. Reason: {str(e)}")

    input("Press Enter to continue...")

def import_stock_csv_from_yahoo(stock_list, symbol, start_date, end_date):
    for stock in stock_list:
        if stock.symbol == symbol:
            try:
                period1 = int(time.mktime(time.strptime(start_date, "%m/%d/%y")))
                period2 = int(time.mktime(time.strptime(end_date, "%m/%d/%y")))

                url = f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={period1}&period2={period2}&interval=1d&events=history"
                response = requests.get(url)

                if response.status_code != 200:
                    raise RuntimeError(f"Failed to download CSV: HTTP {response.status_code}")

                data = StringIO(response.text)
                reader = csv.reader(data)
                next(reader)  # Skip header

                existing_dates = set(d.date for d in stock.DataList)
                imported = 0

                for row in reader:
                    try:
                        date = datetime.strptime(row[0], "%Y-%m-%d")
                        if date in existing_dates:
                            continue
                        close = float(row[4])
                        volume = float(row[6])
                        stock.add_data(DailyData(date, close, volume))
                        imported += 1
                    except:
                        continue

                return imported
            except Exception as e:
                raise RuntimeError(f"CSV Import Error: {e}")

# Begin program
def main():
    #check for database, create if not exists
    if path.exists("stocks.db") == False:
        stock_data.create_database()
    stock_list = []
    main_menu(stock_list)

# Program Starts Here
if __name__ == "__main__":
    # execute only if run as a stand-alone script
    main()