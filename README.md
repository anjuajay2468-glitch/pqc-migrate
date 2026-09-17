# PQC-Migrate

## Evidence-Based Post-Quantum Cryptographic Migration Benchmarking Framework

**PQC-Migrate** is a research-oriented experimental framework for studying the performance and deployment trade-offs of post-quantum cryptographic migration in secure communication protocols.

The project evaluates **classical and hybrid cryptographic configurations across TLS and SSH**, subjects them to controlled network conditions, analyzes the resulting measurements statistically, and uses the empirical evidence to construct an **explainable migration decision framework**.

> **Research focus:** Post-Quantum Cryptography | Applied Cryptography | Network Security | Secure Protocols | Performance Benchmarking | Cryptographic Migration

---

## Research Question

> **How does the performance impact of post-quantum cryptographic migration vary across secure communication protocols and network conditions, and how can empirical evidence be transformed into an explainable migration decision framework?**

### Supporting Research Questions

- How does hybrid post-quantum cryptography compare with classical cryptography in TLS and SSH?
- How do latency, bandwidth limitations, packet loss, and mobile-like conditions affect migration overhead?
- Which observed differences are statistically significant, and how large are their practical effects?
- How can empirical benchmark evidence be incorporated into an explainable migration decision process?

---

# Research at a Glance

| Dimension | Evaluation |
|---|---|
| **Protocols** | TLS, SSH |
| **Classical TLS** | X25519 |
| **Hybrid TLS** | X25519MLKEM768 |
| **Classical SSH** | curve25519-sha256 |
| **Hybrid SSH** | sntrup761x25519-sha512@openssh.com |
| **Network profiles** | 6 |
| **Benchmark observations** | **280** |
| **Statistical testing** | Mannâ€“Whitney U |
| **Multiple-comparison correction** | Benjaminiâ€“Hochberg FDR |
| **Effect-size analysis** | Rank-biserial correlation |
| **Outlier analysis** | IQR-based |
| **Decision framework** | Evidence-based migration model |
| **Framework validation** | 432 decision combinations + benchmark validation |
| **Research status** | Phases 0â€“11 complete; paper in progress |

---

# Why This Project?

Post-quantum cryptography introduces new cryptographic primitives and protocol configurations, but migration is not simply a matter of replacing one algorithm with another.

The practical impact can depend on:

- the communication protocol,
- cryptographic configuration,
- network latency,
- available bandwidth,
- packet loss,
- compatibility requirements,
- performance sensitivity,
- migration urgency, and
- variability in observed measurements.

PQC-Migrate investigates these factors experimentally and connects **measured performance evidence** with **migration decision support**.

The objective is not to prescribe a universal migration strategy, but to provide a reproducible methodology for evaluating migration trade-offs under defined experimental conditions.

---

# What I Built

PQC-Migrate was developed as an end-to-end experimental and analytical pipeline.

### 1. Cryptographic Benchmarking

Implemented experiments comparing classical and hybrid cryptographic configurations for secure communication.

### 2. TLS Integration

Evaluated classical X25519 TLS and the hybrid `X25519MLKEM768` configuration.

### 3. SSH Integration

Evaluated classical `curve25519-sha256` SSH and the hybrid `sntrup761x25519-sha512@openssh.com` configuration.

### 4. Network Simulation

Created controlled network profiles representing:

- baseline connectivity,
- 100 ms latency,
- 200 ms latency,
- 1 Mbps bandwidth,
- 1% packet loss,
- mobile-like conditions.

### 5. Large-Scale Data Collection

Built automated experiment collectors and consolidated the measurements into a validated dataset containing **280 observations**.

### 6. Statistical Analysis

Built an analysis pipeline covering:

- descriptive statistics,
- median and percentile analysis,
- Mannâ€“Whitney U testing,
- Benjaminiâ€“Hochberg FDR correction,
- rank-biserial effect sizes,
- IQR-based outlier detection,
- coefficient-of-variation analysis.

### 7. Evidence Model

Converted benchmark measurements into structured evidence describing protocol- and network-specific migration behavior.

### 8. Migration Decision Engine

Implemented an explainable decision model that considers security requirements, compatibility, performance sensitivity, migration urgency, protocol, network profile, and measured evidence.

### 9. Framework Validation

Validated the decision model across **432 combinations of decision inputs** and against the measured benchmark scenarios.

---

# System Architecture

```text
                    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                    â”‚ Classical Cryptography      â”‚
                    â”‚ X25519 / Curve25519         â”‚
                    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                   â”‚
                                   â”‚
                    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                    â”‚ Hybrid PQC Cryptography     â”‚
                    â”‚ X25519MLKEM768 /             â”‚
                    â”‚ sntrup761x25519-sha512      â”‚
                    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                   â”‚
                                   â–¼
                    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                    â”‚       TLS / SSH Layer       â”‚
                    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                   â”‚
                                   â–¼
                    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                    â”‚   Network Condition Layer   â”‚
                    â”‚                             â”‚
                    â”‚ Baseline                    â”‚
                    â”‚ 100 ms / 200 ms latency     â”‚
                    â”‚ 1 Mbps bandwidth            â”‚
                    â”‚ 1% packet loss              â”‚
                    â”‚ Mobile-like profile        â”‚
                    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                   â”‚
                                   â–¼
                    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                    â”‚     Benchmark Collection    â”‚
                    â”‚        280 observations     â”‚
                    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                   â”‚
                                   â–¼
             â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
             â”‚                     â”‚                     â”‚
             â–¼                     â–¼                     â–¼
      Descriptive Stats      Significance Tests      Variability
             â”‚                     â”‚                     â”‚
             â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                   â–¼
                    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                    â”‚       Evidence Model        â”‚
                    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                   â”‚
                                   â–¼
                    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                    â”‚ Migration Decision Engine   â”‚
                    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                   â”‚
                                   â–¼
                    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                    â”‚ Explainable Migration Path  â”‚
                    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

# Experimental Methodology

## Protocol Evaluation

### TLS

| Configuration | Key Exchange |
|---|---|
| Classical | X25519 |
| Hybrid | X25519MLKEM768 |

### SSH

| Configuration | Key Exchange |
|---|---|
| Classical | curve25519-sha256 |
| Hybrid | sntrup761x25519-sha512@openssh.com |

The experiments compare protocol behavior while keeping the evaluation focused on the defined classical and hybrid configurations.

---

## Network Conditions

Each protocol/configuration pair was evaluated under multiple network environments:

| Profile | Purpose |
|---|---|
| **Baseline** | Reference environment |
| **Latency 100 ms** | Moderate network delay |
| **Latency 200 ms** | High network delay |
| **Bandwidth 1 Mbps** | Bandwidth-constrained environment |
| **Packet Loss 1%** | Lossy network environment |
| **Mobile-like** | Combined constrained/mobile-style conditions |

This allows migration behavior to be examined beyond a single idealized local-network measurement.

---

# Benchmark Dataset

Phase 9 consolidated the experimental measurements into:

**280 observations**

covering:

- TLS and SSH
- classical and hybrid configurations
- six network profiles
- repeated measurements
- dataset validation
- statistical summaries
- hybrid-overhead analysis
- variability analysis.

The dataset and generated analysis artifacts are maintained in:

```text
experiments/large_scale/
```

See:

- `experiments/large_scale/README.md`
- `experiments/large_scale/PHASE9_REPORT.md`
- `experiments/large_scale/results/master_dataset.csv`
- `experiments/large_scale/results/statistical_summary.csv`
- `experiments/large_scale/results/hybrid_overhead_analysis.csv`
- `experiments/large_scale/results/variability_analysis.csv`

---

# Statistical Analysis

The benchmark data is analyzed using a dedicated statistical pipeline.

## Descriptive Analysis

The analysis calculates:

- sample size,
- mean,
- median,
- standard deviation,
- percentiles,
- variability measures.

## Significance Testing

Classical and hybrid measurements are compared using the **two-sided Mannâ€“Whitney U test**.

Because multiple comparisons are performed, the analysis applies **Benjaminiâ€“Hochberg false-discovery-rate correction**.

## Effect Size

Statistical significance is complemented with **rank-biserial effect-size analysis** to characterize the magnitude and direction of observed differences.

## Outlier Analysis

Potential outliers are identified using the **1.5 Ã— IQR rule**.

Outliers are retained rather than automatically deleted so that their effect on the experimental interpretation can be examined.

## Practical Interpretation

The project distinguishes:

> **statistical significance â‰  practical significance**

A statistically significant difference is therefore not automatically interpreted as a meaningful deployment disadvantage.

Detailed outputs are available in:

```text
experiments/analysis/
```

---

# Research Findings

The completed analysis indicates that the performance impact of hybrid post-quantum migration is **context-dependent** rather than a single fixed overhead.

The observed behavior varies with:

- protocol,
- network condition,
- measurement variability, and
- experimental configuration.

The analysis found statistically significant differences in many protocol/network comparisons, while some mobile-condition comparisons did not reach statistical significance after correction.

The results therefore support evaluating PQC migration under representative deployment conditions rather than relying on a single benchmark number.

Detailed findings:

```text
experiments/analysis/results/RESEARCH_FINDINGS.md
experiments/analysis/results/PHASE10_FINAL_REPORT.md
```

Figures:

```text
experiments/analysis/plots/
```

---

# Migration Decision Framework

The final stage of the experimental pipeline converts benchmark evidence into an explainable migration model.

## Decision Inputs

The framework considers:

```text
Security Requirement
Legacy Compatibility
Performance Sensitivity
Migration Urgency
Protocol
Network Profile
Measured Benchmark Evidence
```

## Decision Outputs

The current model supports four strategy categories:

```text
CLASSICAL
HYBRID_TRANSITION
PQC
HYBRID_OR_PQC_EVALUATION
```

The framework does **not** treat these categories as universally optimal choices. Instead, they represent explainable outcomes of the defined decision rules and experimental evidence.

### Framework Validation

The decision engine was evaluated across:

**432 combinations of decision inputs**

and separately validated against the measured benchmark scenarios.

Artifacts:

```text
experiments/migration_framework/
```

Key files:

- `results/FRAMEWORK_SPEC.md`
- `results/DECISION_MODEL_SPEC.md`
- `results/MIGRATION_PATHS.md`
- `results/CASE_STUDIES.md`
- `results/evidence_model.csv`
- `results/migration_decisions.csv`
- `results/decision_validation.csv`
- `results/benchmark_validation.csv`
- `results/PHASE11_FINAL_REPORT.md`

---

# Research Pipeline

```text
Phase 0
Research Foundation
        â†“
Phase 1
PQC Deep Dive
        â†“
Phase 2
Experimental Environment
        â†“
Phase 3
Classical Cryptography Baseline
        â†“
Phase 4
PQC Implementation
        â†“
Phase 5
Hybrid Cryptography
        â†“
Phase 6
TLS Integration
        â†“
Phase 7
SSH Integration
        â†“
Phase 8
Network Simulation
        â†“
Phase 9
Large-Scale Benchmarking
        â†“
Phase 10
Statistical Analysis
        â†“
Phase 11
Migration Decision Framework
        â†“
Phase 12
Research Paper & Publication
```

---

# Repository Structure

```text
pqc-migrate/
â”‚
â”œâ”€â”€ benchmarks/                     # Benchmarking utilities
â”œâ”€â”€ configs/                        # Experimental configuration
â”œâ”€â”€ data/                           # Project data
â”œâ”€â”€ docs/                           # Documentation
â”‚
â”œâ”€â”€ experiments/
â”‚   â”œâ”€â”€ analysis/                   # Statistical analysis & findings
â”‚   â”œâ”€â”€ large_scale/                # Large-scale benchmark collection
â”‚   â”œâ”€â”€ migration_framework/        # Migration decision framework
â”‚   â”œâ”€â”€ network/                    # Network simulation
â”‚   â”œâ”€â”€ ssh/                        # SSH experiments
â”‚   â””â”€â”€ tls/                        # TLS experiments
â”‚
â”œâ”€â”€ include/                        # Header files
â”œâ”€â”€ results/                        # Experimental results
â”œâ”€â”€ scripts/                        # Utility & validation scripts
â”œâ”€â”€ src/                            # Source code
â”œâ”€â”€ tests/                          # Tests
â”œâ”€â”€ third_party/                    # Third-party integration documentation
â”‚
â”œâ”€â”€ CMakeLists.txt                  # Build configuration
â”œâ”€â”€ README.md                       # Project overview
â””â”€â”€ .gitignore                      # Repository exclusions
```

---

# Reproducibility

Reproducibility is a central part of the project.

The repository includes:

- experimental configuration,
- benchmark scripts,
- network profiles,
- automated dataset collectors,
- validation scripts,
- statistical analysis scripts,
- generated benchmark datasets,
- research reports,
- figures,
- framework specifications, and
- framework validation artifacts.

The Phase 10 analysis environment used:

- Python 3.12.3
- pandas
- NumPy
- SciPy
- Matplotlib
- statsmodels

Local virtual environments, build directories, external dependency source trees, generated logs, and private credentials are excluded from version control.

---

# Limitations

The current results are specific to the evaluated:

- cryptographic configurations,
- protocol implementations,
- software environment,
- hardware/environment,
- network profiles, and
- experimental methodology.

The Phase 9 dataset contains complete latency measurements, while some resource-level fields such as CPU time, memory, packet counts, and TCP payload measurements are not populated for every observation.

Consequently, the current findings should be interpreted as evidence from the defined experimental environment rather than as universal performance guarantees for all PQC deployments.

---

# Research Status

| Phase | Status |
|---|---|
| Phase 0 â€” Research Foundation | âœ… Complete |
| Phase 1 â€” PQC Deep Dive | âœ… Complete |
| Phase 2 â€” Experimental Environment | âœ… Complete |
| Phase 3 â€” Classical Baseline | âœ… Complete |
| Phase 4 â€” PQC Implementation | âœ… Complete |
| Phase 5 â€” Hybrid Cryptography | âœ… Complete |
| Phase 6 â€” TLS Integration | âœ… Complete |
| Phase 7 â€” SSH Integration | âœ… Complete |
| Phase 8 â€” Network Simulation | âœ… Complete |
| Phase 9 â€” Large-Scale Benchmarking | âœ… Complete |
| Phase 10 â€” Statistical Analysis | âœ… Complete |
| Phase 11 â€” Migration Framework | âœ… Complete |
| Phase 12 â€” Research Paper | ðŸ”¬ In Progress |

---

# Research Paper

The completed experimental work is being developed into a research manuscript tentatively titled:

> **An Evidence-Based Framework for Post-Quantum Cryptographic Migration Under Heterogeneous Network Conditions**

The manuscript will consolidate:

1. Research motivation
2. Related work
3. Research questions and hypotheses
4. Experimental methodology
5. TLS and SSH benchmark implementation
6. Network-condition experiments
7. Statistical analysis
8. Migration decision framework
9. Framework validation
10. Limitations
11. Future research directions

---

# Technologies

### Cryptography & Protocols
- OpenSSL
- Post-quantum cryptography
- ML-KEM
- X25519
- TLS
- SSH

### Systems & Experimentation
- Linux / WSL
- Bash
- C / C++
- Python
- Network traffic and condition simulation

### Data & Statistics
- Python
- pandas
- NumPy
- SciPy
- statsmodels
- Matplotlib

### Development
- Git
- CMake
- Automated experiment scripts
- Validation tooling

---

# Project Philosophy

PQC-Migrate follows a simple research principle:

> **Measure first. Analyze rigorously. Make the evidence explainable.**

Rather than treating post-quantum migration as a single algorithm-selection problem, the project studies the interaction between cryptographic configuration, secure communication protocols, network conditions, statistical behavior, and deployment constraints.

---

# License

License information will be added before public release.

---

## Author

**Anju Ajayakumar**

B.Tech â€” Electronics & Computer Science Engineering

Research interests include:

- Post-Quantum Cryptography
- Systems & Distributed Systems
- Cloud Infrastructure
- Network Security
- Applied Cryptography
- Secure Systems


