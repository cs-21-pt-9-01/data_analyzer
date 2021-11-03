import csv
from typing import List, Callable, Optional, Dict

import numpy as np

VALID_ATTRS = ['power_j', 'watts', 'watts_since_last', 'watt_h', 'kwatt_h']


class RAPLZoneRow:

    def __init__(self, zone: str, time_elapsed: float, power_j: float, watts: float,
                 watts_since_last: float, start_power: float, prev_power: float,
                 prev_power_reading: float):
        self.zone = zone
        self.time_elapsed = time_elapsed
        self.power_j = power_j
        self.watts = watts
        self.watts_since_last = watts_since_last
        self.start_power = start_power
        self.prev_power = prev_power
        self.prev_power_reading = prev_power_reading


class RAPLData:

    def __init__(self, path: str):
        self.path = path
        self.rows = []  # type: List[RAPLZoneRow]

        self._parse_csv()

    def _parse_csv(self):
        with open(self.path, 'r', newline='') as f:
            data = csv.reader(f, delimiter=',')

            for row in data:
                # if row is headers
                if row[0] == 'zone':
                    continue
                # dont need initial measurement
                if int(float(row[1])) == 0:
                    continue
                self.rows.append(RAPLZoneRow(*row))

    def get_field_as_dict(self, attr: str, _type: Callable = int) -> dict:
        if attr == 'watt_h':
            return self._watt_hours()
        if attr == 'kwatt_h':
            return self._kwatt_hours()
        return {zone: [_type(float(getattr(row, attr))) for row in self.rows if row.zone == zone]
                for zone in self.get_zones()}

    def get_zone_metric(self, attr: str, metric: str, _type: Callable = int):
        if metric == 'max':
            return {zone: max(val) for zone, val in self.get_field_as_dict(attr, _type).items()}
        elif metric == 'min':
            return {zone: min(val) for zone, val in self.get_field_as_dict(attr, _type).items()}
        elif metric == 'median':
            return {zone: np.median(val) for zone, val in self.get_field_as_dict(attr, _type).items()}
        elif metric == 'mean':
            return {zone: np.mean(val) for zone, val in self.get_field_as_dict(attr, _type).items()}
        elif metric == 'avg':
            return {zone: np.average(val) for zone, val in self.get_field_as_dict(attr, _type).items()}
        elif metric == 'total':
            return {zone: val[-1] for zone, val in self.get_field_as_dict(attr, _type).items()}

    def get_zones(self) -> list:
        return list({row.zone for row in self.rows})

    def get_time_stamps(self) -> list:
        zones = self.get_zones()
        # zone is irrelevant and we just need stamps for one
        return [int(float(row.time_elapsed)) for row in self.rows if row.zone == zones[0]]

    def _watt_hours(self) -> dict:
        return {zone: [float(row.power_j) / 3600 for row in self.rows if row.zone == zone] for zone in self.get_zones()}

    def _kwatt_hours(self) -> dict:
        return {zone: [float(row.power_j) / 3600 / 1000 for row in self.rows if row.zone == zone] for zone in self.get_zones()}


class AnalyzedData:

    def __init__(self, name: str, data: List[RAPLData]):
        self.name = name

        self.run_metrics = [RAPLRunMetrics(d) for d in data]
        self.run_data = [RAPLRunData(d) for d in data]
        self.overall = RAPLOverallMetrics(self.run_metrics)

    def to_json(self):
        return {
            'overall': self.overall.to_json(),
            'run_metrics': [x.to_json() for x in self.run_metrics],
            'run_data': [x.to_json() for x in self.run_data]
        }

    def collect_metrics_by_zone(self, attr: str, metric: str) -> dict:
        res = {}
        for m in self.run_metrics:
            attr_obj = getattr(m, attr)
            metric_obj = getattr(attr_obj, metric)

            for zone, value in metric_obj.items():
                if zone not in res:
                    res[zone] = []

                res[zone].append(value)

        return res


class RAPLRunMetrics:

    def __init__(self, data: RAPLData):
        self.power_j = MetricData(data.get_field_as_dict('power_j', float), total=True, as_steps=True)
        self.watts = MetricData(data.get_field_as_dict('watts', float))
        self.watts_since_last = MetricData(data.get_field_as_dict('watts_since_last', float))
        self.watt_h = MetricData(data.get_field_as_dict('watt_h', float), total=True, as_steps=True)
        self.kwatt_h = MetricData(data.get_field_as_dict('kwatt_h', float), total=True, as_steps=True)

    def to_json(self):
        return {
            'power_j': self.power_j.to_json(),
            'watts': self.watts.to_json(),
            'watts_since_last': self.watts_since_last.to_json(),
            'watt_h': self.watt_h.to_json(),
            'kwatt_h': self.kwatt_h.to_json(),
        }


class RAPLRunData:

    def __init__(self, data: RAPLData):
        self.power_j = data.get_field_as_dict('power_j', float)
        self.watts = data.get_field_as_dict('watts', float)
        self.watts_since_last = data.get_field_as_dict('watts_since_last', float)
        self.watt_h = data.get_field_as_dict('watt_h', float)
        self.kwatt_h = data.get_field_as_dict('kwatt_h', float)

    def to_json(self):
        return {
            'power_j': self.power_j,
            'watts': self.watts,
            'watts_since_last': self.watts_since_last,
            'watt_h': self.watt_h,
            'kwatt_h': self.kwatt_h,
        }


class MetricData:

    def __init__(self, data: Dict[str, list], as_steps: bool = False, total=False):
        self.total = {zone: val[-1] for zone, val in
                      data.items()} if total else None  # type: Optional[Dict[str, float]]

        if as_steps:
            steps = {}

            for zone, val in data.items():
                steps[zone] = []

                for i in range(len(val)):
                    if i + 1 >= len(val):
                        continue
                    steps[zone].append(val[i + 1] - val[i])

            data = steps

        self.min = {zone: min(val) for zone, val in data.items()}
        self.max = {zone: max(val) for zone, val in data.items()}
        self.median = {zone: np.median(val) for zone, val in data.items()}
        self.mean = {zone: np.mean(val) for zone, val in data.items()}
        self.avg = {zone: np.average(val) for zone, val in data.items()}

    def to_json(self):
        j = {
            'min': self.min,
            'max': self.max,
            'median': self.median,
            'mean': self.mean,
            'avg': self.avg,
        }

        if self.total:
            j['total'] = self.total

        return j


class RAPLOverallMetrics:

    def __init__(self, data: List[RAPLRunMetrics]):
        self.power_j = self._merge([x.power_j for x in data])
        self.watts = self._merge([x.watts for x in data])
        self.watts_since_last = self._merge([x.watts_since_last for x in data])
        self.watt_h = self._merge([x.watt_h for x in data])
        self.kwatt_h = self._merge([x.kwatt_h for x in data])

    def to_json(self):
        return {
            'power_j': self.power_j,
            'watts': self.watts,
            'watts_since_last': self.watts_since_last,
            'watt_h': self.watt_h,
            'kwatt_h': self.kwatt_h,
        }

    @staticmethod
    def _merge(data: List[MetricData]) -> Dict[str, dict]:
        metrics = [('min', min), ('max', max), ('median', np.median), ('mean', np.mean),
                   ('avg', np.average)]
        zones = list(data[0].min.keys())
        merged = {}

        for m in metrics:
            merged[m[0]] = {zone: m[1]([getattr(d, m[0])[zone] for d in data]) for zone in zones}

        return merged
