import pandas as pd
from pathlib import Path

# ============================================================
# PQC-Migrate Phase 10.3
# Classical vs Hybrid Comparison
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

INPUT = PROJECT_ROOT / "experiments/analysis/results/descriptive_statistics.csv"
OUTPUT = PROJECT_ROOT / "experiments/analysis/results/classical_vs_hybrid.csv"

print("=" * 60)
print("       PQC-Migrate Phase 10.3")
print("       CLASSICAL vs HYBRID")
print("=" * 60)

df = pd.read_csv(INPUT)

required = [
    "protocol",
    "configuration",
    "network_profile",
    "n",
    "mean_latency_us",
    "median_latency_us",
    "p95_latency_us",
    "p99_latency_us"
]

missing = [c for c in required if c not in df.columns]

if missing:
    raise ValueError(f"Missing required columns: {missing}")

classical = df[df["configuration"] == "Classical"].copy()
hybrid = df[df["configuration"] == "Hybrid"].copy()

merge_columns = [
    "protocol",
    "network_profile"
]

classical = classical.rename(columns={
    "n": "classical_n",
    "mean_latency_us": "classical_mean_us",
    "median_latency_us": "classical_median_us",
    "p95_latency_us": "classical_p95_us",
    "p99_latency_us": "classical_p99_us"
})

hybrid = hybrid.rename(columns={
    "n": "hybrid_n",
    "mean_latency_us": "hybrid_mean_us",
    "median_latency_us": "hybrid_median_us",
    "p95_latency_us": "hybrid_p95_us",
    "p99_latency_us": "hybrid_p99_us"
})

comparison = pd.merge(
    classical[
        merge_columns +
        [
            "classical_n",
            "classical_mean_us",
            "classical_median_us",
            "classical_p95_us",
            "classical_p99_us"
        ]
    ],
    hybrid[
        merge_columns +
        [
            "hybrid_n",
            "hybrid_mean_us",
            "hybrid_median_us",
            "hybrid_p95_us",
            "hybrid_p99_us"
        ]
    ],
    on=merge_columns,
    how="inner"
)

# ------------------------------------------------------------
# Differences
# ------------------------------------------------------------

comparison["mean_difference_us"] = (
    comparison["hybrid_mean_us"] -
    comparison["classical_mean_us"]
)

comparison["mean_overhead_pct"] = (
    comparison["mean_difference_us"] /
    comparison["classical_mean_us"]
) * 100

comparison["mean_ratio"] = (
    comparison["hybrid_mean_us"] /
    comparison["classical_mean_us"]
)

comparison["median_difference_us"] = (
    comparison["hybrid_median_us"] -
    comparison["classical_median_us"]
)

comparison["median_overhead_pct"] = (
    comparison["median_difference_us"] /
    comparison["classical_median_us"]
) * 100

comparison["p95_difference_us"] = (
    comparison["hybrid_p95_us"] -
    comparison["classical_p95_us"]
)

comparison["p95_overhead_pct"] = (
    comparison["p95_difference_us"] /
    comparison["classical_p95_us"]
) * 100

comparison["p99_difference_us"] = (
    comparison["hybrid_p99_us"] -
    comparison["classical_p99_us"]
)

comparison["p99_overhead_pct"] = (
    comparison["p99_difference_us"] /
    comparison["classical_p99_us"]
) * 100

# ------------------------------------------------------------
# Order columns
# ------------------------------------------------------------

profile_order = [
    "baseline",
    "latency100",
    "latency200",
    "bandwidth1mbps",
    "loss1",
    "mobile"
]

comparison["network_profile"] = pd.Categorical(
    comparison["network_profile"],
    categories=profile_order,
    ordered=True
)

comparison = comparison.sort_values(
    ["protocol", "network_profile"]
)

# ------------------------------------------------------------
# Save
# ------------------------------------------------------------

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

comparison.to_csv(
    OUTPUT,
    index=False,
    float_format="%.4f"
)

# ------------------------------------------------------------
# Display
# ------------------------------------------------------------

print()
print("=== CLASSICAL vs HYBRID COMPARISON ===")
print(comparison.to_string(index=False))

print()
print(f"Comparison groups: {len(comparison)}")
print(f"Output: {OUTPUT}")
print()
print("Classical vs Hybrid comparison: PASS")
