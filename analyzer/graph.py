from . import util
from .models import RAPLData

from typing import Union

import numpy as np
import matplotlib.pyplot as plt


class GraphGenerator:

    def __init__(self, data: RAPLData):
        self.data = data

    def _round_to(self, attr: str) -> Union[int, float]:
        if 'power' in attr:
            return 100
        elif attr == 'watt_h':
            return 0.1
        elif attr == 'kwatt_h':
            return 0.0001
        elif 'watt' in attr:
            return 2

    def plot(self, attr: str):
        time_stamps = self.data.get_time_stamps()
        del time_stamps[0]
        data = self.data.get_field_as_dict(attr)
        fig, ax = plt.subplots()

        round_to = self._round_to(attr)

        max_x = time_stamps[-1]
        max_y = max([max(y) for y in data.values()])

        major_ticks_time = np.arange(0, max_x, round(max_x / 10))
        minor_ticks_time = np.arange(0, max_x, 2)
        major_ticks_data = np.arange(0, util.round_to_nearest(max_y, round_to), util.round_to_nearest(max_y, round_to) / 10)
        minor_ticks_data = np.arange(0, max_y, round_to / 5)

        for key, data in data.items():
            del data[0]
            ax.plot(time_stamps, data, label=key)

        ax.set_xticks(major_ticks_time)
        ax.set_xticks(minor_ticks_time, minor=True)
        ax.set_yticks(major_ticks_data)
        ax.set_yticks(minor_ticks_data, minor=True)
        ax.set_title(attr)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel(f'Power ({attr})')

        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * .8, box.height])

        legend = ax.legend(loc='lower left', bbox_to_anchor=(1, .8))

        plt.savefig(f'{attr}_plot.png')