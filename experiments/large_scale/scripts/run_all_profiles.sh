#!/bin/bash

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

ITERATIONS="${1:-10}"

TLS_COLLECTOR="$PROJECT_ROOT/experiments/large_scale/scripts/tls_dataset_collector.sh"
SSH_COLLECTOR="$PROJECT_ROOT/experiments/large_scale/scripts/ssh_dataset_collector.sh"

PROFILES=(
    baseline
    latency100
    latency200
    bandwidth1mbps
    loss1
    mobile
)

echo "============================================="
echo "       PQC-Migrate Phase 9.5"
echo "       MULTI-NETWORK DATASET RUNNER"
echo "============================================="
echo
echo "Iterations per configuration: $ITERATIONS"
echo
echo "Profiles:"
printf '  - %s\n' "${PROFILES[@]}"
echo

for PROFILE in "${PROFILES[@]}"
do
    echo
    echo "============================================="
    echo " NETWORK PROFILE: $PROFILE"
    echo "============================================="

    echo
    echo "=== TLS DATA COLLECTION ==="

    "$TLS_COLLECTOR" "$PROFILE" "$ITERATIONS"

    echo
    echo "=== SSH DATA COLLECTION ==="

    "$SSH_COLLECTOR" "$PROFILE" "$ITERATIONS"

    echo
    echo "=== VERIFY BASELINE RESTORATION ==="

    if ! sudo tc qdisc show dev lo | grep -q "noqueue"; then
        echo "ERROR: Network was not restored after $PROFILE"
        exit 1
    fi

    echo "Profile $PROFILE: COMPLETE"
done

echo
echo "============================================="
echo "       PHASE 9.5 COLLECTION COMPLETE"
echo "============================================="

echo
echo "=== FINAL NETWORK STATE ==="

sudo tc qdisc show dev lo

echo
echo "=== DATASET SUMMARY ==="

MASTER_DATASET="$PROJECT_ROOT/experiments/large_scale/results/master_dataset.csv"

echo "Total data rows:"
tail -n +2 "$MASTER_DATASET" | wc -l

echo
echo "Rows by protocol:"
tail -n +2 "$MASTER_DATASET" | cut -d',' -f3 | sort | uniq -c

echo
echo "Rows by configuration:"
tail -n +2 "$MASTER_DATASET" | cut -d',' -f4 | sort | uniq -c

echo
echo "Rows by network profile:"
tail -n +2 "$MASTER_DATASET" | cut -d',' -f8 | sort | uniq -c

echo
echo "Phase 9.5 multi-network collection: PASS"
