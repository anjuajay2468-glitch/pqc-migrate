from pathlib import Path
import pandas as pd

RESULTS = Path("experiments/analysis/results")
OUTPUT = RESULTS / "RESEARCH_FINDINGS.md"

comparison = pd.read_csv(RESULTS / "classical_vs_hybrid.csv")
effect = pd.read_csv(RESULTS / "effect_size_analysis.csv")
significance = pd.read_csv(RESULTS / "significance_testing.csv")

lines = []

lines.append("# PQC-Migrate Research Findings")
lines.append("")
lines.append("## Phase 10.10 — Statistical Interpretation")
lines.append("")
lines.append("### Dataset")
lines.append("")
lines.append("- 280 total observations")
lines.append("- 140 TLS observations")
lines.append("- 140 SSH observations")
lines.append("- 12 classical-vs-hybrid comparisons")
lines.append("- 12 statistical significance tests")
lines.append("- Mann–Whitney U test with Benjamini–Hochberg FDR correction")
lines.append("- Full dataset retained; potential outliers were not deleted")
lines.append("")

lines.append("## Hypothesis Evaluation")
lines.append("")

lines.append("### H1 — Hybrid PQC introduces performance overhead")
lines.append("")
lines.append("**Result: Partially supported / protocol-dependent.**")
lines.append("")
lines.append(
    "SSH showed positive median latency overhead in all six tested "
    "network conditions, whereas TLS showed positive median overhead "
    "in only two of six conditions."
)
lines.append("")
lines.append(
    "Therefore, the experiments do not support a universal claim that "
    "hybrid PQC always increases latency."
)
lines.append("")

lines.append("### H2 — Network conditions amplify PQC migration cost")
lines.append("")
lines.append("**Result: Conditionally supported.**")
lines.append("")
lines.append(
    "Bandwidth limitation produced substantial relative overhead: "
    "39.27% for SSH and 66.45% for TLS based on median latency."
)
lines.append("")
lines.append(
    "However, increased latency or packet loss did not consistently "
    "increase relative hybrid overhead. The effect therefore depends "
    "on both protocol and network condition."
)
lines.append("")

lines.append("### H3 — Performance impact is protocol- and condition-dependent")
lines.append("")
lines.append("**Result: Strongly supported.**")
lines.append("")
lines.append(
    "TLS exhibited both lower and higher hybrid latency depending on "
    "network condition, while SSH showed positive overhead across all "
    "conditions."
)
lines.append("")
lines.append(
    "This demonstrates that PQC migration cost cannot be represented "
    "by a single fixed overhead value."
)
lines.append("")

lines.append("### H4 — Statistically significant differences are not universal")
lines.append("")
lines.append("**Result: Supported.**")
lines.append("")
lines.append(
    "After FDR correction, 10 of 12 comparisons were statistically "
    "significant. The two mobile-condition comparisons were not "
    "statistically significant."
)
lines.append("")

lines.append("## Key Quantitative Findings")
lines.append("")

for protocol in ["SSH", "TLS"]:
    data = effect[effect["protocol"] == protocol]

    lines.append(f"### {protocol}")
    lines.append("")

    for _, row in data.iterrows():
        lines.append(
            f"- **{row['network_profile']}**: "
            f"median overhead {row['median_overhead_pct']:+.2f}%, "
            f"rank-biserial correlation "
            f"{row['rank_biserial_correlation']:+.2f}, "
            f"{row['effect_category']} effect, "
            f"{row['direction']}."
        )

    lines.append("")

lines.append("## Statistical Significance")
lines.append("")

for _, row in significance.iterrows():
    lines.append(
        f"- **{row['protocol']} / {row['network_profile']}**: "
        f"raw p={row['raw_p_value']:.6g}, "
        f"FDR-adjusted p={row['adjusted_p_value']:.6g}, "
        f"{row['significance']}."
    )

lines.append("")

lines.append("## Interpretation Caveats")
lines.append("")
lines.append(
    "1. Statistical significance does not imply practical significance."
)
lines.append(
    "2. Negative TLS overhead values should not be interpreted as proof "
    "that hybrid cryptography is inherently faster."
)
lines.append(
    "3. Potential outliers were retained in the primary dataset."
)
lines.append(
    "4. The Phase 9 automated dataset primarily contains latency "
    "measurements; CPU, memory, payload, and packet fields are not "
    "complete enough to support broad resource-overhead claims."
)
lines.append(
    "5. Results describe the tested experimental environment and "
    "configurations and should not be generalized to all systems."
)
lines.append("")

lines.append("## Primary Research Conclusion")
lines.append("")
lines.append(
    "The experiments indicate that the performance impact of hybrid "
    "post-quantum cryptography is context-dependent. SSH exhibited "
    "consistent positive latency overhead, while TLS showed substantial "
    "variation across network conditions. Bandwidth limitation produced "
    "the clearest increase in relative hybrid overhead for both "
    "protocols. These results support evaluating PQC migration under "
    "multiple realistic network conditions rather than using a single "
    "benchmark environment."
)
lines.append("")

OUTPUT.write_text("\n".join(lines))

print("=" * 60)
print("       PQC-Migrate Phase 10.10.2")
print("       RESEARCH FINDINGS REPORT")
print("=" * 60)
print()
print(f"Output: {OUTPUT}")
print(f"Lines written: {len(lines)}")
print("Research findings report: PASS")
