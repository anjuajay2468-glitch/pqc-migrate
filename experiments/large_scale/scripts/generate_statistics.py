import csv
import statistics
from pathlib import Path
from collections import defaultdict

DATASET = Path(
    "experiments/large_scale/results/master_dataset.csv"
)

OUTPUT = Path(
    "experiments/large_scale/results/statistical_summary.csv"
)

with DATASET.open(newline="") as f:
    rows = list(csv.DictReader(f))

groups = defaultdict(list)

for row in rows:
    key = (
        row["protocol"],
        row["configuration"],
        row["network_profile"],
    )

    groups[key].append(float(row["latency_us"]))

with OUTPUT.open("w", newline="") as f:

    writer = csv.writer(f)

    writer.writerow([
        "protocol",
        "configuration",
        "network_profile",
        "observations",
        "mean_latency_us",
        "median_latency_us",
        "stddev_latency_us",
        "minimum_latency_us",
        "maximum_latency_us",
    ])

    print("=============================================")
    print("       PQC-Migrate Phase 9.7")
    print("       STATISTICAL SUMMARY")
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

        minimum = min(values)
        maximum = max(values)

        writer.writerow([
            protocol,
            configuration,
            profile,
            len(values),
            f"{mean:.2f}",
            f"{median:.2f}",
            f"{stddev:.2f}",
            f"{minimum:.2f}",
            f"{maximum:.2f}",
        ])

        print(
            f"{protocol:5s} | "
            f"{configuration:9s} | "
            f"{profile:16s} | "
            f"N={len(values):2d} | "
            f"mean={mean:10.2f} us | "
            f"median={median:10.2f} us | "
            f"stddev={stddev:10.2f} us"
        )

print()
print("=== OUTPUT ===")
print(OUTPUT)
print("Statistical summary: PASS")
