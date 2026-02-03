---
title: Pod Fails Liveness Probe - Pod
weight: 253
categories:
  - kubernetes
  - pod
---

# PodFailsLivenessProbe-pod

## Meaning

Pods are failing liveness probe checks (triggering alerts like KubePodCrashLooping or KubePodNotReady) because the application is not responding on the liveness endpoint, the application has crashed or hung, the probe configuration is incorrect, or network issues prevent probe execution. Pods show CrashLoopBackOff state in kubectl, pod events show Unhealthy errors with "liveness probe failed" messages, and application logs show crashes, hangs, or health check endpoint failures. Kubelet restarts the container when liveness probes fail repeatedly. This affects the workload plane and indicates application health issues preventing pods from maintaining stable state, typically caused by application crashes, misconfigured probes, or network issues; application errors may appear in application monitoring.

## Impact

KubePodCrashLooping alerts fire; containers are repeatedly restarted by kubelet; pods enter CrashLoopBackOff state; applications cannot maintain stable state; pods consume resources but provide no service; restart counts increase rapidly; application data may be lost on restarts; pod status shows liveness probe failures and restarts. Pods remain in CrashLoopBackOff state indefinitely; pod events show Unhealthy errors continuously; applications cannot maintain stable state and may experience errors or performance degradation.

## Playbook

1. Describe pod <pod-name> in namespace <namespace> to see restart count, last termination reason, and Events showing "Liveness probe failed" with the specific failure message (HTTP status, connection refused, timeout).

2. Retrieve events for pod <pod-name> in namespace <namespace> filtered by reason Unhealthy to see liveness probe failure timestamps and messages.

3. Retrieve the liveness probe configuration for pod <pod-name> in namespace <namespace> to see path, port, timeoutSeconds, periodSeconds, failureThreshold.

4. Execute a request to the liveness probe endpoint from inside pod <pod-name> to verify the endpoint is responding.

5. Retrieve logs from pod <pod-name> in namespace <namespace> including previous container instance to see what happened before the restart.

6. Check the last termination reason for pod <pod-name> in namespace <namespace> - if OOMKilled, the application is running out of memory.

7. Describe Deployment <deployment-name> in namespace <namespace> to review probe configuration and check if initialDelaySeconds is sufficient for application startup.

8. Retrieve resource usage metrics for pod <pod-name> in namespace <namespace> to see if CPU/memory is at limits which may cause the application to become unresponsive.

## Diagnosis

1. Analyze pod events from Playbook steps 1-2 to identify liveness probe failures. Events showing "Unhealthy" with "Liveness probe failed" include the specific failure reason. Unlike readiness probes, liveness probe failures trigger container restarts.

2. If last termination reason shows "OOMKilled" (from Playbook step 6), the application ran out of memory before the liveness probe failed. Address memory issues first - liveness probe failure is a symptom, not the cause.

3. If events show "connection refused" or "timeout" for probes:
   - Application crashed or hung before probe execution
   - Check previous container logs (Playbook step 5) for crash reasons
   - Verify application handles SIGTERM gracefully and recovers

4. If events show HTTP error codes, the application is responding but unhealthy:
   - Check application logs for errors at probe failure timestamps
   - Investigate application-level health check logic
   - Verify dependencies (database, cache, APIs) are healthy

5. If resource usage is at limits (from Playbook step 8), the application may be too slow to respond to probes:
   - CPU throttling causes slow response times - increase CPU limits
   - Memory pressure causes GC pauses - increase memory limits
   - Consider increasing probe timeoutSeconds as a temporary fix

6. If probe configuration has aggressive settings (from Playbook step 3), adjust:
   - timeoutSeconds too short for application response time
   - periodSeconds too frequent causing probe overhead
   - failureThreshold too low causing restarts on transient issues
   - initialDelaySeconds too short for application startup

7. If endpoint responds when tested manually (from Playbook step 4) but probe fails during normal operation, the application becomes unresponsive under load. Profile application for performance issues.

**To resolve liveness probe failures**: Fix the underlying application issue causing unresponsiveness, adjust probe timing to be more tolerant, increase resource limits if constrained, and ensure the liveness endpoint performs minimal work (avoid database queries in liveness checks).

