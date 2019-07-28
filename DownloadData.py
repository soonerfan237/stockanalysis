import yfinance as yf
import pandas as pd
import copy
import datetime

def FetchSymbol(symbol):
    print(symbol)
    yf.pdr_override()
    data = yf.download(symbol, start='2004-12-30', end='2019-12-01')

    data_lw = copy.deepcopy(data)
    data_lw['DateLastWeek'] = data_lw.index - pd.to_timedelta(7, unit='d')
    data_lw = data_lw.set_index('DateLastWeek')

    data = data_lw.join(data, lsuffix='_lw')
    data['Date'] = data.index + pd.to_timedelta(7, unit='d')
    data = data.set_index('Date')

    data['Symbol'] = symbol
    data['ChangeDay'] = data.Open - data.Close
    data['ChangeWeek'] = data.Open_lw - data.Close
    data['ChangeDayBool'] = data.ChangeDay > 0
    data = data[data.Open.notnull()]
    #print(data)
    return data
def DownloadData(symbols):
    pd.set_option('display.expand_frame_repr', False)
    #cols = ['Date','Open_lw','High_lw','Low_lw','Close_lw','Adj Close_lw','Volume_lw','Open','High','Low','Close','Adj Close','Volume','Symbol','ChangeDay','ChangeWeek']
    stockdata = FetchSymbol(symbols[0])
    for symbol in symbols[1:]:
        data = FetchSymbol(symbol)
        stockdata = pd.concat([stockdata, data])
    stockdata = stockdata.sort_index()
    print(stockdata)
    return stockdata