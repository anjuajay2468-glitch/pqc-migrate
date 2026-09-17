# PQC-Migrate Phase 9 — Large-Scale Benchmarking

## 1. Objective

Phase 9 automates repeated TLS and SSH experiments across multiple controlled network conditions and consolidates the resulting measurements into a research dataset.

## 2. Dataset

- Total observations: **280**
- TLS observations: **140**
- SSH observations: **140**
- Classical observations: **140**
- Hybrid observations: **140**
- Successful observations: **280**

## 3. Network Profiles

- `bandwidth1mbps`: 40 observations
- `baseline`: 80 observations
- `latency100`: 40 observations
- `latency200`: 40 observations
- `loss1`: 40 observations
- `mobile`: 40 observations

## 4. Experimental Design

Each protocol was evaluated using two cryptographic configurations:

- Classical
- Hybrid

The experiments were repeated under six network profiles:

- `bandwidth1mbps`
- `baseline`
- `latency100`
- `latency200`
- `loss1`
- `mobile`

## 5. Statistical Analysis

For each protocol, cryptographic configuration, and network profile, the analysis calculates:

- Mean latency
- Median latency
- Standard deviation
- Minimum latency
- Maximum latency
- 95th percentile
- 99th percentile
- Coefficient of variation

## 6. Hybrid Overhead

Hybrid overhead is calculated relative to the classical configuration using:

**Overhead (%) = (Hybrid latency − Classical latency) / Classical latency × 100**

| Protocol | Network profile | Mean overhead |
|---|---|---:|
| SSH | bandwidth1mbps | 36.70% |
| SSH | baseline | 4.03% |
| SSH | latency100 | 1.97% |
| SSH | latency200 | 0.48% |
| SSH | loss1 | 70.31% |
| SSH | mobile | 3.32% |
| TLS | bandwidth1mbps | 63.09% |
| TLS | baseline | -60.21% |
| TLS | latency100 | -2.67% |
| TLS | latency200 | -0.86% |
| TLS | loss1 | -61.78% |
| TLS | mobile | 33.65% |

## 7. Variability

Variability analysis indicates that the effect of hybrid cryptography is not uniform across network conditions. Some constrained or lossy environments exhibit substantially higher latency variability.

The coefficient of variation and percentile measurements are retained to distinguish consistent overhead from individual high-latency observations.

## 8. Important Observations

- Network latency can dominate total connection establishment time, reducing the relative contribution of cryptographic processing.
- Bandwidth-constrained environments show a larger hybrid latency difference in several measurements.
- Lossy and mobile-like environments exhibit greater measurement variability.
- SSH and TLS do not exhibit identical sensitivity to hybrid cryptographic overhead.
- Hybrid performance should therefore be evaluated in the context of the surrounding network conditions rather than using a single fixed overhead value.

## 9. Reproducibility

The experiment is implemented using automated collection scripts under `experiments/large_scale/scripts/`.

Raw measurements are retained in `master_dataset.csv`, while derived statistical datasets are stored separately.

## 10. Limitations

- The current dataset measures handshake/connection latency rather than full application throughput.
- Several resource-utilization fields remain unavailable in the automated collector.
- Baseline currently contains more observations than the other network profiles because earlier baseline experiments were retained.
- The experiments use a controlled local environment and therefore do not represent all real-world network conditions.

## 11. Phase 9 Status

Dataset infrastructure: **PASS**
Automated TLS collection: **PASS**
Automated SSH collection: **PASS**
Multi-network collection: **PASS**
Dataset integrity validation: **PASS**
Statistical analysis: **PASS**
Hybrid overhead analysis: **PASS**
Variability analysis: **PASS**

**Phase 9 dataset consolidation: COMPLETE**