from re import findall
from itertools import chain
from os import listdir, mkdir


def last_cached(directory='data/cache', level=0, result=None):
    if result is None:
        result = [0, None, None]
        if 'data' not in listdir():
            return result[0], result[1:]
    i = highest_file_num(directory)
    if i is not None:
        result[level] = i
        subdirectory = ['participant', 'block', 'trial'][level]
        directory = '/'.join([directory, subdirectory + '_{}'.format(i)])
        return last_cached(directory, level + 1, result) if level < 2 else (result[0], result[1:])
    return result[0], result[1:]


def highest_file_num(directory):
    files = listdir(directory)
    digits = [int(x) for x in chain(*[findall(r'\d+', name) for name in files])]
    return max(digits) if digits else None


def block_cache_path(i):
    directory_structure = {
        0: 'data',
        1: 'cache',
        2: 'participant_{}'.format(i),
        3: 'blockdata.pickle'
    }
    block_cache = generate_filename(directory_structure)
    return block_cache


def generate_filename(directory_structure, level=0, directory=None):
    target_directory = directory_structure[level]
    subdirectory = '/'.join([directory, target_directory]) if directory else target_directory
    if level == max(directory_structure.keys()):
        return subdirectory
    else:
        if target_directory not in listdir(directory):
            mkdir(subdirectory)
        return generate_filename(directory_structure, level + 1, subdirectory)
