---
title: Pods Cannot Pull Secrets - Secret
weight: 240
categories:
  - kubernetes
  - secret
---

# PodsCannotPullSecrets-secret

## Meaning

Pods cannot pull or access Secrets (triggering pod-related alerts) because Secrets do not exist, Secret references are incorrect, RBAC permissions prevent access, or Secrets are not properly mounted. Pods show CrashLoopBackOff or Pending state, pod events show Failed, FailedMount, or Secret access failure errors, and container waiting state reason may indicate Secret access failures. This affects the workload plane and prevents pods from starting or applications from reading Secret data, typically caused by missing Secrets, incorrect references, or RBAC permission issues; missing Secret dependencies may block container initialization.

## Impact

Pods cannot start; applications fail to read secrets; Secret access failures occur; pods enter CrashLoopBackOff or Pending state; KubePodPending alerts fire; authentication credentials are missing; image pull secrets fail; services cannot start without required secrets; environment variables are not populated. Pods show CrashLoopBackOff or Pending state indefinitely; pod events show Failed, FailedMount, or Secret access failure errors; missing Secret dependencies may block container initialization; applications cannot start and may show errors.

## Playbook

1. Retrieve the pod `<pod-name>` in namespace `<namespace>` and inspect image pull secrets, pod volume configuration, container volume mounts, or environment variable sources to identify which Secrets are referenced.

2. Retrieve the Secret `<secret-name>` referenced in the pod and verify it exists in the same namespace.

3. List events in namespace `<namespace>` and filter for Secret-related events, focusing on events with reasons such as `Failed`, `FailedMount`, or messages indicating Secret access failures.

4. Check the pod `<pod-name>` status and inspect container waiting state reason and message fields to identify Secret access errors.

5. Verify RBAC permissions by checking if the pod's service account has permissions to access Secrets in the namespace.

6. Retrieve the Deployment `<deployment-name>` in namespace `<namespace>` and review Secret references in the pod template to verify configuration is correct.

## Diagnosis

1. Compare the pod Secret pull failure timestamps with Secret deletion timestamps, and check whether Secrets were deleted within 30 minutes before pod failures.

2. Compare the pod Secret pull failure timestamps with pod Secret reference modification timestamps in the deployment, and check whether Secret name changes occurred within 30 minutes before pull failures.

3. Compare the pod Secret pull failure timestamps with RBAC Role or RoleBinding modification timestamps, and check whether permission changes occurred within 30 minutes before pull failures.

4. Compare the pod Secret pull failure timestamps with deployment rollout or pod template update timestamps, and check whether Secret reference changes occurred within 1 hour before pull failures.

5. Compare the pod Secret pull failure timestamps with service account modification timestamps, and check whether service account changes occurred within 30 minutes before pull failures.

6. Compare the pod Secret pull failure timestamps with namespace creation or pod namespace change timestamps, and check whether namespace mismatches occurred within 30 minutes before pull failures.

**If no correlation is found within the specified time windows**: Extend the search window (30 minutes → 1 hour, 1 hour → 2 hours), review pod logs for gradual Secret access issues, check for intermittent RBAC permission problems, examine if Secret references drifted over time, verify if Secrets were never created but referenced, and check for API server or etcd issues affecting Secret retrieval. Secret pull failures may result from gradual configuration drift rather than immediate changes.

