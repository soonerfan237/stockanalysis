import yfinance as yf
import pandas as pd
import copy
import pickle
import datetime

def FetchSymbol(symbol):
    print(symbol)
    yf.pdr_override()
    symboldata_dict = dict()
    num_of_days = 0
    data = yf.download(symbol, start='2004-12-30', end='2019-12-01')
    data.insert(0, 'DateID', range(len(data))) #using an ID because there is no data on weekends which meses up calculations
    data.set_index('DateID')
    #print(data)
    data_ld = copy.deepcopy(data)
    #data_ld['DateLastDay'] = data_ld.index - pd.to_timedelta(1, unit='d')
    data_ld['DateID'] = data_ld.DateID + 1
    data_ld = data_ld.set_index('DateID')
    #print(data_ld)
    data = data.join(data_ld, on='DateID', rsuffix='_ld')
    #data['Date'] = data.index + pd.to_timedelta(1, unit='d')
    #data = data.set_index('Date')
    data = data[data.Open.notnull()]
    data = data[data['Open_ld'].notnull()]

    data['Symbol'] = symbol
    #print(data)
    data['PriceChangeDay'] = data['Adj Close'] - data['Adj Close_ld']
    #data['ChangeWeek'] = data.Open_lw - data.Close
    data['ChangeDayBool'] = data.PriceChangeDay > 0

    PriceChangeDayList = list(data.PriceChangeDay)
    PriceChangeDayList = PriceChangeDayList[:-1] #excluding final day because that is the value we are trying to predict. it's not fair to have it included in the feature
    num_of_days = len(PriceChangeDayList)
    #HighLow =
    # for each symbol there will be an array with 2 indices.
    # the first part will be the label - did the stock go up or down that day
    # the next index will contain all the features. so far it will just be a list of historical day to day changes
    if num_of_days > 0:
        symboldata_dict[symbol] = [data['ChangeDayBool'][-1], PriceChangeDayList]
    return symboldata_dict, num_of_days

def DownloadData(symbols):
    print("STARTING DownloadData")
    pd.set_option('display.expand_frame_repr', False)

    stockdata_dict = dict()
    symboldata_dict, max_num_of_days = FetchSymbol(symbols[0])
    stockdata_dict.update(symboldata_dict)
    for symbol in symbols[1:]:
        symboldata_dict, num_of_days = FetchSymbol(symbol)
        if num_of_days > 0:
            #stockdata = pd.concat([stockdata, data])
            stockdata_dict.update(symboldata_dict)
            if num_of_days > max_num_of_days:
                max_num_of_days = num_of_days

    #stockdata = stockdata.sort_index()
    #print(stockdata)

    fileObject = open("stockdata_dict_FULL.pickle", 'wb')  # open the file for writing
    pickle.dump(stockdata_dict, fileObject)
    fileObject.close()
    print("DONE!!!!")

    return stockdata_dict, max_num_of_days