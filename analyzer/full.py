import json
import os

import numpy as np

from .models import AnalyzedData
from .parser import parse_input_paths
from .plot import plot, bar


def full_run(_dir: str, plot_type: str, output: str, title: str):
    if os.path.isdir(_dir):
        for _d in os.listdir(_dir):
            d = f'{_dir}/{_d}'
            plot_run(d, _dir, plot_type, output, title)
    else:
        d = _dir
        plot_run(d, os.path.dirname(_dir), plot_type, output, title)
    print('Done')


def _parse_input(_dir: str) -> dict:
    return {_dir: parse_input_paths([_dir])}


def plot_run(d, _dir, plot_type: str, output: str, title: str):
    data = _parse_input(d)

    # Skip if no data was retrieved.
    if not len(data.get(d)) > 0:
        return

    print('Parsing data')
    res = [AnalyzedData(bench_name, bench_data) for bench_name, bench_data in data.items()]
    del data

    # Create folder for processed results and graphs.
    path = f'{_dir}/processed'
    if not os.path.isdir(path):
        os.makedirs(path)

    for r in res:
        print(f'Writing {r.name} JSON')
        with open(f'{path}/{r.name.split("/")[-1]}.json', 'w') as f:
            f.write(json.dumps(r.to_json(), indent=4))

        print(f'Generating {r.name} graphs')
        # power_j_total = r.collect_metrics_by_zone('run_metrics', 'power_j', 'total')
        power_j_total = r.collect_metrics_by_zone('run_data', 'watts_since_last', 'package-0')

        x = list(range(1, len(r.run_metrics) + 1))

        if plot_type == 'plot':
            plot(plot_type, power_j_total, x, f'{path}/{output}', 'Benchmark no.', 'Power (Joules)',
                 f'{output}')
        elif plot_type == 'bar':
            bar({zone: np.average(value) for zone, value in power_j_total.items()},
                f'{path}/{output}', f'Power (Joules, avg - {len(r.run_metrics)} runs)', 'RAPL Zone',
                f'{title}')
        elif plot_type == 'curve':
            plot(plot_type, power_j_total, [], f'{path}/{output}', 'Time (seconds)',
                 'Power (Watts) since previous measurement', f'{title}')
