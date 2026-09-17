import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATASET = PROJECT_ROOT / "experiments/large_scale/results/master_dataset.csv"
OUTPUT = PROJECT_ROOT / "experiments/analysis/results/descriptive_statistics.csv"

print("=" * 60)
print("       PQC-Migrate Phase 10.2")
print("       DESCRIPTIVE STATISTICS")
print("=" * 60)

df = pd.read_csv(DATASET)

print(f"Dataset: {DATASET}")
print(f"Observations loaded: {len(df)}")

required_columns = [
    "protocol",
    "configuration",
    "network_profile",
    "latency_us",
    "success"
]

missing = [col for col in required_columns if col not in df.columns]

if missing:
    raise ValueError(f"Missing required columns: {missing}")

analysis_df = df[
    (df["success"] == 1) &
    (df["latency_us"].notna())
].copy()

print(f"Successful observations with latency: {len(analysis_df)}")

group_columns = [
    "protocol",
    "configuration",
    "network_profile"
]

records = []

for group_values, group in analysis_df.groupby(group_columns):

    protocol, configuration, network_profile = group_values

    latency = group["latency_us"].astype(float)

    mean = latency.mean()
    median = latency.median()
    stddev = latency.std(ddof=1)
    minimum = latency.min()
    maximum = latency.max()
    range_value = maximum - minimum

    p95 = np.percentile(latency, 95)
    p99 = np.percentile(latency, 99)

    cv = (stddev / mean * 100) if mean != 0 else np.nan

    records.append({
        "protocol": protocol,
        "configuration": configuration,
        "network_profile": network_profile,
        "n": len(latency),
        "mean_latency_us": mean,
        "median_latency_us": median,
        "stddev_latency_us": stddev,
        "min_latency_us": minimum,
        "max_latency_us": maximum,
        "range_latency_us": range_value,
        "p95_latency_us": p95,
        "p99_latency_us": p99,
        "coefficient_variation_pct": cv
    })

result = pd.DataFrame(records)

profile_order = [
    "baseline",
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

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

result.to_csv(
    OUTPUT,
    index=False,
    float_format="%.4f"
)

print()
print("=== DESCRIPTIVE STATISTICS ===")
print(result.to_string(index=False))

print()
print(f"Output: {OUTPUT}")
print()
print("Descriptive statistics generation: PASS")
