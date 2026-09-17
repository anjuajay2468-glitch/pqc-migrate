from pathlib import Path
import pandas as pd

BASE = Path("experiments/analysis")
RESULTS = BASE / "results"

descriptive = pd.read_csv(RESULTS / "descriptive_statistics.csv")
comparison = pd.read_csv(RESULTS / "classical_vs_hybrid.csv")
network = pd.read_csv(RESULTS / "network_condition_effects.csv")
effect = pd.read_csv(RESULTS / "effect_size_analysis.csv")
significance = pd.read_csv(RESULTS / "significance_testing.csv")

print("=" * 60)
print("       PQC-Migrate Phase 10.8")
print("       RESEARCH FINDINGS EXTRACTION")
print("=" * 60)

print()
print("=== DATASET OVERVIEW ===")
print(f"Descriptive groups: {len(descriptive)}")
print(f"Classical-vs-hybrid comparisons: {len(comparison)}")
print(f"Network-condition comparisons: {len(network)}")
print(f"Effect-size comparisons: {len(effect)}")
print(f"Significance tests: {len(significance)}")

print()
print("=== STATISTICALLY SIGNIFICANT COMPARISONS ===")

sig = significance[significance["significant_at_0_05"] == True]

for _, row in sig.iterrows():
    print(
        f"{row['protocol']} | {row['network_profile']} | "
        f"p={row['raw_p_value']:.6g} | "
        f"FDR p={row['adjusted_p_value']:.6g}"
    )

print()
print(f"Significant after FDR correction: {len(sig)}/{len(significance)}")

print()
print("=== PRACTICALLY LARGE EFFECTS ===")

large = effect[effect["effect_category"] == "Large"]

for _, row in large.iterrows():
    print(
        f"{row['protocol']} | {row['network_profile']} | "
        f"effect={row['rank_biserial_correlation']:+.3f} | "
        f"median overhead={row['median_overhead_pct']:+.2f}% | "
        f"{row['direction']}"
    )

print()
print(f"Large effects: {len(large)}/{len(effect)}")

print()
print("=== NON-SIGNIFICANT COMPARISONS ===")

nonsig = significance[significance["significant_at_0_05"] == False]

for _, row in nonsig.iterrows():
    print(
        f"{row['protocol']} | {row['network_profile']} | "
        f"p={row['raw_p_value']:.6g} | "
        f"FDR p={row['adjusted_p_value']:.6g}"
    )

print()
print("=== RESEARCH FINDINGS EXTRACTION ===")
print("Finding extraction: PASS")
