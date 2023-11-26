from tensorflow import keras
from keras import layers
import os
import pandas as pd
import dataloader2
import numpy as np

model = keras.Sequential(layers=[
    layers.Conv2D(32, (2, 12), input_shape=(2,25,1),activation='relu'),
    layers.MaxPool2D((1,3)),
    layers.Flatten(),
    layers.Dense(10, activation='relu'),
    layers.Dense(2, activation='softmax')
])
model.summary()

checkpoint_file = os.path.join('model1min','cp.ckpt')
checkpoint_dir = os.path.dirname(checkpoint_file)
print(checkpoint_dir)
is_trained = lambda: os.path.exists(os.path.join(checkpoint_dir, 'checkpoint'))
is_not_trained = lambda: not is_trained()
if is_trained():
    model.load_weights(checkpoint_file)
    print(f"Loaded weights from {checkpoint_dir}")
else:
    print(f"Did not load any weights")


def getXandIndex(sid_file, ):
    # data = dataloader.acc_data_for_child(sid)
    padding_minutes=1
    data = pd.read_parquet(sid_file)
    padding = padding_minutes*12 # 1 minute is 12 steps
    angle_window = dataloader2.windows(data, 'anglez', padding).dropna()
    enmo_window  = dataloader2.windows(data, 'enmo', padding).dropna()
    X = np.stack([angle_window.to_numpy(), enmo_window.to_numpy()], axis=1)
    return X,angle_window.index 
