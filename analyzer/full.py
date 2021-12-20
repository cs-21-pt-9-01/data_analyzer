from .models import AnalyzedData
from .plot import plot, bar
from .parser import parse_input_paths

import os
import json

import numpy as np


def full_run(_dir: str, plot_type: str):

    for _d in os.listdir(_dir):
        d = f'{_dir}/{_d}'
        print(f'Parsing dir {d}')
        data = _parse_input(d)
        print('Parsing data')
        res = [AnalyzedData(bench_name, bench_data) for bench_name, bench_data in data.items()]
        del data

        for r in res:
            path = f'{d}/processed'

            if not os.path.isdir(path):
                os.makedirs(path)

            print(f'Writing {r.name} JSON')
            with open(f'{path}/{r.name.split("/")[-1]}.json', 'w') as f:
                f.write(json.dumps(r.to_json(), indent=4))

            print(f'Generating {r.name} graphs')
            power_j_total = r.collect_metrics_by_zone('power_j', 'total')

            x = list(range(1, len(r.run_metrics) + 1))
        if plot_type == 'plot':
            plot(power_j_total, x, f'{path}/power_j_total.png', 'Power (Joules)', r.name.split('/')[-1])
        elif plot_type == 'bar':
            bar({zone: np.average(value) for zone, value in power_j_total.items()},
                      f'{path}/power_j_overall_avg', f'Power (Joules, avg - {len(r.run_metrics)} runs)', 'RAPL Zone', r.name.split('/')[-1])

    print('Done')


def _parse_input(_dir: str) -> dict:
    return {_dir: parse_input_paths([_dir])}

