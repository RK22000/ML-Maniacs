'''
Run this file to see a visualization of anglez and enmo of a child sleeping
(Deprecated) Use code from visualizer.ipynb instead
'''
# %% [markdown]
# # Visualizing the data

# %%
import pandas as pd
import dataloader
import os

# %%
events = pd.read_csv(os.path.join('data', 'train_events.csv'))
# events.head()

# %%
nacheck = events.isna()
nacheck['series_id'] = events['series_id']
nacount = nacheck.groupby('series_id').sum()
good_sids = nacount[nacount['step']==0].index
# good_sids

# %%
sid = good_sids[0]
# sid

# %%
# dataloader.init()

# %%
acc_data = dataloader.acc_data_for_child(sid)

# %%
import matplotlib.pyplot as plt
import seaborn as sns

# %%
# fig, ax = plt.subplots()
# sns.scatterplot(data=acc_data, x='anglez', y='enmo', marker='.')

# %%
# lets figure out how to categorize this as sleeping or awake
# given a timestamp is it awake or asleep
# events[events['series_id']]
event = events[events['series_id']==sid]['event']
step = events[events['series_id']==sid]['step']
# Lets ensure that the events are all `onset then wakeup`
assert set([i==('onset', 'wakeup') for i in zip(event[:-1:2], event[1::2])]) == set([True])
sleeping = sum([(acc_data['step'] >= onset) & (acc_data['step'] < wakeup) for onset, wakeup in zip(step[:-1:2], step[1::2])])
# sleeping

# %%
acc_data['activity'] = ['Sleeping' if i else 'Waking' for i in sleeping]
# acc_data.sample(10)

# %%
# fig, ax = plt.subplots()
# sns.scatterplot(ax=ax, data=acc_data, x='anglez', y='enmo', hue='activity', marker='.')

# %%
# fig, axs = plt.subplots(nrows=2)
# sns.scatterplot(ax=axs[0], data=acc_data.loc[acc_data['activity']=='Waking'], x='anglez', y='enmo')
# axs[0].set_title('Waking')
# sns.scatterplot(ax=axs[1], data=acc_data.loc[acc_data['activity']=='Sleeping'], x='anglez', y='enmo')
# axs[1].set_title('Sleeping')
# fig.tight_layout()

# %%
import matplotlib.animation as anim
import matplotlib.axes as axes
import tqdm

fig, ax = plt.subplots()
ax: axes.Axes = ax
ax.set_xlim(-100, 100)
ax.set_ylim(-0.5, 3.5)
ax.set_xlabel('anglez')
ax.set_ylabel('enmo')
point = ax.scatter(2, 1, marker='o')
txt = ax.text(0, 0, 'Some Text')
# title = ax.set_title("This is title")

tq = tqdm.tqdm(range(len(acc_data)))
tqiter = iter(tq)



def animate(step):
    if step==0:
        global tqiter, tq
        tq = tqdm.tqdm(range(len(acc_data)))
        tqiter = iter(tq)
    x, y, activity, ts = acc_data.loc[acc_data['step']==step+1, ['anglez', 'enmo', 'activity', 'timestamp']].iloc[0]
    # x,y = 0,0
    point.set_offsets((x, y))
    point.set_color('orange' if activity=='Waking' else 'blue')
    txt.set_text(f'{activity}, {ts}')
    # title.set_text(f'{activity}, {ts}')
    # print((x,y))
    # next(tqiter)
    next(tqiter)
    return [point, txt, title]

ani = anim.FuncAnimation(fig, animate, frames=len(acc_data), interval=1, blit=True)

# ani.save('scatter.gif')
print("Showing Plot")
plt.show()
print("Finished Showing Figure")



