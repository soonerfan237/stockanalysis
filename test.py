import yfinance as yf
import datetime

symbol = 'MMM'
yf.pdr_override()

data = yf.download(symbol, start='2004-12-30', end='2017-12-01')
print(data)