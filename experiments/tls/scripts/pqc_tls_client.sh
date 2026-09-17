#!/bin/bash

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
OPENSSL="$PROJECT_ROOT/third_party/openssl-pqc/bin/openssl"
OPENSSL_LIB="$PROJECT_ROOT/third_party/openssl-pqc/lib64"

export LD_LIBRARY_PATH="$OPENSSL_LIB"

echo "============================================="
echo "       PQC-Migrate PQC TLS Client"
echo "============================================="
echo
echo "OpenSSL:"
"$OPENSSL" version
echo
echo "Connecting to localhost:4434..."
echo "TLS version: TLS 1.3"
echo "Requested key exchange: X25519MLKEM768"
echo

"$OPENSSL" s_client \
    -connect localhost:4434 \
    -tls1_3 \
    -groups X25519MLKEM768 \
    -brief \
    < /dev/null
