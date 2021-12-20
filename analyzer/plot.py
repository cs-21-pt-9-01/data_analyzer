import matplotlib.pyplot as plt
import numpy as np

VALID_METRICS = ['min', 'max', 'median', 'avg', 'mean']
GRAPH_TYPES = ['plot', 'bar']


def plot(y: dict, x: list, fp: str, ylabel: str, title: str):
    fig, ax = plt.subplots()
    generate_x = not bool(x)

    for zone, values in y.items():
        if generate_x:
            x = range(len(values))
        ax.bar(x, values, label=zone)

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * .8, box.height])
    ax.grid()
    ax.set(xlabel='Benchmark no.', ylabel=ylabel, title=title)

    legend = ax.legend(loc='lower left', bbox_to_anchor=(1, .8))

    plt.savefig(fp)
    plt.close(fig)


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

    #for r in rects:
    #    ax.bar_label(r, padding=3)

    fig.tight_layout()
    fig.autofmt_xdate()

    plt.savefig(output_file)
    plt.close(fig)
