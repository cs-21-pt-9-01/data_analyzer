from .models import AnalyzedData
from . import util

import os
import json


def full_run(_dir: str):
    data = _parse_input(_dir)
    res = [AnalyzedData(bench_name, bench_data) for bench_name, bench_data in data.items()]

    for r in res:
        path = f'{_dir}/{r.name}/processed'

        if not os.path.isdir(path):
            os.makedirs(path)

        with open(f'{path}/{r.name}.json', 'w') as f:
            f.write(json.dumps(r.to_json(), indent=4))


def _parse_input(_dir: str) -> dict:
    return {d.split('/')[-1]: util.parse_input_paths([f'{_dir}/{d}']) for d in os.listdir(_dir)}

