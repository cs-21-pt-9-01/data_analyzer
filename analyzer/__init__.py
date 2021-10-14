from . import util
from .graph import GraphGenerator, VALID_METRICS

from argparse import ArgumentParser

parser = ArgumentParser(description="RAPL data analyzer")
parser.add_argument('input', metavar='file(s) | dir(s)', type=str, nargs='+',
                    help="Input file(s) and/or dir(s) containing RAPL data")


def run():
    args = parser.parse_args()
    data_files = util.parse_input_paths(args.input)
    attrs = ['power_j', 'watts', 'watts_since_last', 'watt_h', 'kwatt_h']

    for data in data_files:
        g = GraphGenerator(data)

        #for attr in attrs:
        #    g.plot(attr)

        for attr in attrs:
            for metric in VALID_METRICS:
                g.bar(attr, metric)
