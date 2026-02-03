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

1. List all nodes and inspect their status to identify nodes with high CPU utilization.

2. Retrieve events across all namespaces sorted by timestamp and filter for CPU-related resource pressure events.

3. Retrieve CPU usage metrics for all nodes and identify nodes consistently running at or near high utilization thresholds.

4. Retrieve CPU usage metrics for control plane pods in namespace `kube-system` (API server, controller-manager, scheduler, etcd) and identify hot spots.

5. List pods across all namespaces with CPU usage metrics and identify specific workloads consuming unusually high CPU.

6. Retrieve logs from API server pods in namespace `kube-system` and filter for elevated request rates or throttling events that may correlate with observed CPU spikes.

## Diagnosis

Begin by analyzing the node status, events, and CPU metrics collected in the Playbook section. Node conditions, pod CPU consumption rankings, and control plane health provide the primary diagnostic signals.

**If events show CPU pressure or EvictionThresholdMet on specific nodes:**
- Those nodes are under critical CPU pressure. Identify top CPU-consuming pods on affected nodes. Consider evicting or rescheduling non-critical workloads. Add node capacity if pressure is cluster-wide.

**If control plane pods (API server, controller-manager, scheduler) show high CPU:**
- Control plane is overloaded. Check API server request rates in logs for throttling messages. Review if recent changes increased API call frequency (new controllers, operators, or CI/CD pipelines).

**If specific workload pods dominate CPU consumption:**
- Application-level issue. Check if those pods have CPU limits set. Review application logs for processing loops or inefficient code. Consider horizontal scaling to distribute load.

**If CPU spikes align with scheduled CronJobs:**
- Batch jobs are consuming CPU during execution windows. Review CronJob schedules for overlapping execution times. Consider staggering job schedules or adding dedicated node pools for batch workloads.

**If CPU usage increased after a Deployment rollout:**
- New application version may have performance regression. Compare CPU usage before and after the rollout using metrics timestamps. Consider rolling back if regression is significant.

**If node CPU is high but pod CPU requests are low:**
- System processes or DaemonSets may be consuming CPU. Check kubelet, container runtime, and logging agent CPU usage. Review DaemonSet resource consumption on affected nodes.

**If events are inconclusive, correlate timestamps:**
1. Check if CPU spikes began after HPA scaling events that increased replica counts.
2. Check if CPU increases align with node removals that concentrated workloads.
3. Check if cluster upgrades introduced performance changes.

**If no clear cause is identified:** Enable CPU profiling on high-consuming pods if the application supports it. Review CPU requests versus actual usage to identify pods that need higher limits or optimization.

