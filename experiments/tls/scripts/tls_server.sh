#!/bin/bash

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
CERT="$PROJECT_ROOT/experiments/tls/configs/certs/server.crt"
KEY="$PROJECT_ROOT/experiments/tls/configs/certs/server.key"

echo "============================================="
echo "       PQC-Migrate TLS Test Server"
echo "============================================="
echo
echo "TLS version: TLS 1.3"
echo "Certificate: RSA-2048"
echo "Port: 4433"
echo
echo "Waiting for TLS client..."
echo

openssl s_server \
    -accept 4433 \
    -cert "$CERT" \
    -key "$KEY" \
    -tls1_3 \
    -www

