#!/bin/bash

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

HOST="localhost"
PORT="22"
USER="pqc-ssh-test"
KEY="$PROJECT_ROOT/experiments/ssh/id_ed25519"
KEX="sntrup761x25519-sha512@openssh.com"
ITERATIONS=100

echo "============================================="
echo "   PQC-Migrate Hybrid SSH Resource Test"
echo "============================================="
echo
echo "Configuration: Hybrid SSH"
echo "Key exchange: $KEX"
echo "Classical component: X25519"
echo "PQC component: Streamlined NTRU Prime"
echo "Iterations: $ITERATIONS"
echo "Server: $HOST:$PORT"
echo

if [ ! -f "$KEY" ]; then
    echo "ERROR: SSH private key not found:"
    echo "$KEY"
    exit 1
fi

total_elapsed=0
total_user=0
total_sys=0
maximum_rss=0
success=0

TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

for ((i=1; i<=ITERATIONS; i++))
do
    TIME_FILE="$TMP_DIR/time"

    if /usr/bin/time \
        -f '%e %U %S %M' \
        -o "$TIME_FILE" \
        ssh \
            -i "$KEY" \
            -p "$PORT" \
            -o KexAlgorithms="$KEX" \
            -o HostKeyAlgorithms=ssh-ed25519 \
            -o IdentitiesOnly=yes \
            -o BatchMode=yes \
            -o StrictHostKeyChecking=no \
            -o UserKnownHostsFile=/dev/null \
            "$USER@$HOST" \
            'true' \
            >/dev/null 2>&1
    then
        stats=$(cat "$TIME_FILE")

        elapsed=$(echo "$stats" | awk '{print $1}')
        user_cpu=$(echo "$stats" | awk '{print $2}')
        sys_cpu=$(echo "$stats" | awk '{print $3}')
        rss=$(echo "$stats" | awk '{print $4}')

        if [ -z "$elapsed" ] || [ -z "$user_cpu" ] || [ -z "$sys_cpu" ] || [ -z "$rss" ]; then
            continue
        fi

        total_elapsed=$(awk -v a="$total_elapsed" -v b="$elapsed" 'BEGIN {print a+b}')
        total_user=$(awk -v a="$total_user" -v b="$user_cpu" 'BEGIN {print a+b}')
        total_sys=$(awk -v a="$total_sys" -v b="$sys_cpu" 'BEGIN {print a+b}')

        if [ "$rss" -gt "$maximum_rss" ]; then
            maximum_rss="$rss"
        fi

        success=$((success + 1))
    fi
done

if [ "$success" -eq 0 ]; then
    echo
    echo "ERROR: No successful SSH hybrid resource measurements."
    echo "Make sure sshd is running."
    exit 1
fi

average_elapsed=$(awk -v x="$total_elapsed" -v n="$success" 'BEGIN {printf "%.6f", x/n}')
average_user=$(awk -v x="$total_user" -v n="$success" 'BEGIN {printf "%.6f", x/n}')
average_sys=$(awk -v x="$total_sys" -v n="$success" 'BEGIN {printf "%.6f", x/n}')

echo
echo "RESULTS"
echo "---------------------------------------------"
echo "Successful measurements: $success / $ITERATIONS"
echo
echo "Average elapsed time: $average_elapsed s"
echo "Average user CPU:     $average_user s"
echo "Average system CPU:   $average_sys s"
echo "Maximum client RSS:   $maximum_rss KB"
echo
echo "RESOURCE MEASUREMENT: SUCCESS"

mkdir -p "$PROJECT_ROOT/experiments/ssh/results"

cat > "$PROJECT_ROOT/experiments/ssh/results/hybrid_ssh_resource.csv" <<CSV
algorithm,category,operation,kex,classical_component,pqc_component,iterations,successful,average_elapsed_s,average_user_cpu_s,average_system_cpu_s,max_rss_kb
sntrup761x25519,HYBRID,connection,$KEX,X25519,Streamlined-NTRU-Prime,$ITERATIONS,$success,$average_elapsed,$average_user,$average_sys,$maximum_rss
CSV
