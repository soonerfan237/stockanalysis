import DownloadData
import RemoveOutliers
import NeuralNet
import pickle
import time
import random

def main():
    start_time = time.time()

    fileObject = open("stock_symbol_list.pickle",'rb')
    symbols = pickle.load(fileObject)
    fileObject.close()
    #symbols = ['DVN', 'MMM', 'YYY', 'AAPL','ADBE','AMZN']
    #symbols = ['JFKKR']
    random.shuffle(symbols)

    stockdata_dict, max_num_of_days = DownloadData.DownloadData(symbols[:1000],'month')
    stockdata_dict = RemoveOutliers.RemoveOutliers(stockdata_dict)
    #fileObject = open("stockdata_dict.pickle",'wb') # open the file for writing
    #pickle.dump(stockdata_dict,fileObject)
    #fileObject.close()

    #fileObject = open("stockdata_dict.pickle",'rb')
    #max_num_of_days = 3668
    #stockdata_dict = pickle.load(fileObject)
    #fileObject.close()

    for i in range(10,100,10):
        NeuralNet.NeuralNet(stockdata_dict, max_num_of_days, i)

    elapsed_time = (time.time() - start_time) / 60
    print("This took " + str(elapsed_time) + " minutes.")
    print("DONE!")

main()