# PQC-Migrate — Migration Framework Case Studies

## Case Study 1 — Modern TLS Infrastructure

### Deployment profile

A modern TLS deployment supports post-quantum cryptography and has no major
legacy compatibility constraint.

Security requirements require post-quantum protection.

### Framework inputs

- Security requirement: `pqc_required`
- Legacy compatibility: `not_required`
- Performance sensitivity: `medium`
- Migration urgency: `high`
- Protocol: `TLS`
- Network profile: `baseline`

### Framework recommendation

**PQC**

### Rationale

Post-quantum protection is mandatory and no legacy compatibility requirement
prevents direct migration.

The measured TLS baseline comparison should still be reviewed as part of
deployment-specific performance validation.

### Migration path

Classical
→ PQC implementation
→ Performance validation
→ Security validation
→ PQC deployment
→ Monitoring

---

## Case Study 2 — Legacy SSH Infrastructure

### Deployment profile

An SSH environment requires post-quantum protection but still contains
legacy systems requiring compatibility.

### Framework inputs

- Security requirement: `pqc_required`
- Legacy compatibility: `required`
- Performance sensitivity: `high`
- Migration urgency: `high`
- Protocol: `SSH`
- Network profile: `bandwidth1mbps`

### Framework recommendation

**HYBRID_TRANSITION**

### Measured evidence

The Phase 10 benchmark reports approximately:

- Median hybrid latency overhead: **+39.27%**
- Statistical significance: **significant**
- Effect category: **Large**

### Rationale

The security requirement prevents a classical-only final state, while the
legacy compatibility requirement prevents immediate direct PQC migration.

Hybrid deployment therefore serves as a transitional strategy.

The measured performance overhead should be explicitly evaluated before
production deployment, especially under bandwidth-constrained conditions.

### Migration path

Classical
→ Hybrid deployment
→ Compatibility validation
→ Performance validation
→ Legacy-system migration
→ PQC deployment
→ Monitoring

---

## Case Study 3 — Bandwidth-Constrained Environment

### Deployment profile

A deployment operates over a constrained network where performance is highly
sensitive.

Post-quantum protection is not yet mandatory, and migration urgency is low.

### Framework inputs

- Security requirement: `classical_acceptable`
- Legacy compatibility: `not_required`
- Performance sensitivity: `high`
- Migration urgency: `low`
- Protocol: `SSH`
- Network profile: `bandwidth1mbps`

### Framework recommendation

**CLASSICAL**

### Measured evidence

The Phase 10 benchmark reports approximately:

- Median hybrid latency overhead: **+39.27%**
- Statistical significance: **significant**
- Effect category: **Large**

### Rationale

The framework does not reject PQC.

Instead, because post-quantum protection is not currently mandatory and the
environment is highly performance-sensitive, the measured overhead justifies
additional deployment-specific evaluation before migration.

The classical configuration remains the current recommendation under the
specified requirements.

### Migration path

Classical
→ Benchmark target PQC/hybrid configuration
→ Network-condition validation
→ Application-level performance testing
→ Security review
→ Migration decision

---

## Case Study 4 — Mobile TLS Environment

### Deployment profile

A TLS deployment operates under mobile-like network conditions.

Classical cryptography remains acceptable and migration urgency is low.

### Framework inputs

- Security requirement: `classical_acceptable`
- Legacy compatibility: `not_required`
- Performance sensitivity: `medium`
- Migration urgency: `low`
- Protocol: `TLS`
- Network profile: `mobile`

### Framework recommendation

**HYBRID_OR_PQC_EVALUATION**

### Measured evidence

The Phase 10 benchmark reports approximately:

- Median hybrid latency overhead: **+9.00%**
- Statistical significance: **not significant**
- Effect category: **Medium**

### Rationale

The measured result does not establish a sufficiently clear performance
advantage for retaining or rejecting a migration strategy solely from this
benchmark.

The framework therefore recommends deployment-specific comparison of hybrid
and direct PQC configurations.

### Migration path

Classical
→ Evaluate hybrid
→ Evaluate PQC
→ Compare security and performance
→ Select target state
→ Validate
→ Deploy

---

## Cross-Case Observation

The four cases demonstrate that the framework does not produce a single
universal recommendation.

The recommendation changes according to:

- Security requirements
- Legacy compatibility
- Performance sensitivity
- Migration urgency
- Protocol
- Network conditions

This supports the central research objective of an evidence-based,
context-dependent PQC migration framework.

---

## Research Limitation

These case studies are representative scenarios based on the current
benchmark dataset.

They are not production deployment recommendations.

Actual migration decisions require application-level testing, security
review, implementation compatibility testing, and organization-specific
requirements.
