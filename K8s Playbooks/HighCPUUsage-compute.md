---
title: High CPU Usage - Cluster
weight: 290
categories:
  - kubernetes
  - compute
---

# HighCPUUsage-compute

## Meaning

One or more nodes or control-plane components are running at sustained high CPU utilization (potentially triggering KubeCPUOvercommit alerts or KubeAPILatencyHigh if affecting API server), leaving very little headroom for normal operations or new workload traffic. High CPU usage causes performance degradation, throttling, and delayed cluster operations.

## Impact

Control plane components become slow; API server response times increase; cluster operations are delayed; nodes may become unresponsive; applications may experience performance degradation; CPU throttling occurs; KubeAPILatencyHigh alerts may fire; API request processing slows; controller reconciliation delays; node resource pressure increases.

## Playbook

1. Retrieve CPU usage metrics for all nodes and identify nodes consistently running at or near high utilization thresholds.

2. List pods in `kube-system` and retrieve CPU usage metrics for control plane pods (such as API server, controller-manager, scheduler, and etcd) to see if any are hot spots.

3. List pods across all namespaces and retrieve CPU usage metrics to identify specific workloads consuming unusually high CPU.

4. List all nodes and check their conditions for CPU-related resource pressure, such as `OutOfcpu` or general resource pressure indicators.

5. Check API server logs and metrics for elevated request rates or throttling events that may correlate with observed CPU spikes.

## Diagnosis

1. Compare the high CPU usage timestamps from node and pod metrics with deployment or scaling event timestamps (events where `reason` contains `ScalingReplicaSet`), and check whether CPU spikes begin within 30 minutes of large scaling operations.

2. Compare the high CPU usage timestamps with control plane pod restart timestamps in `kube-system` and check whether restarts occur within 5 minutes of CPU spikes.

3. Compare the high CPU usage timestamps with API server request rate metrics or events indicating throttling, and check whether CPU spikes align with sustained high QPS or `TooManyRequests` events.

4. Compare the high CPU usage timestamps with workload resource request changes, and check whether CPU increases started within 1 hour of changes that raised requested or actual load.

5. Compare the high CPU usage timestamps with cluster upgrade or maintenance window timestamps, and check whether CPU behavior changed significantly within 1 hour of upgrade activities.

6. Compare the high CPU usage timestamps with node capacity changes from node status and check whether CPU pressure began within 1 hour after capacity reductions or node pool downsizing.

**If no correlation is found within the specified time windows**: Extend the search window (30 minutes → 1 hour, 1 hour → 2 hours), review CPU usage trends over a longer period to identify gradual increases, check for cumulative workload additions that occurred over time, examine HPA scaling behavior for delayed effects, verify if resource requests were increased incrementally, and check for background processes or cron jobs that may have started earlier. CPU pressure may develop gradually from multiple contributing factors.

