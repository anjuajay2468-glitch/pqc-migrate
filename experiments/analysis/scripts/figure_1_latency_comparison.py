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

    x = range(len(data))

    plt.figure(figsize=(10, 6))

    plt.plot(
        x,
        data["classical_median_us"] / 1000,
        marker="o",
        label="Classical",
    )

    plt.plot(
        x,
        data["hybrid_median_us"] / 1000,
        marker="o",
        label="Hybrid",
    )

    plt.xticks(
        list(x),
        [profile_labels[p] for p in data["network_profile"]],
        rotation=20,
        ha="right",
    )

    plt.xlabel("Network condition")
    plt.ylabel("Median latency (ms)")
    plt.title(f"{protocol}: Classical vs Hybrid Median Latency")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output = PLOTS / f"figure_1_{protocol.lower()}_median_latency.png"
    plt.savefig(output, dpi=300)
    plt.close()

    print(f"{protocol}: {output}")

print()
print("Figure 1 generation: PASS")
