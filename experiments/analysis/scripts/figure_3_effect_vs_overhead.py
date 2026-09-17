from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

RESULTS = Path("experiments/analysis/results")
PLOTS = Path("experiments/analysis/plots")
PLOTS.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RESULTS / "effect_size_analysis.csv")

plt.figure(figsize=(10, 6))

for protocol in ["TLS", "SSH"]:
    data = df[df["protocol"] == protocol]

    plt.scatter(
        data["rank_biserial_correlation"],
        data["median_overhead_pct"],
        label=protocol,
        s=70,
    )

    for _, row in data.iterrows():
        plt.annotate(
            row["network_profile"],
            (
                row["rank_biserial_correlation"],
                row["median_overhead_pct"],
            ),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=8,
        )

plt.axhline(0, linewidth=1)
plt.axvline(0, linewidth=1)

plt.xlabel("Rank-biserial correlation")
plt.ylabel("Median latency overhead (%)")
plt.title("Effect Size vs. Practical Latency Overhead")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

output = PLOTS / "figure_3_effect_vs_overhead.png"

plt.savefig(
    output,
    dpi=300,
    bbox_inches="tight",
)

plt.close()

print(f"Output: {output}")
print("Figure 3 generation: PASS")
