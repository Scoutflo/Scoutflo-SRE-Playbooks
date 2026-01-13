---
title: Invalid Memory/CPU Requests - Workload
weight: 231
categories:
  - kubernetes
  - workload
---

# InvalidMemoryCPURequests-workload

## Meaning

Pod CPU or memory requests or limits are configured to values that exceed node or namespace capacity, or violate resource policies (potentially triggering KubePodPending alerts), causing admission or scheduling to reject the pod configuration. This indicates resource specification errors, capacity mismatches, or quota violations preventing pod scheduling.

## Impact

Pods cannot be scheduled; deployments fail to create pods; applications cannot start; resource validation errors prevent workload deployment; services remain unavailable; KubePodPending alerts fire; pods remain in Pending state; resource admission failures occur; scheduling constraints prevent pod placement.

## Playbook

1. Retrieve pod `<pod-name>` in namespace `<namespace>` to find invalid resource specification.

2. List all nodes and retrieve resource usage metrics to verify current node capacity.

3. Retrieve deployment `<deployment-name>` in namespace `<namespace>` and check deployment resource requests and limits.

4. List events in namespace `<namespace>` and filter for resource-related errors.

5. Check pod status and error messages to verify resource validation errors.

## Diagnosis

1. Compare the timestamps when invalid resource errors occurred (from resource-related events) with resource request change timestamps from deployment modifications, and check whether errors begin within 1 hour of resource request changes.

2. Compare the invalid resource error timestamps with node capacity change timestamps, and verify whether errors correlate with node capacity reductions at the same time.

3. Compare the invalid resource error timestamps with deployment change timestamps, and check whether errors begin within 1 hour of deployment changes.

4. Compare the invalid resource error timestamps with resource limit change timestamps from deployment modifications, and verify whether errors correlate with limit increases within 1 hour.

5. Compare the invalid resource error timestamps with cluster scaling event timestamps, and check whether errors correlate with cluster capacity changes.

6. Compare the invalid resource error timestamps with resource quota change timestamps, and verify whether errors begin within 1 hour of quota modifications.

**If no correlation is found within the specified time windows**: Extend the search window (1 hour → 2 hours), review deployment resource specifications for calculation errors, check for namespace resource quota limits, examine node allocatable resources for capacity constraints, verify if resource requests exceed any node's capacity, check for resource policy violations, and review cluster resource capacity changes over time. Invalid resource errors may result from cumulative capacity reductions or quota constraints not immediately visible in single change events.
