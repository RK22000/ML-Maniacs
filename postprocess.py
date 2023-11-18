import numpy as np
import pandas as pd

def smooth(y, n=40*12):
    return np.convolve(y, [1./n]*n, 'same')
def smooth_center(y, n=40*12):
    mid = n//2
    arr = [*list(range(1, mid+1)),*list(range(mid+1, 0, -1))]
    arr_sum = sum(arr)
    arr = [i/arr_sum for i in arr]
    return np.convolve(y, arr, 'same')
def smooth_spread(y, n=40*12):
    mid = n//2
    arr = [*list(range(mid+1, 0, -1)),*list(range(1, mid+1))]
    arr_sum = sum(arr)
    arr = [i/arr_sum for i in arr]
    return np.convolve(y, arr, 'same')
def tabulate(preds, index, data):
    _event, _step = [], []
    for a,b,i in zip(preds[:-1], preds[1:], index[1:]):
        step=False
        if a > 0.5 and b <= 0.5:
            _event.append("wakeup")
            step=True
        elif a < 0.5 and b >= 0.5:
            _event.append("onset")
            step=True
        if step:
            _step.append(data.loc[i, 'step'])
    
    predictions = pd.DataFrame({
        "event": _event,
        "step": _step
    })
    # predictions["series_id"]=sid
    predictions["score"]=1
    return predictions