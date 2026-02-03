---
title: Kubelet Too Many Pods
weight: 20
---

# KubeletTooManyPods

## Meaning

A specific node is running more than 95% of its pod capacity limit (110 by default, configurable) (triggering KubeletTooManyPods alerts) because the node has reached or is approaching the maximum number of pods it can support. Nodes show high pod count approaching capacity limits in cluster dashboards, node metrics indicate resource pressure from high pod density, and pod scheduling may fail for additional pods. This affects the data plane and indicates that pod density is too high, which may strain the Container Runtime Interface (CRI), Container Network Interface (CNI), and operating system resources, typically caused by scheduling imbalances, cluster capacity constraints, or workload distribution issues; applications running on affected nodes may experience performance degradation.

## Impact

KubeletTooManyPods alerts fire; running many pods on a single node places strain on CRI, CNI, and operating system; approaching pod limit may affect performance and availability of that node; node may become unable to schedule additional pods; node performance may degrade; container runtime operations may slow down; CRI, CNI, and operating system resources are strained. Nodes show high pod count approaching capacity limits; pod scheduling fails for additional pods; node performance degrades; applications running on affected nodes may experience performance degradation or resource contention.

## Playbook

1. Describe node <node-name> to see:
   - Conditions section showing Ready status and any pressure conditions
   - Capacity and Allocatable sections showing max pods configuration
   - Non-terminated Pods section showing current pod count and resource usage

2. Retrieve events for node <node-name> sorted by timestamp to see the sequence of node issues related to pod capacity.

3. List pods scheduled on node <node-name> and check the number of pods on node to verify high pod density.

4. Retrieve resource usage metrics for node <node-name> to see current CPU and memory utilization from high pod density.

5. List pods across all namespaces and check pod distribution to identify if pod density is concentrated on specific nodes.

6. Verify cluster autoscaler status and node availability for redistributing pod load by checking cluster autoscaler configuration and node pool status.

## Diagnosis

1. Analyze node events from Playbook step 2 to identify when pod capacity warnings or scheduling events occurred. Events indicating "FailedScheduling" with reason "TooManyPods" or node capacity warnings show the timeline of capacity exhaustion.

2. If node events indicate sudden pod count increase, check the pods list from Playbook step 3 to identify which workloads recently scheduled to this node. Look for recent pod creation timestamps and identify the deployments, jobs, or daemonsets responsible.

3. If node events show gradual pod accumulation, compare pod distribution from Playbook step 5 across all nodes. Uneven distribution indicates scheduling imbalances due to node affinity, taints, or resource constraints on other nodes.

4. If node events indicate resource pressure alongside high pod count, check resource usage metrics from Playbook step 4. High pod density combined with MemoryPressure or DiskPressure indicates the node is resource-constrained.

5. If node capacity and allocatable values from Playbook step 1 show the pod limit is being reached, verify whether the node's maxPods configuration is appropriate for the node size and workload requirements.

6. If cluster autoscaler is enabled, check autoscaler status from Playbook step 6 to verify whether new nodes should be provisioned to distribute the pod load, and why scaling may not be occurring.

7. If high pod count is isolated to this node while other nodes have capacity, investigate pod scheduling constraints (nodeSelector, affinity rules, tolerations) that force pods to this specific node.

**If no root cause is identified from events**: Review pod scheduling policies and affinity rules, check for taints on other nodes preventing scheduling, verify cluster-wide capacity and whether new nodes can be added, and examine workload scaling configurations that may be creating excessive pods.
