---
title: Kube HPA Maxed Out
weight: 20
---

# KubeHpaMaxedOut

## Meaning

Horizontal Pod Autoscaler has been running at maximum replicas for longer than 15 minutes (triggering KubeHpaMaxedOut alerts) because the HPA cannot scale beyond the configured maximum replica limit despite continued high resource demand. HPAs show current replicas matching maximum replicas, HPA target metrics show high resource utilization, and pod resource usage metrics indicate sustained high demand. This affects the workload plane and indicates that either the maximum replica limit is too low, resource requests are misconfigured, or the application requires more capacity than currently allocated, typically caused by sustained high load, inadequate maximum replica configuration, or resource quota constraints; ResourceQuota limits may prevent further scaling.

## Impact

KubeHpaMaxedOut alerts fire; HPA cannot add new pods to handle increased load; applications may experience performance degradation; autoscaling is ineffective; desired replica count matches maximum replicas; applications may become unavailable under sustained high load; scaling operations are blocked; HPA target metrics consistently indicate need for more replicas; applications cannot scale to meet demand despite high resource utilization. HPAs show current replicas matching maximum replicas indefinitely; HPA target metrics show sustained high resource utilization; ResourceQuota limits may prevent further scaling; applications may experience performance degradation or become unavailable under sustained high load.

## Playbook

1. Retrieve the HorizontalPodAutoscaler `<hpa-name>` in namespace `<namespace>` and inspect its status to check current replicas, desired replicas, maximum replicas, and target metrics.

2. Retrieve metrics for current resource usage (CPU, memory, or custom metrics) for pods managed by the HorizontalPodAutoscaler `<hpa-name>` in namespace `<namespace>` to verify high resource demand.

3. Retrieve the Pod `<pod-name>` in namespace `<namespace>` managed by HPA and verify pod resource requests and limits to compare with actual usage and identify misconfigurations.

4. Retrieve the ResourceQuota `<quota-name>` in namespace `<namespace>` and check for resource quota limits that may prevent scaling beyond current levels.

5. Retrieve events for the HorizontalPodAutoscaler `<hpa-name>` in namespace `<namespace>` and filter for scaling-related errors or constraints to identify scaling blockers.

6. Retrieve the Node `<node-name>` resources and verify node capacity and availability to support additional pod replicas if HPA could scale further.

## Diagnosis

Compare HPA reaching maximum replicas timestamp with resource usage metric trends over the last 1 hour and verify whether resource demand consistently exceeded maximum replica capacity, using HPA metrics and pod resource usage as supporting evidence.

Correlate HPA maxed out detection with resource quota exhaustion timestamps within 30 minutes and verify whether resource quotas prevented further scaling, using resource quota status and HPA scaling attempts as supporting evidence.

Analyze HPA target metric values over the last 15 minutes to determine if metrics consistently indicate need for more replicas, using HPA status and target metric values as supporting evidence.

Compare pod resource requests with actual resource usage at maxed out times and verify whether misconfigured resource requests caused premature maxing out, using pod metrics and resource specifications as supporting evidence.

Correlate HPA maxed out with node capacity exhaustion timestamps within 30 minutes and verify whether insufficient node capacity prevented scaling, using node metrics and cluster capacity data as supporting evidence.

Compare HPA maximum replica configuration with historical peak replica requirements over the last 7 days and verify whether maximum replicas are set too low for actual workload patterns, using HPA scaling history and workload metrics as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 7 days for capacity analysis, review HPA target metric configurations, check for application performance issues causing high resource usage, verify cluster autoscaler effectiveness, examine historical scaling patterns. HPA may be maxed out due to sustained high load, inadequate maximum replica limits, or application inefficiencies rather than immediate configuration issues.
