#!/bin/bash

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"

OPENSSL="$PROJECT_ROOT/third_party/openssl-pqc/bin/openssl"
OPENSSL_LIB="$PROJECT_ROOT/third_party/openssl-pqc/lib64"

CERT="$PROJECT_ROOT/experiments/tls/configs/certs/server.crt"
KEY="$PROJECT_ROOT/experiments/tls/configs/certs/server.key"

export LD_LIBRARY_PATH="$OPENSSL_LIB"

echo "============================================="
echo "     PQC-Migrate Hybrid TLS 1.3 Server"
echo "============================================="
echo
echo "OpenSSL:"
"$OPENSSL" version
echo
echo "TLS version: TLS 1.3"
echo "Key exchange: X25519MLKEM768"
echo "Classical component: X25519"
echo "PQC component: ML-KEM-768"
echo "Certificate: RSA-2048"
echo "Port: 4435"
echo
echo "Waiting for hybrid TLS client..."
echo

"$OPENSSL" s_server \
    -accept 4435 \
    -cert "$CERT" \
    -key "$KEY" \
    -tls1_3 \
    -groups X25519MLKEM768 \
    -www
