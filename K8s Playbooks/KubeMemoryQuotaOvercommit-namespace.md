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

1. Retrieve the ResourceQuota `<quota-name>` in namespace `<namespace>` and inspect its status to check memory request usage versus quota limits.

2. List Pod resources in namespace `<namespace>` and aggregate memory requests to compare with namespace quota.

3. Retrieve the Node `<node-name>` resources and check node allocatable memory resources and current memory request allocations across all nodes.

4. Verify cluster autoscaler status and logs for issues preventing node addition by checking cluster autoscaler configuration and logs.

5. Retrieve the Node `<node-name>` resources and check for cordoned or unschedulable nodes that reduce available cluster capacity.

6. Retrieve metrics for the Node `<node-name>` resources and compare memory usage with memory requests to identify overcommitment patterns.

## Diagnosis

Compare namespace memory request growth trends with node capacity additions over the last 24 hours and verify whether request growth exceeded capacity expansion, using resource quota metrics and node addition timestamps as supporting evidence.

Correlate memory overcommit detection timestamps with node removal or cordoning events within 30 minutes and verify whether overcommit became critical after node capacity reduction, using node condition changes and resource quota status as supporting evidence.

Analyze memory request allocation patterns across namespaces over the last 1 hour to identify which namespaces contribute most to overcommitment, using resource quota metrics and pod resource specifications as supporting evidence.

Compare cluster autoscaler activity timestamps with memory overcommit detection times within 30 minutes and verify whether autoscaler failed to add nodes when capacity was needed, using autoscaler logs and node creation events as supporting evidence.

Correlate memory overcommit with deployment or HPA scaling event timestamps within 30 minutes and verify whether recent scaling operations triggered overcommitment, using deployment replica changes and HPA scaling history as supporting evidence.

Compare current memory requests with historical baseline requests over the last 7 days and verify whether overcommitment resulted from gradual request growth or sudden capacity reduction, using resource quota metrics and historical capacity data as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 7 days for capacity planning analysis, review namespace resource quota configurations, check for resource request misconfigurations, verify node pool capacity settings, examine cluster autoscaler configuration. Memory overcommit may result from inadequate capacity planning, misconfigured resource requests, or insufficient cluster scaling rather than immediate operational changes.
