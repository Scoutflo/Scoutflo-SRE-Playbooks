---
title: Service Account Not Found - RBAC
weight: 252
categories:
  - kubernetes
  - rbac
---

# ServiceAccountNotFound-rbac

## Meaning

ServiceAccounts referenced by pods do not exist (triggering KubePodPending alerts) because the ServiceAccount was never created, was deleted, is in a different namespace, or the reference name is incorrect. Pods show Pending state, pod events show ServiceAccount not found errors, and container waiting state reason may indicate ServiceAccount access failures. This affects the workload plane and prevents pods from starting, typically caused by missing ServiceAccounts or incorrect references; missing ServiceAccount dependencies may block container initialization.

## Impact

Pods cannot start; deployments fail to create pods; ServiceAccount references fail; pods remain in Pending state; KubePodPending alerts fire; pod authentication fails; RBAC permissions are not applied; services cannot access required resources; image pull secrets fail if referenced by ServiceAccount. Pods show Pending state indefinitely; pod events show ServiceAccount not found errors; missing ServiceAccount dependencies may block container initialization; applications cannot start and may show errors.

## Playbook

1. Describe pod <pod-name> in namespace <namespace> to see pod status, events, and the ServiceAccount reference causing the issue - look for "serviceaccount not found" in events.

2. Check if the referenced ServiceAccount <serviceaccount-name> exists in namespace <namespace> - if not found, this confirms the issue.

3. Retrieve events for pod <pod-name> in namespace <namespace> to see ServiceAccount-related errors with timestamps.

4. If the ServiceAccount exists, verify its permissions by checking what actions the ServiceAccount <namespace>:<sa-name> can perform.

5. Describe Deployment <deployment-name> in namespace <namespace> and check the pod template's serviceAccountName field to verify the ServiceAccount name is spelled correctly.

6. List all ServiceAccounts in namespace <namespace> to check for similar names (typos) or verify the correct ServiceAccount to use.

7. If cross-namespace access is suspected, list ServiceAccounts across all namespaces and search for <sa-name> to check if it exists in another namespace.

## Diagnosis

1. From Playbook step 2, verify whether the ServiceAccount exists in the expected namespace. The `kubectl get serviceaccount` result determines the primary diagnosis path:
   - If the ServiceAccount does not exist, proceed to step 2 to determine why.
   - If the ServiceAccount exists, proceed to step 5 to check for reference or permission issues.

2. If the ServiceAccount does not exist, determine the root cause:
   - **ServiceAccount was deleted**: Check API server audit logs or events for `delete` operations on ServiceAccounts within 30 minutes before pod failures. Look for operator, controller, or manual deletion activity.
   - **ServiceAccount was never created**: Verify if the ServiceAccount should be created by a Helm chart, operator, or manifest. Check deployment prerequisites and ordering.
   - **ServiceAccount creation failed**: Review namespace events for failed ServiceAccount creation attempts (quota limits, admission webhook rejections, or validation errors).

3. If the pod events (from Playbook step 1 and step 3) show "serviceaccount not found", check for **namespace mismatch**:
   - If the cross-namespace search (from Playbook step 7) finds the ServiceAccount in a different namespace, the issue is a namespace reference error.
   - Verify the pod's namespace matches where the ServiceAccount exists - ServiceAccounts are namespace-scoped and cannot be referenced across namespaces.
   - Check if the pod was deployed to the wrong namespace or if the ServiceAccount was created in the wrong namespace.

4. If the ServiceAccount list (from Playbook step 6) shows similar names, check for **typo in ServiceAccount reference**:
   - Compare the `serviceAccountName` in the Deployment spec (from Playbook step 5) with existing ServiceAccount names.
   - Look for common typos: pluralization (`serviceaccount` vs `serviceaccounts`), case sensitivity, hyphens vs underscores.
   - Verify copy-paste errors from documentation or templates.

5. If the ServiceAccount exists and is correctly referenced, but pods still fail, check for **permission or token issues**:
   - Use the `auth can-i` verification (from Playbook step 4) to confirm the ServiceAccount has required permissions.
   - For Kubernetes 1.24+, verify if a ServiceAccount token Secret was explicitly created (automatic token creation was removed).
   - Check if the ServiceAccount's `automountServiceAccountToken` is set to false when the pod requires API access.

6. If the ServiceAccount was recently working, check for **recent changes**:
   - Compare pod failure timestamps with Deployment rollout timestamps (from Playbook step 5) to identify if `serviceAccountName` was changed in a recent update.
   - Review namespace migration or cluster upgrade activity within 1 hour before failures.
   - Check if GitOps or config management tools recently synced changes affecting ServiceAccount resources.

**If no root cause is identified**: Extend the search window for timestamp correlations (30 minutes to 1 hour), verify etcd health for ServiceAccount retrieval issues, check if admission controllers are blocking ServiceAccount creation, and examine if the ServiceAccount was created but immediately deleted by a controller or cleanup policy. ServiceAccount not found errors may also occur transiently during namespace creation if pods are scheduled before ServiceAccounts are created.

