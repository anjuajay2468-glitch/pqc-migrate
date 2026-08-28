# PQC-Migrate TLS Experimental Results

## Classical TLS Baseline

Configuration:

- TLS 1.3
- X25519 key exchange
- RSA-2048 certificate
- AES-256-GCM cipher
- 100 handshake iterations

Results:

| Metric | Result |
|---|---:|
| Successful handshakes | 100/100 |
| Average latency | 26,211 us |
| Minimum latency | 21,956 us |
| Maximum latency | 32,626 us |

## Hybrid PQC TLS

Configuration:

- TLS 1.3
- X25519MLKEM768 hybrid key exchange
- RSA-2048 certificate
- AES-256-GCM cipher
- OpenSSL 3.5.4
- 100 handshake iterations

Results:
| Successful handshakes | 100/100 |
| Average latency | 8,170 us |
| Minimum latency | 6,832 us |
| Maximum latency | 10,829 us |

Negotiated TLS group:

`X25519MLKEM768`

## Correctness

All 100 hybrid TLS handshakes completed successfully.

The negotiated TLS 1.3 group confirms that the experiment used
X25519 combined with ML-KEM-768 rather than classical X25519 alone.

## Environment

Classical experiments use the system OpenSSL installation.

PQC TLS experiments use the project-local OpenSSL 3.5.4 installation.

The system OpenSSL installation was not modified.

## Reproducibility

Classical TLS:

```bash
./experiments/tls/scripts/tls_handshake_benchmark.sh
