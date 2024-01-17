# Stock-Buy-Sell-Predictor
Program that receives a minimum and maximum revenue, and a sector and returns buy/sell suggestion for stocks that fit the parameters 

Files:

stock_table_create.py - program that takes all stock tickers and receives from yfinance the ticker, sector, revenue, growth rate, and PE for each stock. Enters all information into a pandas data frame where there is a row for each stock and a column for each data type pulled from yfinance. Dataframe saved to a pickle file (stock_table.pkl) to be accessed for data analysis.

ticker_List.csv - Used by stock_table_create.py to access data from yfinance for every stock

stock_buy_sell.py - takes stock table created from stock_table_create.py and filters for best and worst stocks within the revenue and sector parameters entered by user in user interface. Best and worst stocks determined based on P/E and growth rate of stocks compared to the average for the group. 

Formula - (stock PE / group PE - 1) * -1 / 2 + (stock GR / group GR - 1) / 2

Libraries Utilized:
yFinance
Pandas
PySimpleGUI
