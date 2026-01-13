---
title: Context Deadline Exceeded - Control Plane
weight: 246
categories:
  - kubernetes
  - control-plane
---

# ContextDeadlineExceeded-control-plane

## Meaning

Kubernetes API requests are hitting their context deadlines because the API server or a downstream dependency is too slow to respond under current load, contention, or network conditions (potentially triggering KubeAPILatencyHigh or KubeAPIErrorsHigh alerts). This indicates API server performance degradation, etcd latency, or excessive API request rates overwhelming the control plane.

## Impact

API requests timeout; kubectl commands hang or fail; controllers experience delays in reconciliation; deployments and updates are delayed; cluster operations become unreliable; KubeAPILatencyHigh alerts fire; KubeAPIErrorsHigh alerts may fire; context deadline exceeded errors appear in logs; API request timeouts occur; etcd performance degradation may be observed.

## Playbook

1. Retrieve logs from API server pod in namespace `kube-system` and filter for timeout errors including "context deadline exceeded" or "request timeout".

2. Retrieve API server pod in namespace `kube-system` and check current API server timeout configuration and resource usage.

3. List events across all namespaces sorted by timestamp and filter for "too many requests" errors to check for high API request rates.

4. From a pod in the cluster, execute network connectivity tests such as `ping` or `curl` to the API server endpoint to test network connectivity.

5. Retrieve etcd pod in namespace `kube-system` and check etcd performance metrics and resource usage.

## Diagnosis

1. Compare the timestamps when timeout errors occurred (from API server logs) with large list operation timestamps from cluster events, and check whether timeouts begin within 1 minute of high-volume list operations.

2. Compare the timeout occurrence timestamps with API request rate spike timestamps from "too many requests" events, and verify whether timeouts consistently occur during request rate spikes.

3. Compare the timeout occurrence timestamps with controller or operator deployment scaling timestamps, and check whether timeouts correlate with scaling events within 5 minutes.

4. Compare the timeout occurrence timestamps with API server resource usage spike timestamps from pod metrics, and verify whether timeouts correlate with CPU or memory pressure on the API server.

5. Compare the timeout occurrence timestamps with ConfigMap or Deployment change timestamps in namespace `kube-system`, and check whether timeouts begin within 30 minutes of configuration changes.

6. Compare the timeout occurrence timestamps with network connectivity issue timestamps and etcd performance problem timestamps, and verify whether timeouts correlate with network failures or etcd latency spikes at the same time.

**If no correlation is found within the specified time windows**: Extend the search window (1 minute → 5 minutes, 30 minutes → 1 hour), review API server logs for earlier warning signs, check etcd performance metrics for gradual degradation, examine API request patterns for cumulative load increases, verify if API server resource limits are too restrictive, and check for network latency issues from multiple time points. Timeout issues may result from gradual performance degradation or cumulative load not immediately visible in single event timestamps.
