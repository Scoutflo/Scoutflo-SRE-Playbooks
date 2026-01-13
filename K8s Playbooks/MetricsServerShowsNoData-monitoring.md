---
title: Metrics Server Shows No Data - Monitoring
weight: 258
categories:
  - kubernetes
  - monitoring
---

# MetricsServerShowsNoData-monitoring

## Meaning

The metrics server is not collecting or reporting resource metrics (triggering KubeMetricsServerDown or KubeMetricsServerUnavailable alerts) because the metrics-server pods are not running in kube-system namespace, cannot collect metrics from kubelet on nodes, API server connectivity issues prevent metric reporting, or the metrics.k8s.io/v1beta1 API is not accessible. Metrics-server pods show CrashLoopBackOff or Failed state in kube-system namespace, kubectl top commands return no data or errors, and HPA status shows metrics unavailable conditions. This affects the monitoring plane and prevents HPA and resource-based autoscaling from functioning, typically caused by metrics-server pod failures or API connectivity issues; applications cannot automatically scale and may show errors.

## Impact

Metrics are unavailable; HPA cannot scale based on CPU or memory metrics; `kubectl top pod` and `kubectl top node` commands return no data or errors; resource usage metrics are missing; KubeMetricsServerDown alerts fire when metrics-server pods are not running; KubeMetricsServerUnavailable alerts fire when metrics API is unreachable; autoscaling is disabled; resource monitoring is broken; cluster resource visibility is lost; HPA status shows metrics unavailable conditions. Metrics-server pods remain in CrashLoopBackOff or Failed state indefinitely; kubectl top commands return no data or errors; applications cannot automatically scale and may experience errors or performance degradation; autoscaling is disabled.

## Playbook

1. List metrics-server pods in the kube-system namespace and check their status to verify if pods are running and ready.

2. Retrieve logs from the metrics-server pod `<metrics-server-pod-name>` in namespace kube-system and filter for errors, collection failures, or API connectivity issues.

3. Test metrics collection by executing `kubectl top pod` or `kubectl top node` to verify if metrics are being returned.

4. Verify API server connectivity from metrics-server pods by checking if the metrics server can reach the API server endpoint.

5. Check node connectivity from metrics-server pods by verifying if metrics can be collected from kubelet on nodes.

6. List events in namespace kube-system and filter for metrics-server-related events, focusing on events with reasons such as `Failed` or messages indicating collection failures.

## Diagnosis

1. Compare the metrics server no data timestamps with metrics-server pod restart or crash timestamps, and check whether pod failures occurred within 5 minutes before metrics became unavailable.

2. Compare the metrics server no data timestamps with API server unavailability or connectivity failure timestamps, and check whether API server issues occurred within 5 minutes before metrics became unavailable.

3. Compare the metrics server no data timestamps with metrics-server deployment configuration modification timestamps, and check whether configuration changes occurred within 30 minutes before metrics became unavailable.

4. Compare the metrics server no data timestamps with node kubelet unavailability timestamps, and check whether kubelet issues occurred within 5 minutes before metrics collection failures.

5. Compare the metrics server no data timestamps with cluster network plugin restart or failure timestamps, and check whether network infrastructure issues occurred within 1 hour before metrics became unavailable.

6. Compare the metrics server no data timestamps with cluster upgrade or metrics-server image update timestamps, and check whether infrastructure changes occurred within 1 hour before metrics became unavailable.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review metrics-server logs for gradual performance degradation, check for intermittent API server or kubelet connectivity issues, examine if metrics-server configuration drifted over time, verify if node resource constraints developed gradually, and check for network path issues that may have accumulated. Metrics unavailability may result from gradual infrastructure degradation rather than immediate changes.

