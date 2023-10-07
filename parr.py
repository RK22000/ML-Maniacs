import concurrent.futures
import tqdm
import numpy as np
import multiprocessing

def parallelize(func, *iterargs, total=None):
    '''
    Shorthand function to parallelize any other function that takes in multiple iterables as arguments

    Parameters
    ----------
    func: Any function that needs to be parallelized over some iterables
        NOTE: func must be defined in a .py file and not in a jupyter notebook cell
    *iterargs: One or more iterables, each of which hold arguments accepted by `func()` 
    '''
    num_processes = multiprocessing.cpu_count()
    # print(len(iterargs))
    # res = [func(*args) for args in zip(*iterargs)]
    with concurrent.futures.ProcessPoolExecutor(num_processes) as executor:
        # if total is None:
        res =  [i for i in executor.map(func, *iterargs, chunksize=100000)]
        # else:
        #     print('with tqdm')
        #     res = list(tqdm.tqdm(executor.map(func, *iterargs), total=total))
            
    return res
def series_id_in_series_set(series, series_set):
    # if type(series) is str:
    return series in series_set
    # print("Not a string")
    # return [i in series_set for i in series]
