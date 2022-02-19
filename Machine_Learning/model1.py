from mxproxy import mx
import pandas as pd
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

labels = "OPEN", "HIGH", "LOW", "CLOSE", "VOLUME", "CLOSE_TIME", "QUOTE ASSET VOLUME", "TOTAL_TRADES", "TAKER BUY BASE ASSET VOLUME", "TAKER BUY QUOTE ASSET VOLUME", "IGNORE"
df = pd.read_csv('BNBUSDT-5m-2022-01.csv', names=labels)
print(len(df))

# for d in df.itertuples():
# 	print(d)


# -------------------build model
# import tensorflow as tf

inputs = keras.Input(shape=(10, 1), name="CandleSticks")
x = layers.LSTM(5)(inputs)
x = layers.Dropout(0.2)(x)
outputs = layers.Dense(1, activation='linear')(x)
model = keras.Model(inputs=inputs, outputs=outputs)
model.compile(optimizer=keras.optimizers.SGD(learning_rate=0.001),
              loss=keras.losses.MeanSquaredError(),
              metrics=['mse'])

dfiter=list(df.itertuples())
seqdataX=np.array(df['OPEN'].iloc[:100])
seqdataY=np.array(df['OPEN'].iloc[10])
# print(seqdata)
model.summary()
model.fit(seqdataX, seqdataY, batch_size=1)

# x = layers.Dense(64, activation="relu", name="dense_1")(inputs)
# x = layers.Dense(64, activation="relu", name="dense_2")(x)
# outputs = layers.Dense(5, activation="softmax", name="predictions")(x)

# model = keras.Model(inputs=inputs, outputs=outputs)

# data = 0
