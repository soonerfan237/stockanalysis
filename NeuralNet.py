import numpy as np
import pickle
import glob
import csv
import random
import tensorflow as tf
import sklearn
from sklearn.metrics import r2_score

def NeuralNet(stockdata):
    print("STARTING NeuralNet")
    #random.shuffle(stockdata)

    features_train = stockdata.Volume
    features_train = np.array(features_train)
    features_train = features_train.reshape(len(features_train), 1, 1)
    features_train = features_train.astype(list)
    for i in range(len(features_train)):
        features_train[i] = [features_train[i]]
    features_train = features_train.astype(float)

    features_test = stockdata.Volume
    features_test = np.array(features_test)
    features_test = features_test.reshape(len(features_test), 1, 1)
    features_test = features_test.astype(list)
    for i in range(len(features_test)):
        features_test[i] = [features_test[i]]
    features_test = features_test.astype(float)

    labels_train = stockdata.ChangeDayBool
    labels_train = np.array(labels_train)
    labels_train = labels_train.astype(float)

    labels_test = stockdata.ChangeDayBool
    labels_test = np.array(labels_test)
    labels_test = labels_test.astype(float)

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
    print(predictions)

    y_pred = []
    for i in range(0, len(labels_test)):
        # print("REAL: " + str(labels_test[i]) + " | PREDICTED: " + str(np.argmax(predictions[i])))
        y_pred.append(np.argmax(predictions[i]))

    y_true = np.array(labels_test)
    y_true.astype(float)
    y_pred = np.array(y_pred)
    y_pred.astype(float)
    r_squared = r2_score(y_true, y_pred)
    print("R2 = " + str(r_squared))
    print("DONE!!!!")