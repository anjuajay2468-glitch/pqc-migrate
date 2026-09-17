import csv
from pathlib import Path

INPUT = Path(
    "experiments/large_scale/results/statistical_summary.csv"
)

OUTPUT = Path(
    "experiments/large_scale/results/hybrid_overhead_analysis.csv"
)

groups = {}

with INPUT.open(newline="") as f:
    for row in csv.DictReader(f):
        key = (
            row["protocol"],
            row["network_profile"],
        )

        groups.setdefault(key, {})[
            row["configuration"]
        ] = row


with OUTPUT.open("w", newline="") as f:

    writer = csv.writer(f)

    writer.writerow([
        "protocol",
        "network_profile",
        "classical_observations",
        "hybrid_observations",
        "classical_mean_us",
        "hybrid_mean_us",
        "mean_difference_us",
        "mean_overhead_percent",
        "classical_median_us",
        "hybrid_median_us",
        "median_difference_us",
        "median_overhead_percent",
        "classical_stddev_us",
        "hybrid_stddev_us",
    ])

    print("=============================================")
    print("       PQC-Migrate Phase 9.8")
    print("       HYBRID OVERHEAD ANALYSIS")
    print("=============================================")
    print()

    for key in sorted(groups):

        protocol, profile = key

        classical = groups[key]["Classical"]
        hybrid = groups[key]["Hybrid"]

        c_mean = float(classical["mean_latency_us"])
        h_mean = float(hybrid["mean_latency_us"])

        c_median = float(classical["median_latency_us"])
        h_median = float(hybrid["median_latency_us"])

        c_std = float(classical["stddev_latency_us"])
        h_std = float(hybrid["stddev_latency_us"])

        mean_difference = h_mean - c_mean
        median_difference = h_median - c_median

        if c_mean != 0:
            mean_overhead = (
                mean_difference / c_mean * 100
            )
        else:
            mean_overhead = 0

        if c_median != 0:
            median_overhead = (
                median_difference / c_median * 100
            )
        else:
            median_overhead = 0

        writer.writerow([
            protocol,
            profile,
            classical["observations"],
            hybrid["observations"],
            f"{c_mean:.2f}",
            f"{h_mean:.2f}",
            f"{mean_difference:.2f}",
            f"{mean_overhead:.2f}",
            f"{c_median:.2f}",
            f"{h_median:.2f}",
            f"{median_difference:.2f}",
            f"{median_overhead:.2f}",
            f"{c_std:.2f}",
            f"{h_std:.2f}",
        ])

        print(
            f"{protocol:5s} | "
            f"{profile:16s} | "
            f"mean: "
            f"{c_mean:10.2f} -> {h_mean:10.2f} us | "
            f"overhead: {mean_overhead:8.2f}%"
        )

print()
print("=== OUTPUT ===")
print(OUTPUT)
print("Hybrid overhead analysis: PASS")
