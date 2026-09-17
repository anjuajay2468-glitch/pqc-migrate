#!/bin/bash

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "============================================="
echo "       PQC-Migrate Environment Check"
echo "============================================="
echo

echo "[1/7] Checking compiler..."
gcc --version | head -n 1

echo
echo "[2/7] Checking CMake..."
cmake --version | head -n 1

echo
echo "[3/7] Checking OpenSSL..."
openssl version

echo
echo "[4/7] Checking Python..."
python3 --version

echo
echo "[5/7] Checking liboqs..."

if [ -f /usr/local/lib/liboqs.a ] &&
   [ -f /usr/local/include/oqs/oqs.h ]; then
    echo "liboqs: FOUND"
else
    echo "liboqs: NOT FOUND"
    exit 1
fi

echo
echo "[6/7] Checking environment metadata..."

if [ -f "$PROJECT_ROOT/results/metadata/environment.txt" ]; then
    echo "environment.txt: FOUND"
else
    echo "environment.txt: NOT FOUND"
    exit 1
fi

echo
echo "[7/7] Checking experiment configuration..."

cd "$PROJECT_ROOT"

if ./scripts/validate_config.py > /dev/null; then
    echo "experiment.yaml: VALID"
else
    echo "experiment.yaml: INVALID"
    exit 1
fi

echo
echo "============================================="
echo "Environment validation: SUCCESS"
echo "============================================="

