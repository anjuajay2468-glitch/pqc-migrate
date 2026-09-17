import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import mannwhitneyu
from statsmodels.stats.multitest import multipletests

# ============================================================
# PQC-Migrate Phase 10.6
# Statistical Significance Testing
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATASET = PROJECT_ROOT / "experiments/large_scale/results/master_dataset.csv"
OUTPUT = PROJECT_ROOT / "experiments/analysis/results/significance_testing.csv"

ALPHA = 0.05

print("=" * 60)
print("       PQC-Migrate Phase 10.6")
print("       STATISTICAL SIGNIFICANCE TESTING")
print("=" * 60)

df = pd.read_csv(DATASET)

required = [
    "protocol",
    "configuration",
    "network_profile",
    "latency_us",
    "success"
]

missing = [c for c in required if c not in df.columns]

if missing:
    raise ValueError(f"Missing required columns: {missing}")

df = df[
    (df["success"] == 1) &
    (df["latency_us"].notna())
].copy()

df["latency_us"] = df["latency_us"].astype(float)

profiles = [
    "baseline",
    "latency100",
    "latency200",
    "bandwidth1mbps",
    "loss1",
    "mobile"
]

records = []
p_values = []

# ------------------------------------------------------------
# Mann-Whitney U tests
# ------------------------------------------------------------

for protocol in ["SSH", "TLS"]:

    for profile in profiles:

        classical = df[
            (df["protocol"] == protocol) &
            (df["configuration"] == "Classical") &
            (df["network_profile"] == profile)
        ]["latency_us"].values

        hybrid = df[
            (df["protocol"] == protocol) &
            (df["configuration"] == "Hybrid") &
            (df["network_profile"] == profile)
        ]["latency_us"].values

        if len(classical) == 0 or len(hybrid) == 0:
            raise ValueError(
                f"Missing data for {protocol} / {profile}"
            )

        statistic, p_value = mannwhitneyu(
            classical,
            hybrid,
            alternative="two-sided"
        )

        classical_median = np.median(classical)
        hybrid_median = np.median(hybrid)

        median_difference = hybrid_median - classical_median

        records.append({
            "protocol": protocol,
            "network_profile": profile,
            "classical_n": len(classical),
            "hybrid_n": len(hybrid),
            "classical_median_us": classical_median,
            "hybrid_median_us": hybrid_median,
            "median_difference_us": median_difference,
            "u_statistic": statistic,
            "raw_p_value": p_value
        })

        p_values.append(p_value)

# ------------------------------------------------------------
# Benjamini-Hochberg FDR correction
# ------------------------------------------------------------

reject, corrected_p, _, _ = multipletests(
    p_values,
    alpha=ALPHA,
    method="fdr_bh"
)

for i, record in enumerate(records):

    record["adjusted_p_value"] = corrected_p[i]
    record["significant_at_0_05"] = bool(reject[i])

    if reject[i]:
        record["significance"] = "SIGNIFICANT"
    else:
        record["significance"] = "NOT_SIGNIFICANT"

result = pd.DataFrame(records)

result.to_csv(
    OUTPUT,
    index=False,
    float_format="%.6f"
)

# ------------------------------------------------------------
# Display
# ------------------------------------------------------------

print()
print("=== MANN-WHITNEY U TEST RESULTS ===")
print(result.to_string(index=False))

print()
print("=== SIGNIFICANCE SUMMARY ===")

for _, row in result.iterrows():

    print(
        f"{row['protocol']:3s} | "
        f"{row['network_profile']:15s} | "
        f"p={row['raw_p_value']:.6f} | "
        f"adjusted_p={row['adjusted_p_value']:.6f} | "
        f"{row['significance']}"
    )

print()
print(f"Tests performed: {len(result)}")
print(f"Alpha: {ALPHA}")
print(
    f"Significant after FDR correction: "
    f"{result['significant_at_0_05'].sum()}"
)
print(f"Output: {OUTPUT}")
print()
print("Statistical significance testing: PASS")
