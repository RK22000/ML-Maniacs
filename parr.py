import concurrent.futures
import tqdm
import numpy as np
import multiprocessing
import dask.dataframe as dd
import os

def parallelize(func, *iterargs, total):
    '''
    Shorthand function to parallelize any other function that takes in multiple iterables as arguments

    Parameters
    ----------
    func: Any function that needs to be parallelized over some iterables
        NOTE: func must be defined in a .py file and not in a jupyter notebook cell
    *iterargs: One or more iterables, each of which hold arguments accepted by `func()` 
    '''
    num_processes = 6
    print(f'using {num_processes} cores')
    # print(len(iterargs))
    # res = [func(*args) for args in zip(*iterargs)]
    with concurrent.futures.ProcessPoolExecutor(num_processes) as executor:
        # if total is None:
        # res =  [i for i in executor.map(func, *iterargs, chunksize=10)]
        # else:
        #     print('with tqdm')
            res = list(tqdm.tqdm(executor.map(func, *iterargs, chunksize=1), total=total))
            
    return res
def series_id_in_series_set(series, series_set):
    # if type(series) is str:
    return series in series_set
    # print("Not a string")
    # return [i in series_set for i in series]
def save_series_id_to_parquet(df, sid, dir_path):
    # df = grouped_df.get_group(sid)
    dd.to_parquet(df, os.path.join(dir_path, f'{sid}.parquet'), write_index=False, overwrite=True)
    with(open(os.path.join(dir_path, f'{sid}.parquet','done.txt'), 'w')) as f:
        f.write('DONE')
def hello2(abc):
    1+1

