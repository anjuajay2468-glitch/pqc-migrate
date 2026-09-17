import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import mannwhitneyu

# ============================================================
# PQC-Migrate Phase 10.7
# Effect Size & Practical Significance
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATASET = PROJECT_ROOT / "experiments/large_scale/results/master_dataset.csv"
OUTPUT = PROJECT_ROOT / "experiments/analysis/results/effect_size_analysis.csv"

print("=" * 60)
print("       PQC-Migrate Phase 10.7")
print("       EFFECT SIZE & PRACTICAL SIGNIFICANCE")
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

        # ----------------------------------------------------
        # Mann-Whitney U
        # ----------------------------------------------------

        u_stat, p_value = mannwhitneyu(
            classical,
            hybrid,
            alternative="two-sided"
        )

        # ----------------------------------------------------
        # Rank-biserial correlation
        #
        # Positive value = hybrid tends to be slower
        # Negative value = hybrid tends to be faster
        # ----------------------------------------------------

        n1 = len(classical)
        n2 = len(hybrid)

        rank_biserial = (
            (2 * u_stat) / (n1 * n2)
        ) - 1

        # ----------------------------------------------------
        # Descriptive values
        # ----------------------------------------------------

        classical_mean = np.mean(classical)
        hybrid_mean = np.mean(hybrid)

        classical_median = np.median(classical)
        hybrid_median = np.median(hybrid)

        mean_difference = hybrid_mean - classical_mean

        mean_overhead_pct = (
            mean_difference /
            classical_mean
        ) * 100

        median_difference = (
            hybrid_median -
            classical_median
        )

        median_overhead_pct = (
            median_difference /
            classical_median
        ) * 100

        # ----------------------------------------------------
        # Effect-size interpretation
        # ----------------------------------------------------

        magnitude = abs(rank_biserial)

        if magnitude < 0.10:
            effect_category = "Negligible"
        elif magnitude < 0.30:
            effect_category = "Small"
        elif magnitude < 0.50:
            effect_category = "Medium"
        else:
            effect_category = "Large"

        # ----------------------------------------------------
        # Direction
        # ----------------------------------------------------

        if rank_biserial > 0:
            direction = "Hybrid lower latency"
        elif rank_biserial < 0:
            direction = "Hybrid higher latency"
        else:
            direction = "No directional difference"

        records.append({
            "protocol": protocol,
            "network_profile": profile,
            "classical_n": n1,
            "hybrid_n": n2,
            "classical_mean_us": classical_mean,
            "hybrid_mean_us": hybrid_mean,
            "mean_difference_us": mean_difference,
            "mean_overhead_pct": mean_overhead_pct,
            "classical_median_us": classical_median,
            "hybrid_median_us": hybrid_median,
            "median_difference_us": median_difference,
            "median_overhead_pct": median_overhead_pct,
            "u_statistic": u_stat,
            "p_value": p_value,
            "rank_biserial_correlation": rank_biserial,
            "effect_magnitude": magnitude,
            "effect_category": effect_category,
            "direction": direction
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
    ["protocol", "network_profile"]
)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

result.to_csv(
    OUTPUT,
    index=False,
    float_format="%.6f"
)

print()
print("=== EFFECT SIZE RESULTS ===")
print(result.to_string(index=False))

print()
print("=== EFFECT SIZE SUMMARY ===")

for _, row in result.iterrows():

    print(
        f"{row['protocol']:3s} | "
        f"{row['network_profile']:15s} | "
        f"effect={row['rank_biserial_correlation']:+.3f} | "
        f"{row['effect_category']:10s} | "
        f"median overhead={row['median_overhead_pct']:+.2f}% | "
        f"{row['direction']}"
    )

print()
print(f"Comparisons analyzed: {len(result)}")
print(f"Output: {OUTPUT}")
print()
print("Effect size analysis: PASS")
