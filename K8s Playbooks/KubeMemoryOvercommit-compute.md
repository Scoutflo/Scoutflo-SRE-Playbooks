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

1. List Pod resources across the cluster and retrieve memory request allocations to compare with total node memory capacity.

2. Retrieve the Node `<node-name>` resources and check node allocatable memory resources and current memory request allocations across all nodes.

3. Verify cluster autoscaler status and logs for issues preventing node addition by checking cluster autoscaler configuration and logs.

4. Retrieve the Node `<node-name>` resources and check for cordoned or unschedulable nodes that reduce available cluster capacity.

5. Retrieve metrics for the Node `<node-name>` resources and compare memory usage with memory requests to identify overcommitment patterns.

6. Analyze memory request distribution across namespaces to identify major consumers by aggregating memory requests by namespace.

## Diagnosis

Compare memory overcommit detection timestamps with node removal or cordoning event timestamps within 30 minutes and verify whether overcommit became critical after node capacity reduction, using node condition changes and memory allocation metrics as supporting evidence.

Correlate memory overcommit with deployment or HPA scaling event timestamps within 30 minutes and verify whether recent scaling operations triggered overcommitment, using deployment replica changes and memory request allocations as supporting evidence.

Analyze memory request growth trends over the last 24 hours to identify which workloads or namespaces contributed most to overcommitment, using memory allocation metrics and workload scaling history as supporting evidence.

Compare cluster autoscaler activity timestamps with memory overcommit detection times within 30 minutes and verify whether autoscaler failed to add nodes when capacity was needed, using autoscaler logs and node creation events as supporting evidence.

Correlate memory overcommit with pod resource request misconfiguration detection within 1 hour and verify whether pods with excessive memory requests caused overcommitment, using pod resource specifications and memory allocation data as supporting evidence.

Compare current memory requests with historical baseline requests over the last 7 days and verify whether overcommitment resulted from gradual request growth or sudden capacity reduction, using memory allocation metrics and historical capacity data as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 7 days for capacity planning analysis, review pod resource request configurations, check for resource request misconfigurations, verify node pool capacity settings, examine cluster autoscaler configuration. Memory overcommit may result from inadequate capacity planning, misconfigured resource requests, or insufficient cluster scaling rather than immediate operational changes.
