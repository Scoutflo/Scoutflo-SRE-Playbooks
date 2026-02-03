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

1. Describe the ResourceQuota `<quota-name>` in namespace `<namespace>` to inspect its status and check current usage versus hard limits for all resource types to identify which quotas are exceeded.

2. Retrieve events in namespace `<namespace>` sorted by timestamp to identify quota-related errors including 'exceeded quota', 'Forbidden', 'ResourceQuota'.

3. List Pod resources in namespace `<namespace>` and aggregate resource requests to identify major resource consumers.

4. Retrieve the ResourceQuota `<quota-name>` in namespace `<namespace>` and check resource quota configuration to verify quota limits and scope.

5. Verify recent resource creation or scaling operations that may have triggered quota exhaustion by checking deployment and HPA scaling history.

6. List all resources in namespace `<namespace>` and check for unused or unnecessary resources that are consuming quota.

## Diagnosis

1. Analyze namespace events from Playbook to identify quota violation details. Events showing "exceeded quota" or "Forbidden" specify which resource type exceeded limits and by how much. This pinpoints the immediate constraint blocking operations.

2. If events indicate failed pod creation due to quota exceeded, identify what operation attempted to create the pod. Common sources include Deployments scaling up, Jobs starting, CronJobs triggering, or HPA adding replicas.

3. If events indicate CPU or memory requests exceeded quota, analyze which pods have the largest resource requests from Playbook. Pods with requests significantly larger than actual usage may be over-provisioned and consuming quota unnecessarily.

4. If quota was recently exceeded (events have recent timestamps), correlate with deployment or scaling events. A new deployment, version upgrade increasing resource requests, or HPA scaling activity may have pushed usage over limits.

5. If quota shows exceeded but all visible pods are running, check for resource types other than pods - such as PersistentVolumeClaims, Services, or ConfigMaps that may also be quota-limited. ResourceQuota can limit many resource types.

6. If limit ranges are configured in the namespace, pods without explicit resource requests get default values assigned. These defaults may be higher than necessary and cause unexpected quota consumption.

7. If quota limits appear too low for legitimate workload needs, compare current quota configuration with actual workload requirements. Consider whether quota should be increased or if workload resource requests should be right-sized based on actual usage patterns.
