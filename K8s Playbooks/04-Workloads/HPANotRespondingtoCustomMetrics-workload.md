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

1. Describe HPA <hpa-name> in namespace <namespace> to see:
   - Current custom metrics versus target metrics
   - Desired replicas versus current replicas
   - Custom metrics configuration
   - Conditions showing why custom metrics are unavailable
   - Events showing FailedGetObjectMetric or custom metrics errors

2. Retrieve events for HPA <hpa-name> in namespace <namespace> sorted by timestamp to see the sequence of custom metrics failures.

3. List API services and check for metrics-related entries to verify if the custom metrics API (custom.metrics.k8s.io/v1beta1) is available and properly configured.

4. Check the custom metrics adapter pod status in kube-system namespace by listing pods with label app=prometheus-adapter (or app=custom-metrics-apiserver) and retrieve adapter logs to verify it is running and healthy.

5. Verify that the custom metrics adapter service and endpoints in kube-system namespace are accessible and test the custom metrics API availability.

6. Retrieve HPA <hpa-name> configuration in namespace <namespace> and verify that custom metric names referenced in the HPA spec match the metrics available from the custom metrics adapter.

## Diagnosis

1. Analyze HPA events from Playbook to identify custom metrics-related errors. If events show FailedGetObjectMetric, "unable to get custom metric", or "no such metric" errors, use event timestamps and error messages to identify the specific failure.

2. If events indicate custom metrics adapter issues, verify adapter pod status from Playbook step 4. If adapter events show CrashLoopBackOff, restarts, or failures at timestamps when HPA stopped responding, the adapter is the root cause.

3. If events indicate custom metrics API unavailability, verify API service status from Playbook step 3. If APIService events show unavailable or degraded status at failure timestamps, custom metrics API configuration needs attention.

4. If events indicate invalid metric names, verify HPA metric configuration from Playbook step 6. If HPA references metric names that do not exist in the adapter, correct the metric name references to match available metrics.

5. If events indicate Prometheus or external metrics source issues, verify source availability. If Prometheus events show failures at timestamps when custom metrics became unavailable, the metrics source is the root cause.

6. If events indicate service or endpoint changes, verify adapter service from Playbook step 5. If service events show modifications at timestamps when metrics became unavailable, service configuration changes affected metrics availability.

7. If events indicate recent deployments or upgrades, correlate change timestamps with failure onset. If adapter deployment events or cluster upgrade events occurred before custom metrics failures, recent changes may have broken the metrics pipeline.

**If no correlation is found**: Extend the search window (5 minutes to 10 minutes, 30 minutes to 1 hour, 1 hour to 2 hours), review custom metrics adapter logs for gradual performance degradation, check for intermittent connectivity issues with metrics sources, examine if custom metrics API authentication or authorization issues developed over time, verify if custom metrics adapter resource constraints accumulated gradually, and check for DNS or service discovery issues affecting custom metrics API accessibility. Custom metrics unavailability may result from gradual infrastructure degradation rather than immediate changes.

