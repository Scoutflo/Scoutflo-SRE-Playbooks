---
title: Kube Quota Fully Used
weight: 20
---

# KubeQuotaFullyUsed

## Meaning

Resource quota for a namespace has reached its hard limits (triggering KubeQuotaFullyUsed alerts) because resource usage (CPU, memory, pods, etc.) has reached the configured quota maximums. ResourceQuota resources show current usage matching hard limits in kubectl, namespace events show 'exceeded quota' or 'Forbidden' errors, and resource creation operations fail. This affects the workload plane and prevents creation of new resources or scaling of existing workloads in the namespace, typically caused by normal workload growth, inadequate quota sizing, or resource request misconfigurations; applications cannot scale and may show errors.

## Impact

KubeQuotaFullyUsed alerts fire; new app installations may not be possible; resource creation is blocked; deployments fail to scale; namespace has reached capacity limits; applications cannot scale to meet demand; service degradation or unavailability for new workloads; resource creation and scaling operations are completely blocked. ResourceQuota resources show current usage matching hard limits indefinitely; namespace events show 'exceeded quota' or 'Forbidden' errors; resource creation operations fail; applications cannot scale and may experience errors or performance degradation.

## Playbook

1. Describe the ResourceQuota `<quota-name>` in namespace `<namespace>` to inspect its status and check current usage versus hard limits for all resource types to identify which quotas are fully used.

2. Retrieve events in namespace `<namespace>` sorted by timestamp to identify quota-related errors including 'exceeded quota', 'Forbidden', 'ResourceQuota'.

3. List Pod resources in namespace `<namespace>` and aggregate resource requests to identify major resource consumers.

4. Retrieve the ResourceQuota `<quota-name>` in namespace `<namespace>` and check resource quota configuration to verify quota limits and scope.

5. Verify recent resource creation or scaling operations that may have caused quota to reach limits by checking deployment and HPA scaling history.

6. List all resources in namespace `<namespace>` and check for unused or unnecessary resources that are consuming quota.

## Diagnosis

1. Analyze namespace events from Playbook to identify quota-related failures. Events showing "exceeded quota" or "Forbidden" indicate which operations failed due to quota limits. The event messages specify which resource type (cpu, memory, pods, etc.) is at capacity.

2. If events indicate pod quota reached (pods count at limit), identify the number of running pods from Playbook. Determine if this represents expected workload size or if orphaned pods, failed jobs, or completed pods are consuming quota unnecessarily.

3. If events indicate CPU or memory request quota reached, analyze pod resource requests from Playbook. Identify pods with disproportionately large resource requests. A few pods with excessive requests can consume quota that could otherwise support many smaller pods.

4. If events correlate with HPA scaling activity, the autoscaler attempted to add replicas but hit quota limits. Check HPA status from Playbook to see current versus desired replicas. The HPA will continue attempting to scale but cannot proceed until quota is available.

5. If events correlate with recent deployments or job launches, those new workloads pushed quota usage to the limit. Identify recently created resources and verify their resource requests are appropriate.

6. If no clear triggering event exists, the quota reached limits through gradual growth. Compare current usage breakdown from Playbook (used vs hard limits for each resource type) to identify which resources are constrained. Multiple resource types may be at or near limits.

7. If quota appears correctly sized but is fully used, evaluate whether the namespace genuinely needs more capacity or if workload resource requests are over-provisioned. Consider whether completed jobs or failed pods can be cleaned up to reclaim quota.
