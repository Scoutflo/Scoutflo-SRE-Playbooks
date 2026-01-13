---
title: HPA Not Responding to Metrics - Workload
weight: 250
categories:
  - kubernetes
  - workload
---

# HPANotRespondingtoMetrics-workload

## Meaning

The Horizontal Pod Autoscaler (HPA) is not responding to resource metrics (triggering KubeHPAReplicasMismatch or KubeDeploymentReplicasMismatch alerts) because the metrics-server pods are unavailable in kube-system namespace, resource metrics cannot be retrieved from the metrics.k8s.io/v1beta1 API, resource requests for CPU or memory are not defined in deployment pod templates, or the metrics API is not accessible due to network or authentication issues. HPAs show metrics unavailable conditions, metrics-server pods show failures in kube-system namespace, and HPA status shows FailedGetObjectMetric or FailedComputeMetricsReplicas errors. This affects the workload plane and prevents automatic scaling, typically caused by metrics-server failures or missing resource requests; applications cannot adapt to load changes and may show errors.

## Impact

HPA cannot scale pods based on CPU or memory metrics; deployments maintain fixed replica count regardless of resource utilization; automatic scaling is disabled; applications cannot adapt to load changes; pods remain at current replica count even when CPU or memory usage exceeds thresholds; HPA status shows metrics unavailable conditions; KubeHPAReplicasMismatch alerts fire when HPA desired replicas do not match deployment replicas; KubeDeploymentReplicasMismatch alerts fire when deployment cannot scale; manual intervention required for scaling; resource-based autoscaling fails. HPAs show metrics unavailable conditions indefinitely; metrics-server pods show failures; applications cannot adapt to load changes and may experience errors or performance degradation; automatic scaling is disabled.

## Playbook

1. Retrieve the HorizontalPodAutoscaler `<hpa-name>` in namespace `<namespace>` and inspect its status conditions and metrics to identify which metrics are unavailable or invalid.

2. List pods in the kube-system namespace and check the metrics-server pod status, logs, and readiness to verify it is running and functioning correctly.

3. Retrieve the Deployment `<deployment-name>` referenced by the HPA and verify that resource requests for CPU and memory are defined, as HPA requires resource requests to calculate metrics.

4. List events in namespace `<namespace>` and filter for HPA-related events, focusing on events with reasons such as `FailedGetObjectMetric`, `FailedComputeMetricsReplicas`, or messages indicating metrics unavailable.

5. From a test pod, execute `kubectl top pod` or equivalent metrics API queries using Pod Exec tool to verify if metrics are being collected and accessible.

6. Check the metrics-server service and endpoints to verify network connectivity and API accessibility for metrics retrieval.

## Diagnosis

1. Compare the HPA metrics unavailability timestamps with metrics-server pod restart or crash timestamps, and check whether metrics-server failures occurred within 5 minutes before metrics became unavailable.

2. Compare the HPA metrics unavailability timestamps with deployment resource request removal timestamps, and check whether resource requests were removed within 30 minutes before HPA stopped responding to metrics.

3. Compare the HPA metrics unavailability timestamps with metrics-server service or endpoint modification timestamps, and check whether service configuration changes occurred within 10 minutes before metrics became unavailable.

4. Compare the HPA metrics unavailability timestamps with network policy or security policy modification timestamps that may affect metrics-server access, and check whether policy changes occurred within 10 minutes before metrics retrieval failures.

5. Compare the HPA metrics unavailability timestamps with cluster upgrade or metrics-server deployment update timestamps, and check whether infrastructure changes occurred within 1 hour before metrics became unavailable.

6. Compare the HPA metrics unavailability timestamps with node resource pressure or metrics-server resource constraint timestamps, and check whether resource constraints prevented metrics collection within 5 minutes before failures.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review metrics-server logs for gradual performance degradation, check for intermittent network connectivity issues, examine if metrics API authentication or authorization issues developed over time, verify if metrics-server resource constraints accumulated gradually, and check for DNS or service discovery issues affecting metrics-server accessibility. Metrics unavailability may result from gradual infrastructure degradation rather than immediate changes.

