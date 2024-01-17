import pandas as pd
import yfinance as yf
from datetime import datetime

'''
Python file here is used to create the dataframe of all stocks included in the local ticker_list csv
Dataframe is created off of 2 dimensional list that contains the following details of each stock
 - Ticker
 - Industry
 - Revenue
 - Growth rate
 - P/E ratio
 
Dataframe is saved to a pickle file to be used for data analysis
'''
todays_date = datetime.today().date()

#read csv file of tickers into a dataframe and convert to a list
tickerCSV = pd.read_csv("https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=demo")
tickers = list(tickerCSV['symbol'])


#Code below creates a new list and iterates through all tickers from the CSV file
#A ticker will only be included in the resulting DataFrame if the yFinance API includes all the requested info for it
tickerList = []
exception_set = set()

for ticker in tickers:
     try:
          current = yf.Ticker(ticker)
     except:
          exception_set.add(ticker)
          continue
     
     try:
          industry = current.info['sector']
     except:
          exception_set.add(ticker)
          continue
     
     try:
          revenue = current.info['totalRevenue']
     except:
          exception_set.add(ticker)
          continue
     
     try:
          growth = current.info['revenueGrowth']
     except:
          exception_set.add(ticker)
          continue
     
     try:
          if current.info['trailingPE'] == 'Infinity':
               raise Exception()
          pe = current.info['trailingPE']
     except:
          exception_set.add(ticker)
          continue
     
     tickerList.append((ticker, industry, revenue, growth, pe))
     
table = pd.DataFrame(tickerList, columns=['Ticker','Sector', 'Revenue', 'Growth Rate', 'PE Ratio'])

#Save the resulting table to a pickle file that will be used in the other program
table.to_pickle('stock_table.pkl')

#Message indicating that dataframe has been updated and saved to pickle file
print("number of ticker exceptions: ",len(exception_set))
print("number of ticker successes: ",len(tickerList))

print('table complete')





