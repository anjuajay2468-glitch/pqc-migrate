#!/bin/bash

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="$PROJECT_ROOT/build"
RESULTS_DIR="$PROJECT_ROOT/results/crypto"
CSV_FILE="$RESULTS_DIR/baseline.csv"

mkdir -p "$RESULTS_DIR"

cd "$BUILD_DIR"

echo "============================================="
echo "       PQC-Migrate Baseline Benchmark"
echo "============================================="
echo

# Start a fresh dataset
rm -f "$CSV_FILE"

echo "algorithm,category,operation,average_us,minimum_us,maximum_us" > "$CSV_FILE"

echo "[1/5] Running ML-KEM-768..."
./mlkem_benchmark

echo
echo "[2/5] Running X25519..."
./x25519_benchmark

echo
echo "[3/5] Running ML-DSA-65..."
./mldsa_benchmark

echo
echo "[4/5] Running ECDSA P-256..."
./ecdsa_benchmark

echo
echo "[5/5] Running RSA-2048..."
./rsa_benchmark

echo
echo "============================================="
echo "Benchmark suite completed"
echo "============================================="
echo
echo "Results:"
echo "$CSV_FILE"
echo

cat "$CSV_FILE"
