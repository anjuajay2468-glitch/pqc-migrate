# PQC-Migrate Hybrid Cryptography Results

## Experiment

This experiment evaluates a hybrid key-establishment construction
combining classical X25519 with post-quantum ML-KEM-768.

The hybrid construction derives a final 32-byte secret using SHA-256
over the two independent shared-secret contributions and a domain
separation label.

## Configuration

| Parameter | Value |
|---|---|
| Classical component | X25519 |
| PQC component | ML-KEM-768 |
| Combination function | SHA-256 |
| Domain label | PQC-Migrate-HYBRID-X25519-MLKEM768 |
| Iterations | 1000 |

## Correctness

All 1000 validation iterations successfully established matching
component and hybrid shared secrets.

| Test | Result |
|---|---:|
| X25519 agreement | 1000 / 1000 |
| ML-KEM agreement | 1000 / 1000 |
| Hybrid agreement | 1000 / 1000 |
| X25519 tampering detection | 100 / 100 |
| ML-KEM tampering detection | 100 / 100 |

Overall hybrid correctness: **PASS**

## Performance

| Operation | Average (us) | Minimum (us) | Maximum (us) |
|---|---:|---:|---:|
| X25519 | 50.714 | 26.823 | 910.457 |
| ML-KEM-768 | 42.261 | 22.442 | 723.183 |
| Hybrid combination | 1.505 | 0.378 | 96.488 |
| Total hybrid operation | 94.480 | 49.645 | 1032.814 |

All 1000 benchmark iterations completed successfully.

## Interpretation

The hybrid construction combines both independent key-establishment
contributions before deriving the final shared secret.

The measured combination step is substantially smaller than either
cryptographic operation. Its average cost was 1.505 microseconds,
while the total hybrid operation averaged 94.480 microseconds.

The total hybrid cost is therefore primarily determined by performing
both the X25519 and ML-KEM-768 operations rather than by the final
SHA-256 combination.

Compared with X25519 alone, the hybrid construction introduces
additional computational work because both key-establishment
mechanisms are executed.

However, the hybrid approach provides a migration-oriented design in
which a classical and post-quantum component contribute jointly to
the resulting secret.

## Research Significance

This experiment establishes three important properties required for
the later migration experiments:

1. The classical and post-quantum components can be executed
   independently.
2. Their outputs can be combined into a single derived secret.
3. The resulting hybrid construction can be validated and measured
   reproducibly.

The hybrid construction will later be evaluated at the TLS protocol
level and under controlled network conditions.

## Limitations

This experiment measures cryptographic computation in isolation.

It does not yet measure:

- TLS handshake overhead
- Network transmission overhead
- Certificate-size overhead
- CPU utilization
- Memory utilization
- High-latency network behavior
- Packet loss
- Throughput

These measurements are addressed in later phases.

## Output Files

- `hybrid_performance.csv` — detailed hybrid benchmark measurements
- `hybrid_comparison.csv` — classical, PQC, and hybrid comparison
