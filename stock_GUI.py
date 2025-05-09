# Summary: This module contains the user interface and logic for a graphical user interface version of the stock manager program.

from datetime import datetime
from os import path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, simpledialog, filedialog
import csv
import stock_data
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart, sortStocks, sortDailyData
from matplotlib import pyplot as plt
import numpy as np

class StockApp:
    def __init__(self):
        self.stock_list = []
        #check for database, create if not exists
        if path.exists("stocks.db") == False:
            stock_data.create_database()

 # This section creates the user interface

        # Create Window
        self.root = Tk()
        self.root.title("(myname) Stock Manager") #Replace with a suitable name for your program


        # Add Menubar
        self.menubar = Menu(self.root)

        # Add File Menu
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Load from Database", command=self.load)
        self.filemenu.add_command(label="Save to Database", command=self.save)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.root.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        # Add Web Menu 
        self.webmenu = Menu(self.menubar, tearoff=0)
        self.webmenu.add_command(label="Scrape Data from Yahoo! Finance...", command=self.scrape_web_data)
        self.webmenu.add_command(label="Import CSV from Yahoo! Finance...", command=self.importCSV_web_data)
        self.menubar.add_cascade(label="Web", menu=self.webmenu)

        # Add Chart Menu
        self.chartmenu = Menu(self.menubar, tearoff=0)
        self.chartmenu.add_command(label="Display Chart", command=self.display_chart)
        self.menubar.add_cascade(label="Chart", menu=self.chartmenu)

        # Add menus to window (Attach menubar)      
        self.root.config(menu=self.menubar)

        # Add heading information (Heading Label)
        self.headingLabel = Label(self.root, text="Stock Manager", font=("Arial", 14))
        self.headingLabel.pack(pady=10)
        

        # Add stock list (Stock List Frame)
        listFrame = Frame(self.root)
        listFrame.pack(pady=5)
        scrollbar = Scrollbar(listFrame)
        self.stockList = Listbox(listFrame, width=40, height=6, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.stockList.yview)
        self.stockList.bind("<<ListboxSelect>>", self.update_data)
        self.stockList.pack(side=LEFT)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        
        # Add Tabs (Tab Control)
        self.tabControl = ttk.Notebook(self.root)
 
        

        # Set Up Main Tab
        self.mainTab = Frame(self.tabControl)
        self.tabControl.add(self.mainTab, text="Main")

        Label(self.mainTab, text="Symbol:").grid(row=0, column=0, sticky=E)
        self.addSymbolEntry = Entry(self.mainTab)
        self.addSymbolEntry.grid(row=0, column=1)
        Label(self.mainTab, text="Name:").grid(row=1, column=0, sticky=E)
        self.addNameEntry = Entry(self.mainTab)
        self.addNameEntry.grid(row=1, column=1)
        Label(self.mainTab, text="Shares:").grid(row=2, column=0, sticky=E)
        self.addSharesEntry = Entry(self.mainTab)
        self.addSharesEntry.grid(row=2, column=1)
        Button(self.mainTab, text="Add Stock", command=self.add_stock).grid(row=3, columnspan=2, pady=5)

        Label(self.mainTab, text="Update Shares:").grid(row=4, column=0, sticky=E)
        self.updateSharesEntry = Entry(self.mainTab)
        self.updateSharesEntry.grid(row=4, column=1)
        Button(self.mainTab, text="Buy Shares", command=self.buy_shares).grid(row=5, column=0)
        Button(self.mainTab, text="Sell Shares", command=self.sell_shares).grid(row=5, column=1)
        Button(self.mainTab, text="Delete Stock", command=self.delete_stock).grid(row=6, columnspan=2, pady=5)


        # Setup History Tab
        self.historyTab = Frame(self.tabControl)
        self.tabControl.add(self.historyTab, text="History")
        self.dailyDataList = Text(self.historyTab, width=60, height=10)
        self.dailyDataList.pack()
        
        
        # Setup Report Tab
        self.reportTab = Frame(self.tabControl)
        self.tabControl.add(self.reportTab, text="Report")
        self.stockReport = Text(self.reportTab, width=60, height=10)
        self.stockReport.pack()

        self.tabControl.pack(expand=1, fill="both")
        self.root.mainloop()

        ## Call MainLoop
        ##self.root.mainloop()

# This section provides the functionality
       
    # Load stocks and history from database.
    def load(self):
        self.stockList.delete(0,END)
        stock_data.load_stock_data(self.stock_list)
        sortStocks(self.stock_list)
        for stock in self.stock_list:
            self.stockList.insert(END,stock.symbol)
        messagebox.showinfo("Load Data","Data Loaded")

    # Save stocks and history to database.
    def save(self):
        stock_data.save_stock_data(self.stock_list)
        messagebox.showinfo("Save Data","Data Saved")

    # Refresh history and report tabs
    def update_data(self, evt):
        self.display_stock_data()

    # Display stock price and volume history.
    def display_stock_data(self):
        if not self.stockList.curselection():
            return
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
                self.dailyDataList.delete("1.0", END)
                self.stockReport.delete("1.0", END)
                self.dailyDataList.insert(END, "- Date -   - Price -   - Volume -\n")
                self.dailyDataList.insert(END, "=================================\n")
                for daily_data in stock.DataList:
                    row = daily_data.date.strftime("%m/%d/%y") + "   " +  '${:0,.2f}'.format(daily_data.close) + "   " + str(daily_data.volume) + "\n"
                    self.dailyDataList.insert(END, row)
                self.stockReport.insert(END, f"Total Days Tracked: {len(stock.DataList)}\n")
                if stock.DataList:
                    total_value = stock.shares * stock.DataList[-1].close
                    self.stockReport.insert(END, f"Current Value: ${total_value:,.2f}\n")
                break

    # Add new stock to track.    
    def add_stock(self):
        symbol = self.addSymbolEntry.get().upper()
        name = self.addNameEntry.get()
        try:
            shares = float(self.addSharesEntry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for shares.")
            return

        # Check if symbol already exists
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.buy(shares)
                messagebox.showinfo("Updated Stock", f"{shares} shares added to existing stock {symbol}.")
                self.update_stock_list()
                self.clear_add_fields()
                return

        # If new stock, add it
        new_stock = Stock(symbol, name, shares)
        self.stock_list.append(new_stock)
        self.update_stock_list()
        self.clear_add_fields()


    # Buy shares of stock.    
    def buy_shares(self):
        symbol = self.get_selected_symbol()
        if not symbol:
            return
    
        value = self.updateSharesEntry.get()
        if not value or not value.strip():
            messagebox.showerror("Buy Error", "Please enter a number of shares.")
            return
        
        try:
            amount = float(value.strip())
            if amount <= 0:
                raise ValueError("Shares must be greater than 0.")
        except ValueError as ve:
            messagebox.showerror("Buy Error", f"Invalid input: {ve}")
            return
        
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.buy(amount)
                self.headingLabel['text'] = f"{stock.name} - {stock.shares} Shares"
                messagebox.showinfo("Buy Shares", f"Bought {amount} shares of {symbol}.")
                break

        self.updateSharesEntry.delete(0, END)

    # Sell shares of stock.
    def sell_shares(self):
        symbol = self.get_selected_symbol()
        if not symbol:
            return
        
        value = self.updateSharesEntry.get()
        if not value or not value.strip():
            messagebox.showerror("Sell Error", "Please enter a number of shares.")
            return
        
        try:
            amount = float(value.strip())
            if amount <= 0:
                raise ValueError("Shares must be greater than 0.")
        except ValueError as ve:
            messagebox.showerror("Sell Error", f"Invalid input: {ve}")
            return
    
        for stock in self.stock_list:
            if stock.symbol == symbol:
                try:
                    #amount = float(self.updateSharesEntry.get())
                    stock.sell(amount)
                    self.headingLabel['text'] = f"{stock.name} - {stock.shares} Shares"
                    messagebox.showinfo("Sell Shares", f"Sold {amount} shares of {symbol}.")
                except ValueError as ve:
                    messagebox.showerror("Sell Error", str(ve))
                break
    
        self.updateSharesEntry.delete(0, END)

    # Remove stock and all history from being tracked.
    def delete_stock(self):

        symbol = self.get_selected_symbol()
        if not symbol:
            return

        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                self.stock_list.remove(stock)
                self.stockList.delete(self.stockList.curselection())
                messagebox.showinfo("Delete", f"{symbol} Deleted")
                return

    # Get data from web scraping.
    def scrape_web_data(self):

        symbol = self.get_selected_symbol()
        if not symbol:
            return
        ## Yahoo finance only allows 60 days of data 
        dateFrom = simpledialog.askstring("Starting Date","Enter Starting Date (m/d/yy)")
        dateTo = simpledialog.askstring("Ending Date","Enter Ending Date (m/d/yy")
        if not dateFrom or not dateTo:
            messagebox.showwarning("Invalid Input", "Start and End dates must be provided.")
            return
        
        try:
            # Filter to selected stock only
            selected_stock = [stock for stock in self.stock_list if stock.symbol == symbol]
            if not selected_stock:
                messagebox.showerror("Error", f"Stock {symbol} not found in list.")
                return
            
            stock_data.retrieve_stock_web(dateFrom, dateTo, selected_stock)
            self.display_stock_data()
            messagebox.showinfo("Get Data From Web", f"Data Retrieved for {symbol}")
        except Exception as e:
            messagebox.showerror("Cannot Get Data from Web", f"Check Chrome Driver. Error: {str(e)}")

    # Import CSV stock history file.
    def importCSV_web_data(self):
        symbol = self.get_selected_symbol()
        if not symbol:
            return
        
        filename = filedialog.askopenfilename(title=f"Select CSV file for {symbol}",filetypes=[("CSV Files", "*.csv")])

        if not filename:
            return
        
        try:
            stock_data.import_stock_web_csv(self.stock_list, symbol, filename)
            self.display_stock_data()
            messagebox.showinfo("CSV Import", f"Imported data for {symbol} from {filename}.")
        except Exception as e:
            messagebox.showerror("Import Error", str(e))

    # Display stock price chart.
    def display_chart(self):
        symbol = self.get_selected_symbol()
        if not symbol:
            return
        #symbol = self.stockList.get(self.stockList.curselection())
        #display_stock_chart(self.stock_list,symbol)
        self.gui_display_stock_chart(symbol)

    # Additional function implemented for moving avg etc features
    def gui_display_stock_chart(self, symbol):
        
        for stock in self.stock_list:
            if stock.symbol == symbol:
                if not stock.DataList:
                    messagebox.showinfo("No Data", "No data available for this stock.")
                    return
    
                dates = [data.date for data in stock.DataList]
                closes = [data.close for data in stock.DataList]
                volumes = [data.volume for data in stock.DataList]
    
                # Ask user via dialog
                chart_option = simpledialog.askinteger(
                    "Chart Options",
                    "Select Chart Type:\n1 - Price Only\n2 - Price + Volume\n3 - Price + Moving Average\n4 - All",
                    parent=self.root, minvalue=1, maxvalue=4
                )
                if chart_option is None:
                    return
    
                if chart_option in [3, 4]:
                    window = simpledialog.askinteger("Moving Average", "Enter MA Window (e.g. 7):", parent=self.root, minvalue=1)
                    if window is None:
                        window = 7
                else:
                    window = None
    
                fig, ax1 = plt.subplots(figsize=(12, 6))
    
                # Plot price
                ax1.plot(dates, closes, marker='o', linestyle='-', label='Closing Price', color='blue')
                ax1.set_xlabel("Date")
                ax1.set_ylabel("Price ($)", color='blue')
                ax1.tick_params(axis='y', labelcolor='blue')
                ax1.set_title(f"{stock.name} ({stock.symbol}) - Price History")
                ax1.grid(True)
                plt.xticks(rotation=45)
    
                # Moving Average
                if window and window <= len(closes):
                    moving_avg = np.convolve(closes, np.ones(window)/window, mode='valid')
                    valid_dates = dates[window - 1:]
                    ax1.plot(valid_dates, moving_avg, color='green', linestyle='--', label=f'{window}-Day MA')
    
                # Volume on secondary y-axis
                if chart_option in [2, 4]:
                    ax2 = ax1.twinx()
                    ax2.bar(dates, volumes, alpha=0.3, color='gray', label='Volume')
                    ax2.set_ylabel("Volume", color='gray')
                    ax2.tick_params(axis='y', labelcolor='gray')
    
                fig.tight_layout()
                fig.legend(loc="upper left")
                plt.show()
                return
    
        messagebox.showerror("Symbol Not Found", f"Stock symbol {symbol} not found.")
    

    # Adding this helper function to import csv error
    def get_selected_symbol(self):
        """Returns the selected symbol or None if nothing is selected."""
        selection = self.stockList.curselection()
        if not selection:
            messagebox.showwarning("No Stock Selected", "Please select a stock from the list first.")
            return None
        return self.stockList.get(selection)
    
    def update_stock_list(self):
        """Refresh the stock list box."""
        self.stockList.delete(0, END)
        for stock in self.stock_list:
            self.stockList.insert(END, stock.symbol)

    def clear_add_fields(self):
        """Clear input fields after add or update."""
        self.addSymbolEntry.delete(0, END)
        self.addNameEntry.delete(0, END)
        self.addSharesEntry.delete(0, END)

def main():
        app = StockApp()
        

if __name__ == "__main__":
    # execute only if run as a script
    main()