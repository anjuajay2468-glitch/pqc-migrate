import csv
import statistics
from pathlib import Path
from collections import defaultdict

INPUT = Path(
    "experiments/large_scale/results/master_dataset.csv"
)

OUTPUT = Path(
    "experiments/large_scale/results/variability_analysis.csv"
)

groups = defaultdict(list)

with INPUT.open(newline="") as f:
    for row in csv.DictReader(f):
        key = (
            row["protocol"],
            row["configuration"],
            row["network_profile"],
        )

        groups[key].append(
            float(row["latency_us"])
        )


def percentile(values, percentile):
    values = sorted(values)

    if len(values) == 1:
        return values[0]

    position = (len(values) - 1) * percentile
    lower = int(position)
    upper = min(lower + 1, len(values) - 1)

    fraction = position - lower

    return (
        values[lower]
        + (values[upper] - values[lower])
        * fraction
    )


with OUTPUT.open("w", newline="") as f:

    writer = csv.writer(f)

    writer.writerow([
        "protocol",
        "configuration",
        "network_profile",
        "observations",
        "mean_us",
        "median_us",
        "stddev_us",
        "p95_us",
        "p99_us",
        "minimum_us",
        "maximum_us",
        "range_us",
        "coefficient_of_variation_percent",
    ])

    print("=============================================")
    print("       PQC-Migrate Phase 9.9")
    print("       VARIABILITY & OUTLIER ANALYSIS")
    print("=============================================")
    print()

    for key in sorted(groups):

        protocol, configuration, profile = key
        values = groups[key]

        mean = statistics.mean(values)
        median = statistics.median(values)

        stddev = (
            statistics.stdev(values)
            if len(values) > 1
            else 0
        )

        p95 = percentile(values, 0.95)
        p99 = percentile(values, 0.99)

        minimum = min(values)
        maximum = max(values)
        range_value = maximum - minimum

        if mean != 0:
            cv = stddev / mean * 100
        else:
            cv = 0

        writer.writerow([
            protocol,
            configuration,
            profile,
            len(values),
            f"{mean:.2f}",
            f"{median:.2f}",
            f"{stddev:.2f}",
            f"{p95:.2f}",
            f"{p99:.2f}",
            f"{minimum:.2f}",
            f"{maximum:.2f}",
            f"{range_value:.2f}",
            f"{cv:.2f}",
        ])

        print(
            f"{protocol:5s} | "
            f"{configuration:9s} | "
            f"{profile:16s} | "
            f"N={len(values):2d} | "
            f"mean={mean:10.2f} | "
            f"median={median:10.2f} | "
            f"p95={p95:10.2f} | "
            f"CV={cv:7.2f}%"
        )

print()
print("=== OUTPUT ===")
print(OUTPUT)
print("Variability analysis: PASS")
