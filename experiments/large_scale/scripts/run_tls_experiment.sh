#!/bin/bash

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

PROFILE="${1:-baseline}"
ITERATIONS="${2:-10}"

MASTER_DATASET="$PROJECT_ROOT/experiments/large_scale/results/master_dataset.csv"
LOG_DIR="$PROJECT_ROOT/experiments/large_scale/logs"

CLASSICAL_PORT=4433
HYBRID_PORT=4435

CLASSICAL_SCRIPT="$PROJECT_ROOT/experiments/tls/scripts/tls_handshake_benchmark.sh"
HYBRID_SCRIPT="$PROJECT_ROOT/experiments/tls/scripts/hybrid/tls_hybrid_handshake_benchmark.sh"
NETWORK_SCRIPT="$PROJECT_ROOT/experiments/network/scripts/network_profile.sh"

mkdir -p "$LOG_DIR"

echo "============================================="
echo "       PQC-Migrate Phase 9.2"
echo "       AUTOMATED TLS RUNNER"
echo "============================================="
echo
echo "Network profile: $PROFILE"
echo "Iterations per configuration: $ITERATIONS"
echo

if [ ! -x "$NETWORK_SCRIPT" ]; then
    echo "ERROR: Network profile script not found:"
    echo "$NETWORK_SCRIPT"
    exit 1
fi

if [ ! -x "$CLASSICAL_SCRIPT" ]; then
    echo "ERROR: Classical TLS benchmark not found:"
    echo "$CLASSICAL_SCRIPT"
    exit 1
fi

if [ ! -x "$HYBRID_SCRIPT" ]; then
    echo "ERROR: Hybrid TLS benchmark not found:"
    echo "$HYBRID_SCRIPT"
    exit 1
fi

echo "=== APPLY NETWORK PROFILE ==="

"$NETWORK_SCRIPT" "$PROFILE"

echo
echo "=== NETWORK STATE ==="

sudo tc qdisc show dev lo

echo
echo "=== VERIFY TLS SERVERS ==="

ss -ltn | grep -E ':4433|:4435'

echo
echo "=== RUN CLASSICAL TLS ==="

CLASSICAL_LOG="$LOG_DIR/tls_classical_${PROFILE}.log"

ITERATIONS="$ITERATIONS" \
    "$CLASSICAL_SCRIPT" | tee "$CLASSICAL_LOG"

echo
echo "=== RUN HYBRID TLS ==="

HYBRID_LOG="$LOG_DIR/tls_hybrid_${PROFILE}.log"

ITERATIONS="$ITERATIONS" \
    "$HYBRID_SCRIPT" | tee "$HYBRID_LOG"

echo
echo "=== RESTORE BASELINE ==="

"$NETWORK_SCRIPT" baseline

echo
echo "=== FINAL NETWORK STATE ==="

sudo tc qdisc show dev lo

echo
echo "=== TLS RUNNER CHECK ==="

if sudo tc qdisc show dev lo | grep -q "noqueue"; then
    echo "Network restoration: PASS"
else
    echo "ERROR: Network restoration failed"
    exit 1
fi

echo
echo "TLS experiment execution: PASS"
