# Summary: This module contains the functions used by both console and GUI programs to manage stock data.


import sqlite3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import csv
import time
import requests
from io import StringIO
from datetime import datetime
from utilities import clear_screen
from utilities import sortDailyData
from stock_class import Stock, DailyData

# Create the SQLite database
def create_database():
    stockDB = "stocks.db"
    conn = sqlite3.connect(stockDB)
    cur = conn.cursor()
    createStockTableCmd = """CREATE TABLE IF NOT EXISTS stocks (
                            symbol TEXT NOT NULL PRIMARY KEY,
                            name TEXT,
                            shares REAL
                        );"""
    createDailyDataTableCmd = """CREATE TABLE IF NOT EXISTS dailyData (
                                symbol TEXT NOT NULL,
                                date TEXT NOT NULL,
                                price REAL NOT NULL,
                                volume REAL NOT NULL,
                                PRIMARY KEY (symbol, date)
                        );"""   
    cur.execute(createStockTableCmd)
    cur.execute(createDailyDataTableCmd)

# Save stocks and daily data into database
def save_stock_data(stock_list):
    stockDB = "stocks.db"
    conn = sqlite3.connect(stockDB)
    cur = conn.cursor()
    insertStockCmd = """INSERT INTO stocks
                            (symbol, name, shares)
                            VALUES
                            (?, ?, ?); """
    insertDailyDataCmd = """INSERT INTO dailyData
                                    (symbol, date, price, volume)
                                    VALUES
                                    (?, ?, ?, ?);"""
    for stock in stock_list:
        insertValues = (stock.symbol, stock.name, stock.shares)
        try:
            cur.execute(insertStockCmd, insertValues)
            cur.execute("COMMIT;")
        except:
            pass
        for daily_data in stock.DataList: 
            insertValues = (stock.symbol,daily_data.date.strftime("%m/%d/%y"),daily_data.close,daily_data.volume)
            try:
                cur.execute(insertDailyDataCmd, insertValues)
                cur.execute("COMMIT;")
            except:
                pass
    
# Load stocks and daily data from database
def load_stock_data(stock_list):
    stock_list.clear()
    stockDB = "stocks.db"
    conn = sqlite3.connect(stockDB)
    stockCur = conn.cursor()
    stockSelectCmd = """SELECT symbol, name, shares
                    FROM stocks; """
    stockCur.execute(stockSelectCmd)
    stockRows = stockCur.fetchall()
    for row in stockRows:
        new_stock = Stock(row[0],row[1],row[2])
        dailyDataCur = conn.cursor()
        dailyDataCmd = """SELECT date, price, volume
                        FROM dailyData
                        WHERE symbol=?; """
        selectValue = (new_stock.symbol)
        dailyDataCur.execute(dailyDataCmd,(selectValue,))
        dailyDataRows = dailyDataCur.fetchall()
        for dailyRow in dailyDataRows:
            daily_data = DailyData(datetime.strptime(dailyRow[0],"%m/%d/%y"),float(dailyRow[1]),float(dailyRow[2]))
            new_stock.add_data(daily_data)
        stock_list.append(new_stock)
    sortDailyData(stock_list)

# Get stock price history from web using Web Scraping
def retrieve_stock_web(dateStart, dateEnd, stock_list):
    dateFrom = str(int(time.mktime(time.strptime(dateStart, "%m/%d/%y"))))
    dateTo = str(int(time.mktime(time.strptime(dateEnd, "%m/%d/%y"))))
    recordCount = 0

    for stock in stock_list:
        stockSymbol = stock.symbol
        url = f"https://finance.yahoo.com/quote/{stockSymbol}/history?period1={dateFrom}&period2={dateTo}&interval=1d&filter=history&frequency=1d"

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option("prefs", {'profile.managed_default_content_settings.javascript': 2})

        try:
            driver = webdriver.Chrome(options=options)
            driver.implicitly_wait(60)
            driver.get(url)
        except:
            raise RuntimeError("Chrome Driver Not Found")

        soup = BeautifulSoup(driver.page_source, "html.parser")
        dataRows = soup.find_all('tr')

        existing_dates = set(d.date for d in stock.DataList)

        for row in dataRows:
            td = row.find_all('td')
            rowList = [i.text for i in td]
            if len(rowList) == 7:
                try:
                    date = datetime.strptime(rowList[0], "%b %d, %Y")
                    if date in existing_dates:
                        continue
                    close = float(rowList[5].replace(',', ''))
                    volume = float(rowList[6].replace(',', ''))
                    daily_data = DailyData(date, close, volume)
                    stock.add_data(daily_data)
                    recordCount += 1
                except Exception as e:
                    print(f"Skipped row due to error: {e}")
    return recordCount

# Get price and volume history from Yahoo! Finance using CSV import.
def import_stock_web_csv(stock_list, symbol, filename):
    for stock in stock_list:
        if stock.symbol == symbol:
            existing_dates = set(d.date for d in stock.DataList)  # collect existing dates
            with open(filename, newline='') as stockdata:
                datareader = csv.reader(stockdata, delimiter=',')
                next(datareader)  # Skip header
                for row in datareader:
                    try:
                        date = datetime.strptime(row[0], "%Y-%m-%d")
                        if date in existing_dates:
                            continue  # Skip if date already exists
                        close = float(row[4])
                        volume = float(row[6])
                        daily_data = DailyData(date, close, volume)
                        stock.add_data(daily_data)
                    except Exception as e:
                        print(f"Skipping row due to error: {e}")

def import_stock_csv_from_yahoo(stock_list, symbol, start_date, end_date):
    for stock in stock_list:
        if stock.symbol == symbol:
            try:
                period1 = int(time.mktime(time.strptime(start_date, "%m/%d/%y")))
                period2 = int(time.mktime(time.strptime(end_date, "%m/%d/%y")))

                url = f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={period1}&period2={period2}&interval=1d&events=history"
                headers = {
                    "User-Agent": "Mozilla/5.0"
                }

                for attempt in range(3):
                    response = requests.get(url, headers=headers)
                    if response.status_code == 200:
                        break
                    elif response.status_code == 429:
                        print("Rate limited. Retrying after delay...")
                        time.sleep(5 * (attempt + 1))
                    else:
                        raise RuntimeError(f"Failed to download CSV: HTTP {response.status_code}")

                if response.status_code != 200:
                    raise RuntimeError("Failed to download CSV after retries.")

                data = StringIO(response.text)
                reader = csv.reader(data)
                next(reader)

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

def main():
    clear_screen()
    print("This module will handle data storage and retrieval.")

if __name__ == "__main__":
    # execute only if run as a stand-alone script
    main()