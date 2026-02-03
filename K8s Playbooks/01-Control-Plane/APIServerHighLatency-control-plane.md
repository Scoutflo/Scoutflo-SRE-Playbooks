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

1. Describe API server pods in namespace kube-system with label component=kube-apiserver to retrieve detailed API server pod information including status, restarts, resource usage, and any warning conditions.

2. Retrieve events in namespace kube-system sorted by timestamp, filtering for API server errors, throttling events, or performance-related issues.

3. Retrieve API server pod metrics and logs to identify high latency patterns, focusing on request duration (apiserver_request_duration_seconds), queue depth (apiserver_request_queue_depth), and error rates.

4. Check etcd leader status by retrieving the etcd endpoints in kube-system namespace and verify if etcd leader election issues are occurring.

5. Check etcd performance metrics and health status since API server depends on etcd for storage backend, focusing on etcd_request_duration_seconds and etcd_leader_changes metrics to verify if etcd latency is contributing to API server delays.

6. Check API server admission webhook latency by reviewing admission webhook metrics (apiserver_admission_webhook_admission_duration_seconds) to verify if webhook timeouts are causing delays.

7. Check API server pod resource usage (CPU and memory) to verify if resource constraints are causing performance degradation.

8. Review API server audit logs or metrics for patterns in request types, clients, or operations that may be causing high load.

## Diagnosis

1. Analyze API server pod events from Playbook to identify if API server is restarting, resource constrained, or experiencing errors. If events indicate pod restarts or CrashLoopBackOff, correlate restart timestamps with latency spikes to confirm instability as root cause.

2. If events indicate resource pressure (OOMKilled, CPU throttling), verify API server pod resource usage against configured limits. If CPU or memory usage approaches limits during latency spike timestamps from events, resource constraints are the likely cause.

3. If events indicate etcd connectivity issues or timeout errors, analyze etcd pod events and health status. If etcd events show leader elections, slow requests, or unavailability at timestamps preceding API server latency events, etcd is the root cause.

4. If events indicate admission webhook timeouts or failures, review admission webhook metrics and logs. If webhook response times exceed thresholds at event timestamps, webhook latency is contributing to API server delays.

5. If events are inconclusive, analyze API server request queue depth metrics at event timestamps. If queue depth increases precede latency spikes, request backlog from high load is the likely cause.

6. If no pod-level issues are found, examine cluster-level events for scaling operations, large resource creations, or controller reconciliation storms. If cluster events show high-volume operations at timestamps preceding latency issues, load-related factors are the cause.

7. If events indicate network or infrastructure changes, correlate infrastructure change timestamps from events with latency onset. If changes occurred within 1 hour before latency began, infrastructure modifications may be the root cause.

**If no correlation is found**: Review API server logs for gradual performance degradation patterns, check for cumulative resource pressure from multiple controllers or clients, examine etcd storage growth or compaction issues, verify if network path issues accumulated gradually, and check for authentication or authorization processing delays. API server latency may result from gradual system degradation rather than immediate changes.

