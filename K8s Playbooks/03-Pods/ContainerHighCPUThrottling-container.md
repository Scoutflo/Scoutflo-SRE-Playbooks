---
title: Container High CPU Throttling
weight: 20
categories: [kubernetes, container]
---

# ContainerHighCPUThrottling

## Meaning

Container is experiencing high CPU throttling (triggering ContainerHighCPUThrottling or CPUThrottlingHigh alerts) because the container is hitting its CPU limit and being throttled by the Linux CFS scheduler, causing performance degradation. Container metrics show throttled_time increasing, CPU usage consistently near or at the limit, and application response times increasing. This affects the workload plane and indicates the container needs more CPU resources or has inefficient CPU usage patterns; applications experience increased latency; request processing slows down; timeouts may occur.

## Impact

ContainerHighCPUThrottling alerts fire; application response times increase significantly; request processing slows down; timeout errors increase; throughput decreases; latency-sensitive operations fail; health check responses slow; pod may be marked as unhealthy; user-facing latency increases; SLO violations may occur; batch jobs take longer to complete; CPU-bound operations queue up; application threads wait for CPU time.

## Playbook

1. Retrieve the Pod `<pod-name>` in namespace `<namespace>` and inspect container CPU limits and requests to identify the current resource allocation.

2. Retrieve container CPU throttling metrics (container_cpu_cfs_throttled_seconds_total, container_cpu_cfs_throttled_periods_total) for container `<container-name>` to quantify the severity of throttling.

3. Retrieve container CPU usage metrics (container_cpu_usage_seconds_total) and compare against the CPU limit to determine if the container is consistently hitting its limit.

4. Retrieve application metrics or logs for container `<container-name>` and filter for latency or timeout patterns to correlate CPU throttling with application performance degradation.

5. Retrieve the Deployment or StatefulSet `<workload-name>` in namespace `<namespace>` and review CPU resource specifications including requests and limits across all containers.

6. Retrieve the node `<node-name>` where the pod is running and verify node CPU capacity and current utilization to check for node-level resource contention.

7. Check for Vertical Pod Autoscaler (VPA) recommendations if configured, to identify suggested CPU limit adjustments based on historical usage.

## Diagnosis

Compare throttling percentage (throttled_periods / total_periods * 100) with application latency metrics and verify whether throttling above 25% correlates with response time increases, using container metrics and application APM data as supporting evidence.

Correlate CPU throttling patterns with specific times of day or workload patterns and verify whether throttling occurs during peak load periods, using request rate metrics and throttling timestamps as supporting evidence.

Analyze whether CPU requests are set appropriately (requests should reflect typical usage, limits should accommodate bursts) and verify if the request-to-limit ratio is causing over-scheduling, using pod scheduling decisions and node allocation as supporting evidence.

Compare CPU usage patterns across replicas of the same deployment and verify whether throttling affects all pods equally or specific instances, using per-pod metrics and load balancing distribution as supporting evidence.

Check if the application is CPU-bound due to inefficient code, blocking operations, or excessive garbage collection, using application profiling data and GC metrics as supporting evidence.

If no correlation is found within the specified time windows: review application code for CPU-intensive operations, check for runaway threads or infinite loops, verify no cryptocurrency mining or malicious processes, examine JVM or runtime CPU settings, consider whether the workload is fundamentally CPU-bound and needs higher limits.
