---
title: Secrets Not Accessible - Secret
weight: 210
categories:
  - kubernetes
  - secret
---

# SecretsNotAccessible-secret

## Meaning

Secrets are not accessible to pods (triggering pod-related alerts) because Secrets are not mounted correctly, RBAC permissions prevent access, the Secret reference is incorrect, or the pod's service account lacks permissions. Pods show CrashLoopBackOff or Pending state, pod events show FailedMount errors, and container waiting state reason may indicate Secret access failures. This affects the workload plane and prevents pods from reading Secret data, typically caused by RBAC permission issues or incorrect mount configurations; missing Secret dependencies may block container initialization.

## Impact

Pods cannot access secrets; applications fail to read sensitive data; Secret mount failures occur; environment variables are not populated; pods enter CrashLoopBackOff or Pending state; KubePodPending alerts may fire; authentication credentials are missing; services cannot start without required secrets; image pull secrets fail. Pods show CrashLoopBackOff or Pending state indefinitely; pod events show FailedMount errors; missing Secret dependencies may block container initialization; applications cannot start and may show errors.

## Playbook

1. Describe pod <pod-name> in namespace <namespace> to inspect pod volume configuration, container volume mounts, environment variable sources, or image pull secrets to identify which Secret is referenced and how it should be accessed - look in Events section for "FailedMount" with the specific Secret name.

2. Retrieve events in namespace <namespace> for pod <pod-name> sorted by timestamp to see the sequence of Secret-related events, focusing on events with reasons such as FailedMount or messages indicating Secret access or permission failures.

3. Retrieve the Secret <secret-name> in namespace <namespace> and verify it exists and contains the expected data.

4. Check the pod <pod-name> status in namespace <namespace> and inspect container waiting state reason and message fields to identify Secret access errors.

5. Verify RBAC permissions by checking if the pod's service account <service-account-name> has permissions to access Secrets in namespace <namespace>.

6. Retrieve the Deployment <deployment-name> in namespace <namespace> and review Secret references and mount configurations in the pod template.

## Diagnosis

1. Analyze pod events from Playbook to identify the specific Secret access error. Events showing "FailedMount" with "secret not found" indicate the Secret does not exist. Events showing "forbidden" or "unauthorized" indicate RBAC permission issues. Events showing "MountVolume.SetUp failed" indicate mount configuration problems.

2. If events indicate Secret not found, verify the Secret exists in the same namespace as the pod using the Playbook Secret retrieval results. Check if the Secret name in the pod spec matches exactly, including case sensitivity.

3. If events indicate RBAC permission issues, leverage the Playbook RBAC verification results to confirm the service account has "get" and "list" permissions for Secrets. Check if Role or RoleBinding was recently modified or deleted.

4. If events indicate mount configuration problems, review the pod volume and volumeMount configuration from the Playbook describe output. Verify the Secret key names match the keys in the actual Secret data.

5. If events indicate service account issues, verify the pod's service account exists and is correctly referenced. Check if the service account was recently modified or if imagePullSecrets configuration changed.

6. If events are inconclusive, compare the event timestamps with recent deployment rollouts or pod template updates. Check if Secret references or mount paths were changed in the deployment configuration.

**If no clear cause is identified from events**: Review Secret data to ensure it is not empty or malformed, check if the Secret type matches expected usage (Opaque, kubernetes.io/dockerconfigjson, etc.), verify no admission webhooks are blocking Secret access, and examine if node-level issues are preventing volume mounts.

