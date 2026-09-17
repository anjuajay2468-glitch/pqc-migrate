#!/bin/bash

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

PROFILE="${1:-baseline}"
ITERATIONS="${2:-10}"

MASTER_DATASET="$PROJECT_ROOT/experiments/large_scale/results/master_dataset.csv"

HOST="localhost"
PORT="22"
USER="pqc-ssh-test"
KEY="$PROJECT_ROOT/experiments/ssh/id_ed25519"

RUN_ID="$(date +%Y%m%d_%H%M%S)"

echo "============================================="
echo "       PQC-Migrate Phase 9.4"
echo "       SSH DATASET COLLECTOR"
echo "============================================="
echo
echo "Network profile: $PROFILE"
echo "Iterations per configuration: $ITERATIONS"
echo "Run ID: $RUN_ID"
echo

if [ ! -f "$MASTER_DATASET" ]; then
    echo "ERROR: Master dataset does not exist."
    exit 1
fi

if [ ! -f "$KEY" ]; then
    echo "ERROR: SSH private key not found."
    exit 1
fi

echo "=== VERIFY SSH SERVER ==="

ss -ltn | grep ':22'

echo
echo "=== APPLY NETWORK PROFILE ==="

"$PROJECT_ROOT/experiments/network/scripts/network_profile.sh" "$PROFILE"

echo
echo "=== NETWORK STATE ==="

sudo tc qdisc show dev lo

echo
echo "=== CLASSICAL SSH COLLECTION ==="

for ((i=1; i<=ITERATIONS; i++))
do
    start=$(date +%s%N)

    if timeout 10 ssh \
        -i "$KEY" \
        -p "$PORT" \
        -o KexAlgorithms=curve25519-sha256 \
        -o HostKeyAlgorithms=ssh-ed25519 \
        -o IdentitiesOnly=yes \
        -o BatchMode=yes \
        -o StrictHostKeyChecking=no \
        -o UserKnownHostsFile=/dev/null \
        "$USER@$HOST" \
        "true" \
        > /dev/null 2>&1
    then
        end=$(date +%s%N)
        elapsed_us=$(( (end - start) / 1000 ))
        success=1
    else
        end=$(date +%s%N)
        elapsed_us=$(( (end - start) / 1000 ))
        success=0
    fi

    timestamp="$(date -Iseconds)"
    experiment_id="ssh_${PROFILE}_classical_${RUN_ID}_${i}"

    echo "$experiment_id,$timestamp,SSH,Classical,X25519,X25519,None,$PROFILE,$i,$elapsed_us,,,,,,,$success" \
        >> "$MASTER_DATASET"

    echo "Classical iteration $i/$ITERATIONS: ${elapsed_us} us (success=$success)"
done

echo
echo "=== HYBRID SSH COLLECTION ==="

for ((i=1; i<=ITERATIONS; i++))
do
    start=$(date +%s%N)

    if timeout 10 ssh \
        -i "$KEY" \
        -p "$PORT" \
        -o KexAlgorithms=sntrup761x25519-sha512@openssh.com \
        -o HostKeyAlgorithms=ssh-ed25519 \
        -o IdentitiesOnly=yes \
        -o BatchMode=yes \
        -o StrictHostKeyChecking=no \
        -o UserKnownHostsFile=/dev/null \
        "$USER@$HOST" \
        "true" \
        > /dev/null 2>&1
    then
        end=$(date +%s%N)
        elapsed_us=$(( (end - start) / 1000 ))
        success=1
    else
        end=$(date +%s%N)
        elapsed_us=$(( (end - start) / 1000 ))
        success=0
    fi

    timestamp="$(date -Iseconds)"
    experiment_id="ssh_${PROFILE}_hybrid_${RUN_ID}_${i}"

    echo "$experiment_id,$timestamp,SSH,Hybrid,sntrup761x25519,X25519,Streamlined-NTRU-Prime,$PROFILE,$i,$elapsed_us,,,,,,,$success" \
        >> "$MASTER_DATASET"

    echo "Hybrid iteration $i/$ITERATIONS: ${elapsed_us} us (success=$success)"
done

echo
echo "=== RESTORE BASELINE ==="

"$PROJECT_ROOT/experiments/network/scripts/network_profile.sh" baseline

echo
echo "=== FINAL NETWORK STATE ==="

sudo tc qdisc show dev lo

echo
echo "=== DATASET CHECK ==="

tail -n $((ITERATIONS * 2)) "$MASTER_DATASET"

echo
echo "=== VALIDATION ==="

ROWS=$(tail -n $((ITERATIONS * 2)) "$MASTER_DATASET" | wc -l)
EXPECTED=$((ITERATIONS * 2))

echo "Rows collected: $ROWS"
echo "Rows expected:  $EXPECTED"

if [ "$ROWS" -ne "$EXPECTED" ]; then
    echo "ERROR: Dataset row count mismatch."
    exit 1
fi

if ! sudo tc qdisc show dev lo | grep -q "noqueue"; then
    echo "ERROR: Network was not restored."
    exit 1
fi

echo
echo "SSH dataset collection: PASS"
