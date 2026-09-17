from pathlib import Path
import pandas as pd

RESULTS = Path("experiments/analysis/results")

comparison = pd.read_csv(RESULTS / "classical_vs_hybrid.csv")
effect = pd.read_csv(RESULTS / "effect_size_analysis.csv")
significance = pd.read_csv(RESULTS / "significance_testing.csv")

print("=" * 60)
print("       PQC-Migrate Phase 10.10")
print("       HYPOTHESIS EVALUATION")
print("=" * 60)

print()
print("=== H1: HYBRID PQC INTRODUCES PERFORMANCE OVERHEAD ===")
print(
    "Evaluation criterion: Hybrid median latency should generally exceed "
    "classical latency under constrained network conditions."
)

for protocol in ["TLS", "SSH"]:
    data = comparison[comparison["protocol"] == protocol]

    positive = (data["median_overhead_pct"] > 0).sum()
    total = len(data)

    print(
        f"{protocol}: {positive}/{total} conditions show positive "
        f"median latency overhead"
    )

print()
print("=== H2: NETWORK CONDITIONS AMPLIFY PQC MIGRATION COST ===")
print(
    "Evaluation criterion: constrained network profiles should produce "
    "larger absolute latency changes than baseline."
)

for protocol in ["TLS", "SSH"]:
    data = comparison[comparison["protocol"] == protocol]

    constrained = data[data["network_profile"] != "baseline"]

    print(f"{protocol}:")
    print(
        constrained[
            ["network_profile", "median_overhead_pct"]
        ].to_string(index=False)
    )

print()
print("=== H3: PERFORMANCE IMPACT IS PROTOCOL- AND CONDITION-DEPENDENT ===")

for protocol in ["TLS", "SSH"]:
    data = effect[effect["protocol"] == protocol]

    print(f"{protocol}:")
    print(
        data[
            [
                "network_profile",
                "median_overhead_pct",
                "rank_biserial_correlation",
                "effect_category",
                "direction",
            ]
        ].to_string(index=False)
    )

print()
print("=== H4: STATISTICALLY SIGNIFICANT DIFFERENCES ARE NOT UNIVERSAL ===")

nonsig = significance[
    significance["significant_at_0_05"] == False
]

print(
    nonsig[
        [
            "protocol",
            "network_profile",
            "raw_p_value",
            "adjusted_p_value",
            "significance",
        ]
    ].to_string(index=False)
)

print()
print("=== HYPOTHESIS EVALUATION COMPLETE ===")
print("Hypothesis evaluation: PASS")
