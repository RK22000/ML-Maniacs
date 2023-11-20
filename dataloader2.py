import os
import pandas as pd


good_sids = """08db4255286f
0a96f4993bd7
0cfc06c129cc
1087d7b0ff2e
10f8bc1f7b07
18b61dd5aae8
29c75c018220
31011ade7c0a
3452b878e596
349c5562ee2c
3664fe9233f9
483d6545417f
55a47ff9dc8a
5acc9d63b5fd
5f94bb3e1bed
655f19eabf1e
67f5fc60e494
72bbd1ac3edf
76237b9406d5
7822ee8fe3ec
89bd631d1769
8e32047cbc1f
939932f1822d
9ee455e4770d
a596ad0b82aa
a9a2f7fac455
a9e5f5314bcb
af91d9a50547
b364205aba43
c535634d7dcd
c6788e579967
c68260cc9e8f
ca730dbf521d
d150801f3145
d25e479ecbb7
d515236bdeec
d5e47b94477e""".split("\n")

# Show training sids
def train_sids_files():
    prefix = ["data", "sids"]
    files = os.listdir(os.path.join(*prefix))
    return [os.path.join(*prefix,i) for i in files]

# Show test sids
def test_sids_files():
    prefix = ["data", "test_sids"]
    files = os.listdir(os.path.join(*prefix))
    return [os.path.join(*prefix,i) for i in files]

def windows(data, col, buffer=2):
    df2 = dict()
    for i in range(-buffer, buffer+1):
        df2[f'{i}'] = data[col][max(0,i):len(data)+i]
        df2[f'{i}'].index -= i
                # series = data[col].iloc[max(0,i):len(data)+i].copy()
                # series.index -= i
        # df2[f'{i}'].iloc[max(0,i):len(data)+i] = series
    df = pd.DataFrame(df2)
    return df

def annotate_sid(acc_data, events, sid):
    '''
    Annotate the acceleration data in acc_data with sleeping and waking events

    Parameters
    ----------
    acc_data: `pandas.Dataframe` holding acceleration data for a series id `sid`

    evente: `pandas.Dataframe` holding events data from sereis id `sid`

    sid: The series id from events being used to annotate
    '''
    event = events[events['series_id']==sid]['event']
    a = event.copy().iloc[:-1]
    b = event.copy().iloc[1:]
    b.index -= 1
    # Ensure none of the adjacent elements are the same event
    assert sum(a==b) == 0
    step = events[events['series_id']==sid]['step']
    # Lets ensure that the events are all `onset then wakeup`
    # assert set([i==('onset', 'wakeup') for i in zip(event[:-1:2], event[1::2])]) == set([True])
    sleeping = sum([(acc_data['step'] >= onset) & (acc_data['step'] < wakeup) for onset, wakeup in zip(step[:-1:2], step[1::2])])
    acc_data['activity'] = ['Sleeping' if i else 'Waking' for i in sleeping]

def load_sid(sid_file):
    events = pd.read_csv('data/train_events.csv')
    data = pd.read_parquet(sid_file)
    data['timestamp'] = pd.to_datetime(data['timestamp'], utc=True)
    sid = sid_file[-20:-8]
    annotate_sid(data, events, sid)
    return data