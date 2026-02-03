---
title: ConfigMap Not Found - ConfigMap
weight: 209
categories:
  - kubernetes
  - configmap
---

# ConfigMapNotFound-configmap

## Meaning

ConfigMaps referenced in pods or deployments do not exist (triggering KubePodPending alerts) because the ConfigMap was never created, was deleted, is in a different namespace, or the reference name is incorrect. Pods show Pending or CrashLoopBackOff state, pod events show FailedMount errors with ConfigMap not found messages, and container waiting state reason may indicate ConfigMap access failures. This affects the workload plane and prevents pods from starting, typically caused by missing ConfigMaps or incorrect references; missing ConfigMap dependencies may block container initialization.

## Impact

Pods cannot start; deployments fail to create pods; ConfigMap references fail; pods remain in Pending state; KubePodPending alerts fire; applications cannot access configuration; environment variables are not populated; volume mounts fail; services cannot start without required config. Pods show Pending or CrashLoopBackOff state indefinitely; pod events show FailedMount errors with ConfigMap not found messages; missing ConfigMap dependencies may block container initialization; applications cannot start and may show errors.

## Playbook

1. Describe pod <pod-name> in namespace <namespace> to inspect pod volume configuration and environment variable sources to identify which ConfigMap is referenced - look in Events section for "FailedMount" with the specific ConfigMap name that is missing.

2. Retrieve events in namespace <namespace> for pod <pod-name> sorted by timestamp to see the sequence of ConfigMap-related failures, focusing on events with reasons such as FailedMount or messages indicating ConfigMap not found.

3. List ConfigMaps in namespace <namespace> and verify if the referenced ConfigMap exists.

4. Retrieve the Deployment <deployment-name> in namespace <namespace> and review ConfigMap references in the pod template to verify the ConfigMap name is correct.

5. Check the pod <pod-name> status in namespace <namespace> and inspect container waiting state reason and message fields to identify ConfigMap not found errors.

6. List ConfigMaps across all namespaces and search for <configmap-name> to verify if the ConfigMap exists in a different namespace and check if cross-namespace access is required and configured.

## Diagnosis

1. Analyze pod events from Playbook to identify the exact ConfigMap not found error. Events showing "FailedMount" with "configmap not found" confirm the ConfigMap does not exist. Note the specific ConfigMap name mentioned in the error message.

2. If events confirm ConfigMap not found, use Playbook results to verify whether the ConfigMap exists in the cluster. If the ConfigMap listing shows no matching ConfigMap in the pod's namespace, the ConfigMap was either never created or was deleted.

3. If the ConfigMap exists in a different namespace, compare the pod's namespace with where the ConfigMap was found. ConfigMaps cannot be accessed across namespaces - the ConfigMap must be created in the same namespace as the pod.

4. If the ConfigMap name appears correct, check for typos or case sensitivity issues. Compare the exact ConfigMap name in the pod spec (from Playbook describe output) with the actual ConfigMap names in the namespace.

5. If the ConfigMap was recently deleted, review the event timestamps to determine when the ConfigMap became unavailable. Check if a deployment or cleanup process removed the ConfigMap while pods still reference it.

6. If events indicate the ConfigMap reference was recently changed, review the deployment configuration from Playbook output. Check if a recent rollout introduced an incorrect ConfigMap name or if the ConfigMap dependency was not created as part of the deployment.

**If no clear cause is identified from events**: Verify if the ConfigMap creation is managed by Helm, Kustomize, or an operator that may have failed, check if the ConfigMap should be created by an init process that has not completed, and examine if the ConfigMap was part of a namespace migration or cluster restore that was incomplete.

