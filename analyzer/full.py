from .models import AnalyzedData
from .graph import GraphGenerator
from . import util

import os
import json

import numpy as np


def full_run(_dir: str):
    data = _parse_input(_dir)
    res = [AnalyzedData(bench_name, bench_data) for bench_name, bench_data in data.items()]
    graph = GraphGenerator()

    for r in res:
        path = f'{_dir}/{r.name}/processed'

        if not os.path.isdir(path):
            os.makedirs(path)

        with open(f'{path}/{r.name}.json', 'w') as f:
            f.write(json.dumps(r.to_json(), indent=4))

        power_j_total = r.collect_metrics_by_zone('power_j', 'total')

        x = list(range(1, len(r.run_metrics) + 1))
        graph.plot(power_j_total, x, f'{path}/power_j_total.png', 'Power (Joules)', r.name)

        graph.bar({zone: np.average(value) for zone, value in power_j_total.items()},
                  f'{path}/power_j_overall_avg', f'Power (Joules, avg - {len(r.run_metrics)} runs)', 'RAPL Zone', r.name)


def _parse_input(_dir: str) -> dict:
    return {d.split('/')[-1]: util.parse_input_paths([f'{_dir}/{d}']) for d in os.listdir(_dir)}

