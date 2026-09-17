from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]

results = ROOT / "experiments/migration_framework/results"
plots = ROOT / "experiments/migration_framework/plots"

plots.mkdir(parents=True, exist_ok=True)

validation = pd.read_csv(results / "decision_validation.csv")
evidence = pd.read_csv(results / "evidence_model.csv")

# Figure 1 — Recommendation distribution
counts = validation["recommendation"].value_counts()

plt.figure(figsize=(9, 5))
counts.plot(kind="bar")
plt.xlabel("Migration Recommendation")
plt.ylabel("Number of Validated Scenarios")
plt.title("PQC Migration Framework Recommendation Distribution")
plt.xticks(rotation=25, ha="right")
plt.tight_layout()

fig1 = plots / "figure_1_recommendation_distribution.png"
plt.savefig(fig1, dpi=300)
plt.close()

# Figure 2 — Median hybrid overhead by protocol/network
plot_data = evidence.copy()
plot_data["condition"] = (
    plot_data["protocol"] + " — " + plot_data["network_profile"]
)

plt.figure(figsize=(11, 6))
plt.bar(
    plot_data["condition"],
    plot_data["median_overhead_pct"],
)
plt.axhline(0, linewidth=1)
plt.xlabel("Protocol and Network Profile")
plt.ylabel("Hybrid Median Latency Overhead (%)")
plt.title("Measured Hybrid Latency Overhead Used by Migration Framework")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

fig2 = plots / "figure_2_measured_overhead.png"
plt.savefig(fig2, dpi=300)
plt.close()

# Figure 3 — Decision framework architecture
fig, ax = plt.subplots(figsize=(12, 7))
ax.axis("off")

boxes = [
    (0.05, 0.70, "Deployment Inputs"),
    (0.38, 0.70, "Experimental Evidence"),
    (0.71, 0.70, "Decision Model"),
    (0.38, 0.30, "Migration Path"),
    (0.71, 0.30, "Deployment Review"),
]

for x, y, label in boxes:
    ax.text(
        x,
        y,
        label,
        ha="center",
        va="center",
        fontsize=14,
        bbox=dict(boxstyle="round,pad=0.6", fill=False),
    )

arrows = [
    ((0.16, 0.70), (0.31, 0.70)),
    ((0.49, 0.70), (0.64, 0.70)),
    ((0.71, 0.64), (0.49, 0.37)),
    ((0.55, 0.30), (0.68, 0.30)),
]

for start, end in arrows:
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops=dict(arrowstyle="->", linewidth=1.5),
    )

ax.text(
    0.05,
    0.55,
    "Security\nCompatibility\nPerformance\nUrgency",
    ha="center",
    va="center",
    fontsize=11,
)

ax.text(
    0.38,
    0.55,
    "Latency\nP95\nSignificance\nEffect size",
    ha="center",
    va="center",
    fontsize=11,
)

ax.text(
    0.71,
    0.55,
    "Classical\nHybrid\nPQC",
    ha="center",
    va="center",
    fontsize=11,
)

ax.text(
    0.38,
    0.15,
    "Direct PQC\nHybrid transition\nPerformance evaluation",
    ha="center",
    va="center",
    fontsize=11,
)

ax.text(
    0.71,
    0.15,
    "Application testing\nSecurity review\nProduction decision",
    ha="center",
    va="center",
    fontsize=11,
)

ax.set_title(
    "PQC-Migrate Evidence-Based Migration Framework",
    fontsize=16,
    pad=20,
)

fig3 = plots / "figure_3_framework_architecture.png"
plt.savefig(fig3, dpi=300, bbox_inches="tight")
plt.close()

print("=== MIGRATION FRAMEWORK FIGURES ===")
print(f"Figure 1: {fig1}")
print(f"Figure 2: {fig2}")
print(f"Figure 3: {fig3}")

for figure in [fig1, fig2, fig3]:
    if not figure.exists() or figure.stat().st_size == 0:
        raise SystemExit(f"FAIL: missing figure {figure}")

print("Framework visualization: PASS")
