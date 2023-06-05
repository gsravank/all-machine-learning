"""
Utility functions required to parallelize execution
"""

import multiprocess as mp
# import multiprocessing as mp
from concurrent import futures
import os
import time

import numpy as np
import pandas as pd

from utils import get_command_output


def run_command(cmd):
    os.system(cmd)


def run_function(params):
    func = params[0]
    all_args = params[1]

    if type(all_args[-1]) == dict and '__kwargs' in all_args[-1]:
        args = all_args[:-1]
        kwargs = all_args[-1]
        del kwargs['__kwargs']

        return func(*args, **kwargs)
    else:
        args = all_args
        return func(*args)


def run_command_parallel(cmds, num_processes=4, chunksize=1, verbose=False, get_output=False):
    if verbose:
        print("Running {} commands, {} at a time..".format(len(cmds), num_processes))

    t1 = time.time()
    pool = mp.Pool(num_processes)
    if get_output:
        results = pool.map(get_command_output, cmds, chunksize)
    else:
        results = pool.map(run_command, cmds, chunksize)
    pool.close()
    pool.join()
    t2 = time.time()

    total_time = t2 - t1

    if verbose:
        print("Time to run {} commands: {} seconds or {} minutes or {} hours".format(len(cmds), total_time, (total_time) / 60.0, (total_time) / 3600.0))

    if get_output:
        return results
    else:
        return


def run_functions_parallel(function, params_lists, num_processes=4, chunksize=1, verbose=False):
    if verbose:
        print("Running {} functions parallelly, {} at a time..".format(len(params_lists), num_processes))

    t1 = time.time()
    iterable = [(function, params_list) for params_list in params_lists]
    pool = mp.Pool(num_processes)
    results = pool.map(run_function, iterable, chunksize)
    pool.close()
    pool.join()
    t2 = time.time()

    total_time = t2 - t1

    if verbose:
        print("Time to run {}() function, {} times in parallel: {} seconds or {} minutes or {} hours".format(function.__name__, len(params_lists), total_time, (total_time) / 60.0, (total_time) / 3600.0))

    return results


def run_mult_functions_parallel(function_tuple_lists, num_processes=4, chunksize=1, verbose=False):
    if verbose:
        print("Running {} functions parallelly, {} at a time..".format(len(function_tuple_lists), num_processes))
    t1 = time.time()
    pool = mp.Pool(num_processes)
    results = pool.map(run_function, function_tuple_lists, chunksize)
    pool.close()
    pool.join()
    t2 = time.time()
    total_time = t2 - t1
    if verbose:
        print("Time to run mult functions, {} times in parallel: {} seconds or {} minutes or {} hours".format(len(function_tuple_lists), total_time, (total_time) / 60.0, (total_time) / 3600.0))
    return results


def parallelize_dataframe(df, func, n_cores=4):
    """
    Split dataframe and apply function on given dataframe parallelly
    """
    df_split = np.array_split(df, n_cores)
    pool = mp.Pool(n_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df


def run_commands_concurrent(cmds, num_processes=4, verbose=False, get_output=False):
    if verbose:
        print("Running {} commands, {} at a time..".format(len(cmds), num_processes))

    t1 = time.time()
    with futures.ProcessPoolExecutor(max_workers=num_processes) as ex:
        if get_output:
            results = ex.map(get_command_output, cmds)
        else:
            results = ex.map(run_command, cmds)
    t2 = time.time()

    total_time = t2 - t1

    if verbose:
        print("Time to run {} commands: {} seconds or {} minutes or {} hours".format(len(cmds), total_time, (total_time) / 60.0, (total_time) / 3600.0))

    if get_output:
        return list(results)
    else:
        return


def run_functions_concurrent(function, params_lists, num_processes=4, verbose=False):
    if verbose:
        print("Running {} functions parallelly, {} at a time..".format(len(params_lists), num_processes))

    t1 = time.time()
    iterable = [(function, params_list) for params_list in params_lists]
    with futures.ProcessPoolExecutor(max_workers=num_processes) as ex:
        results = ex.map(run_function, iterable)
    t2 = time.time()

    total_time = t2 - t1

    if verbose:
        print("Time to run {}() function, {} times in parallel: {} seconds or {} minutes or {} hours".format(function.__name__, len(params_lists), total_time, (total_time) / 60.0, (total_time) / 3600.0))

    return list(results)


def run_mult_functions_concurrent(function_tuple_lists, num_processes=4, verbose=False):
    if verbose:
        print("Running {} functions parallelly, {} at a time..".format(len(function_tuple_lists), num_processes))

    t1 = time.time()
    with futures.ProcessPoolExecutor(max_workers=num_processes) as ex:
        results = ex.map(run_function, function_tuple_lists)
    t2 = time.time()

    total_time = t2 - t1

    if verbose:
        print("Time to run mult functions, {} times in parallel: {} seconds or {} minutes or {} hours".format(len(function_tuple_lists), total_time, (total_time) / 60.0, (total_time) / 3600.0))

    return list(results)
