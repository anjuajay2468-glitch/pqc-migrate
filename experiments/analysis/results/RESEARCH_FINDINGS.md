# PQC-Migrate Research Findings

## Phase 10.10 — Statistical Interpretation

### Dataset

- 280 total observations
- 140 TLS observations
- 140 SSH observations
- 12 classical-vs-hybrid comparisons
- 12 statistical significance tests
- Mann–Whitney U test with Benjamini–Hochberg FDR correction
- Full dataset retained; potential outliers were not deleted

## Hypothesis Evaluation

### H1 — Hybrid PQC introduces performance overhead

**Result: Partially supported / protocol-dependent.**

SSH showed positive median latency overhead in all six tested network conditions, whereas TLS showed positive median overhead in only two of six conditions.

Therefore, the experiments do not support a universal claim that hybrid PQC always increases latency.

### H2 — Network conditions amplify PQC migration cost

**Result: Conditionally supported.**

Bandwidth limitation produced substantial relative overhead: 39.27% for SSH and 66.45% for TLS based on median latency.

However, increased latency or packet loss did not consistently increase relative hybrid overhead. The effect therefore depends on both protocol and network condition.

### H3 — Performance impact is protocol- and condition-dependent

**Result: Strongly supported.**

TLS exhibited both lower and higher hybrid latency depending on network condition, while SSH showed positive overhead across all conditions.

This demonstrates that PQC migration cost cannot be represented by a single fixed overhead value.

### H4 — Statistically significant differences are not universal

**Result: Supported.**

After FDR correction, 10 of 12 comparisons were statistically significant. The two mobile-condition comparisons were not statistically significant.

## Key Quantitative Findings

### SSH

- **baseline**: median overhead +29.72%, rank-biserial correlation -0.80, Large effect, Hybrid higher latency.
- **latency100**: median overhead +1.04%, rank-biserial correlation -0.92, Large effect, Hybrid higher latency.
- **latency200**: median overhead +0.51%, rank-biserial correlation -1.00, Large effect, Hybrid higher latency.
- **bandwidth1mbps**: median overhead +39.27%, rank-biserial correlation -1.00, Large effect, Hybrid higher latency.
- **loss1**: median overhead +28.68%, rank-biserial correlation -1.00, Large effect, Hybrid higher latency.
- **mobile**: median overhead +2.17%, rank-biserial correlation -0.10, Negligible effect, Hybrid higher latency.

### TLS

- **baseline**: median overhead -59.32%, rank-biserial correlation +1.00, Large effect, Hybrid lower latency.
- **latency100**: median overhead -2.58%, rank-biserial correlation +1.00, Large effect, Hybrid lower latency.
- **latency200**: median overhead -0.92%, rank-biserial correlation +0.80, Large effect, Hybrid lower latency.
- **bandwidth1mbps**: median overhead +66.45%, rank-biserial correlation -1.00, Large effect, Hybrid higher latency.
- **loss1**: median overhead -60.44%, rank-biserial correlation +1.00, Large effect, Hybrid lower latency.
- **mobile**: median overhead +9.00%, rank-biserial correlation -0.40, Medium effect, Hybrid higher latency.

## Statistical Significance

- **SSH / baseline**: raw p=1.6e-05, FDR-adjusted p=9.6e-05, SIGNIFICANT.
- **SSH / latency100**: raw p=0.000583, FDR-adjusted p=0.000777, SIGNIFICANT.
- **SSH / latency200**: raw p=0.000183, FDR-adjusted p=0.000274, SIGNIFICANT.
- **SSH / bandwidth1mbps**: raw p=0.000183, FDR-adjusted p=0.000274, SIGNIFICANT.
- **SSH / loss1**: raw p=0.000183, FDR-adjusted p=0.000274, SIGNIFICANT.
- **SSH / mobile**: raw p=0.73373, FDR-adjusted p=0.73373, NOT_SIGNIFICANT.
- **TLS / baseline**: raw p=0, FDR-adjusted p=1e-06, SIGNIFICANT.
- **TLS / latency100**: raw p=0.000183, FDR-adjusted p=0.000274, SIGNIFICANT.
- **TLS / latency200**: raw p=0.002827, FDR-adjusted p=0.003393, SIGNIFICANT.
- **TLS / bandwidth1mbps**: raw p=0.000183, FDR-adjusted p=0.000274, SIGNIFICANT.
- **TLS / loss1**: raw p=0.000183, FDR-adjusted p=0.000274, SIGNIFICANT.
- **TLS / mobile**: raw p=0.140465, FDR-adjusted p=0.153235, NOT_SIGNIFICANT.

## Interpretation Caveats

1. Statistical significance does not imply practical significance.
2. Negative TLS overhead values should not be interpreted as proof that hybrid cryptography is inherently faster.
3. Potential outliers were retained in the primary dataset.
4. The Phase 9 automated dataset primarily contains latency measurements; CPU, memory, payload, and packet fields are not complete enough to support broad resource-overhead claims.
5. Results describe the tested experimental environment and configurations and should not be generalized to all systems.

## Primary Research Conclusion

The experiments indicate that the performance impact of hybrid post-quantum cryptography is context-dependent. SSH exhibited consistent positive latency overhead, while TLS showed substantial variation across network conditions. Bandwidth limitation produced the clearest increase in relative hybrid overhead for both protocols. These results support evaluating PQC migration under multiple realistic network conditions rather than using a single benchmark environment.
