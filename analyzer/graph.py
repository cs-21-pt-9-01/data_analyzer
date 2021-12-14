import os
from .models import AnalyzedData
from .parser import parse_input_paths
from .plot import groupbar

from decimal import *
import numpy as np

def translate_name(name):
  if name == 'chocolate-doom':
    return 'chocolate-doom (c)'
  elif name == 'crispy-doom':
    return 'crispy-doom (c)'
  elif name == 'eternity':
    return 'eternity (c++)'
  elif name == 'managed-doom':
    return 'managed-doom (c#)'
  elif name == 'mochadoom':
    return 'mochadoom (java)'
  elif name == 'prboom-opengl':
    return 'prboom+ opengl (c)'
  elif name == 'prboom-software' :
    return 'prboom+ software (c)'
  else:
    return 'Unknown'

def grouped_barchart_run(_input: str, output_file: str, title: str):
  overall_data = dict()
  for _d in os.listdir(_input):
    d = f'{_input}/{_d}'
    print(f'Parsing dir {d}')
    data = _parse_input(d, _d)
    overall_data.update(data)
    del data

  data = {
    # Labels will be sorted
    'labels': sorted(overall_data.keys()),
    'results': {}
  }

  # Iterate the benchmarks(hardcoded)
  for benchmark in data['labels']:
    # If the benchmark has not been added, then create dict
    if benchmark not in data:
      data[benchmark] = dict()
    # For every run inside the benchmark
    for run in overall_data[benchmark]:
      zones = dict()
      # For every row in the run of the benchmark
      for row in run.rows:
        if row.zone not in zones:
          zones[row.zone] = 0
        current_power = Decimal(row.power_j)
        # Save the largest value captured in the specific zone
        if current_power > zones[row.zone]:
          zones[row.zone] = current_power
          if row.zone == 'package-0':
            zones['time'] = Decimal(row.time_elapsed)
            zones['temperature'] = Decimal(row.temperature)
      # From the max, save the value to data variable
      for zone, max_value in zones.items():
        if zone not in data[benchmark]:
          data[benchmark][zone] = list()
        data[benchmark][zone].append(max_value)


    zones = list(data[benchmark].keys())
    for zone in zones:
      values = np.array(data[benchmark][zone])
      if zone not in data['results']:
        data['results'][zone] = {'mean': [], 'std': [], 'cnt': []}
      data['results'][zone]['mean'].append(round(values.mean(), 2))
      data['results'][zone]['std'].append(round(values.std(), 2))
      data['results'][zone]['cnt'].append(len(values))
      del data[benchmark][zone]
    del data[benchmark]
  data['labels'] = [translate_name(n) for n in data['labels']]
  import pprint
  pprint.pprint(data)
  groupbar(data, title, output_file)


def total_power_run(input, output_file):
  raise NotImplementedError

def avg_power_run(input, output_file):
  raise NotImplementedError



def _parse_input(_dir: str, name: str) -> dict:
    return {name: parse_input_paths([_dir])}