---
title: Kube Container OOM Killed
weight: 25
categories: [kubernetes, pod]
---

# KubeContainerOOMKilled

## Meaning

Container has been terminated by the OOM (Out of Memory) killer (triggering KubeContainerOOMKilled alerts) because the container exceeded its memory limit and Linux OOM killer terminated the process. Container status shows OOMKilled reason, exit code 137 indicates SIGKILL from OOM, and the pod restarts with memory-related termination. This affects the workload plane and indicates the container needs more memory or has a memory leak; data in memory is lost; service experiences disruption; the container will restart and may be killed again if the underlying issue persists.

## Impact

KubeContainerOOMKilled alerts fire; container is terminated immediately; in-memory data is lost; service experiences downtime during restart; in-flight requests fail; connection pools are reset; dependent services experience connection errors; restart backoff may delay recovery; repeated OOMKills lead to CrashLoopBackOff; data corruption may occur if killed during write operations; users experience service unavailability.

## Playbook

1. Retrieve the Pod `<pod-name>` in namespace `<namespace>` and confirm container termination reason is OOMKilled with exit code 137.

2. Retrieve container memory metrics (container_memory_working_set_bytes) leading up to the OOMKill event to understand memory usage pattern.

3. Retrieve container memory limit from pod spec and compare with peak memory usage to determine if limit is insufficient.

4. Retrieve application logs before OOMKill using --previous flag and filter for memory-related patterns including 'heap', 'OutOfMemory', 'allocation failed', 'GC overhead'.

5. Retrieve memory usage trend over the last 24 hours and determine if memory grows continuously (leak) or spikes during specific operations (load-driven).

6. Check if JVM heap size (for Java applications) is configured correctly relative to container memory limit, accounting for off-heap memory needs.

7. Review Vertical Pod Autoscaler (VPA) recommendations if available for suggested memory limit adjustments.

## Diagnosis

Compare memory growth rate with request patterns and verify whether memory usage is proportional to load (needs scaling) or independent of load (memory leak), using request metrics and memory trends as supporting evidence.

Analyze memory usage pattern before OOMKill and verify whether it was gradual increase (leak) or sudden spike (specific operation), using high-resolution memory metrics as supporting evidence.

Correlate OOMKill timestamps with specific application operations (batch jobs, large queries, file processing) and verify whether specific operations trigger memory spikes, using application logs and operation timestamps as supporting evidence.

Check if the application uses off-heap memory (native memory, memory-mapped files, NIO buffers) that is not tracked in heap metrics but counts against container limit, using native memory tracking and process RSS as supporting evidence.

Verify if memory limit is significantly lower than request (unusual configuration) or if request equals limit (guaranteed QoS appropriate for memory-sensitive workloads), using pod QoS class and resource specs as supporting evidence.

If no correlation is found within the specified time windows: increase memory limit as immediate mitigation, enable heap dump on OOM for analysis, profile application memory usage, review object retention and caching policies, consider splitting memory-intensive operations into separate pods.
