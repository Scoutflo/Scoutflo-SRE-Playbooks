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

1. Describe pod <pod-name> in namespace <namespace> to inspect image pull secrets, pod volume configuration, container volume mounts, or environment variable sources to identify which Secrets are referenced - look in Events section for "Failed" or "FailedMount" with the specific Secret name.

2. Retrieve events in namespace <namespace> for pod <pod-name> sorted by timestamp to see the sequence of Secret-related events, focusing on events with reasons such as Failed, FailedMount, or messages indicating Secret access failures.

3. Retrieve the Secret <secret-name> in namespace <namespace> and verify it exists in the same namespace.

4. Check the pod <pod-name> status in namespace <namespace> and inspect container waiting state reason and message fields to identify Secret access errors.

5. Verify RBAC permissions by checking if the pod's service account <service-account-name> has permissions to access Secrets in namespace <namespace>.

6. Retrieve the Deployment <deployment-name> in namespace <namespace> and review Secret references in the pod template to verify configuration is correct.

## Diagnosis

1. Analyze pod events from Playbook to identify the specific Secret pull error. Events showing "secret not found" indicate the Secret does not exist or is in a different namespace. Events showing "FailedMount" indicate volume mount issues. Events showing "forbidden" indicate RBAC permission problems.

2. If events indicate Secret not found, use the Playbook Secret retrieval results to confirm the Secret does not exist. Check if the Secret was recently deleted, never created, or exists in a different namespace than the pod.

3. If events indicate RBAC permission issues, leverage the Playbook RBAC verification results to confirm the pod's service account has permissions to access Secrets. Verify Role and RoleBinding objects exist and are correctly configured for the service account.

4. If events indicate imagePullSecrets issues (for image pull failures), verify the imagePullSecrets reference in the pod spec points to an existing Secret of type kubernetes.io/dockerconfigjson. Check if the Secret contains valid registry credentials.

5. If events indicate volume mount failures, review the pod volume configuration from Playbook describe output. Verify Secret key references match actual keys in the Secret, and check if optional flag is set appropriately for non-critical Secrets.

6. If events are inconclusive, compare event timestamps with recent deployment changes. Check if the Secret reference was modified, if a new pod template was rolled out, or if namespace configuration changed.

**If no clear cause is identified from events**: Verify the Secret data is not corrupted or empty, check if the Secret was created with the correct type, examine if any admission controllers or policies are blocking Secret access, and review API server logs for Secret retrieval errors.

