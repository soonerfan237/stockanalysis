import numpy as np
import pickle
import glob
import csv
import random
import tensorflow as tf
import sklearn
from sklearn.metrics import r2_score, mean_squared_error
from math import sqrt
from sklearn.preprocessing import minmax_scale
#from tensorflow.python.keras.models import Sequential
#from tensorflow.python.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, Conv1D, MaxPooling2D, MaxPooling1D, LeakyReLU
from tensorflow.python.keras.layers.advanced_activations import LeakyReLU


def NeuralNet(stockdata_dict, max_num_of_days, num_of_days_to_use):
    print("STARTING NeuralNet")
    print("num_of_days_to_use = " + str(num_of_days_to_use))
    #item = stockdata_dict[next(iter(stockdata_dict))]
    symbols = list(stockdata_dict.keys())  # Python 3; use keys = d.keys() in Python 2
    random.shuffle(symbols)

    #features = np.zeros(shape=(len(stockdata_dict), 1, max_num_of_days*2))
    features = np.zeros(shape=(len(stockdata_dict), 1, num_of_days_to_use*2))

    labels = []
    i = 0
    for symbol in symbols:
    #for symbol, values in stockdata_dict.items():
        #print(symbol)
        #print(len(stockdata_dict[symbol][1][0]))
        if len(stockdata_dict[symbol][1][0]) == max_num_of_days: #excluding stocks without full historical data
            #features[i][0] = stockdata_dict[symbol][1][0]+stockdata_dict[symbol][1][1]
            features[i][0] = stockdata_dict[symbol][1][0][:num_of_days_to_use] + stockdata_dict[symbol][1][1][:num_of_days_to_use]
            labels.append(stockdata_dict[symbol][0])
            i+=1

    features = features[:i] #need to remove extra rows because we didn't add rows that were missing historical data.
    features = features.astype(float)
    labels = np.array(labels)
    labels = labels.astype(float)
    # normalized_activity = normalized_activity / np.sqrt(np.sum(normalized_activity ** 2))
    labels = minmax_scale(labels) * 5
    labels = labels.astype(int)

    features_train = features[:int(7*len(features)/10)]
    labels_train = labels[:int(7*len(features)/10)]

    features_test = features[int(7*len(features)/10):]
    labels_test = labels[int(7*len(features)/10):]


    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(1000, input_shape=(len(features_train[0]),)))
    model.add(LeakyReLU(0.2))
    model.add(tf.keras.layers.Dense(500))#, activation=tf.nn.relu))
    model.add(LeakyReLU(0.2))
    model.add(tf.keras.layers.Dense(100))#, activation=tf.nn.relu))
    model.add(LeakyReLU(0.2))
    model.add(tf.keras.layers.Dense(20))#, activation=tf.nn.relu))
    model.add(LeakyReLU(0.2))
    model.add(tf.keras.layers.Dense(6, activation=tf.nn.softmax))
    #tf.keras.models.load_model('model', custom_objects={'leaky_relu': tf.nn.leaky_relu})
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    model.fit(features_train, labels_train, epochs=30, validation_data=(features_test, labels_test))

    model.save("stockanalysis.model")
    new_model = tf.keras.models.load_model("stockanalysis.model")
    predictions = new_model.predict(features_test)
    #new_model.summary()
    #print(predictions)

    y_pred = []
    for i in range(0, len(labels_test)):
        #print("REAL: " + str(labels_test[i]) + " | PREDICTED: " + str(np.argmax(predictions[i])))
        y_pred.append(np.argmax(predictions[i]))

    y_true = np.array(labels_test)
    y_true.astype(float)
    y_pred = np.array(y_pred)
    y_pred.astype(float)
    r_squared = r2_score(y_true, y_pred)
    print("R2 = " + str(r_squared))
    rmse = sqrt(mean_squared_error(y_true, y_pred))
    print("RMSE = " + str(rmse))
    print("DONE!!!!")

    return r_squared, rmse