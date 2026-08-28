# PQC-Migrate Experimental Methodology

## Objective

Measure and compare the computational characteristics of classical and
post-quantum cryptographic algorithms used in the PQC migration study.

## Algorithms

### Classical

- X25519
- RSA-2048
- ECDSA P-256

### Post-Quantum

- ML-KEM-768
- ML-DSA-65

## Benchmark Configuration

Each benchmark uses:

- 1 warm-up operation
- 1000 measured iterations
- CLOCK_MONOTONIC timing
- microsecond measurement resolution
- correctness verification for every iteration

## Measurements

The framework currently records:

- Average execution time
- Minimum execution time
- Maximum execution time

Results are stored in:

results/crypto/baseline.csv

## Experimental Environment

The environment is captured separately in:

results/metadata/environment.txt

This records:

- Operating system
- Kernel
- CPU
- Memory
- Compiler
- OpenSSL
- CMake
- Python
- liboqs

## Reproducibility

The benchmark suite can be executed using:

    ./benchmarks/run_baseline.sh

Each execution starts a fresh baseline CSV dataset.

## Current Baseline

The baseline compares:

| Category | Classical | Post-Quantum |
|---|---|---|
| Key establishment | X25519 | ML-KEM-768 |
| Encryption baseline | RSA-2048 | ML-KEM-768 |
| Digital signatures | ECDSA P-256 | ML-DSA-65 |

## Research Limitations

The current measurements are baseline engineering measurements.

They should not yet be treated as final research results.

Later phases will introduce:

- Repeated experimental runs
- Statistical analysis
- Controlled network conditions
- Protocol-level measurements
- Message-size overhead
- Hybrid cryptographic configurations
- TLS integration
- Migration scenarios
- Network latency and bandwidth simulation

## Experimental Reproducibility

Experiments should be performed under controlled conditions.

The following information should be preserved with experimental results:

- Software versions
- Hardware configuration
- Operating system
- Benchmark configuration
- Number of iterations
- Algorithm parameters
- Raw measurements
- Processed measurements

This information will support reproducibility of the final research results.
