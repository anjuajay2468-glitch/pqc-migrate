from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]

evidence_path = (
    ROOT / "experiments/migration_framework/results/evidence_model.csv"
)

output_path = (
    ROOT / "experiments/migration_framework/results/migration_decisions.csv"
)

evidence = pd.read_csv(evidence_path)


def get_evidence(protocol, network_profile):
    rows = evidence[
        (evidence["protocol"] == protocol)
        & (evidence["network_profile"] == network_profile)
    ]

    if len(rows) != 1:
        raise ValueError(
            f"Expected exactly one evidence row for "
            f"{protocol}/{network_profile}, found {len(rows)}"
        )

    return rows.iloc[0]


def decide(
    security_requirement,
    legacy_compatibility,
    performance_sensitivity,
    migration_urgency,
    protocol,
    network_profile,
):
    row = get_evidence(protocol, network_profile)

    significant = bool(row["significant_at_0_05"])
    effect_large = row["effect_category"] == "Large"
    positive_overhead = float(row["median_overhead_pct"]) > 0
    performance_sensitive_condition = bool(
        row["performance_sensitive_condition"]
    )

    # Security constraint
    if security_requirement == "pqc_required":

        if legacy_compatibility == "required":
            recommendation = "HYBRID_TRANSITION"
            reason = (
                "Post-quantum protection is required while legacy "
                "compatibility is also required; hybrid deployment "
                "provides a transitional migration path."
            )

        else:
            recommendation = "PQC"
            reason = (
                "Post-quantum protection is required and no legacy "
                "compatibility constraint prevents direct PQC deployment."
            )

    # Classical remains eligible when PQC is not mandatory.
    else:

        if migration_urgency == "high":
            if legacy_compatibility == "required":
                recommendation = "HYBRID_TRANSITION"
                reason = (
                    "Migration urgency is high but legacy compatibility "
                    "is required, favoring a transitional hybrid strategy."
                )
            else:
                recommendation = "PQC"
                reason = (
                    "Migration urgency is high and no legacy compatibility "
                    "constraint prevents direct PQC migration."
                )

        elif performance_sensitivity == "high" and performance_sensitive_condition:
            recommendation = "CLASSICAL"
            reason = (
                "PQC is not mandatory and the selected environment has "
                "substantial measured hybrid performance overhead; "
                "performance-sensitive deployment favors retaining the "
                "classical configuration while migration requirements "
                "are evaluated."
            )

        else:
            recommendation = "HYBRID_OR_PQC_EVALUATION"
            reason = (
                "PQC is not mandatory, but migration considerations and "
                "measured experimental evidence justify evaluating hybrid "
                "and direct PQC deployment."
            )

    evidence_level = row["evidence_classification"]

    if significant and effect_large and positive_overhead:
        evidence_summary = (
            "Strong experimental evidence of positive hybrid latency impact."
        )
    elif significant and positive_overhead:
        evidence_summary = (
            "Statistically supported positive hybrid latency difference."
        )
    elif positive_overhead:
        evidence_summary = (
            "Positive hybrid latency overhead observed, without strong "
            "statistical support."
        )
    else:
        evidence_summary = (
            "No positive hybrid latency overhead is supported by the "
            "selected comparison."
        )

    conditions = []

    if recommendation == "PQC":
        conditions.append(
            "Reconsider if protocol support, compatibility, or measured "
            "performance constraints prevent deployment."
        )

    elif recommendation == "HYBRID_TRANSITION":
        conditions.append(
            "Reassess for direct PQC deployment after legacy systems "
            "are upgraded or compatibility constraints are removed."
        )

    elif recommendation == "CLASSICAL":
        conditions.append(
            "Reassess when post-quantum protection becomes mandatory "
            "or migration urgency increases."
        )

    else:
        conditions.append(
            "Collect additional deployment-specific measurements before "
            "selecting the final migration state."
        )

    return {
        "security_requirement": security_requirement,
        "legacy_compatibility": legacy_compatibility,
        "performance_sensitivity": performance_sensitivity,
        "migration_urgency": migration_urgency,
        "protocol": protocol,
        "network_profile": network_profile,
        "recommendation": recommendation,
        "reason": reason,
        "evidence_level": evidence_level,
        "median_overhead_pct": float(row["median_overhead_pct"]),
        "p95_overhead_pct": float(row["p95_overhead_pct"]),
        "adjusted_p_value": float(row["adjusted_p_value"]),
        "rank_biserial_correlation": float(
            row["rank_biserial_correlation"]
        ),
        "effect_category": row["effect_category"],
        "statistically_significant": significant,
        "performance_sensitive_condition": performance_sensitive_condition,
        "evidence_summary": evidence_summary,
        "reconsideration_condition": conditions[0],
    }


# Representative scenarios used to validate the framework.
scenarios = [
    {
        "security_requirement": "pqc_required",
        "legacy_compatibility": "not_required",
        "performance_sensitivity": "medium",
        "migration_urgency": "high",
        "protocol": "TLS",
        "network_profile": "baseline",
    },
    {
        "security_requirement": "pqc_required",
        "legacy_compatibility": "required",
        "performance_sensitivity": "high",
        "migration_urgency": "high",
        "protocol": "SSH",
        "network_profile": "bandwidth1mbps",
    },
    {
        "security_requirement": "classical_acceptable",
        "legacy_compatibility": "required",
        "performance_sensitivity": "high",
        "migration_urgency": "low",
        "protocol": "SSH",
        "network_profile": "bandwidth1mbps",
    },
    {
        "security_requirement": "classical_acceptable",
        "legacy_compatibility": "not_required",
        "performance_sensitivity": "medium",
        "migration_urgency": "low",
        "protocol": "TLS",
        "network_profile": "mobile",
    },
]

results = []

for scenario in scenarios:
    results.append(decide(**scenario))

output = pd.DataFrame(results)

output.to_csv(output_path, index=False)

print("=== MIGRATION DECISION ENGINE ===")
print(f"Scenarios evaluated: {len(output)}")
print(f"Output: {output_path}")
print()
print(output[
    [
        "protocol",
        "network_profile",
        "recommendation",
        "median_overhead_pct",
        "statistically_significant",
        "effect_category",
    ]
].to_string(index=False))

if len(output) != 4:
    raise SystemExit("FAIL: expected 4 representative scenarios")

required_recommendations = {
    "PQC",
    "HYBRID_TRANSITION",
    "CLASSICAL",
    "HYBRID_OR_PQC_EVALUATION",
}

actual_recommendations = set(output["recommendation"])

if not required_recommendations.issubset(actual_recommendations):
    raise SystemExit(
        "FAIL: representative scenarios did not exercise all "
        "decision outcomes"
    )

print()
print("Decision engine: PASS")
