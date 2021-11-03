from . import util
from .models import RAPLData

from typing import Union, List

import numpy as np
import matplotlib.pyplot as plt

VALID_METRICS = ['min', 'max', 'median', 'avg', 'mean']
GRAPH_TYPES = ['plot', 'bar']


class GraphGenerator:

    @staticmethod
    def _round_to(attr: str) -> Union[int, float]:
        if 'power' in attr:
            return 100
        elif attr == 'watt_h':
            return 0.1
        elif attr == 'kwatt_h':
            return 0.0001
        elif 'watt' in attr:
            return 2

    @staticmethod
    def plot(y: dict, x: list, fp: str, ylabel: str, title: str):
        fig, ax = plt.subplots()
        generate_x = not bool(x)

        for zone, values in y.items():
            if generate_x:
                x = range(len(values))
            ax.plot(x, values, label=zone)

        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * .8, box.height])
        ax.grid()
        ax.set(xlabel='Benchmark no.', ylabel=ylabel, title=title)

        legend = ax.legend(loc='lower left', bbox_to_anchor=(1, .8))

        plt.savefig(fp)
        plt.close(fig)

    @staticmethod
    def bar(data: dict, fp: str, ylabel: str, xlabel: str, title: str):
        fig, ax = plt.subplots()

        ax.bar(data.keys(), data.values())
        ax.set(xlabel=xlabel, ylabel=ylabel, title=title)

        plt.savefig(fp)
        plt.close(fig)