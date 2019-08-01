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
    #symbols = ['DVN']
    result_list = []
    random.shuffle(symbols)
    #for time_period in time_periods:
    #    result_list.append("==================")
    #    result_list.append(time_period)
    #    stockdata_dict, max_num_of_days = DownloadData.DownloadData(symbols[:1], time_period)
    #    stockdata_dict = RemoveOutliers.RemoveOutliers(stockdata_dict)
    #    for i in range(10, 1000, 10):
    #        if i < max_num_of_days:
    #            r_squared, rmse = NeuralNet.NeuralNet(stockdata_dict, max_num_of_days, i)
    #            result_list.append("num of days: "+str(i))
    #            result_list.append("r_squared: "+str(r_squared))
    #            result_list.append("rmse: " + str(rmse))

    #            fileObject = open("result_list.pickle",'wb') # open the file for writing
    #            pickle.dump(stockdata_dict,fileObject)
    #            fileObject.close()

    fileObject = open("stockdata_dict_year_FULL_tuesday.pickle",'rb')
    max_num_of_days = 13
    stockdata_dict = pickle.load(fileObject)
    #stockdata_dict = RemoveOutliers.RemoveOutliers(stockdata_dict)
    fileObject.close()
    r_squared, rmse = NeuralNet.NeuralNet(stockdata_dict, max_num_of_days, 10)

    elapsed_time = (time.time() - start_time) / 60
    print("This took " + str(elapsed_time) + " minutes.")
    print("DONE!")

main()