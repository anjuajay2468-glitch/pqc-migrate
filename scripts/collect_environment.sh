#!/bin/bash

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUTPUT_DIR="$PROJECT_ROOT/results/metadata"
OUTPUT_FILE="$OUTPUT_DIR/environment.txt"

mkdir -p "$OUTPUT_DIR"

echo "PQC-Migrate Experimental Environment" > "$OUTPUT_FILE"
echo "====================================" >> "$OUTPUT_FILE"
echo >> "$OUTPUT_FILE"

echo "Timestamp:" >> "$OUTPUT_FILE"
date -u +"%Y-%m-%d %H:%M:%S UTC" >> "$OUTPUT_FILE"
echo >> "$OUTPUT_FILE"

echo "Operating System:" >> "$OUTPUT_FILE"
lsb_release -ds >> "$OUTPUT_FILE"
echo >> "$OUTPUT_FILE"

echo "Kernel:" >> "$OUTPUT_FILE"
uname -r >> "$OUTPUT_FILE"
echo >> "$OUTPUT_FILE"

echo "Architecture:" >> "$OUTPUT_FILE"
uname -m >> "$OUTPUT_FILE"
echo >> "$OUTPUT_FILE"

echo "CPU:" >> "$OUTPUT_FILE"
lscpu | grep -E \
"Model name|Architecture|CPU\(s\)|Thread|Core|Socket" \
>> "$OUTPUT_FILE"
echo >> "$OUTPUT_FILE"

echo "Memory:" >> "$OUTPUT_FILE"
free -h >> "$OUTPUT_FILE"
echo >> "$OUTPUT_FILE"

echo "Compiler:" >> "$OUTPUT_FILE"
gcc --version | head -n 1 >> "$OUTPUT_FILE"
echo >> "$OUTPUT_FILE"

echo "CMake:" >> "$OUTPUT_FILE"
cmake --version | head -n 1 >> "$OUTPUT_FILE"
echo >> "$OUTPUT_FILE"

echo "OpenSSL:" >> "$OUTPUT_FILE"
openssl version >> "$OUTPUT_FILE"
echo >> "$OUTPUT_FILE"

echo "Python:" >> "$OUTPUT_FILE"
python3 --version >> "$OUTPUT_FILE"
echo >> "$OUTPUT_FILE"

echo "liboqs:" >> "$OUTPUT_FILE"
if [ -f /usr/local/lib/liboqs.a ]; then
    echo "/usr/local/lib/liboqs.a" >> "$OUTPUT_FILE"
else
    echo "liboqs not found" >> "$OUTPUT_FILE"
fi

echo >> "$OUTPUT_FILE"

echo "Environment information written to:"
echo "$OUTPUT_FILE"
