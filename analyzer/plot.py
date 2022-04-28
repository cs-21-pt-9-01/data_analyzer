import matplotlib.pyplot as plt
import numpy as np

VALID_METRICS = ['min', 'max', 'median', 'avg', 'mean']
GRAPH_TYPES = ['plot', 'bar']
# Colors from previous project.
ZONE_COLOR = {
    'package-0': [31 / 255, 119 / 255, 180 / 255],
    'core': 'orange',
    'uncore': 'green',
    'dram': 'red'
}


def plot(chart: str, y: dict, x: list, fp: str, xlabel: str, ylabel: str, title: str):
    fig, ax = plt.subplots()
    generate_x = not bool(x)

    for zone, values in y.items():
        if generate_x:
            x = range(len(values))
        if chart == 'plot':
            ax.bar(x, values, label=zone, color=ZONE_COLOR.get(zone))
        elif chart == 'curve':
            ax.plot(x, values, label=zone, color=ZONE_COLOR.get(zone))

    ax.grid()
    create_plot(ax, xlabel, ylabel, title, fp, fig)


def create_plot(ax, xlabel, ylabel, title, fp, fig):
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * .8, box.height])
    ax.set(xlabel=xlabel, ylabel=ylabel, title=title)

    ax.legend(loc='lower left', bbox_to_anchor=(1, .8))

    plt.savefig(fp, bbox_inches='tight')
    plt.close(fig)


def docker_plot(y: dict, fp: str, xlabel: str, ylabel: str, title: str, docker_stat: str):
    fig, ax = plt.subplots()
    # Create x-coordinates.
    # This is sufficient as docker stats are collected every 2 seconds.
    x = range(0, len(y[docker_stat]) * 2, 2)
    ax.plot(x, y[docker_stat], label=docker_stat.upper(), linewidth=1)

    # Hide grid lines
    ax.grid(False)
    # Add vertical lines marking the increase in thread count.
    idle_time = 450
    vertical_line_coordinates = range(0 + idle_time, len(y[docker_stat]) * 2 - idle_time, 450)
    for coordinate in vertical_line_coordinates:
        ax.axvline(x=coordinate, color="purple", ls=":")

    # Set x-axis interval to 450
    ax.xaxis.set_ticks(np.arange(0, len(y[docker_stat]) * 3, 450))

    # Stretch out figure
    fig.set_size_inches(18.5, 10.5)
    create_plot(ax, xlabel, ylabel, title, fp, fig)


def bar(data: dict, fp: str, ylabel: str, xlabel: str, title: str):
    fig, ax = plt.subplots()

    ax.bar(data.keys(), data.values())
    ax.set(xlabel=xlabel, ylabel=ylabel, title=title)
    ax.grid()

    plt.savefig(fp)
    plt.close(fig)


def groupbar(data: dict, title: str, output_file: str, ymax: int):
    column_order = ['package-0', 'core', 'uncore', 'dram']
    benchmarks = data['labels']
    max_index = len(benchmarks)

    # x = numpy array: [0, 1, 2, 3 ... max_index]
    x = np.arange(max_index)
    width = 0.20

    fig, ax = plt.subplots()
    rects = []
    index = 0
    offset = len(column_order) / 2 - 1
    if len(column_order) % 2 == 0:
        offset += .5

    for name in column_order:
        result = data['results'][name]
        x_pos = x + index * width - offset * width
        r = ax.bar(x_pos, result['mean'], width, yerr=result['std'], label=name)
        rects.append(r)
        index += 1

    ax.set_ylabel('Joules')
    ax.set_title(title)
    ax.set_xticks(x, benchmarks)
    ax.legend()
    if ymax is not None:
        ax.set_ylim([0, ymax])

    # for r in rects:
    #    ax.bar_label(r, padding=3)

    fig.tight_layout()
    fig.autofmt_xdate()

    plt.savefig(output_file)
    plt.close(fig)
