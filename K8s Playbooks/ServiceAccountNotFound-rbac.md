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

1. Retrieve the pod `<pod-name>` in namespace `<namespace>` and inspect pod service account name to identify which ServiceAccount is referenced.

2. Retrieve the ServiceAccount `<serviceaccount-name>` in namespace `<namespace>` and verify if it exists.

3. List events in namespace `<namespace>` and filter for ServiceAccount-related events, focusing on events with reasons such as `Failed` or messages indicating ServiceAccount not found.

4. Check the pod `<pod-name>` status and inspect container waiting state reason and message fields to identify ServiceAccount not found errors.

5. Retrieve the Deployment `<deployment-name>` in namespace `<namespace>` and review ServiceAccount references in the pod template to verify the ServiceAccount name is correct.

6. Verify if the ServiceAccount exists in a different namespace and if cross-namespace access is required and configured.

## Diagnosis

1. Compare the pod ServiceAccount not found error timestamps with ServiceAccount deletion timestamps, and check whether ServiceAccounts were deleted within 30 minutes before pod failures.

2. Compare the pod ServiceAccount not found error timestamps with deployment ServiceAccount reference modification timestamps, and check whether ServiceAccount name changes occurred within 30 minutes before not found errors.

3. Compare the pod ServiceAccount not found error timestamps with namespace creation or pod namespace change timestamps, and check whether namespace mismatches occurred within 30 minutes before not found errors.

4. Compare the pod ServiceAccount not found error timestamps with deployment rollout or pod template update timestamps, and check whether ServiceAccount reference changes occurred within 1 hour before not found errors.

5. Compare the pod ServiceAccount not found error timestamps with ServiceAccount creation failure timestamps, and check whether ServiceAccount creation failed within 30 minutes before pod failures.

6. Compare the pod ServiceAccount not found error timestamps with cluster upgrade or namespace migration timestamps, and check whether infrastructure changes occurred within 1 hour before ServiceAccount references became invalid.

**If no correlation is found within the specified time windows**: Extend the search window (30 minutes → 1 hour, 1 hour → 2 hours), review deployment history for ServiceAccount reference changes, check for intermittent namespace or RBAC permission issues, examine if ServiceAccount names drifted over time, verify if ServiceAccounts were never created but referenced, and check for API server or etcd issues affecting ServiceAccount retrieval. ServiceAccount not found errors may result from gradual configuration drift rather than immediate deletions.

