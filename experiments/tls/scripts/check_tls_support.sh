#!/bin/bash

set -e

echo "============================================="
echo "       PQC-Migrate TLS Capability Check"
echo "============================================="
echo

echo "[1/5] OpenSSL version"
openssl version
echo

echo "[2/5] OpenSSL providers"
openssl list -providers
echo

echo "[3/5] Available TLS 1.3 ciphers"
openssl ciphers -v -tls1_3
echo

echo "[4/5] Available public-key algorithms"
openssl list -public-key-algorithms | grep -E \
"RSA|EC|X25519|ML-KEM|ML-DSA|ED25519" || true
echo

echo "[5/5] OpenSSL supported groups"
openssl list -tls1_3 -tls-groups 2>/dev/null || true
echo

echo "============================================="
echo "TLS capability check completed"
echo "============================================="
