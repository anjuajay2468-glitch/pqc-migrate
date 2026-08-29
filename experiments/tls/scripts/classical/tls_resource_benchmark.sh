#!/bin/bash

set -e

HOST="localhost"
PORT="4433"
ITERATIONS=100

echo "============================================="
echo "   PQC-Migrate Classical TLS Resource Test"
echo "============================================="
echo
echo "Configuration: X25519"
echo "Iterations: $ITERATIONS"
echo "Server: $HOST:$PORT"
echo

total_elapsed=0
total_user=0
total_sys=0
max_rss=0
success=0

for ((i=1; i<=ITERATIONS; i++))
do
    tmpfile=$(mktemp)

    if /usr/bin/time \
        -f '%e %U %S %M' \
        -o "$tmpfile" \
        timeout 5 openssl s_client \
            -connect "$HOST:$PORT" \
            -tls1_3 \
            -brief \
            < /dev/null \
            > /dev/null 2>&1
    then
        result=$(cat "$tmpfile")

        elapsed=$(echo "$result" | awk '{print $1}')
        user=$(echo "$result" | awk '{print $2}')
        sys=$(echo "$result" | awk '{print $3}')
        rss=$(echo "$result" | awk '{print $4}')

        total_elapsed=$(awk -v a="$total_elapsed" -v b="$elapsed" 'BEGIN {print a+b}')
        total_user=$(awk -v a="$total_user" -v b="$user" 'BEGIN {print a+b}')
        total_sys=$(awk -v a="$total_sys" -v b="$sys" 'BEGIN {print a+b}')

        if [ "$rss" -gt "$max_rss" ]; then
            max_rss=$rss
        fi

        success=$((success + 1))
    fi

    rm -f "$tmpfile"
done

if [ "$success" -eq 0 ]; then
    echo
    echo "ERROR: No successful measurements."
    echo "Make sure tls_server.sh is running on port 4433."
    exit 1
fi

avg_elapsed=$(awk -v x="$total_elapsed" -v n="$success" \
    'BEGIN {printf "%.6f", x/n}')

avg_user=$(awk -v x="$total_user" -v n="$success" \
    'BEGIN {printf "%.6f", x/n}')

avg_sys=$(awk -v x="$total_sys" -v n="$success" \
    'BEGIN {printf "%.6f", x/n}')

echo
echo "RESULTS"
echo "---------------------------------------------"
echo "Successful measurements: $success / $ITERATIONS"
echo
echo "Average elapsed time: ${avg_elapsed} s"
echo "Average user CPU:     ${avg_user} s"
echo "Average system CPU:   ${avg_sys} s"
echo "Maximum client RSS:   ${max_rss} KB"
echo
echo "RESOURCE MEASUREMENT: SUCCESS"
