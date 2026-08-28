# PQC-Migrate Phase 5 — Hybrid Cryptography

## Objective

Evaluate hybrid cryptographic key establishment combining a
classical mechanism with a post-quantum mechanism.

The primary experimental configuration is:

X25519 + ML-KEM-768

The purpose is to investigate whether hybrid key establishment
provides a practical migration path from classical cryptography
to post-quantum cryptography.

## Configurations

### Classical

X25519

### Post-Quantum

ML-KEM-768

### Hybrid

X25519 + ML-KEM-768

## Experimental Questions

1. What computational overhead does hybrid key establishment add?
2. How much additional key material must be transmitted?
3. Does the hybrid construction preserve shared-secret correctness?
4. How does hybrid performance compare with classical and PQC-only
   configurations?

## Measurements

The experiments will measure:

- Key generation time
- Key establishment time
- Shared-secret derivation time
- Public key material size
- Ciphertext material size
- Shared-secret size
- Correctness
- Hybrid overhead

## Experimental Principle

The hybrid mechanism will combine independently derived classical
and post-quantum shared secrets using a cryptographically secure
key-combination mechanism.

The implementation will clearly distinguish:

- Classical security contribution
- Post-quantum security contribution
- Combination mechanism
- Resulting hybrid secret

Results will be stored under:

`experiments/hybrid/results/`
