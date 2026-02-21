---
title: Container Memory Near Limit
weight: 23
categories: [kubernetes, container]
---

# ContainerMemoryNearLimit

## Meaning

Container memory usage is approaching its limit (triggering ContainerMemoryNearLimit alerts, typically when usage exceeds 80-90% of limit) because the container is consuming most of its allocated memory and risks being OOMKilled if usage increases further. Container metrics show memory working set near the configured limit, the OOM killer may be triggered soon, and the container is operating in a dangerous zone. This affects the workload plane and indicates imminent risk of container termination; applications may crash unexpectedly; proactive action is needed to prevent service disruption.

## Impact

ContainerMemoryNearLimit alerts fire; container at imminent risk of OOMKill; any memory spike will cause termination; application stability is compromised; garbage collection becomes aggressive; response times may increase; memory allocations may fail; out-of-memory exceptions may occur in application; service degradation is likely; data loss risk if container is killed during transaction; restart loop may begin if workload consistently needs more memory.

## Playbook

1. Retrieve the Pod `<pod-name>` in namespace `<namespace>` and inspect container memory limits and current usage percentage.

2. Calculate memory headroom: (limit - working_set) / limit * 100 to determine how close the container is to OOMKill threshold.

3. Retrieve memory usage trend over the last 6 hours and determine if memory is growing (leak), stable (normal), or spiking (load-driven).

4. Retrieve application logs for container `<container-name>` and filter for memory warnings including 'heap', 'memory', 'GC overhead', 'allocation failed' patterns.

5. Check OOMKilled history for this pod using kubectl describe pod and verify if container has been killed previously.

6. Retrieve node memory metrics to ensure the node has available memory if limit is increased.

7. Evaluate if memory request equals limit (guaranteed QoS) or if request is lower (burstable QoS) which affects eviction priority.

## Diagnosis

Compare current memory usage with historical baseline and verify whether current usage is anomalous or represents new normal operating level, using historical metrics and deployment changes as supporting evidence.

Correlate memory growth with recent deployments or configuration changes within 24 hours and verify whether a code change introduced memory regression, using deployment timestamps and memory trends as supporting evidence.

Analyze whether memory usage is proportional to load (expected) or independent of load (potential leak), using request rate metrics and memory correlation as supporting evidence.

Check if container is caching data that could be offloaded to external cache (Redis, Memcached) to reduce memory pressure, using application architecture and caching patterns as supporting evidence.

Verify if memory limit was recently reduced or if this is a new workload with inappropriate initial sizing, using resource history and workload characteristics as supporting evidence.

If no correlation is found within the specified time windows: increase memory limit as immediate mitigation, schedule memory profiling analysis, review application for memory optimization opportunities, consider horizontal scaling to distribute memory load, implement memory-based HPA for automatic scaling.
