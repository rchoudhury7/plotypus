from os import makedirs
from os.path import isdir
from multiprocessing import Pool
from numpy import resize, median, absolute

__all__ = [
    'pmap',
    'make_sure_path_exists',
    'get_signal',
    'get_noise',
    'colvec',
    'mad'
]

def pmap(func, args, processes=None, callback=lambda *x: None, **kwargs):
    if processes is 1:
        results = []
        for arg in args:
            result = func(arg, **kwargs)
            results.append(result)
            callback(result)
        return results
    else:
        p = Pool() if processes is None else Pool(processes)
        results = [p.apply_async(func, (arg,), kwargs, callback)
                   for arg in args]
        p.close()
        p.join()
        return [result.get() for result in results]

def make_sure_path_exists(path):
    """Creates the supplied path. Raises OS error if the path cannot be
    created."""
    try:
      makedirs(path)
    except OSError:
      if not isdir(path):
        raise

def get_signal(data):
    """Returns all of the values that are not outliers."""
    return data[~data.mask].data.reshape(-1, data.shape[1])

def get_noise(data):
    """Returns all identified outliers"""
    return data[data.mask].data.reshape(-1, data.shape[1])

def colvec(X):
    return resize(X, (X.shape[0], 1))

def mad(data, axis=None):
    return median(absolute(data - median(data, axis)), axis)
