# PQC-Migrate Phase 4 — PQC Implementation

## Objective

Evaluate the implementation characteristics of standardized
post-quantum cryptographic algorithms before integrating them
into hybrid protocols.

## Algorithms

### ML-KEM-768

Key establishment:

- Key generation
- Encapsulation
- Decapsulation

Measurements:

- Execution time
- Public key size
- Secret key size
- Ciphertext size
- Shared secret size
- Correctness

### ML-DSA-65

Digital signatures:

- Key generation
- Signing
- Verification

Measurements:

- Execution time
- Public key size
- Secret key size
- Signature size
- Correctness

## Experimental Principle

All PQC measurements must be reproducible and must include
correctness verification.

Results will be stored under:

`experiments/pqc/results/`

The experiments will use the project-supported liboqs
implementation and standardized algorithm parameter sets.

