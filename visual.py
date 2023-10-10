import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
# from matplotlib.cm import ScalarMappable
import matplotlib.animation as anim
from matplotlib.collections import PathCollection
import pandas as pd
import numpy as np

class Visualizaer1:
    def init_frame(ax: Axes, data: pd.DataFrame):
        '''
        Create an empty figure with containers for everything that will go in it.

        Returns
        -------
        A list of the artists
        '''
        points = ax.scatter(x=[], y=[], c=[], cmap='plasma')
        ax.set_xlabel('anglez')
        ax.set_ylabel('enmo')
        xmin = data['anglez'].min()
        xmax = data['anglez'].max()
        buff = (xmax-xmin)*0.1
        ax.set_xlim(xmin-buff, xmax+buff)
        ymin = data['enmo'].min()
        ymax = data['enmo'].max()
        buff = (ymax-ymin)*0.1
        ax.set_ylim(ymin-buff, ymax+buff)
        activity_text = ax.text((xmax+xmin)/2, ymax-data['enmo'].std(), "SOME TEXT", ha='center', weight='bold', va='bottom')
        return [points, activity_text]

    def draw_frame(ts: pd.Timestamp, data: pd.DataFrame, window: pd.Timedelta, x_jit_scale: int, y_jit_scale: int, points: PathCollection, activity_text: plt.Text):
        artists = []
        if type(ts) is not pd.Timestamp:
            ts = pd.Timestamp(ts)
        idx = (data['timestamp'] >= ts-window) & (data['timestamp'] < ts+window)
        data = data.loc[idx, ['step', 'anglez', 'enmo', 'activity']]
        # Set X, Y points
        x = data['anglez']
        y = data['enmo']
        dat_len = len(data)
        mid = data['step'].iat[int(dat_len/2)]
        c = [i - mid for i in data['step']]
        x_jit = (np.random.random_sample(x.shape)-0.5)*x_jit_scale
        y_jit = (np.random.random_sample(y.shape)-0.5)*y_jit_scale
        jit = 0.3
        points.set(offsets=list(zip(x+x_jit*jit,y+y_jit*jit)), array=c)
        artists.append(points)
        # Set the text box
        txt = f"{ts}\n{data['activity'].iat[0]} => {data['activity'].iat[-1]}"
        activity_text.set_text(txt)
        artists.append(activity_text)
        return artists

class Visualizer2:
    def init_frame(ax:Axes, window):
        # fig.colorbar(ScalarMappable(np.linspace))
        ax.axhline(0, color='k')
        points = ax.scatter(x=[], y=[], c=[], cmap='plasma', vmin=0, vmax=0.2)
        ax.set_xlabel('anglez')
        ax.set_xlim(-95, 95)
        ax.set_ylabel('Minute Offset from now')
        window = window.seconds/60
        ax.set_ylim(-1.1*(window/2), 1.3*(window/2))
        # ax.set_ylim(-100, 100)#(window/2))
        activity_text = ax.text(0, 1*window/2, "SOME\nTEXT", ha='center', va='bottom', weight='bold')
        return [points, activity_text]
    def draw_frame(ts: pd.Timestamp, full_data: pd.DataFrame, jitter:float, window, artists: list):
        art2=[]
        if type(ts) is not pd.Timestamp:
            ts = pd.Timestamp(ts)
        data = full_data
        idx = (data['timestamp'] >= ts-window/2) & (data['timestamp'] < ts+window/2)
        data = data.loc[idx, ['step', 'anglez', 'enmo', 'activity', 'timestamp']]
        # Set X points
        x = data['anglez']
        x += (np.random.random_sample(x.shape)-0.5)*jitter*full_data['anglez'].std()

        # Set Y points
        step = data.loc[data['timestamp']==ts, 'step'].iat[0]
        y = [(i-step)/12 for i in data['step']]
        artists[0].set(offsets=list(zip(x,y)), array=data['enmo'])
        art2.append(artists[0])
        txt = f"{ts}\n{data['activity'].iat[0]} => {data['activity'].iat[-1]}"
        artists[1].set_text(txt)
        art2.append(artists[1])
        return art2


