# PQC-Migrate TLS Experiments

This directory contains protocol-level experiments for evaluating
classical and post-quantum cryptographic configurations in TLS.

## Objectives

- Establish a reproducible TLS test environment.
- Measure TLS handshake performance.
- Compare classical and post-quantum configurations.
- Measure key and certificate size overhead.
- Measure connection latency and computational cost.
- Evaluate hybrid configurations.

## Planned Configurations

### Classical

- X25519
- ECDSA P-256
- RSA-2048

### Post-Quantum

- ML-KEM-768
- ML-DSA-65

### Hybrid

Hybrid configurations will combine classical and post-quantum
key establishment mechanisms where supported.

## Experimental Measurements

Future TLS experiments will record:

- Handshake latency
- Connection establishment time
- CPU cost
- Public key size
- Certificate size
- Key exchange message size
- Total handshake bytes
- Success/failure rate

## Experimental Structure

```text
experiments/tls/
├── README.md
├── configs/
├── scripts/
└── results/
