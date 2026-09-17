from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]

analysis = ROOT / "experiments/analysis/results"
output = ROOT / "experiments/migration_framework/results/evidence_model.csv"

comparison = pd.read_csv(analysis / "classical_vs_hybrid.csv")
significance = pd.read_csv(analysis / "significance_testing.csv")
effect = pd.read_csv(analysis / "effect_size_analysis.csv")

keys = ["protocol", "network_profile"]

df = comparison[keys + [
    "classical_n",
    "hybrid_n",
    "classical_median_us",
    "hybrid_median_us",
    "classical_p95_us",
    "hybrid_p95_us",
    "median_difference_us",
    "median_overhead_pct",
    "p95_difference_us",
    "p95_overhead_pct",
]].copy()

sig = significance[keys + [
    "raw_p_value",
    "adjusted_p_value",
    "significant_at_0_05",
]].copy()

eff = effect[keys + [
    "rank_biserial_correlation",
    "effect_category",
    "direction",
]].copy()

df = df.merge(sig, on=keys, how="inner")
df = df.merge(eff, on=keys, how="inner")

def classify_overhead(value):
    if value <= 0:
        return "No_positive_overhead_observed"
    if value < 5:
        return "Low"
    if value < 20:
        return "Moderate"
    if value < 50:
        return "High"
    return "Very_high"

def classify_evidence(row):
    significant = bool(row["significant_at_0_05"])
    effect_large = row["effect_category"] == "Large"
    positive = row["median_overhead_pct"] > 0

    if significant and effect_large and positive:
        return "Strong_positive_hybrid_latency_evidence"

    if significant and positive:
        return "Statistically_supported_positive_hybrid_latency_difference"

    if positive:
        return "Observed_positive_hybrid_latency_difference"

    if significant and not positive:
        return "Statistically_supported_non_positive_difference"

    return "No_statistically_supported_positive_difference"

df["median_overhead_class"] = df["median_overhead_pct"].apply(
    classify_overhead
)

df["evidence_classification"] = df.apply(
    classify_evidence,
    axis=1
)

df["performance_sensitive_condition"] = (
    (df["median_overhead_pct"] >= 20)
    | (df["p95_overhead_pct"] >= 20)
)

columns = [
    "protocol",
    "network_profile",
    "classical_n",
    "hybrid_n",
    "classical_median_us",
    "hybrid_median_us",
    "median_difference_us",
    "median_overhead_pct",
    "median_overhead_class",
    "classical_p95_us",
    "hybrid_p95_us",
    "p95_difference_us",
    "p95_overhead_pct",
    "raw_p_value",
    "adjusted_p_value",
    "significant_at_0_05",
    "rank_biserial_correlation",
    "effect_category",
    "direction",
    "performance_sensitive_condition",
    "evidence_classification",
]

df = df[columns].sort_values(
    ["protocol", "network_profile"]
).reset_index(drop=True)

output.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output, index=False)

print("=== MIGRATION EVIDENCE MODEL ===")
print(f"Comparisons: {len(df)}")
print(f"Output: {output}")
print(
    "Performance-sensitive conditions:",
    int(df["performance_sensitive_condition"].sum())
)
print(
    "Statistically significant comparisons:",
    int(df["significant_at_0_05"].sum())
)

if len(df) != 12:
    raise SystemExit("FAIL: expected 12 protocol/network comparisons")

required = [
    "median_overhead_pct",
    "p95_overhead_pct",
    "adjusted_p_value",
    "rank_biserial_correlation",
    "evidence_classification",
]

if not all(column in df.columns for column in required):
    raise SystemExit("FAIL: required evidence columns missing")

print("Evidence model: PASS")
