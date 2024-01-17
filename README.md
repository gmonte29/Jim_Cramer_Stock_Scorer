# Stock-Buy-Sell-Predictor
Program that receives a minimum and maximum revenue, and a sector and returns buy/sell suggestion for stocks that fit the parameters 

Stock Score Formula - (stock PE / group PE - 1) * -1 / 2 + (stock GR / group GR - 1) / 2

Libraries Utilized:
Flask==2.3.2
pandas==2.1.4
PySimpleGUI==4.60.5
yfinance==0.2.35
gunicorn==21.2.0
