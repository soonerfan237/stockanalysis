import DownloadData
import NeuralNet
import pickle

def main():

    symbols = ['DVN','MMM']
    stockdata = DownloadData.DownloadData(symbols)
    fileObject = open("stockdata.pickle",'wb') # open the file for writing
    pickle.dump(stockdata,fileObject)
    fileObject.close()

    #fileObject = open("stockdata.pickle",'rb')
    #stockdata = pickle.load(fileObject)
    #fileObject.close()

    NeuralNet.NeuralNet(stockdata)

main()