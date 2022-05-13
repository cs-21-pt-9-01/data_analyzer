from analyzer.models import DockerStatsRow
import csv
import re
from .plot import docker_plot
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


def micro_docker_run(_dir: str, output: str, title: str):
    # Read row data into list and count the line number.
    # reader.line_num moves the file pointer and the file is thus not usable after being called.
    with open(_dir, 'r', newline='\n') as f:
        reader = csv.reader((','.join(line.split()) for line in f if "CONTAINER" not in line), delimiter=',')
        data = list(reader)
        total_row_count = reader.line_num

    pet = {}
    user = {}
    store = {}
    gateway = {}
    first_row = True
    skip_counter = 0
    current_row_counter = 0

    for row in data:
        current_row_counter += 1
        row = parse_stats_row(row)
        # Create keys with empty lists
        if first_row:
            pet = initialize_dict(pet)
            user = initialize_dict(user)
            store = initialize_dict(store)
            gateway = initialize_dict(gateway)
            first_row = False

        # Add values to lists
        docker_row = DockerStatsRow(*row)
        if docker_row.name == "petstore-gateway-java":
            gateway["container_id"].append(docker_row.container_id)
            gateway["name"].append(docker_row.name)
            gateway["cpu"].append(docker_row.cpu)
            gateway["memory"].append(docker_row.memory)
            gateway["memory_limit"].append(docker_row.memory_limit)
            gateway["memory_percentage"].append(docker_row.memory_percentage)
            gateway["network_input"].append(docker_row.network_input)
            gateway["network_output"].append(docker_row.network_output)
            gateway["block_input"].append(docker_row.block_input)
            gateway["block_output"].append(docker_row.block_output)
            gateway["pids"].append(docker_row.pids)
        elif docker_row.name == "petstore-pet-java":
            pet["container_id"].append(docker_row.container_id)
            pet["name"].append(docker_row.name)
            pet["cpu"].append(docker_row.cpu)
            pet["memory"].append(docker_row.memory)
            pet["memory_limit"].append(docker_row.memory_limit)
            pet["memory_percentage"].append(docker_row.memory_percentage)
            pet["network_input"].append(docker_row.network_input)
            pet["network_output"].append(docker_row.network_output)
            pet["block_input"].append(docker_row.block_input)
            pet["block_output"].append(docker_row.block_output)
            pet["pids"].append(docker_row.pids)
        elif docker_row.name == "petstore-user-java":
            user["container_id"].append(docker_row.container_id)
            user["name"].append(docker_row.name)
            user["cpu"].append(docker_row.cpu)
            user["memory"].append(docker_row.memory)
            user["memory_limit"].append(docker_row.memory_limit)
            user["memory_percentage"].append(docker_row.memory_percentage)
            user["network_input"].append(docker_row.network_input)
            user["network_output"].append(docker_row.network_output)
            user["block_input"].append(docker_row.block_input)
            user["block_output"].append(docker_row.block_output)
            user["pids"].append(docker_row.pids)
        elif docker_row.name == "petstore-store-java":
            store["container_id"].append(docker_row.container_id)
            store["name"].append(docker_row.name)
            store["cpu"].append(docker_row.cpu)
            store["memory"].append(docker_row.memory)
            store["memory_limit"].append(docker_row.memory_limit)
            store["memory_percentage"].append(docker_row.memory_percentage)
            store["network_input"].append(docker_row.network_input)
            store["network_output"].append(docker_row.network_output)
            store["block_input"].append(docker_row.block_input)
            store["block_output"].append(docker_row.block_output)
            store["pids"].append(docker_row.pids)

    path = f'{os.path.dirname(_dir)}/processed'
    if not os.path.isdir(path):
        os.makedirs(path)
    values = {}
    values["gateway"] = dict(gateway)
    values["pet"] = dict(pet)
    values["user"] = dict(user)
    values["store"] = dict(store)
    docker_plot(gateway, f"{path}/combined_{output}", "Time (seconds)",
                "Microservice CPU usage (%)", f"{title}", "cpu", values)
    #docker_plot(pet, f"{path}/pet_{output}", "Time (seconds)",
    #            "Pet CPU usage (%)", f"{title}", "cpu", skip_counter)
    #docker_plot(user, f"{path}/user_{output}", "Time (seconds)",
    #            "User CPU usage (%)", f"{title}", "cpu", skip_counter)
    #docker_plot(store, f"{path}/store_{output}", "Time (seconds)",
    #            "Store CPU usage (%)", f"{title}", "cpu", skip_counter)
    print('Done')
