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

1. Describe API server pods in namespace kube-system with label component=kube-apiserver to retrieve detailed API server pod information including status, resource usage, and timeout configuration.

2. Retrieve events in namespace kube-system sorted by timestamp, filtering for timeout errors, "too many requests" errors, or context deadline exceeded messages.

3. Retrieve logs from API server pod in namespace kube-system and filter for timeout errors including "context deadline exceeded" or "request timeout".

4. From a pod in the cluster, verify network connectivity to the API server endpoint to test network connectivity.

5. Retrieve etcd pod information in namespace kube-system and check etcd performance metrics and resource usage.

## Diagnosis

1. Analyze timeout and throttling events from Playbook to identify the pattern of context deadline exceeded errors. If events show "too many requests" or throttling messages, high API request volume is the likely cause.

2. If events indicate API server resource pressure, verify API server pod resource usage at event timestamps. If CPU or memory usage approaches limits when timeout events occurred, resource constraints are causing timeouts.

3. If events indicate etcd connectivity issues or slow responses, analyze etcd pod events and health status. If etcd events show latency spikes or leader election issues at timestamps preceding timeout events, etcd performance is the root cause.

4. If events show controller or operator scaling activity, correlate scaling event timestamps with timeout onset. If timeouts began shortly after scaling operations, increased controller reconciliation load is overwhelming the API server.

5. If events indicate large list operations or watch storms, identify which clients or controllers are generating high request volumes. If events show specific resources or namespaces with high activity at timeout timestamps, targeted optimization can resolve the issue.

6. If events show configuration changes in kube-system namespace, correlate change timestamps with timeout onset. If configuration modifications occurred before timeouts began, recent changes may have introduced the problem.

7. If events indicate network issues or connectivity failures, verify network path health at event timestamps. If network events show failures or latency at the same time as timeouts, network problems are contributing factors.

**If no correlation is found**: Review API server logs for earlier warning signs, check etcd performance metrics for gradual degradation, examine API request patterns for cumulative load increases, verify if API server resource limits are too restrictive, and check for network latency issues. Timeout issues may result from gradual performance degradation or cumulative load.
