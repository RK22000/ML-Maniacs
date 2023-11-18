import numpy as np
import dataloader
from tensorflow import keras
from keras import layers
import os

checkpoint_file = os.path.join('training_checkpoints', 'cp.ckpt')
checkpoint_dir = os.path.dirname(checkpoint_file)
if not os.path.exists(os.path.join('training_checkpoints', 'checkpoint')):
    raise Exception("Checkpoints do not exist")

model = keras.Sequential(layers=[
    layers.Conv2D(32, (2, 50), input_shape = (2, 121,1), activation='relu'),
    layers.MaxPool2D((1,8)),
    layers.Flatten(),
    layers.Dense(10, activation='relu'),
    layers.Dense(2, activation='softmax')
])
model.summary()


model.load_weights(checkpoint_file)


def getXandIndex(sid, padding_minutes=5):
    data = dataloader.acc_data_for_child(sid)
    padding = padding_minutes*12 # 1 minute is 12 steps
    angle_window = dataloader.windows(data, 'anglez', padding).dropna()
    enmo_window  = dataloader.windows(data, 'enmo', padding).dropna()
    X = np.stack([angle_window.to_numpy(), enmo_window.to_numpy()], axis=1)
    return X,angle_window.index 
