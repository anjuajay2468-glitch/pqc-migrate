import csv
from pathlib import Path
from collections import Counter

DATASET = Path(
    "experiments/large_scale/results/master_dataset.csv"
)

EXPECTED_PROFILES = {
    "baseline",
    "latency100",
    "latency200",
    "bandwidth1mbps",
    "loss1",
    "mobile",
}

EXPECTED_PROTOCOLS = {"TLS", "SSH"}
EXPECTED_CONFIGS = {"Classical", "Hybrid"}

with DATASET.open(newline="") as f:
    rows = list(csv.DictReader(f))

print("=============================================")
print("       PQC-Migrate Phase 9.6")
print("       DATASET INTEGRITY VALIDATION")
print("=============================================")

print()
print("Total rows:", len(rows))

errors = []

# ------------------------------------------------
# Required columns
# ------------------------------------------------

required_columns = [
    "experiment_id",
    "timestamp",
    "protocol",
    "configuration",
    "algorithm",
    "classical_component",
    "pqc_component",
    "network_profile",
    "iteration",
    "latency_us",
    "success",
]

fieldnames = rows[0].keys() if rows else []

for column in required_columns:
    if column not in fieldnames:
        errors.append(f"Missing column: {column}")

# ------------------------------------------------
# Basic row validation
# ------------------------------------------------

for i, row in enumerate(rows, start=2):

    if row["protocol"] not in EXPECTED_PROTOCOLS:
        errors.append(
            f"Row {i}: invalid protocol {row['protocol']}"
        )

    if row["configuration"] not in EXPECTED_CONFIGS:
        errors.append(
            f"Row {i}: invalid configuration "
            f"{row['configuration']}"
        )

    if row["network_profile"] not in EXPECTED_PROFILES:
        errors.append(
            f"Row {i}: invalid network profile "
            f"{row['network_profile']}"
        )

    try:
        latency = float(row["latency_us"])
        if latency <= 0:
            errors.append(
                f"Row {i}: invalid latency {latency}"
            )
    except ValueError:
        errors.append(
            f"Row {i}: invalid latency value "
            f"{row['latency_us']}"
        )

    try:
        iteration = int(row["iteration"])
        if not 1 <= iteration <= 10:
            errors.append(
                f"Row {i}: invalid iteration {iteration}"
            )
    except ValueError:
        errors.append(
            f"Row {i}: invalid iteration"
        )

    if row["success"] not in {"0", "1"}:
        errors.append(
            f"Row {i}: invalid success value "
            f"{row['success']}"
        )

# ------------------------------------------------
# Duplicate experiment IDs
# ------------------------------------------------

ids = [row["experiment_id"] for row in rows]
duplicates = [
    item
    for item, count in Counter(ids).items()
    if count > 1
]

if duplicates:
    errors.append(
        f"Duplicate experiment IDs: {len(duplicates)}"
    )

# ------------------------------------------------
# Distribution
# ------------------------------------------------

print()
print("=== PROTOCOL DISTRIBUTION ===")

for protocol, count in sorted(
    Counter(r["protocol"] for r in rows).items()
):
    print(f"{protocol:8s}: {count}")

print()
print("=== CONFIGURATION DISTRIBUTION ===")

for config, count in sorted(
    Counter(r["configuration"] for r in rows).items()
):
    print(f"{config:10s}: {count}")

print()
print("=== NETWORK DISTRIBUTION ===")

for profile, count in sorted(
    Counter(r["network_profile"] for r in rows).items()
):
    print(f"{profile:16s}: {count}")

print()
print("=== SUCCESS DISTRIBUTION ===")

for success, count in sorted(
    Counter(r["success"] for r in rows).items()
):
    print(f"success={success}: {count}")

# ------------------------------------------------
# Expected balanced design
# ------------------------------------------------

print()
print("=== BALANCE CHECK ===")

minimum_per_cell = 10

for protocol in sorted(EXPECTED_PROTOCOLS):
    for config in sorted(EXPECTED_CONFIGS):
        for profile in sorted(EXPECTED_PROFILES):

            count = sum(
                1
                for r in rows
                if r["protocol"] == protocol
                and r["configuration"] == config
                and r["network_profile"] == profile
            )

            status = "PASS" if count >= minimum_per_cell else "FAIL"

            print(
                f"{protocol:5s} | "
                f"{config:9s} | "
                f"{profile:16s} | "
                f"{count:2d} | {status}"
            )

            if count < minimum_per_cell:
                errors.append(
                    f"Unbalanced cell: "
                    f"{protocol}/{config}/{profile} "
                    f"has only {count} rows"
                )

# ------------------------------------------------
# Final result
# ------------------------------------------------

print()
print("=== FINAL VALIDATION ===")

if errors:
    print(f"FAIL: {len(errors)} issue(s)")
    print()

    for error in errors[:20]:
        print(" -", error)

    raise SystemExit(1)

print("Dataset integrity: PASS")
print("No duplicate experiment IDs: PASS")
print("All required fields valid: PASS")
print("Experimental cells balanced: PASS")
