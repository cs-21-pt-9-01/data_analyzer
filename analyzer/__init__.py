from . import util
from .graph import GraphGenerator

from argparse import ArgumentParser

parser = ArgumentParser(description="RAPL data analyzer")
parser.add_argument('input', metavar='file(s) | dir(s)', type=str, nargs='+',
                    help="Input file(s) and/or dir(s) containing RAPL data")


def run():
    args = parser.parse_args()
    data_files = util.parse_input_paths(args.input)

    for data in data_files:
        g = GraphGenerator(data)
        g.plot('power_j')
        g.plot('watts')
        g.plot('watts_since_last')
        g.plot('watt_h')
        g.plot('kwatt_h')
