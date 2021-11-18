from . import util
from .full import full_run
from .graph import GraphGenerator, VALID_METRICS, GRAPH_TYPES
from .models import VALID_ATTRS
from .cochran import cochran

from argparse import ArgumentParser

parser = ArgumentParser(description="RAPL data analyzer")
parser.add_argument('--input', metavar='file(s) | dir(s)', type=str, nargs=1,
                    help="Input file(s) and/or dir(s) containing RAPL data")

parser.add_argument('-c', type=str, nargs=1)

def run():
    args = parser.parse_args()
    if args.c:
        cochran(args.c[0])
    else:
        full_run(args.input[0])
