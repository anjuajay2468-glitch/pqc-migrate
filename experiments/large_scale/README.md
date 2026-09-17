# PQC-Migrate Large-Scale Benchmarking

## Objective

Phase 9 automates repeated cryptographic experiments across
multiple secure communication protocols and network conditions.

The objective is to produce a reproducible research dataset
for statistical analysis in Phase 10.

## Protocols

- TLS 1.3
- SSH

## Cryptographic configurations

### Classical

- X25519

### Hybrid

- X25519 + ML-KEM-768 for TLS
- X25519 + Streamlined NTRU Prime for SSH

## Network profiles

- baseline
- latency100
- latency200
- bandwidth1mbps
- loss1
- mobile

## Measurements

- handshake/connection latency
- elapsed time
- user CPU time
- system CPU time
- memory usage
- TCP payload
- packet count
- success/failure

## Dataset

The master dataset is stored in:

experiments/large_scale/results/master_dataset.csv

Each row represents one experimental measurement.

## Reproducibility

All experiments are executed using scripts stored under:

experiments/large_scale/scripts/
