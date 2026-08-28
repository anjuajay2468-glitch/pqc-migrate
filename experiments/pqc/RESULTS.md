# PQC-Migrate Phase 4 — PQC Implementation Results

## Objective

This phase evaluates the implementation characteristics of
ML-KEM-768 and ML-DSA-65 using the project's liboqs-based
cryptographic environment.

The evaluation covers correctness, standardized object sizes,
and execution performance.

---

## ML-KEM-768

### Correctness

The following operations were successfully verified:

- Key generation
- Encapsulation
- Decapsulation
- Shared-secret equality

All correctness checks passed.

### Parameter Sizes

| Parameter | Size |
|---|---:|
| Public key | 1184 bytes |
| Secret key | 2400 bytes |
| Ciphertext | 1088 bytes |
| Shared secret | 32 bytes |

### Performance

| Operation | Average (µs) | Minimum (µs) | Maximum (µs) |
|---|---:|---:|---:|
| Key generation | 13.410 | 9.264 | 1112.967 |
| Encapsulation | 13.051 | 9.760 | 309.780 |
| Decapsulation | 15.657 | 11.822 | 291.190 |

All 1000 benchmark iterations passed correctness checks.

---

## ML-DSA-65

### Correctness

The following operations were successfully verified:

- Key generation
- Signing
- Verification

All correctness checks passed.

### Parameter Sizes

| Parameter | Size |
|---|---:|
| Public key | 1952 bytes |
| Secret key | 4032 bytes |
| Signature | 3309 bytes |

### Performance

| Operation | Average (µs) | Minimum (µs) | Maximum (µs) |
|---|---:|---:|---:|
| Key generation | 39.243 | 32.163 | 450.215 |
| Signing | 104.323 | 40.216 | 899.279 |
| Verification | 36.783 | 31.081 | 137.323 |

All 1000 benchmark iterations passed correctness checks.

---

## Classical Comparison

The classical comparison dataset contains measurements
from the Phase 3 baseline:

- X25519
- ECDSA P-256

These measurements are compared with:

- ML-KEM-768
- ML-DSA-65

The comparison is intended to characterize migration
trade-offs rather than claim that classical and PQC
operations are mathematically identical.

For KEMs, X25519 key generation and shared-secret derivation
are compared with the corresponding ML-KEM key-establishment
operations.

For signatures, ECDSA P-256 and ML-DSA-65 key generation,
signing, and verification are compared.

---

## Reproducibility

PQC performance benchmarks use:

- 1000 iterations
- 1 warm-up operation
- `CLOCK_MONOTONIC`
- microsecond timing
- correctness verification

Performance results:

`experiments/pqc/results/pqc_performance.csv`

Classical comparison:

`experiments/pqc/results/classical_vs_pqc.csv`

The underlying benchmark programs are located in:

`build/mlkem_benchmark`

`build/mldsa_benchmark`

---

## Interpretation

The results demonstrate that PQC algorithms can be
implemented and executed successfully in the experimental
environment.

The measurements also show that migration introduces
different computational and data-size characteristics.

In particular, ML-DSA signatures and keys are substantially
larger than ECDSA P-256 equivalents, while ML-KEM provides
fast key-establishment operations in this experimental
environment.

These observations will be investigated further during
hybrid TLS, SSH, network simulation, and statistical analysis
phases.

The measurements should not be interpreted as universal
performance characteristics because they depend on hardware,
software versions, implementation, compiler configuration,
and experimental conditions.
