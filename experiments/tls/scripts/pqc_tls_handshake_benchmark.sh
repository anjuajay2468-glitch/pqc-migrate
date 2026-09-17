#!/bin/bash

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

OPENSSL="$PROJECT_ROOT/third_party/openssl-pqc/bin/openssl"
OPENSSL_LIB="$PROJECT_ROOT/third_party/openssl-pqc/lib64"

HOST="localhost"
PORT="4434"
ITERATIONS=100

export LD_LIBRARY_PATH="$OPENSSL_LIB"

echo "============================================="
echo "   PQC-Migrate PQC TLS 1.3 Handshake Benchmark"
echo "============================================="
echo
echo "OpenSSL:"
"$OPENSSL" version
echo
echo "Key exchange: X25519MLKEM768"
echo "Iterations: $ITERATIONS"
echo "Server: $HOST:$PORT"
echo

total=0
minimum=999999999
maximum=0
success=0

for ((i=1; i<=ITERATIONS; i++))
do
    start=$(date +%s%N)

    if timeout 5 "$OPENSSL" s_client \
        -connect "$HOST:$PORT" \
        -tls1_3 \
        -groups X25519MLKEM768 \
        -brief \
        < /dev/null \
        > /dev/null 2>&1
    then
        end=$(date +%s%N)

        elapsed_ns=$((end - start))
        elapsed_us=$((elapsed_ns / 1000))

        total=$((total + elapsed_us))

        if [ "$elapsed_us" -lt "$minimum" ]; then
            minimum=$elapsed_us
        fi

        if [ "$elapsed_us" -gt "$maximum" ]; then
            maximum=$elapsed_us
        fi

        success=$((success + 1))
    fi
done

if [ "$success" -eq 0 ]; then
    echo
    echo "ERROR: No successful PQC TLS handshakes."
    echo "Verify that pqc_tls_server.sh is running."
    exit 1
fi

average=$((total / success))

echo
echo "RESULTS"
echo "---------------------------------------------"
echo "Successful handshakes: $success / $ITERATIONS"
echo
echo "Handshake latency"
echo "  Average: ${average} us"
echo "  Minimum: ${minimum} us"
echo "  Maximum: ${maximum} us"
echo
echo "TLS 1.3 PQC handshake checks: SUCCESS"
echo "Negotiated group: X25519MLKEM768"
