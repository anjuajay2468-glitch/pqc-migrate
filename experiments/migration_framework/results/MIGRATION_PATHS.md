# PQC-Migrate — Migration Paths

## 1. Purpose

Migration paths define how an organization can move from an existing
classical cryptographic deployment toward post-quantum cryptography while
accounting for security, compatibility, and performance constraints.

The paths complement the quantitative migration decision model.

---

## 2. Path A — Direct PQC Migration

### Starting state

Classical cryptography.

### Conditions

- Post-quantum protection is required.
- Legacy compatibility does not prevent direct PQC deployment.
- Target protocol and infrastructure support the selected PQC mechanism.
- Performance validation is acceptable for the deployment.

### Path

Classical
→ PQC implementation
→ Performance validation
→ Security validation
→ PQC deployment
→ Monitoring

### Rationale

Direct migration avoids maintaining a transitional hybrid configuration when
the deployment environment can support PQC directly.

---

## 3. Path B — Hybrid Transition

### Starting state

Classical cryptography with compatibility constraints.

### Conditions

- Post-quantum protection is required or migration urgency is high.
- Legacy systems still require compatibility.
- Hybrid cryptography is supported by the deployment environment.

### Path

Classical
→ Hybrid deployment
→ Compatibility validation
→ Performance validation
→ Legacy-system migration
→ PQC deployment
→ Monitoring

### Rationale

Hybrid deployment provides a transitional state while legacy systems are
being upgraded.

---

## 4. Path C — Performance-Constrained Evaluation

### Starting state

Classical deployment.

### Conditions

- Classical cryptography remains acceptable under current requirements.
- Performance sensitivity is high.
- Experimental evidence indicates substantial PQC/hybrid performance impact.

### Path

Classical
→ Benchmark target PQC/hybrid configuration
→ Network-condition validation
→ Application-level performance testing
→ Security review
→ Migration decision

### Rationale

The purpose of this path is not to reject PQC.

It delays final migration selection until deployment-specific performance
constraints are measured.

---

## 5. Path D — Hybrid-or-PQC Evaluation

### Starting state

Classical deployment.

### Conditions

- Migration is being considered.
- Classical cryptography is still acceptable.
- Experimental evidence does not establish a single clearly preferred
  performance strategy for the deployment.

### Path

Classical
→ Evaluate hybrid
→ Evaluate PQC
→ Compare security and performance
→ Select target state
→ Validate
→ Deploy

### Rationale

Additional deployment-specific evidence is required before selecting the
final migration state.

---

## 6. Common Migration Stages

All paths should include the following lifecycle stages where applicable:

1. Cryptographic inventory
2. Dependency identification
3. Security requirement assessment
4. Protocol and implementation compatibility assessment
5. Performance benchmarking
6. Pilot deployment
7. Monitoring
8. Migration
9. Legacy decommissioning where appropriate

---

## 7. Validation Requirements

Before production deployment:

- Verify cryptographic implementation support.
- Validate protocol compatibility.
- Measure application-level performance.
- Test representative network conditions.
- Verify security requirements.
- Confirm rollback procedures.
- Monitor production behavior after deployment.

---

## 8. Research Traceability

Each migration path must remain connected to the experimental evidence used
by the migration decision framework.

Performance-related decisions should reference:

- Median latency
- P95 latency
- Hybrid overhead
- Statistical significance
- Effect size
- Network profile

---

## 9. Scope

These paths are research decision-support patterns derived from the
PQC-Migrate experimental framework.

They are not universal operational policies and must be adapted to the
specific deployment environment.
