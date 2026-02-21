---
title: Container High Memory Usage
weight: 21
categories: [kubernetes, container]
---

# ContainerHighMemoryUsage

## Meaning

Container is experiencing high memory usage (triggering ContainerHighMemoryUsage or ContainerMemoryNearLimit alerts) because the container is consuming memory close to or at its limit, risking OOMKill. Container metrics show memory usage consistently above 80-90% of the limit, memory working set grows over time, and the container may be at risk of being terminated by the OOM killer. This affects the workload plane and indicates potential memory leak, undersized memory limits, or memory-intensive workload; applications may crash unexpectedly; data loss may occur if processes are killed; service availability degrades.

## Impact

ContainerHighMemoryUsage alerts fire; container at risk of OOMKill; application may crash unexpectedly; data in memory may be lost; pod restarts increase; service availability degrades; response times may increase due to garbage collection; memory-intensive operations fail; connection pools may be exhausted; file descriptors may leak; swap usage increases if enabled; node memory pressure may occur affecting other pods.

## Playbook

1. Retrieve the Pod `<pod-name>` in namespace `<namespace>` and inspect container memory limits and requests to identify the current resource allocation.

2. Retrieve container memory metrics (container_memory_working_set_bytes, container_memory_usage_bytes) for container `<container-name>` and compare against the memory limit.

3. Retrieve memory usage trends over the last 24 hours and determine if memory is growing steadily (indicating a leak) or fluctuating with load (normal behavior).

4. Retrieve application metrics or logs for container `<container-name>` and filter for memory-related patterns including 'OutOfMemory', 'heap', 'GC', 'memory pressure' to identify application-level memory issues.

5. Retrieve the Deployment or StatefulSet `<workload-name>` in namespace `<namespace>` and review memory resource specifications including requests and limits.

6. Check for OOMKilled events in pod history using `kubectl describe pod` or events API to verify if container has been killed previously due to memory.

7. If applicable, retrieve JVM heap metrics (jvm_memory_used_bytes, jvm_gc_collection_seconds) or language-specific memory metrics to identify heap vs off-heap memory issues.

## Diagnosis

Compare memory usage growth rate with uptime and verify whether memory increases linearly over time (indicating memory leak) versus stabilizing after warmup, using memory metrics and pod restart timestamps as supporting evidence.

Correlate memory spikes with request rate or specific operations and verify whether memory usage is load-dependent, using request metrics and memory timeline as supporting evidence.

Analyze garbage collection metrics (if applicable) and verify whether GC is running frequently but not reclaiming memory (indicating retained references), using GC metrics and heap usage as supporting evidence.

Compare memory usage across replicas of the same deployment and verify whether all pods show similar patterns or only specific instances leak memory, using per-pod metrics as supporting evidence.

Check if memory usage drops after pod restart but gradually climbs again, confirming memory leak pattern, using historical memory metrics and restart events as supporting evidence.

If no correlation is found within the specified time windows: review application code for object retention, check for caching without eviction policies, verify database connection pools are bounded, examine file handle and socket leaks, consider heap dump analysis for memory leak investigation.
