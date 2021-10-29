import csv
from typing import List, Callable

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