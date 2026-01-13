---
title: Pods Exceeding Resource Quota - Workload
weight: 248
categories:
  - kubernetes
  - workload
---

# PodsExceedingResourceQuota-workload

## Meaning

Pods cannot be created or updated (triggering KubePodPending alerts) because the namespace ResourceQuota limits have been exceeded. ResourceQuota resources show current usage exceeding hard limits in kubectl, pod events show "exceeded quota" or "Forbidden" errors, and pod creation requests are rejected by the API server. This affects the workload plane and prevents new workloads from starting, typically caused by normal workload growth or inadequate quota sizing; applications cannot scale.

## Impact

New pods cannot be created; deployments fail to scale; pod creation requests are rejected; applications cannot deploy new replicas; services cannot get new pods; pods remain in Pending state; KubePodPending alerts fire; pod events show "exceeded quota" errors; namespace resource allocation is blocked. ResourceQuota resources show current usage exceeding hard limits indefinitely; pod events show "exceeded quota" or "Forbidden" errors; applications cannot scale and may experience errors or performance degradation.

## Playbook

1. Retrieve ResourceQuota objects in namespace `<namespace>` and inspect their spec to identify which resource types have limits (CPU, memory, pods, persistent volume claims, etc.).

2. Retrieve ResourceQuota status in namespace `<namespace>` and compare `status.used` with `spec.hard` to identify which quotas are exceeded.

3. List all pods in namespace `<namespace>` and calculate total resource requests to verify current namespace resource usage.

4. Retrieve the pod `<pod-name>` in namespace `<namespace>` that is failing and inspect its resource requests to see which resources would exceed the quota.

5. List events in namespace `<namespace>` and filter for quota-related errors, focusing on events with reasons such as `FailedCreate` and messages containing "exceeded quota" or "quota".

6. Check if multiple deployments or workloads in the namespace are competing for the same quota limits.

## Diagnosis

1. Compare the pod creation failure timestamps with ResourceQuota modification timestamps, and check whether quota limits were reduced within 30 minutes before pods started failing to create.

2. Compare the pod creation failure timestamps with deployment scaling or replica increase timestamps, and check whether workload increases occurred within 30 minutes before quota limits were exceeded.

3. Compare the pod creation failure timestamps with pod resource request modification timestamps in deployments, and check whether resource requests were increased within 30 minutes before quota limits were exceeded.

4. Compare the pod creation failure timestamps with new workload deployment timestamps in the namespace, and check whether additional workloads were added within 30 minutes before quota limits were exceeded.

5. Compare the pod creation failure timestamps with PersistentVolumeClaim creation timestamps if quota includes storage limits, and check whether PVC creation occurred within 30 minutes before quota limits were exceeded.

6. Compare the pod creation failure timestamps with namespace creation or ResourceQuota creation timestamps, and check whether quota constraints were introduced within 1 hour before pod creation failures, indicating newly enforced limits.

**If no correlation is found within the specified time windows**: Extend the search window (30 minutes → 1 hour, 1 hour → 2 hours), review namespace resource usage trends for gradual quota exhaustion, check for cumulative resource requests from multiple deployments, examine if quota limits were always too restrictive but only recently enforced, verify if resource requests in existing pods were increased over time, and check for gradual workload growth that exceeded quota capacity. Resource quota issues may result from cumulative resource usage rather than immediate changes.

