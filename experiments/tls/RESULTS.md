# PQC-Migrate TLS Experimental Results

## Objective

This experiment evaluates TLS 1.3 migration from classical X25519 key exchange to the hybrid X25519 + ML-KEM-768 key exchange.

The experiment measures handshake correctness, latency, network traffic overhead, CPU usage, and memory usage.

## Classical TLS Baseline

Configuration:
- TLS 1.3
- X25519 key exchange
- RSA-2048 certificate
- TLS_AES_256_GCM_SHA384
- System OpenSSL 3.0.13
- 100 handshake iterations

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
- Classical component: X25519
- PQC component: ML-KEM-768
- RSA-2048 certificate
- TLS_AES_256_GCM_SHA384
- OpenSSL 3.5.4
- 100 handshake iterations

| Metric | Result |
|---|---:|
| Successful handshakes | 100/100 |
| Average latency | 8,170 us |
| Minimum latency | 6,832 us |
| Maximum latency | 10,829 us |

Negotiated TLS group: `X25519MLKEM768`

## Latency Comparison

| Configuration | Average | Minimum | Maximum |
|---|---:|---:|---:|
| Classical X25519 | 26,211 us | 21,956 us | 32,626 us |
| Hybrid X25519MLKEM768 | 8,170 us | 6,832 us | 10,829 us |

The hybrid configuration was faster in this particular testbed. This must not be interpreted as evidence that hybrid cryptography intrinsically reduces cryptographic computation because the configurations use different OpenSSL versions and include complete local TLS process behavior.

## TLS Traffic Comparison

| Configuration | Key Exchange | TCP Payload | IP Packets |
|---|---|---:|---:|
| Classical | X25519 | 2,386 bytes | 16 |
| Hybrid | X25519MLKEM768 | 4,642 bytes | 16 |

Additional hybrid payload: **2,256 bytes**

Hybrid payload overhead: **94.55%**

The packet count remained unchanged while the hybrid handshake carried substantially more TCP payload.

Capture files:
- `captures/classical_tls_x25519.pcap`
- `captures/hybrid_tls_x25519mlkem768.pcap`

## Resource Measurement

Resource measurements were collected by running the TLS handshake benchmark under GNU `/usr/bin/time`.

### Classical X25519

| Metric | Result |
|---|---:|
| Benchmark elapsed time | 3.17 s |
| User CPU | 2.27 s |
| System CPU | 0.42 s |
| Maximum RSS | 8,704 KB |

### Hybrid X25519MLKEM768

| Metric | Result |
|---|---:|
| Benchmark elapsed time | 1.01 s |
| User CPU | 0.43 s |
| System CPU | 0.28 s |
| Maximum RSS | 9,600 KB |

These are benchmark-process measurements, not isolated measurements of the cryptographic primitives. The classical configuration uses system OpenSSL 3.0.13 while the hybrid configuration uses project-local OpenSSL 3.5.4.

## Correctness

Classical TLS: **100/100 successful handshakes**.

Hybrid TLS: **100/100 successful handshakes**.

The hybrid connection negotiated `X25519MLKEM768`, confirming successful TLS 1.3 hybrid key exchange.

## Final Comparison

| Property | Classical | Hybrid |
|---|---|---|
| TLS version | TLS 1.3 | TLS 1.3 |
| Key exchange | X25519 | X25519MLKEM768 |
| PQC component | None | ML-KEM-768 |
| Certificate | RSA-2048 | RSA-2048 |
| Cipher | AES-256-GCM | AES-256-GCM |
| Successful handshakes | 100/100 | 100/100 |
| Average latency | 26,211 us | 8,170 us |
| TCP payload | 2,386 B | 4,642 B |
| IP packets | 16 | 16 |
| Maximum RSS | 8,704 KB | 9,600 KB |

## Limitations

1. Classical and hybrid configurations use different OpenSSL versions.
2. Measurements include process and operating-system effects.
3. Network measurements were collected over the local loopback interface.
4. Traffic comparison is based on one complete capture per configuration.
5. Resource measurements are benchmark-process measurements.
6. Self-signed RSA-2048 certificates were used in the local testbed.
7. Results may vary with CPU load, scheduling, OpenSSL builds, and system configuration.

## Reproducibility

Classical TLS:
`./experiments/tls/scripts/tls_handshake_benchmark.sh`

PQC TLS:
`./experiments/tls/scripts/pqc_tls_handshake_benchmark.sh`

Hybrid TLS:
`./experiments/tls/scripts/hybrid/tls_hybrid_handshake_benchmark.sh`

Hybrid TLS negotiation:
`./experiments/tls/scripts/hybrid/tls_hybrid_client.sh`

## Conclusion

The experiment demonstrates a working TLS 1.3 migration path from classical X25519 to the hybrid X25519MLKEM768 group.

The hybrid configuration successfully negotiated TLS 1.3, completed 100/100 handshake attempts, retained X25519, added ML-KEM-768 protection, increased observed TCP payload by 94.55%, and was successfully captured and analyzed at the packet level.
