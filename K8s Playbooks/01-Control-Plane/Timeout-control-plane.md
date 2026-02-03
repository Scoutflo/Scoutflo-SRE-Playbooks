---
title: Timeout - API Server
weight: 237
categories:
  - kubernetes
  - control-plane
---

# Timeout-control-plane

## Meaning

The API server is timing out requests (triggering KubeAPILatencyHigh alerts) because it or its backing services such as etcd or critical network paths cannot process operations within the configured timeout window. API server latency exceeds thresholds, causing context deadline exceeded errors and request timeouts.

## Impact

API requests timeout; kubectl commands hang or fail; controllers experience delays; deployments and updates are delayed; cluster operations become unreliable; etcd may be overloaded; KubeAPILatencyHigh alerts fire; API server response times increase; TooManyRequests throttling occurs; control plane components become unresponsive.

## Playbook

1. Describe pods in namespace kube-system with label component=kube-apiserver to retrieve detailed API server pod information including status, resource usage, and timeout configuration.

2. List events in namespace kube-system sorted by last timestamp to retrieve recent control plane events, filtering for timeout errors, throttling (TooManyRequests), or context deadline exceeded messages.

3. Retrieve logs from the API server pod in `kube-system` and filter for timeout-related messages such as `context deadline exceeded` or `request timeout`.

4. List all nodes and retrieve resource usage metrics for control plane nodes to see whether they are under CPU or memory pressure during timeout periods.

5. From a test pod, verify basic TCP connectivity to the API server on port 6443 using tools such as `telnet`, `nc`, or `curl` to rule out network path issues.

6. Retrieve the etcd pod in `kube-system` and review its health and performance metrics (latency, disk I/O, leader elections) to detect backend slowness.

## Diagnosis

1. Analyze timeout and throttling events from Playbook to identify the pattern of timeout errors. If events show "context deadline exceeded", "TooManyRequests", or throttling messages, use event timestamps to determine when timeouts began.

2. If events indicate API server resource pressure, verify API server pod resource usage from Playbook step 4. If CPU or memory usage was high at timeout event timestamps, resource constraints are causing timeouts.

3. If events indicate etcd performance issues, analyze etcd pod health and metrics from Playbook step 6. If etcd events show latency spikes, slow requests, or leader elections at timestamps preceding timeouts, etcd is the root cause.

4. If events show scaling operations or high controller activity, identify which operations generated load. If events show large scaling operations or controller reconciliation at timeout timestamps, load-related factors are causing timeouts.

5. If events indicate API server restarts or instability, correlate restart timestamps with timeout patterns. If API server restarts occurred at or before timeout spikes, pod instability is contributing to timeout issues.

6. If events show network policy or firewall changes, correlate change timestamps with timeout onset. If network configuration modifications occurred before timeouts began, network changes may have introduced latency or connectivity issues.

7. If events show throttling (TooManyRequests), identify which clients or controllers are generating high request volumes. If specific clients appear in throttling events, targeted optimization can resolve the issue.

**If no correlation is found**: Extend the search window, review etcd performance metrics over a longer period for gradual degradation, check for cumulative API request rate increases, examine control plane node resource usage trends, and verify if timeout thresholds were recently modified. API timeouts may result from gradual resource exhaustion or cumulative load rather than immediate events.

