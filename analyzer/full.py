from .models import AnalyzedData
from .graph import GraphGenerator
from . import util

import os
import json

import numpy as np


def full_run(_dir: str):
    graph = GraphGenerator()

    for _d in os.listdir(_dir):
        d = f'{_dir}/{_d}'
        print(f'Parsing dir {d}')
        data = util.parse_input(d)
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
            graph.plot(power_j_total, x, f'{path}/power_j_total.png', 'Power (Joules)', r.name.split('/')[-1])

            graph.bar({zone: np.average(value) for zone, value in power_j_total.items()},
                      f'{path}/power_j_overall_avg', f'Power (Joules, avg - {len(r.run_metrics)} runs)', 'RAPL Zone', r.name.split('/')[-1])

    print('Done')



