# PQC TLS OpenSSL Environment

The PQC TLS experiments require OpenSSL 3.5.4 or later.

For this project, OpenSSL 3.5.4 was built as a project-local dependency
and was intentionally not committed to the repository.

The system OpenSSL installation was not modified.

Required capabilities:

- ML-KEM-768
- TLS 1.3
- X25519MLKEM768 hybrid key exchange

The exact build environment is documented in:

`results/metadata/environment.txt`
