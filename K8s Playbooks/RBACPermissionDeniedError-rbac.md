---
title: RBAC Permission Denied Error - RBAC
weight: 223
categories:
  - kubernetes
  - rbac
---

# RBACPermissionDeniedError-rbac

## Meaning

API requests from a user or service account are being rejected with forbidden or permission denied errors (potentially triggering KubeAPIErrorsHigh alerts) because the RBAC roles and bindings do not grant the necessary permissions on the targeted resources. API requests return 403 status codes, Role or RoleBinding resources may show missing permissions, and pod logs may show permission denied errors. This indicates RBAC configuration errors, missing permissions, or role binding issues preventing authorized access to cluster resources; applications using Kubernetes API may show errors.

## Impact

API operations fail with permission denied; pods cannot access required resources; controllers cannot reconcile state; deployments fail; applications cannot perform required actions; cluster operations are blocked; KubeAPIErrorsHigh alerts may fire; forbidden errors appear in logs; permission denied errors occur; RBAC validation failures prevent operations. API requests return 403 status codes indefinitely; Role or RoleBinding resources may show missing permissions; applications using Kubernetes API may experience errors or performance degradation; cluster operations are blocked.

## Playbook

1. Check if current user can perform action `<action>` on resource `<resource>` to check current user's permissions.

2. List role bindings in namespace `<namespace>` and cluster role bindings to check RoleBinding or ClusterRoleBinding configuration.

3. Retrieve service account `<service-account-name>` in namespace `<namespace>` and verify service account permissions if service account is used.

4. Check role binding and cluster role binding modification timestamps to check for recent RBAC configuration changes.

5. Retrieve logs from pod `<pod-name>` in namespace `<namespace>` or check API server logs to verify error messages in pod logs or API server logs.

6. List validating and mutating admission webhooks to check if webhooks block requests.

## Diagnosis

1. Compare the timestamps when permission denied errors occurred (from pod logs or API server logs) with RoleBinding or ClusterRoleBinding change timestamps, and check whether errors begin within 1 hour of role binding modifications.

2. Compare the permission denied error timestamps with service account change timestamps, and verify whether errors correlate with service account modifications at the same time.

3. Compare the permission denied error timestamps with deployment or configuration change timestamps, and check whether errors begin within 1 hour of deployment changes.

4. Compare the permission denied error timestamps with cluster upgrade or maintenance window timestamps, and verify whether errors correlate with infrastructure changes within 1 hour.

5. Compare the permission denied error timestamps with user or service account change timestamps, and check whether errors correlate with account modifications.

6. Compare the permission denied error timestamps with namespace change timestamps, resource creation timestamps, or admission webhook block timestamps, and verify whether errors correlate with namespace or webhook changes at the same time.

**If no correlation is found within the specified time windows**: Extend the search window (1 hour → 2 hours), review RBAC role definitions for missing permissions, check for namespace-level role bindings that may override cluster roles, examine admission webhook logs for blocking decisions, verify if service account tokens are valid, check for role aggregation issues, and review RBAC audit logs for detailed permission checks. Permission denied errors may result from cumulative permission changes or role binding conflicts not immediately visible in single change events.
