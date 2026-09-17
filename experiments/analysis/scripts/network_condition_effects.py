import pandas as pd
from pathlib import Path

# ============================================================
# PQC-Migrate Phase 10.4
# Network-Condition Effects
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

INPUT = PROJECT_ROOT / "experiments/analysis/results/descriptive_statistics.csv"
OUTPUT = PROJECT_ROOT / "experiments/analysis/results/network_condition_effects.csv"

print("=" * 60)
print("       PQC-Migrate Phase 10.4")
print("       NETWORK-CONDITION EFFECTS")
print("=" * 60)

df = pd.read_csv(INPUT)

required = [
    "protocol",
    "configuration",
    "network_profile",
    "mean_latency_us",
    "median_latency_us",
    "p95_latency_us"
]

missing = [c for c in required if c not in df.columns]

if missing:
    raise ValueError(f"Missing required columns: {missing}")

baseline = df[df["network_profile"] == "baseline"].copy()

baseline = baseline.rename(columns={
    "mean_latency_us": "baseline_mean_us",
    "median_latency_us": "baseline_median_us",
    "p95_latency_us": "baseline_p95_us"
})

profiles = df[df["network_profile"] != "baseline"].copy()

result = pd.merge(
    profiles,
    baseline[
        [
            "protocol",
            "configuration",
            "baseline_mean_us",
            "baseline_median_us",
            "baseline_p95_us"
        ]
    ],
    on=["protocol", "configuration"],
    how="left"
)

# ------------------------------------------------------------
# Mean latency impact
# ------------------------------------------------------------

result["mean_change_us"] = (
    result["mean_latency_us"] -
    result["baseline_mean_us"]
)

result["mean_change_pct"] = (
    result["mean_change_us"] /
    result["baseline_mean_us"]
) * 100

# ------------------------------------------------------------
# Median latency impact
# ------------------------------------------------------------

result["median_change_us"] = (
    result["median_latency_us"] -
    result["baseline_median_us"]
)

result["median_change_pct"] = (
    result["median_change_us"] /
    result["baseline_median_us"]
) * 100

# ------------------------------------------------------------
# P95 latency impact
# ------------------------------------------------------------

result["p95_change_us"] = (
    result["p95_latency_us"] -
    result["baseline_p95_us"]
)

result["p95_change_pct"] = (
    result["p95_change_us"] /
    result["baseline_p95_us"]
) * 100

# ------------------------------------------------------------
# Sort
# ------------------------------------------------------------

profile_order = [
    "latency100",
    "latency200",
    "bandwidth1mbps",
    "loss1",
    "mobile"
]

result["network_profile"] = pd.Categorical(
    result["network_profile"],
    categories=profile_order,
    ordered=True
)

result = result.sort_values(
    ["protocol", "configuration", "network_profile"]
)

# ------------------------------------------------------------
# Select output columns
# ------------------------------------------------------------

result = result[
    [
        "protocol",
        "configuration",
        "network_profile",
        "baseline_mean_us",
        "mean_latency_us",
        "mean_change_us",
        "mean_change_pct",
        "baseline_median_us",
        "median_latency_us",
        "median_change_us",
        "median_change_pct",
        "baseline_p95_us",
        "p95_latency_us",
        "p95_change_us",
        "p95_change_pct"
    ]
]

# ------------------------------------------------------------
# Save
# ------------------------------------------------------------

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

result.to_csv(
    OUTPUT,
    index=False,
    float_format="%.4f"
)

print()
print("=== NETWORK CONDITION EFFECTS ===")
print(result.to_string(index=False))

print()
print(f"Comparison groups: {len(result)}")
print(f"Output: {OUTPUT}")
print()
print("Network-condition analysis: PASS")
