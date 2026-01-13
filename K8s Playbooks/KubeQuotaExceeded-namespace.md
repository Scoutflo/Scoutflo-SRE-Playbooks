---
title: Kube Quota Exceeded
weight: 20
---

# KubeQuotaExceeded

## Meaning

Resource quota for a namespace has exceeded its hard limits (triggering KubeQuotaExceeded alerts) because resource usage (CPU, memory, pods, etc.) has reached or exceeded the configured quota maximums. ResourceQuota resources show current usage exceeding hard limits in kubectl, namespace events show 'exceeded quota' or 'Forbidden' errors, and resource creation operations fail. This affects the workload plane and prevents creation of new resources or scaling of existing workloads in the namespace, typically caused by normal workload growth, inadequate quota sizing, or resource request misconfigurations; applications cannot scale and may show errors.

## Impact

KubeQuotaExceeded alerts fire; inability to create resources in Kubernetes; new pods cannot be created; deployments fail to scale; resource creation is blocked; namespace operations are severely limited; applications cannot scale to meet demand; service degradation or unavailability. ResourceQuota resources show current usage exceeding hard limits indefinitely; namespace events show 'exceeded quota' or 'Forbidden' errors; resource creation operations fail; applications cannot scale and may experience errors or performance degradation.

## Playbook

1. Retrieve the ResourceQuota `<quota-name>` in namespace `<namespace>` and inspect its status to check current usage versus hard limits for all resource types to identify which quotas are exceeded.

2. List Pod resources in namespace `<namespace>` and aggregate resource requests to identify major resource consumers.

3. Retrieve the ResourceQuota `<quota-name>` in namespace `<namespace>` and check resource quota configuration to verify quota limits and scope.

4. Retrieve events for namespace `<namespace>` and filter for quota-related error patterns including 'exceeded quota', 'Forbidden', 'ResourceQuota' to identify quota-related errors.

5. Verify recent resource creation or scaling operations that may have triggered quota exhaustion by checking deployment and HPA scaling history.

6. List all resources in namespace `<namespace>` and check for unused or unnecessary resources that are consuming quota.

## Diagnosis

Compare quota exhaustion timestamps with deployment or scaling event timestamps within 30 minutes and verify whether quota was exceeded immediately after scaling operations, using resource quota metrics and deployment history as supporting evidence.

Correlate quota exhaustion with resource request misconfiguration detection within 1 hour and verify whether pods with excessive resource requests caused quota exhaustion, using pod resource specifications and quota usage as supporting evidence.

Analyze resource quota usage growth trends over the last 24 hours to identify which resource types exceeded limits first, using resource quota metrics and historical usage data as supporting evidence.

Compare quota exhaustion with HPA scaling event timestamps within 30 minutes and verify whether HPA scaling triggered quota exhaustion, using HPA events and resource quota status as supporting evidence.

Correlate quota exhaustion with namespace resource creation event timestamps within 1 hour and verify whether recent resource creation caused quota to be exceeded, using resource creation events and quota usage changes as supporting evidence.

Compare current quota limits with historical peak usage over the last 30 days and verify whether quota limits are set too low for actual workload requirements, using resource quota metrics and workload growth trends as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 30 days for capacity planning analysis, review namespace resource quota configurations, check for gradual workload growth exceeding quotas, verify resource request accuracy, examine historical quota usage patterns. Quota may be exceeded due to normal workload growth, inadequate quota sizing, or resource request misconfigurations rather than immediate operational changes.
