import yfinance as yf
import pandas as pd
import copy
import pickle
import datetime

def FetchSymbolDay(symbol):
    print(symbol)
    yf.pdr_override()
    symboldata_dict = dict()
    num_of_days = 0
    data = yf.download(symbol, start='2004-12-30', end='2019-12-01')
    data.insert(0, 'DateID', range(len(data))) #using an ID because there is no data on weekends which meses up calculations
    data.set_index('DateID')
    #print(data)

    #JOINING PREVIOUS DAYS DATA
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

    #JOINING PREVIOUS WEEKS DATA
    data_lw = copy.deepcopy(data)
    data_lw['DateID'] = data_lw.DateID + 7
    data_lw = data_lw.set_index('DateID')
    data = data.join(data_lw, on='DateID', rsuffix='_lw')
    data = data[data.Open.notnull()]
    data = data[data['Open_lw'].notnull()]

    #JOINING PREVIOUS MONTHS DATA
    data_lm = copy.deepcopy(data)
    data_lm['DateID'] = data_lm.DateID + 30
    data_lm = data_lm.set_index('DateID')
    data = data.join(data_lm, on='DateID', rsuffix='_lm')
    data = data[data.Open.notnull()]
    data = data[data['Open_lm'].notnull()]

    #JOINING PREVIOUS YEARS DATA
    data_ly = copy.deepcopy(data)
    data_ly['DateID'] = data_ly.DateID + 365
    data_ly = data_ly.set_index('DateID')
    data = data.join(data_ly, on='DateID', rsuffix='_ly')
    data = data[data.Open.notnull()]
    data = data[data['Open_ly'].notnull()]

    data['Symbol'] = symbol
    data['PriceChangeDay'] = data['Adj Close'] - data['Adj Close_ld']
    data['VolumeChangeDay'] = data['Volume'] - data['Volume_ld']
    data['PriceChangeWeek'] = data['Adj Close'] - data['Adj Close_lw']
    data['VolumeChangeWeek'] = data['Volume'] - data['Volume_lw']
    data['PriceChangeMonth'] = data['Adj Close'] - data['Adj Close_lm']
    data['VolumeChangeMonth'] = data['Volume'] - data['Volume_lm']
    data['PriceChangeYear'] = data['Adj Close'] - data['Adj Close_ly']
    data['VolumeChangeYear'] = data['Volume'] - data['Volume_ly']

    #TODO: add another label to see whether stock went up or down over course of week

    PriceChangeDayList = list(data.PriceChangeDay)
    #PriceChangeDayList = PriceChangeDayList[:-1] #excluding final day because that is the value we are trying to predict. it's not fair to have it included in the feature
    VolumeChangeDayList = list(data.VolumeChangeDay)
    #VolumeChangeDayList = VolumeChangeDayList[:-1]

    PriceChangeWeekList = list(data.PriceChangeWeek)
    VolumeChangeWeekList = list(data.VolumeChangeWeek)

    PriceChangeMonthList = list(data.PriceChangeMonth)
    VolumeChangeMonthList = list(data.VolumeChangeMonth)

    PriceChangeYearList = list(data.PriceChangeYear)
    VolumeChangeYearList = list(data.VolumeChangeYear)

    #TODO: add feature which is a list of the total change in stock market prices each day
    num_of_days = len(PriceChangeDayList)-1
    #HighLow =
    # for each symbol there will be an array with 2 indices.
    # the first part will be the label - did the stock go up or down that day
    # the next index will contain all the features. so far it will just be a list of historical day to day changes
    if num_of_days > 0:
        symboldata_dict[symbol] = [ PriceChangeDayList[-1], [ PriceChangeDayList[:-1], VolumeChangeDayList[:-1] ] ]
    return data, symboldata_dict, num_of_days


def FetchSymbolWeek(symbol):
    print(symbol)
    yf.pdr_override()
    symboldata_dict = dict()
    num_of_days = 0
    data = yf.download(symbol, start='2004-12-30', end='2019-12-01')
    data.insert(0, 'DateID',
                range(len(data)))  # using an ID because there is no data on weekends which meses up calculations
    data.set_index('DateID')
    # print(data)

    # JOINING PREVIOUS WEEKS DATA
    data_lw = copy.deepcopy(data)
    data_lw['DateID'] = data_lw.DateID + 7
    data_lw = data_lw.set_index('DateID')
    data = data.join(data_lw, on='DateID', rsuffix='_lw')
    data = data[data.Open.notnull()]
    data = data[data['Open_lw'].notnull()]

    data['Symbol'] = symbol
    data['PriceChangeWeek'] = data['Adj Close'] - data['Adj Close_lw']
    data['VolumeChangeWeek'] = data['Volume'] - data['Volume_lw']

    # TODO: add another label to see whether stock went up or down over course of week

    PriceChangeWeekList = list(data.PriceChangeWeek)[::7]
    VolumeChangeWeekList = list(data.VolumeChangeWeek)[::7]

    # TODO: add feature which is a list of the total change in stock market prices each day
    num_of_days = len(PriceChangeWeekList) - 1
    # HighLow =
    # for each symbol there will be an array with 2 indices.
    # the first part will be the label - did the stock go up or down that day
    # the next index will contain all the features. so far it will just be a list of historical day to day changes
    if num_of_days > 0:
        symboldata_dict[symbol] = [PriceChangeWeekList[-1], [PriceChangeWeekList[:-1], VolumeChangeWeekList[:-1]]]
    return data, symboldata_dict, num_of_days

def FetchSymbolMonth(symbol):
    print(symbol)
    yf.pdr_override()
    symboldata_dict = dict()
    num_of_days = 0
    data = yf.download(symbol, start='2004-12-30', end='2019-12-01')
    data.insert(0, 'DateID',
                range(len(data)))  # using an ID because there is no data on weekends which meses up calculations
    data.set_index('DateID')
    # print(data)

    # JOINING PREVIOUS MONTHS DATA
    data_lm = copy.deepcopy(data)
    data_lm['DateID'] = data_lm.DateID + 30
    data_lm = data_lm.set_index('DateID')
    data = data.join(data_lm, on='DateID', rsuffix='_lm')
    data = data[data.Open.notnull()]
    data = data[data['Open_lm'].notnull()]

    data['Symbol'] = symbol
    data['PriceChangeMonth'] = data['Adj Close'] - data['Adj Close_lm']
    data['VolumeChangeMonth'] = data['Volume'] - data['Volume_lm']

    # TODO: add another label to see whether stock went up or down over course of week

    PriceChangeMonthList = list(data.PriceChangeMonth)[::30]
    VolumeChangeMonthList = list(data.VolumeChangeMonth)[::30]

    # TODO: add feature which is a list of the total change in stock market prices each day
    num_of_days = len(PriceChangeMonthList) - 1
    # HighLow =
    # for each symbol there will be an array with 2 indices.
    # the first part will be the label - did the stock go up or down that day
    # the next index will contain all the features. so far it will just be a list of historical day to day changes
    if num_of_days > 0:
        symboldata_dict[symbol] = [PriceChangeMonthList[-1], [PriceChangeMonthList[:-1], VolumeChangeMonthList[:-1]]]
    return data, symboldata_dict, num_of_days

def FetchSymbolYear(symbol):
    print(symbol)
    yf.pdr_override()
    symboldata_dict = dict()
    num_of_days = 0
    data = yf.download(symbol, start='2004-12-30', end='2019-12-01')
    data.insert(0, 'DateID',
                range(len(data)))  # using an ID because there is no data on weekends which meses up calculations
    data.set_index('DateID')
    # print(data)

    # JOINING PREVIOUS YEARS DATA
    data_ly = copy.deepcopy(data)
    data_ly['DateID'] = data_ly.DateID + 365
    data_ly = data_ly.set_index('DateID')
    data = data.join(data_ly, on='DateID', rsuffix='_ly')
    data = data[data.Open.notnull()]
    data = data[data['Open_ly'].notnull()]

    data['Symbol'] = symbol
    data['PriceChangeYear'] = data['Adj Close'] - data['Adj Close_ly']
    data['VolumeChangeYear'] = data['Volume'] - data['Volume_ly']

    # TODO: add another label to see whether stock went up or down over course of week

    PriceChangeYearList = list(data.PriceChangeYear)[::365]
    VolumeChangeYearList = list(data.VolumeChangeYear)[::365]

    # TODO: add feature which is a list of the total change in stock market prices each day
    num_of_days = len(PriceChangeYearList) - 1
    # HighLow =
    # for each symbol there will be an array with 2 indices.
    # the first part will be the label - did the stock go up or down that day
    # the next index will contain all the features. so far it will just be a list of historical day to day changes
    if num_of_days > 0:
        symboldata_dict[symbol] = [PriceChangeYearList[-1], [PriceChangeYearList[:-1], VolumeChangeYearList[:-1]]]
    return data, symboldata_dict, num_of_days

def DownloadData(symbols, time_period):
    print("STARTING DownloadData")
    pd.set_option('display.expand_frame_repr', False)

    stockdata_dict = dict()
    if time_period == 'day':
        stockdata, symboldata_dict, max_num_of_days = FetchSymbolDay(symbols[0])
    elif time_period == 'week':
        stockdata, symboldata_dict, max_num_of_days = FetchSymbolWeek(symbols[0])
    elif time_period == 'month':
        stockdata, symboldata_dict, max_num_of_days = FetchSymbolMonth(symbols[0])
    elif time_period == 'year':
        stockdata, symboldata_dict, max_num_of_days = FetchSymbolYear(symbols[0])
    #min_pricechangeday = pricechangeday
    #max_pricechangeday = pricechangeday
    stockdata_dict.update(symboldata_dict)
    for symbol in symbols[1:]:
        if time_period == 'day':
            data, symboldata_dict, num_of_days = FetchSymbolDay(symbol)
        elif time_period == 'week':
            data, symboldata_dict, num_of_days = FetchSymbolWeek(symbol)
        elif time_period == 'month':
            data, symboldata_dict, num_of_days = FetchSymbolMonth(symbol)
        elif time_period == 'year':
            data, symboldata_dict, num_of_days = FetchSymbolYear(symbol)
        if num_of_days > 0:
            stockdata = pd.concat([stockdata, data])
            stockdata_dict.update(symboldata_dict)
            if num_of_days > max_num_of_days:
                max_num_of_days = num_of_days
            #if pricechangeday < min_pricechangeday:
            #    min_pricechangeday = pricechangeday
            #if pricechangeday > max_pricechangeday:
            #    max_pricechangeday = pricechangeday

    #stockdata = stockdata.sort_index()
    #print(stockdata)

    fileObject = open("stockdata_RAW.pickle", 'wb')  # open the file for writing
    pickle.dump(stockdata, fileObject)
    fileObject.close()

    fileObject = open("stockdata_dict_"+time_period+".pickle", 'wb')  # open the file for writing
    pickle.dump(stockdata_dict, fileObject)
    fileObject.close()
    print("DONE!!!!")

    return stockdata_dict, max_num_of_days