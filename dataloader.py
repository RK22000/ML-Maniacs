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

def acc_data_for_child(sid):
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
    dir_path = os.path.join('data', 'parsed')
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    file_path = os.path.join(dir_path, f'{sid}.parquet')
    path_clean = os.path.join(file_path, '.clean.txt')
    if os.path.exists(path_clean):
        return pd.read_parquet(file_path)
    dd.to_parquet(grouped_data.get_group(sid), file_path, write_index=False)
    with(open(path_clean, 'w')) as f:
        f.write('')
    return pd.read_parquet(file_path)



# # %%
# c1 = acc_data_for_child('038441c925bb')

# # %%
# c1

# # %%


# # %%
# c1 = acc_data_for_child('038441c925bb')

# # %%
# c1
