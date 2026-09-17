# PQC-Migrate — Migration Decision Model Specification

## 1. Purpose

The migration decision model converts experimental performance evidence and
deployment constraints into an explainable migration recommendation.

The model is a decision-support mechanism, not a replacement for security
engineering or organizational cryptographic policy.

---

## 2. Candidate Strategies

The model evaluates:

- Classical
- Hybrid
- PQC

These represent migration states rather than individual cryptographic
algorithms.

---

## 3. Decision Inputs

### 3.1 Security Requirement

Values:

- `classical_acceptable`
- `pqc_required`

Interpretation:

If post-quantum protection is required, classical-only deployment cannot be
selected as the final migration strategy.

---

### 3.2 Legacy Compatibility

Values:

- `required`
- `not_required`

If legacy compatibility is required and the target environment cannot
support direct PQC deployment, hybrid migration is considered a transitional
strategy.

---

### 3.3 Performance Sensitivity

Values:

- `low`
- `medium`
- `high`

Performance sensitivity represents how strongly application performance
constrains migration decisions.

This is an application/deployment input and is not automatically inferred
from statistical significance.

---

### 3.4 Migration Urgency

Values:

- `low`
- `medium`
- `high`

Migration urgency represents how strongly the deployment needs to move away
from quantum-vulnerable classical cryptography.

---

### 3.5 Protocol

Values:

- `TLS`
- `SSH`

The recommendation is conditioned on the protocol because Phase 10 showed
protocol-dependent behavior.

---

### 3.6 Network Profile

Values:

- `baseline`
- `latency100`
- `latency200`
- `bandwidth1mbps`
- `loss1`
- `mobile`

The network profile selects the corresponding experimental evidence.

---

## 4. Evidence Inputs

The model consumes:

- Median hybrid latency overhead
- P95 hybrid latency overhead
- FDR-adjusted p-value
- Statistical significance
- Rank-biserial correlation
- Effect category
- Evidence classification

These values originate from the Phase 10 statistical analysis.

---

## 5. Evidence Strength

The model categorizes experimental performance evidence as:

### Strong

All of the following:

- statistically significant
- large effect
- positive median hybrid overhead

### Moderate

Statistically significant positive hybrid latency difference without all
criteria for strong evidence.

### Observed

Positive hybrid overhead is observed but statistical support is insufficient.

### Non-positive

No positive hybrid latency difference is supported by the measured data.

---

## 6. Decision Rules

### Rule 1 — Security requirement

If:

`security_requirement = pqc_required`

then:

- Classical cannot be the final recommendation.

---

### Rule 2 — No PQC requirement

If:

`security_requirement = classical_acceptable`

then classical remains an eligible strategy.

The framework may still recommend migration when migration urgency or future
security requirements justify it.

---

### Rule 3 — Legacy compatibility

If:

`legacy_compatibility = required`

and direct PQC deployment is not feasible, hybrid is preferred as a
transitional migration strategy.

---

### Rule 4 — Direct PQC migration

If:

- PQC is required
- legacy compatibility is not required
- direct PQC deployment is feasible

then PQC is the preferred final migration state.

---

### Rule 5 — Performance-sensitive deployment

If experimental evidence indicates substantial hybrid overhead under the
selected network/protocol condition, the framework must explicitly report
that performance constraint.

It must not override a mandatory security requirement solely because of
performance.

---

### Rule 6 — Experimental evidence

Performance recommendations must reference measured evidence from the
corresponding protocol and network profile.

---

### Rule 7 — Statistical caution

A statistically significant result is not automatically considered an
operationally significant result.

The model must expose:

- p-value
- adjusted p-value
- effect size
- latency overhead

alongside the recommendation.

---

## 7. Recommendation Types

The framework can produce:

### `CLASSICAL`

Classical deployment remains acceptable under the supplied requirements.

### `HYBRID_TRANSITION`

Hybrid deployment is recommended as a migration bridge because compatibility
or deployment constraints prevent immediate direct PQC migration.

### `PQC`

Direct PQC deployment is recommended as the target migration state.

### `HYBRID_OR_PQC_EVALUATION`

Experimental evidence indicates a meaningful performance trade-off and
additional deployment evaluation is recommended before selecting the final
configuration.

---

## 8. Explainability Requirements

Every recommendation must include:

1. Recommended strategy
2. Reason
3. Security consideration
4. Compatibility consideration
5. Performance evidence
6. Statistical evidence
7. Conditions that could change the recommendation

---

## 9. Important Limitation

The current benchmark does not provide complete quantitative CPU and memory
measurements.

Therefore CPU and memory must remain qualitative decision inputs until
additional measurements are collected.

---

## 10. Research Traceability

Every performance-related recommendation must be traceable to the Phase 10
evidence model.

The framework must not invent performance values or unsupported conclusions.

---

## 11. Research Question

Can experimentally measured PQC performance evidence be transformed into an
explainable migration recommendation while preserving security,
compatibility, and performance constraints?

