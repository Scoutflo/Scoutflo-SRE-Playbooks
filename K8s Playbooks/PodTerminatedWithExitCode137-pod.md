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

1. Retrieve the pod `<pod-name>` in namespace `<namespace>` and inspect container termination exit code to confirm exit code 137 and container termination reason to verify OOM kill.

2. List events in namespace `<namespace>` and filter for OOM kill events associated with the pod, focusing on events with reasons such as `OOMKilled` or messages containing "out of memory".

3. Check the node where the pod was scheduled for node-level memory pressure conditions (MemoryPressure) and system OOM kill events by checking node status conditions and system logs (dmesg) using Pod Exec tool or SSH if node access is available.

4. Retrieve the Deployment `<deployment-name>` in namespace `<namespace>` and review resource limits, specifically `resources.limits.memory`, to verify if memory limits are too restrictive.

5. Check the pod `<pod-name>` resource usage metrics to verify actual memory consumption compared to configured limits and identify if memory usage is approaching or exceeding limits.

6. Retrieve logs from the pod `<pod-name>` in namespace `<namespace>` and filter for memory-related errors, allocation failures, or application memory issues that may indicate memory leaks or excessive usage.

## Diagnosis

1. Compare the pod termination timestamps (exit code 137) with pod memory usage metric spikes, and check whether memory consumption exceeded limits within 5 minutes before termination.

2. Compare the pod termination timestamps with node-level OOM kill event timestamps from system logs (dmesg), and check whether system OOM kills occurred within 5 minutes before pod terminations.

3. Compare the pod termination timestamps with node MemoryPressure condition timestamps, and check whether node-level memory pressure occurred within 5 minutes before pod OOM kills.

4. Compare the pod termination timestamps with memory limit modification timestamps in the deployment, and check whether memory limits were reduced within 30 minutes before OOM kills began.

5. Compare the pod termination timestamps with deployment rollout or image update timestamps, and check whether application changes occurred within 1 hour before OOM kills, indicating the new version may have memory leaks or higher memory requirements.

6. Compare the pod termination timestamps with application error log timestamps indicating memory allocation failures or memory-related errors, and check whether memory issues were logged within 5 minutes before termination.

7. Compare the pod termination timestamps with cluster scaling events or workload increases that may have caused resource competition, and check whether resource pressure increased within 30 minutes before OOM kills.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review application logs for gradual memory leak patterns, check for intermittent memory spikes from specific operations, examine memory usage trends for gradual increase over time, verify if application dependencies started consuming more memory, and check for node-level memory pressure that may have developed gradually. OOM kills may result from cumulative memory pressure rather than immediate limit changes.

