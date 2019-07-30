import numpy as np
import copy #needed to deepcopy dictionary so i can delete stuff during loop

def RemoveOutliers(stockdata_dict):
    print("STARTING RemoveOutliers")
    print("TOTAL SYMBOLS: " + str(len(stockdata_dict)))

    pricechange_list = []
    for symbol, values in stockdata_dict.items():
        pricechange_list.append(values[0])

    pricechange_list = np.array(pricechange_list)
    pricechange_list = pricechange_list.astype(float)
    stdev = np.std(pricechange_list)
    mean = np.mean(pricechange_list)

    stockdata_dict_new = copy.deepcopy(stockdata_dict)
    delete_count = 0
    for symbol, values in stockdata_dict.items():
        if abs(values[0]-mean) > 2*stdev:
            del stockdata_dict_new[symbol]
            delete_count += 1

    print("REMOVED OUTLIERS: " + str(delete_count))
    print("REMAINING SYMBOLS: " + str(len(stockdata_dict_new)))
    return stockdata_dict_new