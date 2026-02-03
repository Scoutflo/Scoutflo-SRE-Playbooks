---
title: Kube Memory Quota Overcommit
weight: 20
aliases:
  - /kubememquotaovercommit/
---

# KubeMemoryQuotaOvercommit

## Meaning

Cluster has overcommitted memory resource requests for namespaces (triggering KubeMemoryQuotaOvercommit alerts) because the total memory requests across all pods exceed available cluster capacity, preventing the cluster from tolerating node failures. ResourceQuota resources show memory request usage exceeding available cluster capacity, node allocatable memory metrics indicate insufficient capacity, and pod scheduling may fail with InsufficientMemory errors. This indicates capacity planning issues in the compute plane, where memory allocation exceeds physical or allocatable resources, typically caused by inadequate capacity planning, misconfigured resource requests, or insufficient cluster scaling; cluster autoscaler may fail to add nodes.

## Impact

KubeMemoryQuotaOvercommit alerts fire; in the event of a node failure, pods will be in Pending state due to insufficient memory resources; new workloads cannot be scheduled; deployments fail to scale; cluster cannot tolerate node failures; pod scheduling fails with InsufficientMemory errors; capacity constraints prevent workload deployment. ResourceQuota resources show memory request usage exceeding available cluster capacity; node allocatable memory metrics indicate insufficient capacity; pod scheduling fails with InsufficientMemory errors; cluster autoscaler may fail to add nodes; applications cannot scale and may experience errors or performance degradation.

## Playbook

1. Describe the ResourceQuota `<quota-name>` in namespace `<namespace>` to inspect its status and check memory request usage versus quota limits.

2. Retrieve events in namespace `<namespace>` sorted by timestamp to identify quota-related events and resource allocation issues.

3. List Pod resources in namespace `<namespace>` and aggregate memory requests to compare with namespace quota.

4. Retrieve the Node `<node-name>` resources and check node allocatable memory resources and current memory request allocations across all nodes.

5. Verify cluster autoscaler status and logs for issues preventing node addition by checking cluster autoscaler configuration and logs.

6. Retrieve the Node `<node-name>` resources and check for cordoned or unschedulable nodes that reduce available cluster capacity.

7. Retrieve metrics for the Node `<node-name>` resources and compare memory usage with memory requests to identify overcommitment patterns.

## Diagnosis

1. Analyze events from Playbook to identify memory-related scheduling failures. Events showing "InsufficientMemory" or "FailedScheduling" indicate pods that could not be placed due to memory constraints. The timestamps indicate when overcommit became problematic.

2. If events indicate pods pending due to insufficient memory, compare total memory requests across all pods with total node allocatable memory from Playbook. This shows the extent of overcommitment and how much additional capacity is needed.

3. If overcommit correlates with node removal or cordoning events, capacity reduction caused the overcommit condition. Check node events for recently removed, cordoned, or NotReady nodes that reduced available cluster memory.

4. If overcommit correlates with recent scaling or deployment events, those operations increased memory requests beyond available capacity. Identify which deployments scaled up or which new workloads were deployed.

5. If cluster autoscaler events show scaling failures or no scaling activity despite pending pods, verify autoscaler status from Playbook. Check for node group maximum limits, cloud provider quota limits, or autoscaler configuration issues preventing capacity expansion.

6. If overcommit exists but no pods are currently pending, the cluster may tolerate the condition until a node failure occurs. A node failure would cause pods to be evicted but unable to reschedule due to insufficient remaining capacity.

7. If memory requests across namespaces significantly exceed actual memory usage (high request-to-usage ratio), consider right-sizing pod memory requests. Over-provisioned requests cause artificial overcommit that could be resolved by reducing requests to match actual usage patterns.
