#Helper Functions

import matplotlib.pyplot as plt
import numpy as np

from os import system, name

# Function to Clear the Screen
def clear_screen():
    if name == "nt": # User is running Windows
        _ = system('cls')
    else: # User is running Linux or Mac
        _ = system('clear')

# Function to sort the stock list (alphabetical) (Updated function- Kruthi)
def sortStocks(stock_list):
    stock_list.sort(key=lambda stock: stock.symbol)


# Function to sort the daily stock data (oldest to newest) for all stocks (Updated function- Kruthi)
def sortDailyData(stock_list):
    for stock in stock_list:
        stock.DataList.sort(key=lambda data: data.date)

# Function to create stock chart
def display_stock_chart(stock_list, symbol):
    for stock in stock_list:
        if stock.symbol == symbol:
            if not stock.DataList:
                print("No data available for chart.")
                return

            dates = [data.date for data in stock.DataList]
            closes = [data.close for data in stock.DataList]
            volumes = [data.volume for data in stock.DataList]

            # Ask user what to display
            print("\nChart Options:")
            print("1 - Price Only")
            print("2 - Price with Volume Bars")
            print("3 - Price with Moving Average")
            print("4 - Price + Volume + Moving Average")
            option = input("Choose chart type (1-4): ")

            plt.figure(figsize=(12, 6))

            # Price Line
            plt.plot(dates, closes, marker='o', linestyle='-', label='Closing Price')

            # Volume as bar chart
            if option in ["2", "4"]:
                plt.twinx()
                plt.bar(dates, volumes, alpha=0.3, color='gray', label='Volume')

            # Moving Average
            if option in ["3", "4"]:
                try:
                    window = int(input("Enter moving average window (e.g., 7): "))
                    if window < 1:
                        raise ValueError
                except:
                    print("Invalid input. Defaulting to 7-day moving average.")
                    window = 7

                moving_avg = np.convolve(closes, np.ones(window)/window, mode='valid')
                valid_dates = dates[window - 1:]
                plt.plot(valid_dates, moving_avg, color='green', linestyle='--', label=f'{window}-Day MA')

            plt.title(f"{stock.name} ({stock.symbol}) - Price History")
            plt.xlabel("Date")
            plt.ylabel("Price ($)")
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.legend()
            plt.tight_layout()
            plt.show()
            return

    print("Stock symbol not found in list.")
