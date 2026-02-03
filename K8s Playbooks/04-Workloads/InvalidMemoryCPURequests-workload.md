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

1. Describe deployment <deployment-name> in namespace <namespace> to see:
   - Resource requests and limits for all containers
   - Conditions showing why pod creation is failing
   - Events showing resource validation errors or scheduling failures

2. Retrieve events for deployment <deployment-name> in namespace <namespace> sorted by timestamp to see the sequence of resource-related errors.

3. Describe pod <pod-name> in namespace <namespace> to find invalid resource specification and detailed error messages.

4. Analyse node capacity by describing nodes and checking allocated resources to verify current node capacity.

5. Describe ResourceQuota and LimitRange objects in namespace <namespace> to verify namespace constraints.

## Diagnosis

1. Analyze deployment and pod events from Playbook to identify resource validation or scheduling errors. If events show "Insufficient" errors, "exceeds" messages, or admission rejections, use event timestamps and error details to identify the specific constraint.

2. If events indicate pod resource requests exceed node capacity, analyze node capacity from Playbook step 4. If no single node can accommodate the pod's resource requests, reduce requests or add larger nodes.

3. If events indicate LimitRange violations, examine LimitRange configuration from Playbook step 5. If pod requests violate LimitRange min/max constraints, adjust requests to comply with namespace policies.

4. If events indicate ResourceQuota violations, verify quota status from Playbook step 5. If adding the pod would exceed namespace quota limits, quota must be increased or existing workloads reduced.

5. If events indicate recent deployment modifications, correlate modification timestamps with error onset. If resource specification changes occurred before validation errors, recent changes introduced invalid values.

6. If events indicate recent node changes, verify if node capacity decreased. If node removal or resizing events occurred before errors, reduced cluster capacity caused previously valid requests to become unschedulable.

7. If events indicate configuration calculation issues, verify resource request values in deployment spec. If requests are unreasonably large (e.g., typos like 100Gi memory instead of 100Mi), correct the specification errors.

**If no correlation is found**: Extend the search window (1 hour to 2 hours), review deployment resource specifications for calculation errors, check for namespace resource quota limits, examine node allocatable resources for capacity constraints, verify if resource requests exceed any node's capacity, check for resource policy violations, and review cluster resource capacity changes over time. Invalid resource errors may result from cumulative capacity reductions or quota constraints not immediately visible in single change events.
