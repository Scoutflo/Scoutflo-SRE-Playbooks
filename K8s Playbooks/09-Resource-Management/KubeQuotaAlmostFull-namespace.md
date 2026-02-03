---
title: Kube Quota Almost Full
weight: 20
---

# KubeQuotaAlmostFull

## Meaning

Resource quota for a namespace is approaching its limits (triggering KubeQuotaAlmostFull alerts) because resource usage (CPU, memory, pods, etc.) is close to the configured quota maximums. ResourceQuota resources show current usage approaching hard limits in kubectl, resource usage metrics indicate increasing trends, and namespace capacity constraints become critical. This affects the workload plane and indicates that the namespace may soon be unable to create new resources or scale existing workloads, typically caused by normal workload growth, inadequate quota sizing, or resource request misconfigurations; applications may be unable to scale and may show errors.

## Impact

KubeQuotaAlmostFull alerts fire; future deployments may not be possible; scaling operations may fail; new pods cannot be created; resource quota usage approaches limits; namespace capacity constraints become critical; applications may be unable to scale to meet demand. ResourceQuota resources show current usage approaching hard limits; resource usage metrics indicate increasing trends; applications may be unable to scale and may experience errors or performance degradation; namespace capacity constraints become critical.

## Playbook

1. Describe the ResourceQuota `<quota-name>` in namespace `<namespace>` to inspect its status and check current usage versus hard limits for all resource types.

2. Retrieve events in namespace `<namespace>` sorted by timestamp to identify quota-related events and resource allocation warnings.

3. List Pod resources in namespace `<namespace>` and aggregate resource requests to identify major resource consumers.

4. Retrieve metrics for resource usage trends in namespace `<namespace>` over the last 24 hours to identify growth patterns.

5. Verify if any recent deployments or scaling operations contributed to quota usage increase by checking deployment and HPA scaling history.

6. List all resources in namespace `<namespace>` and check for unused or unnecessary resources that could be cleaned up.

## Diagnosis

1. Analyze ResourceQuota status from Playbook to identify which resource types are approaching limits. Compare current usage against hard limits for each resource type (cpu, memory, pods, etc.) to determine which will be exhausted first.

2. If CPU or memory requests are approaching limits, analyze pod resource requests from Playbook. Identify pods with the largest requests and evaluate if those requests match actual usage. Over-provisioned requests waste quota capacity.

3. If pod count is approaching limit, count running pods from Playbook. Determine if the pod count represents necessary workloads or if orphaned pods, completed jobs, or failed pods could be cleaned up.

4. If events show recent scaling activity or deployments, correlate quota growth with those operations. Increasing replica counts or deploying new services directly increases quota consumption.

5. If quota usage has grown gradually without obvious triggering events, examine namespace usage trends over time. Normal workload growth may require periodic quota increases as part of capacity planning.

6. If multiple resource types are simultaneously approaching limits, the namespace may need a comprehensive quota increase. If only one resource type is near limit while others have capacity, consider rebalancing resource requests or quota allocation.

7. If quota limits appear appropriate but usage is high, evaluate workload efficiency. Right-sizing pod resource requests based on actual usage can reclaim significant quota capacity without changing workload functionality.
