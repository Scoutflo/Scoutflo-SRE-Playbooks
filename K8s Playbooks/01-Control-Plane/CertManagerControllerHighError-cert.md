---
title: Cert Manager Controller High Error Rate
weight: 44
categories: [kubernetes, cert-manager]
---

# CertManagerControllerHighError

## Meaning

Cert-manager controller is experiencing high error rate (triggering CertManagerControllerHighError alerts) because certificate operations are failing frequently, indicating systemic issues with issuers, configuration, or cluster connectivity. Controller metrics show elevated error counts, certificate operations are not completing successfully, and certificate management is degraded. This affects certificate issuance and renewal across the cluster; certificates may not be issued or renewed; increased manual intervention needed.

## Impact

CertManagerControllerHighError alerts fire; certificate operations fail frequently; new certificate requests may fail; renewals may be delayed; certificate status is unreliable; manual intervention required more often; certificate-dependent deployments are delayed; security posture may be affected by renewal failures.

## Playbook

1. Retrieve cert-manager controller logs and filter for ERROR level messages to identify common failure patterns.

2. Check controller metrics for error rate breakdown by operation type (issuance, renewal, sync).

3. Identify which Issuers or ClusterIssuers have the most failures.

4. Verify API server connectivity and RBAC permissions for cert-manager.

5. Check for Certificate or CertificateRequest resources stuck in error states.

6. Verify webhook service is healthy and responding correctly.

7. Check for resource contention or throttling affecting controller operation.

## Diagnosis

Categorize errors by type and identify if errors are concentrated on specific issuers, namespaces, or certificate types, using error logs and metrics breakdown as supporting evidence.

Check for API server connectivity issues that prevent cert-manager from reading or updating resources, using API server latency metrics and error logs as supporting evidence.

Verify issuer credentials (ACME accounts, CA secrets, Vault tokens) are valid and not expired, using issuer status and credential validation as supporting evidence.

Check for rate limiting from external ACME providers causing operation failures, using ACME responses in logs as supporting evidence.

Analyze controller restart history and verify if restarts correlate with error spikes (suggesting controller instability), using pod restart timestamps and error metrics as supporting evidence.

If no correlation is found within the specified time windows: review recent cert-manager or cluster upgrades, verify CRD compatibility, check for memory or CPU constraints, review RBAC changes, consider cert-manager reinstallation if controller is corrupt.
