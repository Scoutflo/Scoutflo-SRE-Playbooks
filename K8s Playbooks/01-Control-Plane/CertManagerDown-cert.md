---
title: Cert Manager Down
weight: 42
categories: [kubernetes, cert-manager]
---

# CertManagerDown

## Meaning

Cert-manager controller is not running or not healthy (triggering CertManagerDown alerts) because the cert-manager pods are crashing, not scheduled, or not responding to health checks. Cert-manager deployment shows zero ready replicas, no certificate operations are being processed, and new certificate issuance and renewals are blocked. This affects all certificate management in the cluster; new certificates cannot be issued; renewals will not occur; certificate infrastructure is non-functional.

## Impact

CertManagerDown alerts fire; no new certificates can be issued; certificate renewals stop; pending certificate requests are not processed; new deployments requiring certificates are blocked; expiring certificates are not renewed; HTTPS outages will occur as certificates expire; compliance requirements are at risk; security posture degrades.

## Playbook

1. Retrieve cert-manager deployments in the cert-manager namespace and verify replica status.

2. Check cert-manager controller pod status, restart count, and events.

3. Retrieve cert-manager controller logs for startup failures or runtime errors.

4. Verify cert-manager webhook deployment is healthy (required for cert-manager operation).

5. Check for resource constraints preventing pod scheduling (CPU, memory, node availability).

6. Verify cert-manager CRDs are installed correctly and not corrupted.

7. Check for conflicts with other operators or admission webhooks.

## Diagnosis

Analyze controller pod status and identify if pods are CrashLooping, Pending, or missing, using pod status and events as supporting evidence.

Check for OOMKilled events indicating memory limits are too low for cert-manager operation, using container status and memory metrics as supporting evidence.

Verify webhook service is accessible as cert-manager cannot function without its webhook, using webhook pod status and service endpoints as supporting evidence.

Check for CRD version mismatches after cert-manager upgrades that may cause controller failures, using CRD versions and controller compatibility as supporting evidence.

Analyze controller logs for specific error patterns (API access denied, leader election failures, watch errors), using log analysis as supporting evidence.

If no correlation is found within the specified time windows: restart cert-manager pods, verify RBAC permissions are correct, check for API server connectivity, reinstall cert-manager if CRDs are corrupted, verify leader election lease is not stuck.
