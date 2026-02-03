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

1. Describe pod <pod-name> in namespace <namespace> to see restart count, last termination reason (OOMKilled, Error, Completed), exit code, and recent events showing why the pod is restarting.

2. Retrieve the last termination state for pod <pod-name> in namespace <namespace> - if reason is OOMKilled, this is the root cause.

3. Retrieve events for pod <pod-name> in namespace <namespace> sorted by timestamp to see OOMKill events, liveness probe failures, or container runtime errors.

4. Retrieve logs from the previous container instance for pod <pod-name> in namespace <namespace> to see error messages and stack traces from before the crash.

5. Describe Deployment <deployment-name> in namespace <namespace> to check resource requests/limits, liveness probe settings (timeoutSeconds, failureThreshold), and readiness probe configuration.

6. Retrieve resource usage metrics for pod <pod-name> in namespace <namespace> to see if memory or CPU is approaching limits.

7. If OOMKilled, describe node <node-name> and check Conditions section to see if node-level memory pressure is contributing.

## Diagnosis

1. Analyze pod events from Playbook steps 1-3 to identify the primary restart reason. Order diagnosis by most common causes:

2. If termination reason shows "OOMKilled" (from Playbook steps 1-2):
   - Container exceeded memory limits
   - Check memory usage metrics (Playbook step 6) vs limits
   - Increase memory limits or fix memory leaks
   - Exit code 137 confirms OOM kill

3. If termination reason shows "Error" with non-zero exit code (from Playbook step 1):
   - Application crashed with error
   - Check previous container logs (Playbook step 4) for stack traces
   - Common exit codes: 1 (general error), 139 (segfault), 143 (SIGTERM not handled)

4. If events show liveness probe failures before restarts (from Playbook step 3):
   - Application became unresponsive
   - Check probe configuration (Playbook step 5)
   - Verify probe timeouts are appropriate for application
   - Review if resource limits are causing slow responses

5. If events show "BackOff" indicating CrashLoopBackOff:
   - Container is crashing immediately after start
   - Check container command/args configuration
   - Verify required dependencies (ConfigMap, Secret, volumes) exist
   - Review application startup logs

6. If node shows resource pressure (from Playbook step 7):
   - Node-level issues affecting pod stability
   - Consider moving pod to a healthier node
   - Check if eviction is causing restarts

7. If restarts correlate with deployment changes (from Playbook step 5):
   - New application version has bugs
   - Configuration changes broke the application
   - Consider rolling back to previous version

**To reduce restart frequency**: Fix the underlying cause identified in termination reason and logs. For OOMKilled, increase memory or fix leaks. For application errors, fix bugs or configuration. For probe failures, adjust probe timing or fix application responsiveness.

