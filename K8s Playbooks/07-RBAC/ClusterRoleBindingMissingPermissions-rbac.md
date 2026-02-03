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

1. Test the specific permission that is failing by checking if the user or ServiceAccount <namespace>:<sa-name> can perform <verb> on <resource> to immediately identify which action is denied and confirm the permission gap.

2. List all permissions for the affected user or ServiceAccount <namespace>:<sa-name> to see the complete set of granted permissions and identify what is missing.

3. Describe ClusterRoleBinding <binding-name> to inspect subjects, role reference, and any annotations showing which users or service accounts are bound and which ClusterRole is referenced.

4. Describe ClusterRole <role-name> to inspect its rules and verify which permissions are granted, comparing against the denied action from Step 1.

5. Retrieve events across all namespaces filtered by reason Forbidden to identify authorization-related events indicating permission denials.

6. Check API server audit logs if available to review authorization decisions for forbidden or unauthorized actions.

7. Verify if the ClusterRoleBinding includes all required subjects (users, service accounts, groups) that need the permissions by comparing subjects list with the identity from Step 1.

## Diagnosis

1. From Playbook step 1, the `auth can-i` check identifies the specific permission gap (verb + resource). Use this result to focus investigation on why this exact permission is missing from the RBAC chain.

2. If the `auth can-i` result shows "no" for the required verb+resource, check the ClusterRole rules (from Playbook step 4):
   - If the ClusterRole does not include the required verb+resource rule, the issue is **missing ClusterRole rules**. Compare ClusterRole modification timestamps with permission denial onset to determine if rules were recently removed.
   - If the ClusterRole has wildcard rules that should cover the permission, check for explicit deny rules or resource group mismatches.

3. If the ClusterRole has the required rules but the subject is not listed in the ClusterRoleBinding (from Playbook step 3), the issue is **missing subject binding**:
   - Verify if the user, ServiceAccount, or group was recently removed from the binding.
   - Check if the subject name or namespace is misspelled in the binding.
   - For ServiceAccounts, confirm the format is `system:serviceaccount:<namespace>:<sa-name>`.

4. If both ClusterRole and ClusterRoleBinding appear correct, check for **namespace scope mismatch**:
   - If accessing namespaced resources, verify whether a Role/RoleBinding should be used instead of ClusterRole/ClusterRoleBinding.
   - Check if the ClusterRoleBinding was mistakenly created as a RoleBinding in a specific namespace.

5. If the ClusterRole is expected to inherit rules via aggregation, check for **missing aggregation rules**:
   - Verify that aggregated ClusterRoles have the correct `aggregationRule.clusterRoleSelectors` labels.
   - Confirm that child ClusterRoles contributing rules still exist and have matching labels.

6. If the ClusterRole or ClusterRoleBinding was deleted or replaced, confirm deletion timestamps from API server audit logs (from Playbook step 6):
   - Check for `delete` or `patch` operations on the ClusterRole within 30 minutes before permission denials.
   - Look for controller or operator activity that may have modified RBAC resources.

7. If all RBAC resources appear correct, review Forbidden events (from Playbook step 5) and API server audit logs (from Playbook step 6) for authorization decision details:
   - Check if denials are intermittent (possible caching or API server sync issues).
   - Verify if multiple authorization modes are configured and if another authorizer is denying the request.
   - Look for impersonation headers that may affect the evaluated identity.

**If no root cause is identified**: Extend the search window for timestamp correlations (30 minutes to 1 hour, 1 hour to 2 hours), check for gradual RBAC policy drift via GitOps or policy controllers, verify etcd health for RBAC resource retrieval issues, and examine if admission controllers or OPA/Gatekeeper policies are interfering with RBAC decisions.

