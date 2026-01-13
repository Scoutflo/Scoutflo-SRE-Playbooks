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

1. Retrieve the ResourceQuota `<quota-name>` in namespace `<namespace>` and inspect its status to check current usage versus hard limits for all resource types to verify approaching limits.

2. List Pod resources in namespace `<namespace>` and aggregate resource requests to identify major resource consumers.

3. Retrieve the ResourceQuota `<quota-name>` in namespace `<namespace>` and check resource quota configuration to verify quota limits and scope.

4. Retrieve metrics for resource usage trends in namespace `<namespace>` over the last 24 hours to identify growth patterns.

5. Verify if any recent deployments or scaling operations contributed to quota usage increase by checking deployment and HPA scaling history.

6. List all resources in namespace `<namespace>` and check for unused or unnecessary resources that could be cleaned up.

## Diagnosis

Compare resource quota usage growth trends with deployment or scaling event timestamps over the last 24 hours and verify whether recent scaling operations accelerated quota consumption, using resource quota metrics and deployment history as supporting evidence.

Correlate quota approaching limits with resource request misconfiguration detection within 1 hour and verify whether pods with excessive resource requests are consuming quota unnecessarily, using pod resource specifications and quota usage as supporting evidence.

Analyze resource quota usage patterns across resource types over the last 7 days to identify which resource types are growing fastest, using resource quota metrics and historical usage data as supporting evidence.

Compare current quota usage with historical baseline usage over the last 30 days and verify whether quota limits are set appropriately for actual workload requirements, using resource quota metrics and workload growth trends as supporting evidence.

Correlate quota approaching limits with namespace resource creation event timestamps within 1 hour and verify whether recent resource creation accelerated quota consumption, using resource creation events and quota usage changes as supporting evidence.

Compare quota configuration with similar namespace quotas to verify whether quota limits are consistent with namespace importance and workload requirements, using quota configurations and namespace characteristics as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 30 days for capacity planning analysis, review namespace resource quota configurations, check for gradual workload growth, verify resource request accuracy, examine historical quota usage patterns. Quota may be approaching limits due to normal workload growth, inadequate quota sizing, or resource request misconfigurations rather than immediate operational changes.
