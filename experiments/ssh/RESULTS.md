# PQC-Migrate SSH Experimental Results

## 1. Objective

This experiment evaluates the practical impact of migrating SSH
key exchange from classical X25519 to the OpenSSH hybrid
X25519 + Streamlined NTRU Prime mechanism.

The experiment measures:

- SSH connection establishment latency
- CPU usage
- client memory usage
- transmitted TCP payload
- IP packet count
- hybrid traffic overhead
- successful connection rate
- negotiated key-exchange correctness

The hybrid SSH key-exchange algorithm used is:

`sntrup761x25519-sha512@openssh.com`

---

## 2. Experimental Environment

Protocol:

- SSH-2
- OpenSSH 9.6p1
- Ubuntu 24.04.4 LTS
- x86_64
- Local loopback interface (`lo`)
- SSH server port 22

Classical configuration:

`curve25519-sha256`

Hybrid configuration:

`sntrup761x25519-sha512@openssh.com`

Hybrid components:

- Classical: X25519
- PQ component: Streamlined NTRU Prime

A dedicated local SSH test account was used for the experiments.

---

## 3. Classical SSH Baseline

Configuration:

- Classical SSH
- KEX: `curve25519-sha256`
- 100 connection attempts

Results:

| Metric | Result |
|---|---:|
| Successful connections | 100/100 |
| Average connection latency | 207311 us |
| Minimum latency | 184897 us |
| Maximum latency | 433975 us |
| Average elapsed time | 0.188600 s |
| Average user CPU | 0.001500 s |
| Average system CPU | 0.000100 s |
| Maximum client RSS | 8344 KB |
| TCP payload | 5234 bytes |
| IP packets | 39 |

---

## 4. Hybrid SSH

Configuration:

- Hybrid SSH
- KEX: `sntrup761x25519-sha512@openssh.com`
- Classical component: X25519
- PQ component: Streamlined NTRU Prime
- 100 connection attempts

Results:

| Metric | Result |
|---|---:|
| Successful connections | 100/100 |
| Average connection latency | 301296 us |
| Minimum latency | 241006 us |
| Maximum latency | 864382 us |
| Average elapsed time | 0.225600 s |
| Average user CPU | 0.056200 s |
| Average system CPU | 0.000300 s |
| Maximum client RSS | 8356 KB |
| TCP payload | 7450 bytes |
| IP packets | 39 |

Negotiated KEX:

`sntrup761x25519-sha512@openssh.com`

---

## 5. Traffic Analysis

The packet captures were collected on the local loopback interface.

| Metric | Classical | Hybrid |
|---|---:|---:|
| TCP payload | 5234 B | 7450 B |
| IP packets | 39 | 39 |
| Additional payload | 0 B | 2216 B |
| Payload overhead | 0.00% | 42.34% |

The hybrid configuration transmitted 2216 additional TCP payload bytes,
corresponding to a measured payload increase of 42.34%.

The number of IP packets remained unchanged at 39 in both captures.

This demonstrates that the additional hybrid key-exchange material
increased the amount of data transmitted without increasing the
packet count in this particular local experiment.

---

## 6. Resource Analysis

The hybrid configuration required more client CPU time than the
classical configuration.

Average user CPU:

- Classical: 0.001500 s
- Hybrid: 0.056200 s

Maximum client RSS remained almost unchanged:

- Classical: 8344 KB
- Hybrid: 8356 KB

The measured peak RSS difference was therefore only 12 KB.

Average elapsed connection time increased from 0.188600 s to
0.225600 s.

This corresponds to an approximately 19.1% increase in elapsed
connection time in this experiment.

---

## 7. Correctness

All 100 classical SSH connections completed successfully.

All 100 hybrid SSH connections completed successfully.

The hybrid benchmark explicitly requested:

`sntrup761x25519-sha512@openssh.com`

and the negotiated KEX was confirmed as:

`sntrup761x25519-sha512@openssh.com`

Therefore the experiment successfully demonstrated an actual
hybrid SSH key exchange rather than merely measuring a classical
connection.

---

## 8. Interpretation

The results show a measurable migration cost when using hybrid SSH.

The hybrid configuration increased:

- connection establishment latency
- user CPU consumption
- transmitted TCP payload

while producing almost no change in peak client RSS in this
local test environment.

The traffic increase was particularly visible, with a measured
42.34% increase in TCP payload.

However, these measurements were obtained on a localhost loopback
connection. Therefore they should not be interpreted as estimates
of Internet-wide performance.

Network latency, bandwidth limitations, packet loss, and system
load have not yet been varied.

Those factors will be investigated in the network simulation phase.

---

## 9. Reproducibility

Classical benchmark:

`./experiments/ssh/scripts/classical_ssh_benchmark.sh`

Hybrid benchmark:

`./experiments/ssh/scripts/hybrid_ssh_benchmark.sh`

Classical resource benchmark:

`./experiments/ssh/scripts/classical_ssh_resource_benchmark.sh`

Hybrid resource benchmark:

`./experiments/ssh/scripts/hybrid_ssh_resource_benchmark.sh`

Packet captures:

- `captures/classical_ssh_x25519.pcap`
- `captures/hybrid_ssh_sntrup761x25519.pcap`

Traffic analysis:

- `results/ssh_traffic_comparison.csv`
- `results/ssh_capture_metadata.txt`

Consolidated dataset:

- `results/ssh_final_comparison.csv`

---

## 10. Limitations

The SSH experiment uses the OpenSSH hybrid mechanism
`sntrup761x25519-sha512@openssh.com`.

This is distinct from the ML-KEM-768 hybrid mechanism used in the
TLS experiment.

Therefore the TLS and SSH results should not be treated as direct
algorithm-for-algorithm comparisons.

The experiments are also performed on a local WSL2 environment
using loopback networking.

Further network-condition experiments are required before making
general performance conclusions.

---

## 11. Phase 7 Conclusion

Phase 7 successfully demonstrated and measured both classical and
hybrid SSH connections.

The experiment provides evidence for:

- successful classical SSH operation
- successful hybrid SSH operation
- negotiated hybrid KEX
- latency measurements
- CPU measurements
- memory measurements
- network traffic measurements
- reproducible packet captures

Phase 7 SSH integration: COMPLETE.
