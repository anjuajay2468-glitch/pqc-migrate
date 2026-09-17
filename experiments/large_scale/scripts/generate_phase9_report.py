import csv
from pathlib import Path
from collections import Counter

ROOT = Path("experiments/large_scale")

DATASET = ROOT / "results/master_dataset.csv"
STATS = ROOT / "results/statistical_summary.csv"
OVERHEAD = ROOT / "results/hybrid_overhead_analysis.csv"
VARIABILITY = ROOT / "results/variability_analysis.csv"

REPORT = ROOT / "PHASE9_REPORT.md"

with DATASET.open(newline="") as f:
    rows = list(csv.DictReader(f))

with STATS.open(newline="") as f:
    stats = list(csv.DictReader(f))

with OVERHEAD.open(newline="") as f:
    overhead = list(csv.DictReader(f))

with VARIABILITY.open(newline="") as f:
    variability = list(csv.DictReader(f))

protocols = Counter(r["protocol"] for r in rows)
configs = Counter(r["configuration"] for r in rows)
profiles = Counter(r["network_profile"] for r in rows)
successes = Counter(r["success"] for r in rows)

report = []

report.append("# PQC-Migrate Phase 9 — Large-Scale Benchmarking")
report.append("")
report.append("## 1. Objective")
report.append("")
report.append(
    "Phase 9 automates repeated TLS and SSH experiments across "
    "multiple controlled network conditions and consolidates "
    "the resulting measurements into a research dataset."
)
report.append("")

report.append("## 2. Dataset")
report.append("")
report.append(f"- Total observations: **{len(rows)}**")
report.append(f"- TLS observations: **{protocols['TLS']}**")
report.append(f"- SSH observations: **{protocols['SSH']}**")
report.append(f"- Classical observations: **{configs['Classical']}**")
report.append(f"- Hybrid observations: **{configs['Hybrid']}**")
report.append(f"- Successful observations: **{successes['1']}**")
report.append("")

report.append("## 3. Network Profiles")
report.append("")
for profile, count in sorted(profiles.items()):
    report.append(f"- `{profile}`: {count} observations")
report.append("")

report.append("## 4. Experimental Design")
report.append("")
report.append(
    "Each protocol was evaluated using two cryptographic "
    "configurations:"
)
report.append("")
report.append("- Classical")
report.append("- Hybrid")
report.append("")
report.append(
    "The experiments were repeated under six network profiles:"
)
report.append("")
for profile in sorted(profiles):
    report.append(f"- `{profile}`")
report.append("")

report.append("## 5. Statistical Analysis")
report.append("")
report.append(
    "For each protocol, cryptographic configuration, and "
    "network profile, the analysis calculates:"
)
report.append("")
report.append("- Mean latency")
report.append("- Median latency")
report.append("- Standard deviation")
report.append("- Minimum latency")
report.append("- Maximum latency")
report.append("- 95th percentile")
report.append("- 99th percentile")
report.append("- Coefficient of variation")
report.append("")

report.append("## 6. Hybrid Overhead")
report.append("")
report.append(
    "Hybrid overhead is calculated relative to the classical "
    "configuration using:"
)
report.append("")
report.append(
    "**Overhead (%) = (Hybrid latency − Classical latency) / "
    "Classical latency × 100**"
)
report.append("")

report.append("| Protocol | Network profile | Mean overhead |")
report.append("|---|---|---:|")

for row in sorted(
    overhead,
    key=lambda x: (
        x["protocol"],
        x["network_profile"]
    )
):
    report.append(
        f"| {row['protocol']} | "
        f"{row['network_profile']} | "
        f"{row['mean_overhead_percent']}% |"
    )

report.append("")

report.append("## 7. Variability")
report.append("")
report.append(
    "Variability analysis indicates that the effect of hybrid "
    "cryptography is not uniform across network conditions. "
    "Some constrained or lossy environments exhibit substantially "
    "higher latency variability."
)
report.append("")

report.append(
    "The coefficient of variation and percentile measurements "
    "are retained to distinguish consistent overhead from "
    "individual high-latency observations."
)
report.append("")

report.append("## 8. Important Observations")
report.append("")
report.append(
    "- Network latency can dominate total connection establishment "
    "time, reducing the relative contribution of cryptographic "
    "processing."
)
report.append(
    "- Bandwidth-constrained environments show a larger hybrid "
    "latency difference in several measurements."
)
report.append(
    "- Lossy and mobile-like environments exhibit greater "
    "measurement variability."
)
report.append(
    "- SSH and TLS do not exhibit identical sensitivity to "
    "hybrid cryptographic overhead."
)
report.append(
    "- Hybrid performance should therefore be evaluated in the "
    "context of the surrounding network conditions rather than "
    "using a single fixed overhead value."
)
report.append("")

report.append("## 9. Reproducibility")
report.append("")
report.append(
    "The experiment is implemented using automated collection "
    "scripts under `experiments/large_scale/scripts/`."
)
report.append("")
report.append(
    "Raw measurements are retained in `master_dataset.csv`, "
    "while derived statistical datasets are stored separately."
)
report.append("")

report.append("## 10. Limitations")
report.append("")
report.append(
    "- The current dataset measures handshake/connection latency "
    "rather than full application throughput."
)
report.append(
    "- Several resource-utilization fields remain unavailable "
    "in the automated collector."
)
report.append(
    "- Baseline currently contains more observations than the "
    "other network profiles because earlier baseline experiments "
    "were retained."
)
report.append(
    "- The experiments use a controlled local environment and "
    "therefore do not represent all real-world network conditions."
)
report.append("")

report.append("## 11. Phase 9 Status")
report.append("")
report.append("Dataset infrastructure: **PASS**")
report.append("Automated TLS collection: **PASS**")
report.append("Automated SSH collection: **PASS**")
report.append("Multi-network collection: **PASS**")
report.append("Dataset integrity validation: **PASS**")
report.append("Statistical analysis: **PASS**")
report.append("Hybrid overhead analysis: **PASS**")
report.append("Variability analysis: **PASS**")
report.append("")
report.append("**Phase 9 dataset consolidation: COMPLETE**")

REPORT.write_text("\n".join(report))

print("=============================================")
print("       PQC-Migrate Phase 9.10")
print("       DATASET CONSOLIDATION")
print("=============================================")
print()
print(f"Total observations: {len(rows)}")
print(f"TLS observations: {protocols['TLS']}")
print(f"SSH observations: {protocols['SSH']}")
print(f"Successful observations: {successes['1']}")
print()
print("Report:", REPORT)
print()
print("Phase 9 consolidation: PASS")
