---
title: HPA Not Responding to Custom Metrics - Workload
weight: 277
categories:
  - kubernetes
  - workload
---

# HPANotRespondingtoCustomMetrics-workload

## Meaning

The Horizontal Pod Autoscaler (HPA) is not responding to custom metrics (triggering KubeHPAReplicasMismatch or KubeDeploymentReplicasMismatch alerts) because the custom metrics API (custom.metrics.k8s.io/v1beta1) is not configured, the metrics adapter pods (prometheus-adapter, custom-metrics-apiserver) are unavailable in kube-system namespace, custom metrics are not being collected from external sources, or HPA references invalid custom metric names that do not exist in the metrics adapter. HPAs show custom metrics unavailable conditions, custom metrics adapter pods show failures in kube-system namespace, and HPA status shows FailedGetObjectMetric errors. This affects the workload plane and prevents custom metric-based scaling, typically caused by custom metrics adapter failures or invalid metric references; applications cannot adapt to business metric changes and may show errors.

## Impact

HPA cannot scale based on custom metrics; deployments maintain fixed replica count regardless of custom metric thresholds; application-specific scaling is disabled; pods cannot scale based on business metrics like request rate or queue depth; HPA status shows custom metrics unavailable conditions; scaling decisions are limited to resource metrics only; KubeHPAReplicasMismatch alerts fire when HPA desired replicas do not match deployment replicas; KubeDeploymentReplicasMismatch alerts fire when deployment cannot scale; custom metric-based autoscaling fails; applications cannot adapt to business metric changes. HPAs show custom metrics unavailable conditions indefinitely; custom metrics adapter pods show failures; applications cannot adapt to business metric changes and may experience errors or performance degradation; custom metric-based autoscaling fails.

## Playbook

1. Retrieve the HorizontalPodAutoscaler `<hpa-name>` in namespace `<namespace>` and inspect its status conditions and custom metrics configuration to identify which custom metrics are unavailable.

2. List CustomResourceDefinition objects and verify if the custom metrics API (metrics.k8s.io/v1beta1 or custom.metrics.k8s.io/v1beta1) is available and properly configured.

3. List pods in the kube-system namespace and check the custom metrics adapter pod status (e.g., prometheus-adapter, custom-metrics-apiserver) to verify it is running and healthy.

4. List events in namespace `<namespace>` and filter for HPA-related events, focusing on events with reasons such as `FailedGetObjectMetric` or messages indicating custom metrics unavailable.

5. Verify that the custom metrics adapter service and endpoints are accessible and that the custom metrics API server is responding to queries.

6. Check HPA configuration to verify that custom metric names referenced in the HPA spec match the metrics available from the custom metrics adapter.

## Diagnosis

1. Compare the HPA custom metrics unavailability timestamps with custom metrics adapter pod restart or failure timestamps, and check whether adapter failures occurred within 5 minutes before custom metrics became unavailable.

2. Compare the HPA custom metrics unavailability timestamps with custom metrics API configuration or CRD modification timestamps, and check whether API configuration changes occurred within 30 minutes before custom metrics became unavailable.

3. Compare the HPA custom metrics unavailability timestamps with HPA custom metric name modification timestamps, and check whether metric name changes occurred within 30 minutes before HPA stopped responding to custom metrics.

4. Compare the HPA custom metrics unavailability timestamps with custom metrics adapter service or endpoint modification timestamps, and check whether service configuration changes occurred within 10 minutes before custom metrics became unavailable.

5. Compare the HPA custom metrics unavailability timestamps with Prometheus or external metrics source unavailability timestamps, and check whether metrics source failures occurred within 5 minutes before custom metrics became unavailable.

6. Compare the HPA custom metrics unavailability timestamps with cluster upgrade or custom metrics adapter deployment update timestamps, and check whether infrastructure changes occurred within 1 hour before custom metrics became unavailable.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review custom metrics adapter logs for gradual performance degradation, check for intermittent connectivity issues with metrics sources, examine if custom metrics API authentication or authorization issues developed over time, verify if custom metrics adapter resource constraints accumulated gradually, and check for DNS or service discovery issues affecting custom metrics API accessibility. Custom metrics unavailability may result from gradual infrastructure degradation rather than immediate changes.

