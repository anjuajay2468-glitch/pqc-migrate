import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# PQC-Migrate Phase 10.5
# Distribution & Outlier Analysis
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATASET = PROJECT_ROOT / "experiments/large_scale/results/master_dataset.csv"
SUMMARY_OUTPUT = PROJECT_ROOT / "experiments/analysis/results/outlier_summary.csv"
DETAIL_OUTPUT = PROJECT_ROOT / "experiments/analysis/results/outlier_observations.csv"

print("=" * 60)
print("       PQC-Migrate Phase 10.5")
print("       DISTRIBUTION & OUTLIER ANALYSIS")
print("=" * 60)

df = pd.read_csv(DATASET)

required = [
    "experiment_id",
    "protocol",
    "configuration",
    "network_profile",
    "iteration",
    "latency_us",
    "success"
]

missing = [c for c in required if c not in df.columns]

if missing:
    raise ValueError(f"Missing required columns: {missing}")

analysis_df = df[
    (df["success"] == 1) &
    (df["latency_us"].notna())
].copy()

analysis_df["latency_us"] = analysis_df["latency_us"].astype(float)

group_columns = [
    "protocol",
    "configuration",
    "network_profile"
]

summary_records = []
outlier_records = []

for group_values, group in analysis_df.groupby(group_columns):

    protocol, configuration, network_profile = group_values

    x = group["latency_us"]

    q1 = x.quantile(0.25)
    q3 = x.quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    flagged = group[
        (group["latency_us"] < lower_bound) |
        (group["latency_us"] > upper_bound)
    ].copy()

    mean_all = x.mean()
    median_all = x.median()

    if len(flagged) > 0:
        x_without = group.loc[
            ~group["experiment_id"].isin(flagged["experiment_id"]),
            "latency_us"
        ]

        mean_without = x_without.mean()
        median_without = x_without.median()
    else:
        mean_without = mean_all
        median_without = median_all

    summary_records.append({
        "protocol": protocol,
        "configuration": configuration,
        "network_profile": network_profile,
        "n": len(x),
        "q1_us": q1,
        "q3_us": q3,
        "iqr_us": iqr,
        "lower_bound_us": lower_bound,
        "upper_bound_us": upper_bound,
        "outlier_count": len(flagged),
        "outlier_pct": len(flagged) / len(x) * 100,
        "mean_all_us": mean_all,
        "median_all_us": median_all,
        "mean_without_outliers_us": mean_without,
        "median_without_outliers_us": median_without
    })

    for _, row in flagged.iterrows():

        outlier_records.append({
            "experiment_id": row["experiment_id"],
            "protocol": protocol,
            "configuration": configuration,
            "network_profile": network_profile,
            "iteration": row["iteration"],
            "latency_us": row["latency_us"],
            "lower_bound_us": lower_bound,
            "upper_bound_us": upper_bound
        })

summary = pd.DataFrame(summary_records)
outliers = pd.DataFrame(outlier_records)

profile_order = [
    "baseline",
    "latency100",
    "latency200",
    "bandwidth1mbps",
    "loss1",
    "mobile"
]

summary["network_profile"] = pd.Categorical(
    summary["network_profile"],
    categories=profile_order,
    ordered=True
)

summary = summary.sort_values(
    ["protocol", "configuration", "network_profile"]
)

SUMMARY_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

summary.to_csv(
    SUMMARY_OUTPUT,
    index=False,
    float_format="%.4f"
)

outliers.to_csv(
    DETAIL_OUTPUT,
    index=False,
    float_format="%.4f"
)

print()
print("=== OUTLIER SUMMARY ===")
print(summary.to_string(index=False))

print()
print("=== FLAGGED OBSERVATIONS ===")

if len(outliers) > 0:
    print(outliers.to_string(index=False))
else:
    print("No IQR outliers detected.")

print()
print(f"Groups analyzed: {len(summary)}")
print(f"Flagged observations: {len(outliers)}")
print(f"Summary output: {SUMMARY_OUTPUT}")
print(f"Detail output: {DETAIL_OUTPUT}")
print()
print("Distribution & outlier analysis: PASS")
