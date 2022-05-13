import csv
from typing import List, Callable, Optional, Dict

import numpy as np

VALID_ATTRS = ['power_j', 'watts', 'watts_since_last', 'watt_h', 'kwatt_h']
DESIRED_ORDER = ['package-0', 'core', 'uncore', 'dram']


class RAPLZoneRow:

    def __init__(self, zone: str, time_elapsed: float, power_j: float, watts: float,
                 watts_since_last: float, start_power: float, prev_power: float,
                 prev_power_reading: float, temperature: float):
        self.zone = zone
        self.time_elapsed = time_elapsed
        self.power_j = power_j
        self.watts = watts
        self.watts_since_last = watts_since_last
        self.start_power = start_power
        self.prev_power = prev_power
        self.prev_power_reading = prev_power_reading
        self.temperature = temperature


class RAPLData:

    def __init__(self, path: str, xmin: int, xmax: int):
        self.path = path
        self.rows = []  # type: List[RAPLZoneRow]
        self.xmin = xmin
        self.xmax = xmax
        self.rapl_zones = 4
        self._parse_csv()

    def _parse_csv(self):
        with open(self.path, 'r', newline='') as f:
            data = csv.reader(f, delimiter=',')

            row_count = 0
            for row in data:
                # Check if row should be skipped.
                if self.xmin is not None:
                    if row_count < self.xmin * self.rapl_zones:
                        row_count += 1
                        continue
                # Check if we have reached max.
                if self.xmax is not None:
                    if row_count >= self.xmax * self.rapl_zones:
                        return
                # if row is headers
                if row[0] == 'zone':
                    continue
                # dont need initial measurement
                if int(float(row[1])) == 0:
                    row_count += 1
                    continue
                self.rows.append(RAPLZoneRow(*row))
                row_count += 1

    def get_field_as_dict(self, attr: str, _type: Callable = int) -> dict:
        if attr == 'watt_h':
            return self._watt_hours()
        if attr == 'kwatt_h':
            return self._kwatt_hours()
        return {zone: [_type(float(getattr(row, attr))) for row in self.rows if row.zone == zone]
                for zone in self.get_zones()}

    def get_zones(self) -> list:
        return list({row.zone for row in self.rows})

    def get_time_stamps(self) -> list:
        zones = self.get_zones()
        # zone is irrelevant and we just need stamps for one
        return [int(float(row.time_elapsed)) for row in self.rows if row.zone == zones[0]]

    def _watt_hours(self) -> dict:
        return {zone: [float(row.power_j) / 3600 for row in self.rows if row.zone == zone] for zone in self.get_zones()}

    def _kwatt_hours(self) -> dict:
        return {zone: [float(row.power_j) / 3600 / 1000 for row in self.rows if row.zone == zone] for zone in
                self.get_zones()}


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

    def collect_metrics_by_zone(self, rapl_data: str, attr: str, metric: str, key_prefix: str) -> dict:
        if rapl_data == 'run_metrics':  # Used for Bar plot
            return self.retrieve_data_from_list(self.run_metrics, attr, metric, key_prefix, True)
        elif rapl_data == 'run_data':  # Used for Curve plot
            return self.retrieve_data_from_list(self.run_data, attr, metric, key_prefix, False)

    @staticmethod
    def retrieve_data_from_list(metrics, attr: str, metric: str, key_prefix: str, is_data_dict: bool):
        res = {}
        for m in metrics:
            attr_obj = getattr(m, attr)
            # Is the data stored in a dictionary?
            if is_data_dict:
                metric_obj = getattr(attr_obj, metric)
                for zone, value in metric_obj.items():
                    if zone not in res:
                        res[zone] = []

                    res[zone].append(value)
            else:
                # Collect data for all or a single metric
                if metric is None:
                    for zone in attr_obj.keys():
                        metric_obj = attr_obj.get(zone)
                        for value in metric_obj:
                            if zone not in res:
                                res[zone] = []

                            res[zone].append(value)
                else:
                    res[metric] = []
                    res[metric] = attr_obj[metric]

        if metric is None:
            # Reorder data for consistent graphs.
            reordered_dict = {k: res[k] for k in DESIRED_ORDER}
            # Add prefix to key names.
            if key_prefix != "":
                renamed_dict = {key_prefix + key: reordered_dict[key] for key, value in reordered_dict.items()}
                return renamed_dict

            return reordered_dict
        else:
            # No dict to reorder due to only having 1 entry.
            # Add prefix to key names.
            if key_prefix != "":
                renamed_dict = {key_prefix + key: res[key] for key, value in res.items()}
                return renamed_dict

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


class DockerStatsRow:
    def __init__(self, container_id: str, name: str, cpu: float, memory: float,
                 memory_limit: float, memory_percentage: float, network_input: float,
                 network_output: float, block_input: float, block_output: float, pids: int):
        self.container_id = container_id
        self.name = name
        self.cpu = float(cpu)
        self.memory = float(memory)
        self.memory_limit = float(memory_limit)
        self.memory_percentage = float(memory_percentage)
        self.network_input = network_input
        self.network_output = network_output
        self.block_input = block_input
        self.block_output = block_output
        self.pids = int(pids)
