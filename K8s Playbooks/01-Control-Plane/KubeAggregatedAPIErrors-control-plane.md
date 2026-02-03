---
title: Kube Aggregated API Errors
weight: 20
---

# KubeAggregatedAPIErrors

## Meaning

Kubernetes aggregated API server is experiencing intermittent failures or high error rates (triggering KubeAggregatedAPIErrors alerts when errors appear unavailable over 4 times averaged over the past 10 minutes) because the aggregated API server is experiencing reliability problems, connectivity issues, or resource constraints. Aggregated API server pods show intermittent failures or high restart counts, aggregated API server logs show connection timeout errors or rate limit errors, and aggregated API endpoints return intermittent 500 or 503 errors. This affects the control plane and indicates degraded aggregated API functionality, typically caused by network instability, pod instability, configuration issues, or capacity problems; applications using custom resources may show errors.

## Impact

KubeAggregatedAPIErrors alerts fire; aggregated API endpoints return intermittent errors; custom resources may be unreliable; HPA may fail if using custom metrics; cluster functionality dependent on aggregated APIs is degraded; inability to see cluster metrics intermittently; unable to use custom metrics to scale reliably; cluster operations experience intermittent failures; custom resource definitions may be temporarily unavailable; metrics-based autoscaling becomes unreliable. Aggregated API endpoints return intermittent 500 or 503 errors; custom resources become unreliable; applications using custom resources may experience errors or performance degradation.

## Playbook

1. Describe all apiservice resources to retrieve detailed information about all aggregated API services and identify any services experiencing errors or intermittent failures.

2. List events in namespace kube-system sorted by last timestamp to retrieve recent control plane events, filtering for aggregated API errors, timeouts, or connectivity issues.

3. Retrieve the Pod `<pod-name>` in namespace `<namespace>` for aggregated API server deployments and inspect its status, restart count, and container states to identify pods in error states.

4. Retrieve logs from the Pod `<pod-name>` in namespace `<namespace>` and filter for error patterns including 'error', 'failed', 'timeout', 'connection refused', 'rate limit' to identify error causes.

5. Retrieve metrics for aggregated API server error rates and response times to identify error patterns and performance degradation.

6. Retrieve the Service `<service-name>` for aggregated API server endpoints in namespace `<namespace>` and verify network connectivity between API server and aggregated API server endpoints.

7. Retrieve NetworkPolicy resources in namespace `<namespace>` and check if network policies intermittently block communication between API server and aggregated API servers.

## Diagnosis

1. Analyze aggregated API server pod events from Playbook to identify if pod instability is causing intermittent errors. If events show restarts, probe failures, or transient errors, use event timestamps to correlate with error spikes.

2. If events indicate pod restarts or instability, examine restart patterns and causes from Playbook step 3. If restarts are frequent at timestamps when errors spike, pod instability is causing intermittent failures.

3. If events indicate network connectivity issues, verify service endpoints and connectivity from Playbook step 6. If network events show intermittent failures at error timestamps, network instability is the root cause.

4. If events indicate network policy changes, examine NetworkPolicy modifications from Playbook step 7. If policy changes occurred before errors increased, network configuration may be intermittently blocking communication.

5. If events indicate resource pressure, verify pod resource usage at error timestamps. If CPU or memory approached limits during error spikes, resource constraints are causing intermittent failures.

6. If events indicate API server load issues, analyze API server metrics at error timestamps. If API server latency or error rates increased when aggregated API errors spiked, upstream API server problems are contributing.

7. If events show consistent error patterns (not intermittent), the issue is persistent rather than transient. If errors occur at regular intervals, investigate scheduled operations or recurring triggers at those timestamps.

8. If events show intermittent error patterns, focus on transient causes such as network instability, resource bursts, or competing workloads at error timestamps.

**If no correlation is found**: Extend timeframes to 1 hour for infrastructure changes, review aggregated API server configuration, check for network instability, verify API server aggregation layer health, examine historical aggregated API error patterns. Aggregated API errors may result from network instability, resource constraints, or reliability issues rather than immediate changes.
