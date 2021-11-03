import matplotlib.pyplot as plt

VALID_METRICS = ['min', 'max', 'median', 'avg', 'mean']
GRAPH_TYPES = ['plot', 'bar']


class GraphGenerator:

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
        ax.grid()

        plt.savefig(fp)
        plt.close(fig)