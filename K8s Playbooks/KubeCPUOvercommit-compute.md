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

1. List Pod resources across the cluster and retrieve CPU request allocations to compare with total node CPU capacity.

2. Retrieve the Node `<node-name>` resources and check node allocatable CPU resources and current CPU request allocations across all nodes.

3. Verify cluster autoscaler status and logs for issues preventing node addition by checking cluster autoscaler configuration and logs.

4. Retrieve the Node `<node-name>` resources and check for cordoned or unschedulable nodes that reduce available cluster capacity.

5. Retrieve metrics for the Node `<node-name>` resources and compare CPU usage with CPU requests to identify overcommitment patterns.

6. Analyze CPU request distribution across namespaces to identify major consumers by aggregating CPU requests by namespace.

## Diagnosis

Compare CPU overcommit detection timestamps with node removal or cordoning event timestamps within 30 minutes and verify whether overcommit became critical after node capacity reduction, using node condition changes and CPU allocation metrics as supporting evidence.

Correlate CPU overcommit with deployment or HPA scaling event timestamps within 30 minutes and verify whether recent scaling operations triggered overcommitment, using deployment replica changes and CPU request allocations as supporting evidence.

Analyze CPU request growth trends over the last 24 hours to identify which workloads or namespaces contributed most to overcommitment, using CPU allocation metrics and workload scaling history as supporting evidence.

Compare cluster autoscaler activity timestamps with CPU overcommit detection times within 30 minutes and verify whether autoscaler failed to add nodes when capacity was needed, using autoscaler logs and node creation events as supporting evidence.

Correlate CPU overcommit with pod resource request misconfiguration detection within 1 hour and verify whether pods with excessive CPU requests caused overcommitment, using pod resource specifications and CPU allocation data as supporting evidence.

Compare current CPU requests with historical baseline requests over the last 7 days and verify whether overcommitment resulted from gradual request growth or sudden capacity reduction, using CPU allocation metrics and historical capacity data as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 7 days for capacity planning analysis, review pod resource request configurations, check for resource request misconfigurations, verify node pool capacity settings, examine cluster autoscaler configuration. CPU overcommit may result from inadequate capacity planning, misconfigured resource requests, or insufficient cluster scaling rather than immediate operational changes.
