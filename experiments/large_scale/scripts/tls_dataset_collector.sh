#!/bin/bash

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

PROFILE="${1:-baseline}"
ITERATIONS="${2:-10}"

MASTER_DATASET="$PROJECT_ROOT/experiments/large_scale/results/master_dataset.csv"

CLASSICAL_HOST="localhost"
CLASSICAL_PORT="4433"

HYBRID_HOST="localhost"
HYBRID_PORT="4435"

OPENSSL_HYBRID="$PROJECT_ROOT/third_party/openssl-pqc/bin/openssl"
OPENSSL_HYBRID_LIB="$PROJECT_ROOT/third_party/openssl-pqc/lib64"

RUN_ID="$(date +%Y%m%d_%H%M%S)"

echo "============================================="
echo "       PQC-Migrate Phase 9.3"
echo "       TLS DATASET COLLECTOR"
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

echo "=== VERIFY TLS SERVERS ==="

ss -ltn | grep -E ':4433|:4435'

echo
echo "=== APPLY NETWORK PROFILE ==="

"$PROJECT_ROOT/experiments/network/scripts/network_profile.sh" "$PROFILE"

echo
echo "=== NETWORK STATE ==="

sudo tc qdisc show dev lo

echo
echo "=== CLASSICAL TLS COLLECTION ==="

for ((i=1; i<=ITERATIONS; i++))
do
    start=$(date +%s%N)

    if timeout 5 openssl s_client \
        -connect "$CLASSICAL_HOST:$CLASSICAL_PORT" \
        -tls1_3 \
        -brief \
        < /dev/null \
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
    experiment_id="tls_${PROFILE}_classical_${RUN_ID}_${i}"

    echo "$experiment_id,$timestamp,TLS,Classical,X25519,X25519,None,$PROFILE,$i,$elapsed_us,,,,,,,$success" \
        >> "$MASTER_DATASET"

    echo "Classical iteration $i/$ITERATIONS: ${elapsed_us} us (success=$success)"
done

echo
echo "=== HYBRID TLS COLLECTION ==="

export LD_LIBRARY_PATH="$OPENSSL_HYBRID_LIB"

for ((i=1; i<=ITERATIONS; i++))
do
    start=$(date +%s%N)

    if timeout 5 "$OPENSSL_HYBRID" s_client \
        -connect "$HYBRID_HOST:$HYBRID_PORT" \
        -tls1_3 \
        -groups X25519MLKEM768 \
        -brief \
        < /dev/null \
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
    experiment_id="tls_${PROFILE}_hybrid_${RUN_ID}_${i}"

    echo "$experiment_id,$timestamp,TLS,Hybrid,X25519MLKEM768,X25519,ML-KEM-768,$PROFILE,$i,$elapsed_us,,,,,,,$success" \
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
echo "TLS dataset collection: PASS"
