# Phase 10 — Statistical Analysis & Research Findings

Generated: 2026-09-02T14:45:05

## 1. Objective

Phase 10 analyzes the Phase 9 large-scale PQC migration benchmark dataset using descriptive statistics, classical-vs-hybrid comparisons, network-condition analysis, outlier analysis, statistical significance testing, effect-size analysis, visualization, and hypothesis evaluation.

## 2. Dataset

- Total observations: 280
- TLS observations: 140
- SSH observations: 140
- Classical observations: 0
- Hybrid observations: 0
- Successful observations: 280

The complete Phase 9 dataset was retained as the primary analysis dataset.
Potential outliers were identified using the IQR rule but were not deleted.

## 3. Statistical Methods

- Descriptive statistics: N, mean, median, standard deviation, minimum, maximum, range, P95, P99, coefficient of variation.
- Classical vs Hybrid comparison: absolute and percentage differences in latency statistics.
- Network-condition analysis: change relative to the corresponding baseline.
- Outlier detection: 1.5 × IQR rule.
- Statistical significance: two-sided Mann–Whitney U test.
- Multiple-comparison correction: Benjamini–Hochberg FDR.
- Effect size: rank-biserial correlation.
- Primary significance threshold: alpha = 0.05.

## 4. Main Research Findings

### H1 — Hybrid latency overhead

Partially supported and protocol-dependent. SSH showed positive median latency overhead for all tested network profiles, whereas TLS showed mixed behavior.

### H2 — Network conditions amplify migration cost

Conditionally supported. Bandwidth limitation produced clear relative overhead for both protocols, while latency and packet-loss conditions did not consistently increase relative hybrid overhead.

### H3 — Protocol and network context matter

Strongly supported. The observed hybrid performance impact varied substantially between TLS and SSH and across network conditions.

### H4 — Significant differences are not universal

Supported. Mobile conditions were not statistically significant for either TLS or SSH after testing, while most other comparisons were significant.

## 5. Significance Results

10 of 12 classical-vs-hybrid comparisons were statistically significant after Benjamini–Hochberg FDR correction. The two non-significant comparisons were SSH-mobile and TLS-mobile.

## 6. Important Interpretation Constraints

Statistical significance does not imply practical significance. Large statistical effects must be interpreted together with the absolute latency differences.

Negative TLS hybrid-overhead values are dataset-specific observations and should not be interpreted as evidence that hybrid TLS inherently improves performance.

Potential outliers were retained in the primary dataset. Outlier analysis is used to characterize variability and tail behavior rather than selectively removing observations.

The Phase 9 automated dataset primarily contains latency measurements. CPU, memory, TCP payload, and packet-count fields are incomplete and therefore are not used to claim comprehensive resource overhead.

Results describe the tested implementation, hardware/software environment, cryptographic algorithms, and network profiles and should not be generalized beyond those experimental conditions without additional validation.

## 7. Reproducibility

All six core statistical analysis scripts were re-executed successfully. SHA-256 hashes of all seven core CSV outputs were identical before and after re-execution, establishing deterministic analysis outputs.

## 8. Artifact Validation

- PASS — Dataset exists
- PASS — Dataset rows = 280
- PASS — Dataset columns = 17
- PASS — All observations successful
- PASS — TLS observations = 140
- PASS — SSH observations = 140
- PASS — Classical observations = 140
- PASS — Hybrid observations = 140
- PASS — Result artifact: descriptive_statistics.csv
- PASS — Result artifact: classical_vs_hybrid.csv
- PASS — Result artifact: network_condition_effects.csv
- PASS — Result artifact: outlier_summary.csv
- PASS — Result artifact: outlier_observations.csv
- PASS — Result artifact: significance_testing.csv
- PASS — Result artifact: effect_size_analysis.csv
- PASS — Result artifact: RESEARCH_FINDINGS.md
- PASS — Plot artifact: figure_1_ssh_median_latency.png
- PASS — Plot artifact: figure_1_tls_median_latency.png
- PASS — Plot artifact: figure_2_ssh_hybrid_overhead.png
- PASS — Plot artifact: figure_2_tls_hybrid_overhead.png
- PASS — Plot artifact: figure_3_effect_vs_overhead.png

**Overall Phase 10 validation: PASS**
