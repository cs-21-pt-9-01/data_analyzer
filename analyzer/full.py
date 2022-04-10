import json
import os

import numpy as np

from .models import AnalyzedData
from .parser import parse_input_paths
from .plot import plot, bar


def full_run(_dir: str, plot_type: str, output: str, title: str, rapl_attr: str, zone_or_metric: str,
             xmin: int, xmax: int):
    if os.path.isdir(_dir):
        power_j_total = {}
        for _d in os.listdir(_dir):
            d = f'{_dir}/{_d}'
            temp = plot_run(d, _dir, plot_type, output, title, rapl_attr, zone_or_metric, xmin, xmax)

            # Don't update if we don't use it later.
            if plot_type == 'curve':
                # May parse a file without data.
                if temp is not None:
                    power_j_total.update(temp)

        if plot_type == 'curve':
            path = f'{_dir}/processed'
            plot(plot_type, power_j_total, [], f'{path}/{output}', 'Time (seconds)',
                 'Power (Watts) since previous measurement', f'{title}')
    else:
        d = _dir
        power_j_total = plot_run(d, os.path.dirname(_dir), plot_type, output, title, rapl_attr, zone_or_metric,
                                 xmin, xmax)
        if plot_type == 'curve':
            path = f'{os.path.dirname(_dir)}/processed'
            plot(plot_type, power_j_total, [], f'{path}/{output}', 'Time (seconds)',
                 'Power (Watts) since previous measurement', f'{title}')
    print('Done')


def _parse_input(_dir: str, xmin: int, xmax: int) -> dict:
    return {_dir: parse_input_paths([_dir], xmin, xmax)}


def plot_run(d, _dir, plot_type: str, output: str, title: str, rapl_attr: str, zone_or_metric: str,
             xmin: int, xmax: int):
    data = _parse_input(d, xmin, xmax)

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
    power_j_total = {}
    for r in res:
        print(f'Writing {r.name} JSON')
        with open(f'{path}/{r.name.split("/")[-1]}.json', 'w') as f:
            f.write(json.dumps(r.to_json(), indent=4))

        print(f'Generating {r.name} graphs')
        if plot_type == 'plot' or plot_type == 'bar':
            power_j_total = r.collect_metrics_by_zone('run_metrics', rapl_attr,
                                                      zone_or_metric, "")
        elif plot_type == 'curve':
            # Create a prefix to be used when multiple lines are to be plotted.
            # Simply use the last word before file extension.
            rapl_zone_prefix = r.name.split("-")
            rapl_zone_prefix = rapl_zone_prefix[len(rapl_zone_prefix) - 1].replace(".csv", "")
            power_j_total = r.collect_metrics_by_zone('run_data', rapl_attr,
                                                      zone_or_metric, rapl_zone_prefix + "-")
        x = list(range(1, len(r.run_metrics) + 1))

        if plot_type == 'plot':
            plot(plot_type, power_j_total, x, f'{path}/{output}', 'Benchmark no.', 'Power (Joules)',
                 f'{output}')
        elif plot_type == 'bar':
            bar({zone: np.average(value) for zone, value in power_j_total.items()},
                f'{path}/{output}', f'Power (Joules, avg - {len(r.run_metrics)} runs)', 'RAPL Zone',
                f'{title}')

    return power_j_total
