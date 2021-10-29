from . import util
from .full import full_run
from .graph import GraphGenerator, VALID_METRICS, GRAPH_TYPES
from .models import VALID_ATTRS

import sys
from argparse import ArgumentParser

parser = ArgumentParser(description="RAPL data analyzer")
parser.add_argument('input', metavar='file(s) | dir(s)', type=str, nargs='+',
                    help="Input file(s) and/or dir(s) containing RAPL data")

subparsers = parser.add_subparsers(dest='subcmd')

graph = subparsers.add_parser('graph', help='Graph generation')
graph.add_argument('-t, --graph-type', type=str, nargs='+', help='Type of graph to generate',
                   choices=['plot', 'bar', 'all'], default='all')
graph.add_argument('-a, --attr', type=str, nargs='+', help='Metric to generate graphs from',
                   choices=['power_j', 'watts', 'watts_since_last', 'watt_h', 'kwatt_h', 'all'],
                   default='all')
graph.add_argument('-m, --metric', type=str, nargs='+', help='Metric to generate graph from',
                   choices=['min', 'max', 'median', 'avg', 'mean', 'all'], default='all')

metric = subparsers.add_parser('metric', help='Metric generation')
metric.add_argument('-t, --metric-type')

full = subparsers.add_parser('full', help="Generate everything necessary")


def run():
    args = parser.parse_args()

    #data_files = util.parse_input_paths(args.input)

    #if len(data_files) == 0:
    #    print('Error: no data files found')
    #    exit(1)

    #if args.subcmd == 'metric':
    #    pass
    #elif args.subcmd == 'graph':
    #    graph_types = GRAPH_TYPES if args.t[0] == 'all' else args.t
    #    for graph_type in graph_types:
    #        for data in data_files:
    #            g = GraphGenerator(data)
    #            attrs = VALID_ATTRS if args.a[0] == 'all' else args.a
    #            for attr in attrs:
    #                if graph_type == 'plot':
    #                    g.plot(attr)
    #                elif graph_type == 'bar':
    #                    metrics = VALID_METRICS if args.m[0] == 'all' else args.m
    #                    for metric in metrics:
    #                        g.bar(attr, metric)
    if args.subcmd == 'full':
        full_run(args.input[0])
    else:
        print(f'Error: unrecognized subcommand {args.subcmd}')
