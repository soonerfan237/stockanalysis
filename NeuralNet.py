import numpy as np
import pickle
import glob
import csv
import random
import tensorflow as tf
import sklearn
from sklearn.metrics import r2_score

def NeuralNet(stockdata_dict, max_num_of_days):
    print("STARTING NeuralNet")

    #item = stockdata_dict[next(iter(stockdata_dict))]
    symbols = list(stockdata_dict.keys())  # Python 3; use keys = d.keys() in Python 2
    random.shuffle(symbols)
    #random.shuffle(stockdata)
    features = np.zeros(shape=(len(stockdata_dict), 1, max_num_of_days))
    #features = []
    labels = []
    i = 0
    for symbol in symbols:
    #for symbol, values in stockdata_dict.items():
        print(symbol)
        print(len(stockdata_dict[symbol][1]))
        if len(stockdata_dict[symbol][1]) == max_num_of_days: #excluding stocks without full historical data
            #features.append(np.array(values[1]))
            features[i][0] = stockdata_dict[symbol][1]
            #features.append(values[1])
            labels.append(stockdata_dict[symbol][0])
            i+=1

    features = features[:i] #need to remove extra rows because we didn't add rows that were missing historical data.
    features = features.astype(float)
    labels = np.array(labels).astype(float)

    features_train = features[:int(7*len(features)/10)]
    labels_train = labels[:int(7*len(features)/10)]

    features_test = features[int(7*len(features)/10):]
    labels_test = labels[int(7*len(features)/10):]

    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(500, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(500, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(100, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(100, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(2, activation=tf.nn.softmax))

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    model.fit(features_train, labels_train, epochs=20)#, validation_data=(features_test, labels_test))

    model.save("stockanalysis.model")
    new_model = tf.keras.models.load_model("stockanalysis.model")
    predictions = new_model.predict(features_test)
    new_model.summary()
    #print(predictions)

    y_pred = []
    for i in range(0, len(labels_test)):
        print("REAL: " + str(labels_test[i]) + " | PREDICTED: " + str(np.argmax(predictions[i])))
        y_pred.append(np.argmax(predictions[i]))

    y_true = np.array(labels_test)
    y_true.astype(float)
    y_pred = np.array(y_pred)
    y_pred.astype(float)
    r_squared = r2_score(y_true, y_pred)
    print("R2 = " + str(r_squared))
    print("DONE!!!!")