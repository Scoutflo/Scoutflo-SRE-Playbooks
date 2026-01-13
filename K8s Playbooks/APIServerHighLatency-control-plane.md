---
title: API Server High Latency - Control Plane
weight: 263
categories:
  - kubernetes
  - control-plane
---

# APIServerHighLatency-control-plane

## Meaning

The Kubernetes API server is experiencing high latency (triggering KubeAPILatencyHigh alerts) because it is under heavy load, experiencing resource constraints, network issues, or storage backend performance problems. API server metrics show high request latency exceeding 1 second, API server request queue depth metrics indicate request backlog, and etcd performance metrics may show latency issues. This affects the control plane and indicates API server performance degradation that delays cluster operations, typically caused by heavy load, resource constraints, etcd performance issues, or admission webhook timeouts; applications using Kubernetes API may show errors.

## Impact

API requests take longer than 1 second to complete; kubectl commands experience delays; controller reconciliation is slow; deployments and updates are delayed; cluster operations are sluggish; timeouts may occur; KubeAPILatencyHigh alerts fire; API server metrics show high request latency; cluster responsiveness is degraded. API server metrics show sustained high request latency; API server request queue depth metrics indicate request backlog; etcd performance metrics may show latency issues; applications using Kubernetes API may experience errors or performance degradation; controller reconciliation is slow.

## Playbook

1. Retrieve API server pod status in kube-system namespace and check for restarts, crashes, or health issues that may indicate underlying problems.

2. Retrieve API server pod metrics and logs to identify high latency patterns, focusing on request duration (apiserver_request_duration_seconds), queue depth (apiserver_request_queue_depth), and error rates.

3. Check etcd leader status by retrieving the etcd endpoints in kube-system namespace and verify if etcd leader election issues are occurring.

4. Check etcd performance metrics and health status since API server depends on etcd for storage backend, focusing on etcd_request_duration_seconds and etcd_leader_changes metrics to verify if etcd latency is contributing to API server delays.

5. Check API server admission webhook latency by reviewing admission webhook metrics (apiserver_admission_webhook_admission_duration_seconds) to verify if webhook timeouts are causing delays.

6. Check API server pod resource usage (CPU and memory) to verify if resource constraints are causing performance degradation.

7. List events in the kube-system namespace and filter for API server errors, throttling events, or performance-related issues.

8. Review API server audit logs or metrics for patterns in request types, clients, or operations that may be causing high load.

## Diagnosis

1. Compare the API server high latency timestamps with etcd performance degradation timestamps (etcd_request_duration_seconds spikes), and check whether etcd latency increases occur within 5 minutes before API server latency spikes.

2. Compare the API server high latency timestamps with etcd leader election change timestamps (etcd_leader_changes), and check whether leader election issues occurred within 5 minutes before API server latency spikes.

3. Compare the API server high latency timestamps with admission webhook response time spikes (apiserver_admission_webhook_admission_duration_seconds), and check whether webhook timeouts occurred within 5 minutes before API server latency increases.

4. Compare the API server high latency timestamps with API server request queue depth spikes (apiserver_request_queue_depth), and check whether queue depth increases occurred within 5 minutes before latency issues, indicating request backlog.

5. Compare the API server high latency timestamps with API server pod resource usage spikes (CPU or memory), and check whether resource pressure coincides with latency increases within 5 minutes.

6. Compare the API server high latency timestamps with API server pod restart or crash timestamps, and check whether pod instability occurs within 5 minutes before latency issues.

7. Compare the API server high latency timestamps with cluster scaling events or large resource creation timestamps, and check whether high-load operations occurred within 30 minutes before latency increases.

8. Compare the API server high latency timestamps with cluster upgrade, maintenance windows, or infrastructure change timestamps, and check whether system changes occurred within 1 hour before latency problems began.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review API server logs for gradual performance degradation patterns, check for cumulative resource pressure from multiple controllers or clients, examine etcd storage growth or compaction issues that may have developed over time, verify if network path issues accumulated gradually, and check for authentication or authorization processing delays that may have increased over time. API server latency may result from gradual system degradation rather than immediate changes.

