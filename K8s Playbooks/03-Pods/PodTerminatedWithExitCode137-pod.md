---
title: Pod Terminated With Exit Code 137 - Pod
weight: 242
categories:
  - kubernetes
  - pod
---

# PodTerminatedWithExitCode137-pod

## Meaning

Pods are being terminated with exit code 137 (triggering KubePodCrashLooping or KubePodNotReady alerts) because the container was killed by the kernel due to out-of-memory (OOM) conditions. Pods show exit code 137 in container termination status, pod events show OOMKilled events, and node conditions may show MemoryPressure. This affects the workload plane and indicates memory limit violations, typically caused by memory limits being too restrictive or node memory exhaustion; application errors may appear in application monitoring.

## Impact

Pods are terminated unexpectedly; containers are killed by OOM; applications lose in-memory state; pods enter CrashLoopBackOff state; deployments cannot maintain desired replica count; services lose endpoints; KubePodCrashLooping alerts fire; pod status shows exit code 137; restart counts increase; application data may be lost on termination. Pods show exit code 137 in container termination status; pod events show OOMKilled events; application errors may appear in application monitoring; applications lose in-memory state and may show errors.

## Playbook

1. Describe pod <pod-name> in namespace <namespace> to inspect container termination exit code to confirm exit code 137 and container termination reason to verify OOM kill.

2. Retrieve events in namespace <namespace> for pod <pod-name> sorted by timestamp to identify OOM kill events associated with the pod, focusing on events with reasons such as OOMKilled or messages containing "out of memory".

3. Check the node where the pod was scheduled for node-level memory pressure conditions (MemoryPressure) and system OOM kill events by checking node status conditions and system logs (dmesg) using Pod Exec tool or SSH if node access is available.

4. Retrieve the Deployment <deployment-name> in namespace <namespace> and review resource limits, specifically resources.limits.memory, to verify if memory limits are too restrictive.

5. Check the pod <pod-name> resource usage metrics to verify actual memory consumption compared to configured limits and identify if memory usage is approaching or exceeding limits.

6. Retrieve logs from the pod <pod-name> in namespace <namespace> and filter for memory-related errors, allocation failures, or application memory issues that may indicate memory leaks or excessive usage.

## Diagnosis

1. Analyze pod events from Playbook steps 1-2 to confirm the OOMKilled termination reason. Events showing "OOMKilled" in the termination reason field confirm memory exhaustion as the root cause. Exit code 137 indicates SIGKILL (128 + 9).

2. If container termination reason shows "OOMKilled" (from Playbook step 1), there are two possible scenarios:
   - Container memory limit exceeded: The container used more memory than its configured limit (resources.limits.memory)
   - Node-level OOM: The node ran out of memory and the kernel killed the container

3. If pod events show OOMKilled without node MemoryPressure condition (from Playbook step 3), the issue is container-level memory limits being too restrictive. Compare actual memory usage (Playbook step 5) with configured limits (Playbook step 4) to determine appropriate limit increases.

4. If node conditions show MemoryPressure (from Playbook step 3), the issue is node-level memory exhaustion. Check system logs (dmesg) for kernel OOM killer messages and identify which processes consumed excessive memory.

5. If pod logs (Playbook step 6) show memory allocation failures, OutOfMemoryError, or similar errors before termination, the application has a memory leak or insufficient heap configuration. Review application memory settings (e.g., JVM heap size, Node.js max-old-space-size).

6. If events indicate recent deployment changes, correlate OOM kill onset with deployment rollout timestamps to identify if new application versions have higher memory requirements or memory leaks.

7. If memory usage metrics show gradual increase over time before OOMKill, investigate memory leaks in the application code or unbounded caching.

**If no clear root cause is identified from pod events**: Review application-specific memory configurations, check for memory-intensive operations that may cause spikes, verify if memory requests are set appropriately for scheduling, examine if other pods on the same node are consuming excessive memory, and consider implementing memory profiling to identify leak sources.

