from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

RESULTS = Path("experiments/analysis/results")
PLOTS = Path("experiments/analysis/plots")
PLOTS.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RESULTS / "classical_vs_hybrid.csv")

profiles = [
    "baseline",
    "latency100",
    "latency200",
    "bandwidth1mbps",
    "loss1",
    "mobile",
]

profile_labels = {
    "baseline": "Baseline",
    "latency100": "100 ms latency",
    "latency200": "200 ms latency",
    "bandwidth1mbps": "1 Mbps",
    "loss1": "1% loss",
    "mobile": "Mobile",
}

for protocol in ["TLS", "SSH"]:
    data = df[df["protocol"] == protocol].copy()

    data["network_profile"] = pd.Categorical(
        data["network_profile"],
        categories=profiles,
        ordered=True,
    )

    data = data.sort_values("network_profile")

    labels = [profile_labels[p] for p in data["network_profile"]]

    plt.figure(figsize=(10, 6))

    plt.bar(
        labels,
        data["median_overhead_pct"],
    )

    plt.axhline(
        0,
        linewidth=1,
    )

    plt.xlabel("Network condition")
    plt.ylabel("Hybrid median latency overhead (%)")
    plt.title(f"{protocol}: Hybrid PQC Latency Overhead")
    plt.xticks(rotation=20, ha="right")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    output = PLOTS / f"figure_2_{protocol.lower()}_hybrid_overhead.png"

    plt.savefig(
        output,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print(f"{protocol}: {output}")

print()
print("Figure 2 generation: PASS")
