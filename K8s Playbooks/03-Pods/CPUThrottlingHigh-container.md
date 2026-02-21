---
title: CPU Throttling High
weight: 22
categories: [kubernetes, container]
---

# CPUThrottlingHigh

## Meaning

Container is experiencing significant CPU throttling (triggering CPUThrottlingHigh alerts, typically when throttling exceeds 25% of periods) because the container's CPU usage is being limited by the CFS bandwidth controller when it exceeds its CPU limit. Container metrics show high throttled_periods ratio, application latency increases during throttling, and performance becomes inconsistent. This affects the workload plane and indicates insufficient CPU limits for the workload's requirements; latency-sensitive applications suffer performance degradation; batch processing slows down; user experience degrades.

## Impact

CPUThrottlingHigh alerts fire; application latency increases unpredictably; request processing becomes inconsistent; P99 latency spikes; timeout errors increase; throughput decreases below expected levels; health checks may intermittently fail; user-facing operations slow down; SLO violations occur; real-time processing delays; microservice call chains experience cascading delays; worker threads starve for CPU time.

## Playbook

1. Retrieve the Pod `<pod-name>` in namespace `<namespace>` and inspect container CPU limits and requests to identify current resource allocation and the limit-to-request ratio.

2. Calculate throttling percentage using metrics: (container_cpu_cfs_throttled_periods_total / container_cpu_cfs_periods_total * 100) to quantify severity.

3. Retrieve CPU usage patterns over the last hour and identify if throttling is constant or occurs during specific peak periods.

4. Retrieve application latency metrics (p50, p95, p99) and correlate with throttling timestamps to confirm performance impact.

5. Retrieve the Deployment or StatefulSet resource specifications and evaluate if CPU limits are set appropriately for the workload type.

6. Check if the workload is using burstable QoS class (requests < limits) and determine if guaranteed QoS would be more appropriate.

7. Review Vertical Pod Autoscaler (VPA) recommendations if available for data-driven resource adjustment suggestions.

## Diagnosis

Compare CPU throttling with request rate and verify whether throttling only occurs during peak load periods, suggesting the need for higher limits during bursts, using request metrics and throttling correlation as supporting evidence.

Analyze CPU usage against requests versus limits and verify whether requests are set too high (over-provisioning) or limits too low (under-provisioning), using actual usage metrics as supporting evidence.

Correlate throttling across replicas and verify whether load balancing is uneven causing some pods to throttle while others are underutilized, using per-pod CPU metrics and request distribution as supporting evidence.

Check for CPU-intensive initialization or periodic tasks that spike CPU usage and cause temporary throttling, using CPU usage timeline and job schedules as supporting evidence.

Evaluate if the application is single-threaded and cannot effectively use multiple CPU cores, causing throttling on limit while not fully utilizing available request, using thread metrics and CPU distribution as supporting evidence.

If no correlation is found within the specified time windows: consider removing CPU limits entirely (use requests only for scheduling), profile the application for CPU optimization opportunities, evaluate horizontal scaling instead of vertical, review if the workload is appropriate for containerized deployment, check for noisy neighbor effects on the node.
