import DownloadData
import RemoveOutliers
import NeuralNet
import pickle
import time

def main():
    start_time = time.time()

    fileObject = open("stock_symbol_list.pickle",'rb')
    symbols = pickle.load(fileObject)
    fileObject.close()
    #symbols = ['DVN', 'MMM', 'YYY', 'AAPL','ADBE','AMZN']
    #symbols = ['JFKKR']
    stockdata_dict, max_num_of_days = DownloadData.DownloadData(symbols[:20])
    stockdata_dict = RemoveOutliers.RemoveOutliers(stockdata_dict)
    fileObject = open("stockdata_dict.pickle",'wb') # open the file for writing
    pickle.dump(stockdata_dict,fileObject)
    fileObject.close()

    NeuralNet.NeuralNet(stockdata_dict, max_num_of_days)

    elapsed_time = (time.time() - start_time) / 60
    print("This took " + str(elapsed_time) + " minutes.")
    print("DONE!")

main()