from .models import RAPLData
from . import util

import os
import re
import json


def full_run(_dir: str):
    """
    benchmark
        x files
            y zones
    """
    # TODO: steps as metric
    metrics = ['max', 'min', 'median', 'mean', 'avg', 'total']
    attrs = ['power_j', 'watts', 'watts_since_last', 'watt_h', 'kwatt_h']
    json_fn = _dir.split('/')[-1]
    data = _parse_input(_dir)
    res = {}

    for bench_type, bench_data in data.items():
        if bench_type not in res:
            res[bench_type] = {}

        res[bench_type]['run_metrics'] = {}
        res[bench_type]['run_data'] = {}

        for d in bench_data:  # type: RAPLData
            zones = d.get_zones()

            for z in zones:



            res[bench_type]['run_metrics'].append({
                attr: {metric: d.get_zone_metric(attr, metric, float) for metric in metrics}
                for attr in attrs})

            res[bench_type]['run_data'].append({
                attr: d.get_field_as_dict(attr, float) for attr in attrs})



    with open(f'{json_fn}.json', 'w') as f:
        f.write(json.dumps(res, indent=4))


def _parse_input(_dir: str) -> dict:
    return {d.split('/')[-1]: util.parse_input_paths([f'{_dir}/{d}']) for d in os.listdir(_dir)}

