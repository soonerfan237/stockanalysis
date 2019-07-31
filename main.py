import DownloadData
import RemoveOutliers
import NeuralNet
import pickle
import time
import random

def main():
    start_time = time.time()
    time_periods = ['day','week','month','year']
    fileObject = open("stock_symbol_list.pickle",'rb')
    symbols = pickle.load(fileObject)
    fileObject.close()
    #symbols = ['DVN', 'MMM', 'YYY', 'AAPL','ADBE','AMZN']
    #symbols = ['JFKKR']
    result_list = []
    random.shuffle(symbols)
    for time_period in time_periods:
        result_list.append("==================")
        result_list.append(time_period)
        stockdata_dict, max_num_of_days = DownloadData.DownloadData(symbols[:20], time_period)
        stockdata_dict = RemoveOutliers.RemoveOutliers(stockdata_dict)
        for i in range(10, 100, 10):
            if i < max_num_of_days:
                r_squared, rmse = NeuralNet.NeuralNet(stockdata_dict, max_num_of_days, i)
                result_list.append("num of days: "+str(i))
                result_list.append("r_squared: "+str(r_squared))
                result_list.append("rmse: " + str(rmse))
    #max_num_of_days_DAY = max_num_of_days
    #stockdata_dict, max_num_of_days = DownloadData.DownloadData(symbols[:20], 'week')
    #max_num_of_days_WEEK = max_num_of_days
    #stockdata_dict, max_num_of_days = DownloadData.DownloadData(symbols[:20],'month')
    #max_num_of_days_MONTH = max_num_of_days
    #stockdata_dict, max_num_of_days = DownloadData.DownloadData(symbols[:20], 'year')
    #max_num_of_days_YEAR = max_num_of_days

    #stockdata_dict = RemoveOutliers.RemoveOutliers(stockdata_dict)
    #fileObject = open("stockdata_dict.pickle",'wb') # open the file for writing
    #pickle.dump(stockdata_dict,fileObject)
    #fileObject.close()

    #fileObject = open("stockdata_dict.pickle",'rb')
    #max_num_of_days = 3668
    #stockdata_dict = pickle.load(fileObject)
    #fileObject.close()

    for i in range(10,100,10):
        if i < max_num_of_days:
            r_squared, rmse = NeuralNet.NeuralNet(stockdata_dict, max_num_of_days, i)

    elapsed_time = (time.time() - start_time) / 60
    print("This took " + str(elapsed_time) + " minutes.")
    print("DONE!")

main()