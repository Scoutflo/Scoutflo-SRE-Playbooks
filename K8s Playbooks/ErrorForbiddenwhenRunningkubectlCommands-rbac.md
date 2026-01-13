---
title: Error Forbidden when Running kubectl Commands - RBAC
weight: 261
categories:
  - kubernetes
  - rbac
---

# ErrorForbiddenwhenRunningkubectlCommands-rbac

## Meaning

kubectl commands return Forbidden (403) errors (triggering KubeAPIErrorsHigh alerts) because the user or service account lacks required RBAC permissions, Role or RoleBinding resources are missing or incorrect, or permissions were revoked. API requests return 403 status codes, Role or RoleBinding resources may show missing permissions, and authorization failures prevent resource management. This affects the authentication and authorization plane and prevents cluster operations, typically caused by missing RBAC permissions or incorrect Role/RoleBinding configurations; applications using Kubernetes API may show errors.

## Impact

kubectl commands fail with Forbidden errors; cluster operations are blocked; users cannot perform required actions; KubeAPIErrorsHigh alerts fire; API server returns 403 status codes; authorization failures prevent resource management; service accounts cannot access required resources; applications fail due to permission denials. API requests return 403 status codes indefinitely; Role or RoleBinding resources may show missing permissions; applications using Kubernetes API may experience errors or performance degradation; cluster operations are blocked.

## Playbook

1. Verify the current user or service account identity by checking kubeconfig context or pod service account.

2. Retrieve the Role or ClusterRole bound to the user or service account and inspect its rules to verify which permissions are granted.

3. Retrieve the RoleBinding or ClusterRoleBinding for the user or service account and verify the binding exists and references the correct role.

4. Test specific permissions using `kubectl auth can-i <verb> <resource>` to identify which actions are denied.

5. List events in the namespace or cluster and filter for authorization-related events, focusing on events with reasons such as `Forbidden` or messages indicating permission denials.

6. Check API server audit logs if available to review authorization decisions and identify which permissions are missing.

## Diagnosis

1. Compare the Forbidden error timestamps with Role or ClusterRole modification timestamps, and check whether permissions were removed within 30 minutes before Forbidden errors.

2. Compare the Forbidden error timestamps with RoleBinding or ClusterRoleBinding deletion timestamps, and check whether bindings were removed within 30 minutes before Forbidden errors.

3. Compare the Forbidden error timestamps with user or service account modification timestamps, and check whether account changes occurred within 30 minutes before Forbidden errors.

4. Compare the Forbidden error timestamps with cluster upgrade or RBAC policy update timestamps, and check whether infrastructure changes occurred within 1 hour before Forbidden errors, affecting permission enforcement.

5. Compare the Forbidden error timestamps with API server configuration modification timestamps, and check whether authorization settings were changed within 30 minutes before Forbidden errors.

6. Compare the Forbidden error timestamps with resource creation or namespace creation timestamps, and check whether new resources or namespaces were created within 30 minutes before Forbidden errors, requiring new permissions.

**If no correlation is found within the specified time windows**: Extend the search window (30 minutes → 1 hour, 1 hour → 2 hours), review API server audit logs for gradual permission changes, check for intermittent RBAC policy enforcement issues, examine if Role or RoleBinding configurations drifted over time, verify if permissions were gradually restricted, and check for API server or etcd issues affecting RBAC retrieval. Forbidden errors may result from gradual permission policy changes rather than immediate revocations.

