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

1. Retrieve the pod `<pod-name>` in namespace `<namespace>` and inspect pod volume configuration and environment variable sources to identify which ConfigMap is referenced.

2. List ConfigMaps in namespace `<namespace>` and verify if the referenced ConfigMap exists.

3. Retrieve the Deployment `<deployment-name>` in namespace `<namespace>` and review ConfigMap references in the pod template to verify the ConfigMap name is correct.

4. List events in namespace `<namespace>` and filter for ConfigMap-related events, focusing on events with reasons such as `FailedMount` or messages indicating ConfigMap not found.

5. Check the pod `<pod-name>` status and inspect container waiting state reason and message fields to identify ConfigMap not found errors.

6. Verify if the ConfigMap exists in a different namespace and if cross-namespace access is required and configured.

## Diagnosis

1. Compare the pod ConfigMap not found error timestamps with ConfigMap deletion timestamps, and check whether ConfigMaps were deleted within 30 minutes before pod failures.

2. Compare the pod ConfigMap not found error timestamps with deployment ConfigMap reference modification timestamps, and check whether ConfigMap name changes occurred within 30 minutes before not found errors.

3. Compare the pod ConfigMap not found error timestamps with namespace creation or pod namespace change timestamps, and check whether namespace mismatches occurred within 30 minutes before not found errors.

4. Compare the pod ConfigMap not found error timestamps with deployment rollout or pod template update timestamps, and check whether ConfigMap reference changes occurred within 1 hour before not found errors.

5. Compare the pod ConfigMap not found error timestamps with ConfigMap creation failure timestamps, and check whether ConfigMap creation failed within 30 minutes before pod failures.

6. Compare the pod ConfigMap not found error timestamps with cluster upgrade or namespace migration timestamps, and check whether infrastructure changes occurred within 1 hour before ConfigMap references became invalid.

**If no correlation is found within the specified time windows**: Extend the search window (30 minutes → 1 hour, 1 hour → 2 hours), review deployment history for ConfigMap reference changes, check for intermittent namespace or RBAC permission issues, examine if ConfigMap names drifted over time, verify if ConfigMaps were never created but referenced, and check for API server or etcd issues affecting ConfigMap retrieval. ConfigMap not found errors may result from gradual configuration drift rather than immediate deletions.

