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

1. Describe deployment <deployment-name> in namespace <namespace> to see:
   - Resource requests and limits for all containers
   - Conditions showing why pod creation is failing
   - Events showing FailedCreate or quota exceeded errors

2. Retrieve events for deployment <deployment-name> in namespace <namespace> sorted by timestamp to see the sequence of quota-related errors.

3. Describe ResourceQuota objects in namespace <namespace> to identify which resource types have limits and compare used resources with hard limits.

4. List all pods in namespace <namespace> and analyse total resource requests to verify current namespace resource usage.

5. Describe pod <pod-name> in namespace <namespace> and inspect its resource requests to see which resources would exceed the quota.

6. Check if multiple deployments or workloads in namespace <namespace> are competing for the same quota limits by listing deployments, statefulsets, and daemonsets.

## Diagnosis

1. Analyze deployment and pod events from Playbook to identify quota-related errors. If events show "exceeded quota", "Forbidden", or "FailedCreate" errors, use event timestamps to determine when quota limits were first exceeded.

2. If events indicate quota exceeded errors, examine ResourceQuota status from Playbook step 3. If current usage equals or exceeds hard limits, identify which resource types (CPU, memory, pods, storage) are exhausted.

3. If events indicate recent deployment scaling, correlate scaling timestamps with quota errors. If replica increase events occurred before quota errors, scaling requests pushed usage beyond quota limits.

4. If events indicate resource request modifications, verify if per-pod requests were increased. If resource request events show increases before quota errors, higher per-pod allocation exceeded namespace quota.

5. If events indicate new workload deployments, identify additional workloads consuming quota. If new deployment events occurred in the namespace before quota errors, competing workloads exhausted available quota.

6. If events indicate ResourceQuota modifications, verify if limits were reduced. If quota modification events show reduced limits before errors, quota reduction caused existing workloads to exceed new limits.

7. If events indicate PVC creation (for storage quotas), verify storage quota consumption. If PVC events occurred before quota errors and storage limits are reached, storage quota is the constraint.

**If no correlation is found**: Extend the search window (30 minutes to 1 hour, 1 hour to 2 hours), review namespace resource usage trends for gradual quota exhaustion, check for cumulative resource requests from multiple deployments, examine if quota limits were always too restrictive but only recently enforced, verify if resource requests in existing pods were increased over time, and check for gradual workload growth that exceeded quota capacity. Resource quota issues may result from cumulative resource usage rather than immediate changes.

