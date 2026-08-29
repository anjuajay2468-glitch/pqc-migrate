#!/bin/bash

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"

OPENSSL="$PROJECT_ROOT/third_party/openssl-pqc/bin/openssl"
OPENSSL_LIB="$PROJECT_ROOT/third_party/openssl-pqc/lib64"

export LD_LIBRARY_PATH="$OPENSSL_LIB"

echo "============================================="
echo "     PQC-Migrate Hybrid TLS 1.3 Client"
echo "============================================="
echo
echo "OpenSSL:"
"$OPENSSL" version
echo
echo "Connecting to localhost:4435..."
echo "TLS version: TLS 1.3"
echo "Requested key exchange: X25519MLKEM768"
echo "Classical component: X25519"
echo "PQC component: ML-KEM-768"
echo

"$OPENSSL" s_client \
    -connect localhost:4435 \
    -tls1_3 \
    -groups X25519MLKEM768 \
    -brief \
    < /dev/null
