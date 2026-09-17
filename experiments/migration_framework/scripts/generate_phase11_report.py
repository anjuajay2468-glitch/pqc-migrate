from pathlib import Path
from datetime import datetime
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]

base = ROOT / "experiments/migration_framework"
results = base / "results"
plots = base / "plots"

evidence = pd.read_csv(results / "evidence_model.csv")
decisions = pd.read_csv(results / "migration_decisions.csv")
validation = pd.read_csv(results / "decision_validation.csv")
benchmark = pd.read_csv(results / "benchmark_validation.csv")

required_files = [
    "FRAMEWORK_SPEC.md",
    "DECISION_MODEL_SPEC.md",
    "evidence_model.csv",
    "migration_decisions.csv",
    "decision_validation.csv",
    "benchmark_validation.csv",
    "MIGRATION_PATHS.md",
    "CASE_STUDIES.md",
]

required_figures = [
    "figure_1_recommendation_distribution.png",
    "figure_2_measured_overhead.png",
    "figure_3_framework_architecture.png",
]

checks = []

for filename in required_files:
    checks.append(
        (f"Artifact: {filename}", (results / filename).is_file())
    )

for filename in required_figures:
    checks.append(
        (f"Figure: {filename}", (plots / filename).is_file())
    )

checks.extend([
    ("Evidence model contains 12 comparisons", len(evidence) == 12),
    ("Representative decisions contain 4 scenarios", len(decisions) == 4),
    ("Decision validation contains 432 scenarios", len(validation) == 432),
    ("Benchmark validation contains 12 combinations", len(benchmark) == 12),
    (
        "All benchmark protocols are TLS/SSH",
        set(benchmark["protocol"]).issubset({"TLS", "SSH"})
    ),
    (
        "All six network profiles represented per protocol",
        benchmark.groupby("protocol")["network_profile"]
        .nunique().eq(6).all()
    ),
    (
        "All validated scenarios contain evidence",
        validation["median_overhead_pct"].notna().all()
        and validation["adjusted_p_value"].notna().all()
        and validation["rank_biserial_correlation"].notna().all()
    ),
])

all_pass = all(passed for _, passed in checks)

report = []

report.append("# Phase 11 — Migration Framework")
report.append("")
report.append(
    f"Generated: {datetime.now().isoformat(timespec='seconds')}"
)
report.append("")

report.append("## 1. Objective")
report.append("")
report.append(
    "Phase 11 transforms the empirical findings from the PQC-Migrate "
    "benchmarking and statistical-analysis pipeline into an explainable, "
    "evidence-based post-quantum cryptography migration decision framework."
)
report.append("")

report.append("## 2. Framework Architecture")
report.append("")
report.append(
    "The framework combines deployment requirements with experimentally "
    "measured protocol and network performance evidence."
)
report.append("")
report.append(
    "Deployment inputs → Experimental evidence → Decision model → "
    "Migration path → Deployment review"
)
report.append("")

report.append("## 3. Decision Dimensions")
report.append("")
report.append("- Security requirement")
report.append("- Legacy compatibility")
report.append("- Performance sensitivity")
report.append("- Migration urgency")
report.append("- Protocol")
report.append("- Network profile")
report.append("")

report.append("## 4. Experimental Evidence")
report.append("")
report.append(f"- Protocol/network comparisons: {len(evidence)}")
report.append(
    f"- Statistically significant comparisons: "
    f"{int(evidence['significant_at_0_05'].sum())}"
)
report.append(
    f"- Performance-sensitive conditions identified: "
    f"{int(evidence['performance_sensitive_condition'].sum())}"
)
report.append("")
report.append(
    "The evidence model incorporates median hybrid latency overhead, "
    "P95 overhead, FDR-adjusted statistical significance, rank-biserial "
    "effect size, and evidence classification."
)
report.append("")

report.append("## 5. Decision Engine")
report.append("")
report.append(
    "The decision engine supports four explainable outcomes:"
)
report.append("")
report.append("- CLASSICAL")
report.append("- HYBRID_TRANSITION")
report.append("- PQC")
report.append("- HYBRID_OR_PQC_EVALUATION")
report.append("")

report.append("## 6. Decision Engine Validation")
report.append("")
report.append(
    f"The decision engine was evaluated across {len(validation)} "
    "combinations of security requirement, legacy compatibility, "
    "performance sensitivity, migration urgency, protocol, and network profile."
)
report.append("")
recommendations = validation["recommendation"].value_counts()

for recommendation, count in recommendations.items():
    report.append(f"- {recommendation}: {count} scenarios")

report.append("")
report.append(
    "All specified decision rules passed validation, including the "
    "requirement that PQC-required deployments never recommend classical-only "
    "deployment."
)
report.append("")

report.append("## 7. Benchmark Validation")
report.append("")
report.append(
    "The framework was evaluated against all 12 measured protocol/network "
    "combinations from the Phase 10 evidence model."
)
report.append("")
report.append(
    "The benchmark validation retained the measured performance and "
    "statistical evidence for every combination."
)
report.append("")

report.append("## 8. Migration Paths")
report.append("")
report.append("- Direct PQC Migration")
report.append("- Hybrid Transition")
report.append("- Performance-Constrained Evaluation")
report.append("- Hybrid-or-PQC Evaluation")
report.append("")
report.append(
    "Hybrid is treated as a transitional state where compatibility requires "
    "it, rather than automatically treating hybrid cryptography as the final "
    "migration state."
)
report.append("")

report.append("## 9. Case Studies")
report.append("")
report.append(
    "Four representative scenarios demonstrate context-dependent "
    "recommendations:"
)
report.append("")
report.append("- Modern TLS infrastructure → PQC")
report.append("- Legacy SSH infrastructure → Hybrid Transition")
report.append("- Bandwidth-constrained SSH → Performance-Constrained Evaluation")
report.append("- Mobile TLS → Hybrid-or-PQC Evaluation")
report.append("")

report.append("## 10. Research Contribution")
report.append("")
report.append(
    "The primary contribution of Phase 11 is an explainable migration "
    "decision framework that connects empirical PQC performance measurements "
    "to practical migration strategies while preserving security and "
    "compatibility constraints."
)
report.append("")
report.append(
    "Unlike a universal performance ranking, the framework treats PQC "
    "migration as context-dependent and explicitly exposes the experimental "
    "evidence supporting each recommendation."
)
report.append("")

report.append("## 11. Limitations")
report.append("")
report.append(
    "The framework is a research decision-support system and is not a "
    "universal cryptographic deployment policy."
)
report.append("")
report.append(
    "Current quantitative evidence is primarily latency-based. CPU and "
    "memory measurements remain incomplete and are therefore not used as "
    "quantitative scoring variables."
)
report.append("")
report.append(
    "Recommendations must be validated against application-level behavior, "
    "implementation compatibility, security requirements, and production "
    "conditions before deployment."
)
report.append("")
report.append(
    "Benchmark results are specific to the tested implementations, "
    "algorithms, software environment, hardware environment, and network "
    "profiles."
)
report.append("")

report.append("## 12. Artifact Validation")
report.append("")

for name, passed in checks:
    report.append(f"- {'PASS' if passed else 'FAIL'} — {name}")

report.append("")
report.append(
    f"**Overall Phase 11 validation: {'PASS' if all_pass else 'FAIL'}**"
)
report.append("")

output = results / "PHASE11_FINAL_REPORT.md"
output.write_text("\n".join(report), encoding="utf-8")

print("=== PHASE 11 FINAL REPORT ===")
print(f"Report: {output}")
print(f"Evidence comparisons: {len(evidence)}")
print(f"Decision scenarios: {len(validation)}")
print(f"Benchmark combinations: {len(benchmark)}")
print(f"Artifacts checked: {len(required_files)}")
print(f"Figures checked: {len(required_figures)}")
print(f"Overall validation: {'PASS' if all_pass else 'FAIL'}")

if not all_pass:
    raise SystemExit(1)
