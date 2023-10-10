# %% [markdown]
# # Dataloaders to load partial data

# %%
import dask.dataframe as dd
import os
import time

# %%
data_parquet = os.path.join('data','train_series.parquet')
data: dd.DataFrame = None
grouped_data = None

def init(source_file = None):
    '''
    Initialize the dataloader by reading in the data_parquet file

    Parameters
    ----------
    source_file: The parquet file from which to read the data.
        Defaults to None to use `train_series.parquet` in the `data/` directory
    '''
    print(f"Reading {data_parquet}")
    t=time.time()
    # data: dd.DataFrame = dd.read_parquet(data_parquet, columns=['step', 'series_id', 'anglez', 'enmo'], categories=['series_id'])
    global data, grouped_data
    data = dd.read_parquet(data_parquet)#, columns=['step', 'series_id', 'anglez', 'enmo'], categories=['series_id'])
    grouped_data = data.groupby('series_id')
    print(f"Pseudo read and grouped {len(data)} rows from {data_parquet} in {time.time()-t:.3f} seconds")

# # %%
# init()

# # %%
# data

# # %%
# grouped_data

# %%
def all_series_ids():
    '''
    Get all the `series_id`s present in the dataset
    
    Returns
    -------
    A pandas.Series containing all the unique `series_id` in the dataset
    '''
    if hasattr(all_series_ids, 'sids'): return all_series_ids.sids
    all_series_ids.sids = data['series_id'].unique().compute()
    return all_series_ids.sids

# # %%
# all_series_ids()

# %%
import pandas as pd

def acc_data_for_child(sid, verbose=False):
    '''
    Extract, cache, and return the data for given child in the dataset. 
    If the cached `.parquet` file already exists for that child then just read and return from that cached file.

    Parameters
    ----------
    sid: `series_id` of the child whose data is to be retrieved.

    Returns
    -------
    `pandas.DataFrame` of the child's data
    '''
    t = time.time()
    dir_path = os.path.join('data', 'parsed')
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    file_path = os.path.join(dir_path, f'{sid}.parquet')
    path_clean = os.path.join(file_path, '.clean.txt')
    if os.path.exists(path_clean):
        df = pd.read_parquet(file_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
        if verbose: print(f'loaded dataframe in {time.time()-t: .3f} seconds')
        return df
    dd.to_parquet(grouped_data.get_group(sid), file_path, write_index=False)
    with(open(path_clean, 'w')) as f:
        f.write('')
    df = pd.read_parquet(file_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
    if verbose: print(f'loaded dataframe in {time.time()-t: .3f} seconds')
    return df

# def save_acc_data_for_child

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
    step = events[events['series_id']==sid]['step']
    # Lets ensure that the events are all `onset then wakeup`
    assert set([i==('onset', 'wakeup') for i in zip(event[:-1:2], event[1::2])]) == set([True])
    sleeping = sum([(acc_data['step'] >= onset) & (acc_data['step'] < wakeup) for onset, wakeup in zip(step[:-1:2], step[1::2])])
    acc_data['activity'] = ['Sleeping' if i else 'Waking' for i in sleeping]



# # %%
# c1 = acc_data_for_child('038441c925bb')

# # %%
# c1

# # %%


# # %%
# c1 = acc_data_for_child('038441c925bb')

# # %%
# c1
