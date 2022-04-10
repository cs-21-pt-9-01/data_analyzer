from argparse import ArgumentParser

from .full import full_run
from .graph import grouped_barchart_run, total_power_run, avg_power_run

parser = ArgumentParser(description="RAPL data analyzer")
parser.add_argument('--input', metavar='file(s) | dir(s)', type=str,
                    help="Input file(s) and/or dir(s) containing RAPL data", required=True)

graphs = ['grouped_barchart', 'power_j_total', 'power_j_avg', 'power_curve']
graphs_requiring_attribute = ['power_j_total', 'power_j_avg', 'power_curve']
VALID_RAPL_ZONE = ['package-0', 'core', 'uncore', 'dram']
VALID_ATTRS = ['power_j', 'watts', 'watts_since_last', 'watt_h', 'kwatt_h']
VALID_METRICS = ['avg', 'max', 'mean', 'median', 'min', 'total']

parser.add_argument('--graph', choices=graphs,
                    help="Name of the graph to output", required=True)

parser.add_argument('--output', type=str,
                    help='Output file', default='plot.png')
parser.add_argument('--zone', type=str, choices=VALID_RAPL_ZONE,
                    help='Name of RAPL Zone to be plotted. Leave empty for all.', default=None)
parser.add_argument('--attr', type=str, choices=VALID_ATTRS,
                    help="Name of RAPL attribute to be plotted.", default=None)
parser.add_argument('--metric', type=str, choices=VALID_METRICS,
                    help="Name of metric to be plotted.", default=None)
parser.add_argument('--title', type=str,
                    help='Title of the plot created', default='Default')
parser.add_argument('--ymax', type=int,
                    help='The Y-axis max', default=None)
parser.add_argument('--xmin', type=int,
                    help='The X-axis min', default=None)
parser.add_argument('--xmax', type=int,
                    help='The X-axis max', default=None)


def run():
    args = parser.parse_args()
    if args.graph == 'grouped_barchart':
        grouped_barchart_run(args.input, args.output, args.title, args.ymax)
    elif args.attr is not None:
        if args.graph == 'power_j_total':
            full_run(args.input, 'plot', args.output, args.title, args.attr, args.metric, args.xmin, args.xmax)
        elif args.graph == 'power_j_avg':
            full_run(args.input, 'bar', args.output, args.title, args.attr, args.metric, args.xmin, args.xmax)
        elif args.graph == 'power_curve':
            # 'power_curve' automatically plots multiple lines in a single graph when a dir is specified.
            full_run(args.input, 'curve', args.output, args.title, args.attr, args.zone, args.xmin, args.xmax)
    elif args.attr is None:
        raise RuntimeError(f'Graphs of type, ' + str(graphs_requiring_attribute) + ' require the --attr argument.')
    else:
        raise NotImplementedError(f'The method for the option "{args.graph}" is not implented')
