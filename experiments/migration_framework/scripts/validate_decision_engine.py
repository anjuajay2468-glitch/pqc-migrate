from pathlib import Path
import itertools
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]

engine_path = ROOT / "experiments/migration_framework/scripts/migration_decision_engine.py"
evidence_path = ROOT / "experiments/migration_framework/results/evidence_model.csv"
output_path = ROOT / "experiments/migration_framework/results/decision_validation.csv"

# Load the decision function from the engine without executing its
# representative-scenario section.
source = engine_path.read_text()
source = source.split("# Representative scenarios used to validate the framework.")[0]

namespace = {
    "__file__": str(engine_path),
    "__name__": "__validation__",
}
exec(source, namespace)

decide = namespace["decide"]

security_requirements = [
    "classical_acceptable",
    "pqc_required",
]

legacy_options = [
    "required",
    "not_required",
]

performance_options = [
    "low",
    "medium",
    "high",
]

urgency_options = [
    "low",
    "medium",
    "high",
]

protocols = [
    "TLS",
    "SSH",
]

network_profiles = [
    "baseline",
    "latency100",
    "latency200",
    "bandwidth1mbps",
    "loss1",
    "mobile",
]

rows = []

for values in itertools.product(
    security_requirements,
    legacy_options,
    performance_options,
    urgency_options,
    protocols,
    network_profiles,
):
    (
        security,
        legacy,
        performance,
        urgency,
        protocol,
        network,
    ) = values

    result = decide(
        security_requirement=security,
        legacy_compatibility=legacy,
        performance_sensitivity=performance,
        migration_urgency=urgency,
        protocol=protocol,
        network_profile=network,
    )

    rows.append(result)

df = pd.DataFrame(rows)

output_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_path, index=False)

print("=== DECISION ENGINE VALIDATION ===")
print(f"Scenarios evaluated: {len(df)}")
print(f"Output: {output_path}")
print()
print("Recommendations:")
print(df["recommendation"].value_counts().to_string())

print()
print("=== RULE VALIDATION ===")

checks = []

# Rule 1:
# PQC-required deployments must never recommend CLASSICAL.
check = not (
    (df["security_requirement"] == "pqc_required")
    & (df["recommendation"] == "CLASSICAL")
).any()
checks.append(("PQC-required never recommends CLASSICAL", check))

# Rule 2:
# PQC-required + legacy-required must always use hybrid transition.
mask = (
    (df["security_requirement"] == "pqc_required")
    & (df["legacy_compatibility"] == "required")
)
check = (df.loc[mask, "recommendation"] == "HYBRID_TRANSITION").all()
checks.append(("PQC-required + legacy-required -> HYBRID_TRANSITION", check))

# Rule 3:
# PQC-required + no legacy constraint must always recommend PQC.
mask = (
    (df["security_requirement"] == "pqc_required")
    & (df["legacy_compatibility"] == "not_required")
)
check = (df.loc[mask, "recommendation"] == "PQC").all()
checks.append(("PQC-required + no legacy constraint -> PQC", check))

# Rule 4:
# Classical acceptable + high urgency + legacy required -> hybrid.
mask = (
    (df["security_requirement"] == "classical_acceptable")
    & (df["migration_urgency"] == "high")
    & (df["legacy_compatibility"] == "required")
)
check = (df.loc[mask, "recommendation"] == "HYBRID_TRANSITION").all()
checks.append(("High urgency + legacy-required -> HYBRID_TRANSITION", check))

# Rule 5:
# Classical acceptable + high urgency + no legacy constraint -> PQC.
mask = (
    (df["security_requirement"] == "classical_acceptable")
    & (df["migration_urgency"] == "high")
    & (df["legacy_compatibility"] == "not_required")
)
check = (df.loc[mask, "recommendation"] == "PQC").all()
checks.append(("High urgency + no legacy constraint -> PQC", check))

# Rule 6:
# Classical acceptable + low/medium urgency + no legacy requirement +
# high performance sensitivity + performance-sensitive condition -> classical.
mask = (
    (df["security_requirement"] == "classical_acceptable")
    & (df["migration_urgency"].isin(["low", "medium"]))
    & (df["legacy_compatibility"] == "not_required")
    & (df["performance_sensitivity"] == "high")
    & (df["performance_sensitive_condition"])
)
check = (df.loc[mask, "recommendation"] == "CLASSICAL").all()
checks.append(("High performance sensitivity + substantial overhead -> CLASSICAL", check))

# Rule 7:
# Every recommendation must retain evidence fields.
required_columns = [
    "median_overhead_pct",
    "p95_overhead_pct",
    "adjusted_p_value",
    "rank_biserial_correlation",
    "effect_category",
    "evidence_summary",
]

check = all(column in df.columns for column in required_columns)
checks.append(("All recommendations retain experimental evidence", check))

for name, passed in checks:
    print(f"{'PASS' if passed else 'FAIL'} — {name}")

if not all(passed for _, passed in checks):
    raise SystemExit("Decision engine validation: FAIL")

print()
print("Decision engine validation: PASS")
