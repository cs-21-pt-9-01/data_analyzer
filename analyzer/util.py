from .models import RAPLData

import os
import math
from typing import List


ALLOWED_FILE_TYPES = ['csv']


def parse_input_paths(paths: List[str]) -> List[RAPLData]:
    res = []

    for path in paths:
        if os.path.isfile(path):
            ext = path.split('.')[-1]

            if ext not in ALLOWED_FILE_TYPES:
                print(f'Warning: {path} is not a valid file type, skipping.. ({ALLOWED_FILE_TYPES})')
                continue
            res.append(RAPLData(path))

        elif os.path.isdir(path):
            nested_paths = [f'{path}/{p}' for p in os.listdir(path)]
            res.extend(parse_input_paths(nested_paths))

        else:
            print(f'Warning: {path} is not a valid file or directory, skipping..')

    return res


def round_to_nearest(num: int, to: int):
    return math.ceil(num / to) * to