#!/bin/bash

set -e

echo "============================================="
echo "       PQC-Migrate TLS Test Client"
echo "============================================="
echo

echo "Connecting to localhost:4433..."
echo "TLS version: TLS 1.3"
echo

openssl s_client \
    -connect localhost:4433 \
    -tls1_3 \
    -brief \
    < /dev/null
