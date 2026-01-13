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

1. Retrieve logs from the API server pod in `kube-system` and filter for timeout-related messages such as `context deadline exceeded` or `request timeout`.

2. Inspect the API server pod definition in `kube-system` to review its resource requests and limits, and compare with actual resource usage metrics.

3. List all nodes and retrieve resource usage metrics for control plane nodes to see whether they are under CPU or memory pressure during timeout periods.

4. List events across all namespaces, sorted by timestamp, and filter for indications of high API request rates or throttling (for example, `TooManyRequests` reasons).

5. From a test pod, verify basic TCP connectivity to the API server on port 6443 using tools such as `telnet`, `nc`, or `curl` to rule out network path issues.

6. Retrieve the etcd pod in `kube-system` and review its health and performance metrics (latency, disk I/O, leader elections) to detect backend slowness.

## Diagnosis

1. Compare the API timeout log timestamps from the API server (log entries containing `timeout` or `request timeout`) with controller or operator pod restart timestamps in `kube-system`, and check whether restarts occur within 5 minutes of timeout spikes.

2. Compare the API timeout log timestamps with API server pod resource usage metrics (CPU and memory) and node metrics, and check whether timeouts align with periods of high resource utilization.

3. Compare the API timeout log timestamps with deployment scaling event timestamps from cluster events (events where `reason` contains `ScalingReplicaSet`), and check whether timeouts begin within 5 minutes of large scaling operations.

4. Compare API request rate spike timestamps from events (events where `reason` contains `TooManyRequests`) with controller pod creation/deletion timestamps in `kube-system`, and check whether bursts of controller activity align with timeout periods.

5. Compare the API timeout log timestamps with API server pod restart counts and restart timestamps, and check whether frequent restarts correspond to periods of increased timeouts.

6. Compare the API timeout log timestamps with NetworkPolicy modification timestamps and firewall rule change times, as well as with etcd performance metrics, and check whether new policies, firewall changes, or degraded etcd performance appear within 10 minutes of the timeout spikes.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 10 minutes → 30 minutes), review etcd performance metrics over a longer period for gradual degradation, check for cumulative API request rate increases, examine control plane node resource usage trends, and verify if timeout thresholds were recently modified. API timeouts may result from gradual resource exhaustion or cumulative load rather than immediate events.

