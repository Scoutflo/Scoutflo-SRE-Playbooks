---
title: Pods Restarting Frequently - Pod
weight: 269
categories:
  - kubernetes
  - pod
---

# PodsRestartingFrequently-pod

## Meaning

Pods are restarting frequently (triggering KubePodCrashLooping alerts) because applications are crashing due to errors, out-of-memory conditions, liveness probe failures, container runtime issues, or resource constraints. Pods show high restart counts in kubectl, pods enter CrashLoopBackOff state, and application logs show fatal errors, panic messages, or exceptions. This affects the workload plane and indicates unstable applications that cannot maintain running state, typically caused by application errors, OOM kills, or liveness probe failures; application crashes and exceptions may appear in application monitoring.

## Impact

Pods enter CrashLoopBackOff state; applications cannot maintain stable state; services experience frequent disruptions; pods consume resources but provide intermittent service; restart counts increase rapidly; application data may be lost on each restart; KubePodCrashLooping alerts fire; deployments cannot achieve desired replica count; user-facing services are unreliable. Pods show high restart counts indefinitely; pods remain in CrashLoopBackOff state; application logs show fatal errors, panic messages, or exceptions; application crashes and exceptions may appear in application monitoring; applications cannot maintain stable state.

## Playbook

1. Retrieve the pod `<pod-name>` in namespace `<namespace>` and inspect pod restart count and container termination reason to identify restart patterns and causes.

2. Retrieve logs from the pod `<pod-name>` in namespace `<namespace>` and filter for error patterns, crash messages, stack traces, or out-of-memory indicators that explain restarts.

3. List events in namespace `<namespace>` and filter for events related to the pod, focusing on OOM kill events, liveness probe failures, or container runtime errors.

4. Retrieve the Deployment `<deployment-name>` in namespace `<namespace>` and review resource requests and limits to verify if memory or CPU constraints may be causing issues.

5. Check the pod `<pod-name>` resource usage metrics to verify if CPU throttling, memory pressure, or other resource constraints are affecting the application.

6. Retrieve the pod `<pod-name>` and inspect container waiting state reason or container termination reason to identify specific restart causes.

## Diagnosis

1. Compare the pod restart timestamps with out-of-memory kill event timestamps, and check whether OOM kills occur within 5 minutes before each restart, indicating memory limit issues.

2. Compare the pod restart timestamps with application error or crash log timestamps, and check whether application errors consistently occur within 5 minutes before restarts.

3. Compare the pod restart timestamps with resource limit or request modification timestamps in the deployment, and check whether resource constraints were changed within 30 minutes before frequent restarts began.

4. Compare the pod restart timestamps with liveness probe failure timestamps, and check whether probe failures occur within the `failureThreshold` period before each restart.

5. Compare the pod restart timestamps with deployment rollout or image update timestamps, and check whether application changes occurred within 1 hour before frequent restarts began, indicating the new version may have bugs.

6. Compare the pod restart timestamps with node resource pressure condition timestamps (MemoryPressure, DiskPressure), and check whether node-level resource issues coincide with pod restarts within 5 minutes.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review application logs for gradual memory leaks or performance degradation patterns, check for intermittent external dependency failures causing crashes, examine resource usage trends for gradual constraint development, verify if application configuration changes introduced instability over time, and check for container runtime or node-level issues that may cause restarts. Frequent restarts may result from cumulative application or infrastructure problems rather than immediate failures.

