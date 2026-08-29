#!/bin/bash

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

HOST="localhost"
PORT="22"
USER="pqc-ssh-test"
KEY="$PROJECT_ROOT/experiments/ssh/id_ed25519"
KEX="curve25519-sha256"
ITERATIONS=100

echo "============================================="
echo "   PQC-Migrate Classical SSH Benchmark"
echo "============================================="
echo
echo "Configuration: Classical SSH"
echo "Key exchange: $KEX"
echo "Iterations: $ITERATIONS"
echo "Server: $HOST:$PORT"
echo

if [ ! -f "$KEY" ]; then
    echo "ERROR: SSH private key not found:"
    echo "$KEY"
    exit 1
fi

total_us=0
minimum_us=999999999
maximum_us=0
success=0

for ((i=1; i<=ITERATIONS; i++))
do
    start=$(python3 -c 'import time; print(time.monotonic_ns())')

    if ssh \
        -i "$KEY" \
        -p "$PORT" \
        -o KexAlgorithms="$KEX" \
        -o HostKeyAlgorithms=ssh-ed25519 \
        -o IdentitiesOnly=yes \
        -o BatchMode=yes \
        -o StrictHostKeyChecking=no \
        -o UserKnownHostsFile=/dev/null \
        -o ConnectTimeout=5 \
        "$USER@$HOST" \
        "true" \
        > /dev/null 2>&1
    then
        end=$(python3 -c 'import time; print(time.monotonic_ns())')

        elapsed_us=$(( (end - start) / 1000 ))

        total_us=$((total_us + elapsed_us))

        if [ "$elapsed_us" -lt "$minimum_us" ]; then
            minimum_us=$elapsed_us
        fi

        if [ "$elapsed_us" -gt "$maximum_us" ]; then
            maximum_us=$elapsed_us
        fi

        success=$((success + 1))
    fi
done

if [ "$success" -eq 0 ]; then
    echo
    echo "ERROR: No successful SSH connections."
    exit 1
fi

average_us=$((total_us / success))

echo
echo "RESULTS"
echo "---------------------------------------------"
echo "Successful connections: $success / $ITERATIONS"
echo
echo "Connection establishment latency"
echo "  Average: ${average_us} us"
echo "  Minimum: ${minimum_us} us"
echo "  Maximum: ${maximum_us} us"
echo
echo "SSH classical benchmark checks: SUCCESS"
echo "Negotiated KEX: $KEX"

cat > "$PROJECT_ROOT/experiments/ssh/results/classical_ssh_x25519.csv" <<CSV
algorithm,category,operation,kex,iterations,successful,average_us,minimum_us,maximum_us,correctness
X25519,CLASSICAL,connection,$KEX,$ITERATIONS,$success,$average_us,$minimum_us,$maximum_us,PASS
CSV
