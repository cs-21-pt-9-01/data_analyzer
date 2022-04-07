from argparse import ArgumentParser

from .full import full_run
from .graph import grouped_barchart_run, total_power_run, avg_power_run

parser = ArgumentParser(description="RAPL data analyzer")
parser.add_argument('--input', metavar='file(s) | dir(s)', type=str,
                    help="Input file(s) and/or dir(s) containing RAPL data", required=True)

graphs = ['grouped_barchart', 'power_j_total', 'power_j_avg', 'power_curve']

parser.add_argument('--graph', choices=graphs,
                    help="Name of the graph to output", required=True)

parser.add_argument('--output', type=str,
                    help='Output file', default='plot.png')

parser.add_argument('--title', type=str,
                    help='Title of the plot created', default='Default')
parser.add_argument('--ymax', type=int,
                    help='The Y-axis max', default=None)


def run():
    args = parser.parse_args()
    if args.graph == 'grouped_barchart':
        grouped_barchart_run(args.input, args.output, args.title, args.ymax)
    elif args.graph == 'power_j_total':
        full_run(args.input, 'plot', args.output, args.title)
    elif args.graph == 'power_j_avg':
        full_run(args.input, 'bar', args.output, args.title)
    elif args.graph == 'power_curve':
        full_run(args.input, 'curve', args.output, args.title)
    else:
        raise NotImplementedError(f'The method for the option "{args.graph}" is not implented')
