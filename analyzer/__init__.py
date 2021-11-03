from . import util
from .full import full_run
from .graph import GraphGenerator, VALID_METRICS, GRAPH_TYPES
from .models import VALID_ATTRS

import sys
from argparse import ArgumentParser

parser = ArgumentParser(description="RAPL data analyzer")
parser.add_argument('input', metavar='file(s) | dir(s)', type=str, nargs=1,
                    help="Input file(s) and/or dir(s) containing RAPL data")


def run():
    args = parser.parse_args()
    full_run(args.input[0])
