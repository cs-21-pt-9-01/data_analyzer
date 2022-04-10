import os
from typing import List

from .models import RAPLData

ALLOWED_FILE_TYPES = ['csv']
""" Nested directory option.
        elif os.path.isdir(path):
            nested_paths = [f'{path}/{p}' for p in os.listdir(path)]
            res.extend(parse_input_paths(nested_paths))
"""


def parse_input_paths(paths: List[str], xmin: int, xmax: int) -> List[RAPLData]:
    res = []

    for path in paths:
        if os.path.isfile(path):
            ext = path.split('.')[-1]

            if ext not in ALLOWED_FILE_TYPES:
                print(f'Warning: {path} is not a valid file type, skipping.. ({ALLOWED_FILE_TYPES})')
                continue
            res.append(RAPLData(path, xmin, xmax))

        else:
            print(f'Warning: {path} is not a valid file or directory, skipping..')

    return res
