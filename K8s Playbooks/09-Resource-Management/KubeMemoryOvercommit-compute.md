---
title: Kube Memory Overcommit
weight: 20
aliases:
  - /kubememovercommit/
---

# KubeMemoryOvercommit

## Meaning

Cluster has overcommitted memory resource requests for pods and cannot tolerate node failure (triggering KubeMemoryOvercommit alerts) because the total memory requests across all pods exceed available cluster capacity, preventing the cluster from maintaining availability during node failures. Pod memory request allocations exceed total node memory capacity, node allocatable memory metrics indicate insufficient capacity, and pod scheduling may fail with InsufficientMemory errors. This affects the compute plane and indicates capacity planning issues where memory allocation exceeds physical resources, typically caused by inadequate capacity planning, misconfigured resource requests, or insufficient cluster scaling; cluster autoscaler may fail to add nodes.

## Impact

KubeMemoryOvercommit alerts fire; cluster cannot tolerate node failure; in the event of a node failure, some pods will be in Pending state; new workloads cannot be scheduled; pod scheduling fails with InsufficientMemory errors; capacity constraints prevent workload deployment; cluster resilience is compromised. Pod memory request allocations exceed total node memory capacity; node allocatable memory metrics indicate insufficient capacity; pod scheduling fails with InsufficientMemory errors; cluster autoscaler may fail to add nodes; applications cannot scale and may experience errors or performance degradation.

## Playbook

1. Describe all nodes to inspect allocatable memory resources and current memory request allocations.

2. Retrieve events across all namespaces sorted by timestamp to identify memory-related scheduling failures and resource constraint events.

3. List Pod resources across the cluster and retrieve memory request allocations to compare with total node memory capacity.

4. Verify cluster autoscaler status and logs for issues preventing node addition by checking cluster autoscaler configuration and logs.

5. Retrieve the Node `<node-name>` resources and check for cordoned or unschedulable nodes that reduce available cluster capacity.

6. Retrieve metrics for the Node `<node-name>` resources and compare memory usage with memory requests to identify overcommitment patterns.

7. Analyze memory request distribution across namespaces to identify major consumers by aggregating memory requests by namespace.

## Diagnosis

Begin by analyzing the node allocatable resources, pod memory requests, and events collected in the Playbook section. Node capacity versus total requests, scheduling failure events, and autoscaler status provide the primary diagnostic signals.

**If events show FailedScheduling with Insufficient memory:**
- New pods cannot be scheduled due to memory overcommit. The cluster needs more capacity. Either add nodes, reduce memory requests on existing pods, or evict non-critical workloads.

**If node describe shows high memory request allocation percentage (over 100%):**
- Total memory requests exceed node capacity. Identify pods with largest memory requests using the namespace aggregation from the Playbook. Target these for request optimization.

**If cluster autoscaler logs show "scale up needed but not possible":**
- Autoscaler cannot add nodes. Check for node pool limits, quota restrictions, or cloud provider capacity issues. Increase max nodes in autoscaler configuration or request quota increases.

**If autoscaler logs show "node not needed" despite overcommit:**
- Autoscaler configuration may have restrictive settings. Check `--scale-down-utilization-threshold` and ensure autoscaler considers memory requests, not just usage.

**If specific namespaces dominate memory requests:**
- Focus optimization on high-consuming namespaces. Review deployments in those namespaces for oversized memory requests. Compare requests with actual usage to right-size.

**If overcommit occurred after node cordoning or removal:**
- Capacity reduction caused overcommit. Either uncordon the nodes if they are healthy, add replacement capacity, or reschedule workloads to remaining nodes.

**If events are inconclusive, correlate timestamps:**
1. Check if overcommit began after HPA scaled up deployments by examining replica count changes.
2. Check if nodes were removed or cordoned shortly before overcommit detection.
3. Check if new deployments with large memory requests were created.

**If no clear cause is identified:** Compare memory requests with actual memory usage across pods. Pods with requests far exceeding usage are candidates for request reduction. Use metrics to establish baseline usage patterns before adjusting requests.
