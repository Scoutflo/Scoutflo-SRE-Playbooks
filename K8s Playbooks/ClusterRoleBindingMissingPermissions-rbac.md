---
title: ClusterRoleBinding Missing Permissions - RBAC
weight: 218
categories:
  - kubernetes
  - rbac
---

# ClusterRoleBindingMissingPermissions-rbac

## Meaning

ClusterRoleBindings do not grant sufficient permissions (triggering KubeAPIErrorsHigh alerts) because the referenced ClusterRole lacks required rules, the binding does not include all necessary subjects, or permissions were removed from the ClusterRole. ClusterRoleBinding resources show missing permissions, ClusterRole resources may show insufficient rules, and API requests return 403 status codes. This affects the authentication and authorization plane and prevents cluster-wide operations, typically caused by missing ClusterRole rules or incorrect ClusterRoleBinding configurations; applications using Kubernetes API may show errors.

## Impact

Cluster-wide operations fail; users cannot perform required actions; service accounts lack permissions; KubeAPIErrorsHigh alerts fire; API server returns Forbidden errors; authorization failures prevent cluster management; applications fail due to permission denials; cluster administration is blocked. ClusterRoleBinding resources show missing permissions indefinitely; ClusterRole resources may show insufficient rules; applications using Kubernetes API may experience errors or performance degradation; cluster administration is blocked.

## Playbook

1. Retrieve the ClusterRoleBinding `<binding-name>` and inspect its subjects and role reference to verify which users or service accounts are bound and which ClusterRole is referenced.

2. Retrieve the ClusterRole referenced by the binding and inspect its rules to verify which permissions are granted.

3. Test specific permissions using `kubectl auth can-i <verb> <resource>` for the bound user or service account to identify which actions are denied.

4. List events in the cluster and filter for authorization-related events, focusing on events with reasons such as `Forbidden` or messages indicating permission denials.

5. Check API server audit logs if available to review authorization decisions and identify which permissions are missing from the ClusterRole.

6. Verify if the ClusterRoleBinding includes all required subjects (users, service accounts, groups) that need the permissions.

## Diagnosis

1. Compare the permission denial timestamps with ClusterRole rule modification timestamps, and check whether permissions were removed from the ClusterRole within 30 minutes before permission denials.

2. Compare the permission denial timestamps with ClusterRoleBinding modification timestamps, and check whether subjects were removed from the binding within 30 minutes before permission denials.

3. Compare the permission denial timestamps with ClusterRole deletion or replacement timestamps, and check whether ClusterRoles were changed within 30 minutes before permission denials.

4. Compare the permission denial timestamps with cluster upgrade or RBAC policy update timestamps, and check whether infrastructure changes occurred within 1 hour before permission denials, affecting permission enforcement.

5. Compare the permission denial timestamps with new resource type creation timestamps, and check whether new resource types were introduced within 30 minutes before permission denials, requiring new permissions in ClusterRole rules.

6. Compare the permission denial timestamps with API server configuration modification timestamps, and check whether authorization settings were changed within 30 minutes before permission denials.

**If no correlation is found within the specified time windows**: Extend the search window (30 minutes → 1 hour, 1 hour → 2 hours), review API server audit logs for gradual permission changes, check for intermittent RBAC policy enforcement issues, examine if ClusterRole or ClusterRoleBinding configurations drifted over time, verify if permissions were gradually restricted, and check for API server or etcd issues affecting RBAC retrieval. Missing permissions may result from gradual RBAC policy changes rather than immediate modifications.

