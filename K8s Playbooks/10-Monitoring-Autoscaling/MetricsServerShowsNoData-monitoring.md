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

1. Describe the metrics-server deployment in namespace `kube-system` to inspect its status, configuration, and events.

2. Retrieve events in the `kube-system` namespace sorted by timestamp to identify metrics-server-related failures and collection issues.

3. List metrics-server pods in the kube-system namespace and check their status to verify if pods are running and ready.

4. Retrieve logs from the metrics-server pod `<metrics-server-pod-name>` in namespace kube-system and filter for errors, collection failures, or API connectivity issues.

5. Test metrics collection by executing `kubectl top pod` or `kubectl top node` to verify if metrics are being returned.

6. Verify API server connectivity from metrics-server pods by checking if the metrics server can reach the API server endpoint.

7. Check node connectivity from metrics-server pods by verifying if metrics can be collected from kubelet on nodes.

## Diagnosis

Begin by analyzing the metrics-server deployment status, pod logs, and `kubectl top` test results collected in the Playbook section. Pod readiness, API connectivity, and kubelet accessibility provide the primary diagnostic signals.

**If metrics-server pods are not Running or show CrashLoopBackOff:**
- The metrics server itself is failing. Check pod logs for startup errors. Common causes include missing RBAC permissions, invalid command-line flags, or certificate issues.

**If logs show "unable to fetch metrics from node" or kubelet connection errors:**
- Metrics server cannot reach kubelet on nodes. Check if `--kubelet-insecure-tls` flag is needed (common in self-signed certificate environments). Verify kubelet is running and accessible on port 10250.

**If logs show certificate verification failures:**
- TLS certificate issues between metrics-server and kubelet. Add `--kubelet-insecure-tls` flag for testing, or properly configure kubelet serving certificates.

**If logs show API server connection failures:**
- Metrics server cannot register with the API server. Check metrics-server service account RBAC permissions. Verify the APIService `v1beta1.metrics.k8s.io` is registered and healthy.

**If `kubectl top` returns "metrics API not available":**
- The metrics API is not registered. Check if the APIService exists: `kubectl get apiservice v1beta1.metrics.k8s.io`. If missing, reinstall metrics-server.

**If metrics-server pod is Running but HPA shows "unknown" metrics:**
- Metrics are delayed or the specific metric is not available. Check metrics-server logs for collection errors. Verify the target pods have resource requests set (required for percentage-based HPA).

**If events are inconclusive, correlate timestamps:**
1. Check if metrics became unavailable after metrics-server Deployment changes by examining revision history.
2. Check if node kubelet issues occurred simultaneously across multiple nodes.
3. Check if API server configuration changes affected the metrics aggregation layer.

**If no clear cause is identified:** Test kubelet metrics endpoint directly from a debug pod: `curl -k https://<node-ip>:10250/stats/summary`. This isolates whether the issue is kubelet-side or metrics-server-side.

