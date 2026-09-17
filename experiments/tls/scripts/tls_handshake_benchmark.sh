#!/bin/bash

set -e

HOST="localhost"
PORT="4433"
ITERATIONS=100

echo "============================================="
echo "     PQC-Migrate TLS 1.3 Handshake Benchmark"
echo "============================================="
echo
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

    if timeout 5 openssl s_client \
        -connect "$HOST:$PORT" \
        -tls1_3 \
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
    echo "ERROR: No successful TLS handshakes."
    echo "Make sure tls_server.sh is running."
    exit 1
fi

average=$((total / success))

echo "RESULTS"
echo "---------------------------------------------"
echo "Successful handshakes: $success / $ITERATIONS"
echo
echo "Handshake latency"
echo "  Average: ${average} us"
echo "  Minimum: ${minimum} us"
echo "  Maximum: ${maximum} us"
echo
echo "TLS 1.3 handshake checks: SUCCESS"
