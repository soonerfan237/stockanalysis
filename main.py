import DownloadData
import NeuralNet
import pickle

def main():

    fileObject = open("stock_symbol_list.pickle",'rb')
    symbols = pickle.load(fileObject)
    fileObject.close()
    #symbols = ['DVN', 'MMM', 'YYY', 'AAPL','ADBE','AMZN']
    #symbols = ['JFKKR']
    stockdata_dict, max_num_of_days = DownloadData.DownloadData(symbols[:20])
    fileObject = open("stockdata_dict.pickle",'wb') # open the file for writing
    pickle.dump(stockdata_dict,fileObject)
    fileObject.close()

    NeuralNet.NeuralNet(stockdata_dict, max_num_of_days)

main()