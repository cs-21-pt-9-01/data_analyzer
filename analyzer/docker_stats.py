from analyzer.models import DockerStatsRow
import csv
import re
# import pandas as pd
from .plot import plot
import os


def parse_stats_row(row):
    row.pop(4)
    row.pop(7)
    row.pop(9)
    row[2] = row[2].replace('%', '')
    row[3] = re.sub('[a-z]', '', row[3].lower())
    row[4] = re.sub('[a-z]', '', row[4].lower())
    row[5] = row[5].replace('%', '')
    row[6] = re.sub('[a-z]', '', row[6].lower())
    row[7] = re.sub('[a-z]', '', row[7].lower())
    row[8] = re.sub('[a-z]', '', row[8].lower())
    row[9] = re.sub('[a-z]', '', row[9].lower())
    return row


def remove_outlier(dataFrame, col_name='cpu', threshold=100):
    return dataFrame[dataFrame[col_name] > threshold]


def initialize_dict(values):
    values["container_id"] = []
    values["name"] = []
    values["cpu"] = []
    values["memory"] = []
    values["memory_limit"] = []
    values["memory_percentage"] = []
    values["network_input"] = []
    values["network_output"] = []
    values["block_input"] = []
    values["block_output"] = []
    values["pids"] = []
    return values


def docker_run(_dir: str, output: str, title: str):
    # Read row data into list and count the line number.
    # reader.line_num moves the file pointer and the file is thus not usable after being called.
    with open(_dir, 'r', newline='\n') as f:
        reader = csv.reader((','.join(line.split()) for line in f if "CONTAINER" not in line), delimiter=',')
        data = list(reader)
        total_row_count = reader.line_num

    values = {}
    first_row = True
    previous_cpu_value = 0
    skip_counter = 0
    current_row_counter = 0

    for row in data:
        current_row_counter += 1
        row = parse_stats_row(row)
        # Create keys with empty lists
        if first_row:
            values = initialize_dict(values)
            first_row = False

        # Skip outliers.
        # Outliers = sudden drop of 100% in CPU usage
        if float(row[2]) < (previous_cpu_value - 100):
            if not current_row_counter > (total_row_count - skip_counter):
                skip_counter += 1
                continue

        # Add values to lists
        docker_row = DockerStatsRow(*row)
        values["container_id"].append(docker_row.container_id)
        values["name"].append(docker_row.name)
        values["cpu"].append(docker_row.cpu)
        values["memory"].append(docker_row.memory)
        values["memory_limit"].append(docker_row.memory_limit)
        values["memory_percentage"].append(docker_row.memory_percentage)
        values["network_input"].append(docker_row.network_input)
        values["network_output"].append(docker_row.network_output)
        values["block_input"].append(docker_row.block_input)
        values["block_output"].append(docker_row.block_output)
        values["pids"].append(docker_row.pids)
        previous_cpu_value = float(row[2])

    # df = remove_outlier(pd.DataFrame(data=values), threshold=0)
    # values = df.to_dict("list")

    print("Outliers: " + str(skip_counter))

    path = f'{os.path.dirname(_dir)}/processed'
    if not os.path.isdir(path):
        os.makedirs(path)
    plot("curve", values, [], f"{path}/{output}", "Time (seconds)",
         "CPU usage", f"{title}", docker_stat="cpu")
    print('Done')
