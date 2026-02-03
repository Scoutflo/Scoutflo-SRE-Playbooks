---
title: Kube CPU Overcommit
weight: 20
---

# KubeCPUOvercommit

## Meaning

Cluster has overcommitted CPU resource requests for pods and cannot tolerate node failure (triggering KubeCPUOvercommit alerts) because the total CPU requests across all pods exceed available cluster capacity, preventing the cluster from maintaining availability during node failures. Pod CPU request allocations exceed total node CPU capacity, node allocatable CPU metrics indicate insufficient capacity, and pod scheduling may fail with InsufficientCPU errors. This affects the compute plane and indicates capacity planning issues where resource allocation exceeds physical resources, typically caused by inadequate capacity planning, misconfigured resource requests, or insufficient cluster scaling; cluster autoscaler may fail to add nodes.

## Impact

KubeCPUOvercommit alerts fire; cluster cannot tolerate node failure; in the event of a node failure, some pods will be in Pending state; new workloads cannot be scheduled; pod scheduling fails with InsufficientCPU errors; capacity constraints prevent workload deployment; cluster resilience is compromised. Pod CPU request allocations exceed total node CPU capacity; node allocatable CPU metrics indicate insufficient capacity; pod scheduling fails with InsufficientCPU errors; cluster autoscaler may fail to add nodes; applications cannot scale and may experience errors or performance degradation.

## Playbook

1. Describe all nodes to inspect allocatable CPU resources and current CPU request allocations.

2. Retrieve events across all namespaces sorted by timestamp to identify CPU-related scheduling failures and resource constraint events.

3. List Pod resources across the cluster and retrieve CPU request allocations to compare with total node CPU capacity.

4. Verify cluster autoscaler status and logs for issues preventing node addition by checking cluster autoscaler configuration and logs.

5. Retrieve the Node `<node-name>` resources and check for cordoned or unschedulable nodes that reduce available cluster capacity.

6. Retrieve metrics for the Node `<node-name>` resources and compare CPU usage with CPU requests to identify overcommitment patterns.

7. Analyze CPU request distribution across namespaces to identify major consumers by aggregating CPU requests by namespace.

## Diagnosis

Begin by analyzing the node allocatable resources, pod CPU requests, and events collected in the Playbook section. Node capacity versus total requests, scheduling failure events, and autoscaler status provide the primary diagnostic signals.

**If events show FailedScheduling with Insufficient cpu:**
- New pods cannot be scheduled due to CPU overcommit. The cluster needs more capacity. Either add nodes, reduce CPU requests on existing pods, or evict non-critical workloads.

**If node describe shows high CPU request allocation percentage (over 100%):**
- Total CPU requests exceed node capacity. Identify pods with largest CPU requests using the namespace aggregation from the Playbook. Target these for request optimization.

**If cluster autoscaler logs show "scale up needed but not possible":**
- Autoscaler cannot add nodes. Check for node pool limits, quota restrictions, or cloud provider capacity issues. Increase max nodes in autoscaler configuration or request quota increases.

**If autoscaler logs show "node not needed" despite overcommit:**
- Autoscaler configuration may have restrictive settings. Check `--scale-down-utilization-threshold` and ensure autoscaler considers CPU requests, not just usage.

**If specific namespaces dominate CPU requests:**
- Focus optimization on high-consuming namespaces. Review deployments in those namespaces for oversized CPU requests. Compare requests with actual usage to right-size.

**If overcommit occurred after node cordoning or removal:**
- Capacity reduction caused overcommit. Either uncordon the nodes if they are healthy, add replacement capacity, or reschedule workloads to remaining nodes.

**If events are inconclusive, correlate timestamps:**
1. Check if overcommit began after HPA scaled up deployments by examining replica count changes.
2. Check if nodes were removed or cordoned shortly before overcommit detection.
3. Check if new deployments with large CPU requests were created.

**If no clear cause is identified:** Compare CPU requests with actual CPU usage across pods. Pods with requests far exceeding usage are candidates for request reduction. Note that CPU requests primarily affect scheduling, while CPU limits affect throttling. Focus on right-sizing requests based on actual usage patterns.
