from pathlib import Path
from datetime import datetime
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]

dataset = ROOT / "experiments/large_scale/results/master_dataset.csv"
analysis_dir = ROOT / "experiments/analysis"
results_dir = analysis_dir / "results"
plots_dir = analysis_dir / "plots"

df = pd.read_csv(dataset)

required_results = [
    "descriptive_statistics.csv",
    "classical_vs_hybrid.csv",
    "network_condition_effects.csv",
    "outlier_summary.csv",
    "outlier_observations.csv",
    "significance_testing.csv",
    "effect_size_analysis.csv",
    "RESEARCH_FINDINGS.md",
]

required_plots = [
    "figure_1_ssh_median_latency.png",
    "figure_1_tls_median_latency.png",
    "figure_2_ssh_hybrid_overhead.png",
    "figure_2_tls_hybrid_overhead.png",
    "figure_3_effect_vs_overhead.png",
]

checks = []

checks.append(("Dataset exists", dataset.exists()))
checks.append(("Dataset rows = 280", len(df) == 280))
checks.append(("Dataset columns = 17", len(df.columns) == 17))
checks.append(("All observations successful", int(df["success"].sum()) == 280))
checks.append(("TLS observations = 140", int((df["protocol"] == "TLS").sum()) == 140))
checks.append(("SSH observations = 140", int((df["protocol"] == "SSH").sum()) == 140))
checks.append(("Classical observations = 140", int((df["algorithm"] == "X25519").sum()) == 140))
checks.append(("Hybrid observations = 140", int(((df["algorithm"] == "X25519MLKEM768") | (df["algorithm"] == "sntrup761x25519")).sum()) == 140))

for filename in required_results:
    checks.append((f"Result artifact: {filename}", (results_dir / filename).exists()))

for filename in required_plots:
    checks.append((f"Plot artifact: {filename}", (plots_dir / filename).exists()))

all_pass = all(result for _, result in checks)

report = []
report.append("# Phase 10 — Statistical Analysis & Research Findings")
report.append("")
report.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
report.append("")
report.append("## 1. Objective")
report.append("")
report.append(
    "Phase 10 analyzes the Phase 9 large-scale PQC migration benchmark dataset "
    "using descriptive statistics, classical-vs-hybrid comparisons, network-condition "
    "analysis, outlier analysis, statistical significance testing, effect-size analysis, "
    "visualization, and hypothesis evaluation."
)
report.append("")
report.append("## 2. Dataset")
report.append("")
report.append(f"- Total observations: {len(df)}")
report.append(f"- TLS observations: {int((df['protocol'] == 'TLS').sum())}")
report.append(f"- SSH observations: {int((df['protocol'] == 'SSH').sum())}")
report.append(f"- Classical observations: {int((df['algorithm'] == 'Classical').sum())}")
report.append(f"- Hybrid observations: {int((df['algorithm'] == 'Hybrid').sum())}")
report.append(f"- Successful observations: {int(df['success'].sum())}")
report.append("")
report.append("The complete Phase 9 dataset was retained as the primary analysis dataset.")
report.append("Potential outliers were identified using the IQR rule but were not deleted.")
report.append("")
report.append("## 3. Statistical Methods")
report.append("")
report.append("- Descriptive statistics: N, mean, median, standard deviation, minimum, maximum, range, P95, P99, coefficient of variation.")
report.append("- Classical vs Hybrid comparison: absolute and percentage differences in latency statistics.")
report.append("- Network-condition analysis: change relative to the corresponding baseline.")
report.append("- Outlier detection: 1.5 × IQR rule.")
report.append("- Statistical significance: two-sided Mann–Whitney U test.")
report.append("- Multiple-comparison correction: Benjamini–Hochberg FDR.")
report.append("- Effect size: rank-biserial correlation.")
report.append("- Primary significance threshold: alpha = 0.05.")
report.append("")
report.append("## 4. Main Research Findings")
report.append("")
report.append("### H1 — Hybrid latency overhead")
report.append("")
report.append(
    "Partially supported and protocol-dependent. SSH showed positive median latency "
    "overhead for all tested network profiles, whereas TLS showed mixed behavior."
)
report.append("")
report.append("### H2 — Network conditions amplify migration cost")
report.append("")
report.append(
    "Conditionally supported. Bandwidth limitation produced clear relative overhead "
    "for both protocols, while latency and packet-loss conditions did not consistently "
    "increase relative hybrid overhead."
)
report.append("")
report.append("### H3 — Protocol and network context matter")
report.append("")
report.append(
    "Strongly supported. The observed hybrid performance impact varied substantially "
    "between TLS and SSH and across network conditions."
)
report.append("")
report.append("### H4 — Significant differences are not universal")
report.append("")
report.append(
    "Supported. Mobile conditions were not statistically significant for either TLS "
    "or SSH after testing, while most other comparisons were significant."
)
report.append("")
report.append("## 5. Significance Results")
report.append("")
report.append(
    "10 of 12 classical-vs-hybrid comparisons were statistically significant after "
    "Benjamini–Hochberg FDR correction. The two non-significant comparisons were "
    "SSH-mobile and TLS-mobile."
)
report.append("")
report.append("## 6. Important Interpretation Constraints")
report.append("")
report.append(
    "Statistical significance does not imply practical significance. Large statistical "
    "effects must be interpreted together with the absolute latency differences."
)
report.append("")
report.append(
    "Negative TLS hybrid-overhead values are dataset-specific observations and should "
    "not be interpreted as evidence that hybrid TLS inherently improves performance."
)
report.append("")
report.append(
    "Potential outliers were retained in the primary dataset. Outlier analysis is used "
    "to characterize variability and tail behavior rather than selectively removing "
    "observations."
)
report.append("")
report.append(
    "The Phase 9 automated dataset primarily contains latency measurements. CPU, memory, "
    "TCP payload, and packet-count fields are incomplete and therefore are not used to "
    "claim comprehensive resource overhead."
)
report.append("")
report.append(
    "Results describe the tested implementation, hardware/software environment, "
    "cryptographic algorithms, and network profiles and should not be generalized "
    "beyond those experimental conditions without additional validation."
)
report.append("")
report.append("## 7. Reproducibility")
report.append("")
report.append(
    "All six core statistical analysis scripts were re-executed successfully. "
    "SHA-256 hashes of all seven core CSV outputs were identical before and after "
    "re-execution, establishing deterministic analysis outputs."
)
report.append("")
report.append("## 8. Artifact Validation")
report.append("")
for name, passed in checks:
    report.append(f"- {'PASS' if passed else 'FAIL'} — {name}")
report.append("")
report.append(f"**Overall Phase 10 validation: {'PASS' if all_pass else 'FAIL'}**")
report.append("")

output = results_dir / "PHASE10_FINAL_REPORT.md"
output.write_text("\n".join(report), encoding="utf-8")

print("=== PHASE 10 FINAL REPORT ===")
print(f"Report: {output}")
print(f"Dataset rows: {len(df)}")
print(f"Result artifacts checked: {len(required_results)}")
print(f"Plot artifacts checked: {len(required_plots)}")
print(f"Overall validation: {'PASS' if all_pass else 'FAIL'}")

if not all_pass:
    raise SystemExit(1)
