# RAPL data analysis

## Data processing
The data analyzer accepts nested directories containing csv files as defined by [cs-21-pt-9-01/rapl.rs#csv-output](https://github.com/cs-21-pt-9-01/rapl.rs#csv-output) as input.

This data will be converted to json on the form

```json
{
  "overall": {
    "power_j": {
      "min": {
        "package-0": 10.36710000000312,
        ... RAPL zones
      },
      ... data metrics
    },
    ... power metrics
  },
  "run_metrics": [
    {
      "watts": {
        "min": {
          "package-0": 14.944565853605146,
          ... RAPL zones
        },
        ... data metrics
      },
      ... power metrics
    },
    ... run metrics
  ],
  "run_data": [
    {
      "watt_h": {
        "uncore": [
          1.2171640388294502e-05,
          4.377414038830771e-05,
          0.00010043497372164212,
          ... data points
        ],
        ... RAPL zones
      },
      ... power metrics
    },
    ... run data
  ]
}
```

where
- "*overall*": meta-data about the benchmark runs
- "*run_metrics*": *data* metrics for each of the benchmark runs
- "*run_data*": all recorded data points for each of the benchmark runs
- `RAPL zones`: the different RAPL zones available in your CPU - see [cs-21-pt-9-01/rapl.rs#list](https://github.com/cs-21-pt-9-01/rapl.rs#list)
- `data metrics`: the calculated metrics - `[ min, max, median, mean, average ]` and, where applicable, the `total` amount (i.e., last measurement)
  - where applicable, the data is converted to steps beforehand (joules, w/h, kw/h)
- `power metrics`: the RAPL-related metrics calculated by [rapl.rs](https://github.com/cs-21-pt-9-01/rapl.rs)
  - power in joules, average watts, average watts per measurement, watt hours, kilowatt hours

A full example can be seen here: [cs-21-pt-9-01/benchmark_data](https://github.com/cs-21-pt-9-01/benchmark_data/blob/master/26102021/chocolate-doom/processed/chocolate-doom.json)

## Graphs

See `./sample/` for examples