---
title: CrashLoopBackOff - Pod
weight: 201
categories:
  - kubernetes
  - pod
---

# CrashLoopBackOff-pod

## Meaning

A pod container repeatedly starts and exits with errors shortly after launch, causing Kubernetes to back off and restart it in a CrashLoopBackOff state (triggering KubePodCrashLooping alerts) instead of reaching a stable Running state. This indicates application configuration errors, resource constraints, dependency failures, or container image issues preventing successful pod startup.

## Impact

Application pods fail to start; services become unavailable; deployments cannot achieve desired replica count; applications experience downtime; dependent services may fail; KubePodCrashLooping alerts fire; pods remain in CrashLoopBackOff state; containers exit repeatedly; application errors prevent pod stability; replica counts mismatch desired state.

## Playbook

1. Describe pod `<pod-name>` in namespace `<namespace>` to see pod status, restart count, termination reason (OOMKilled, Error, etc.), and recent events - this immediately shows why the pod is crashing.

2. Retrieve events in namespace `<namespace>` for pod `<pod-name>` sorted by timestamp to see the sequence of failures with timestamps.

3. Retrieve pod `<pod-name>` in namespace `<namespace>` and check container termination reason from container status - if OOMKilled, the issue is memory limits.

4. Retrieve logs from pod `<pod-name>` in namespace `<namespace>` from the previous (crashed) container to see what happened before the crash.

5. Describe deployment `<deployment-name>` in namespace `<namespace>` to check container image, resource limits, environment variables, and liveness/readiness probe configuration.

6. Retrieve rollout history for deployment `<deployment-name>` in namespace `<namespace>` to check if the issue started after a recent deployment.

## Diagnosis

1. Analyze pod events from Playbook steps 1-2 to identify the primary failure reason. Events showing "BackOff" with "CrashLoopBackOff" indicate container crashes. Events showing "Back-off restarting failed container" confirm the crash loop pattern.

2. If termination reason shows "OOMKilled" (from Playbook step 3), the issue is memory exhaustion. The container exceeded its memory limit and was killed by the kernel. Increase memory limits or investigate memory leaks in the application.

3. If termination reason shows "Error" with a non-zero exit code, analyze container logs from the previous crashed instance (Playbook step 4) to identify application-level errors causing the crash. Common causes include:
   - Exit code 1: Application error or uncaught exception
   - Exit code 137: SIGKILL (OOMKilled or manual kill)
   - Exit code 139: SIGSEGV (segmentation fault)
   - Exit code 143: SIGTERM (graceful termination failed)

4. If pod events indicate "ImagePullBackOff" or "ErrImagePull", the container image cannot be pulled. Verify image name, tag, registry accessibility, and imagePullSecrets configuration.

5. If pod events indicate "CreateContainerConfigError", check for missing ConfigMaps, Secrets, or environment variable references in the pod specification.

6. If events indicate recent deployment changes (from Playbook step 6), correlate crash onset with the deployment rollout timestamp to identify if code or configuration changes are the root cause.

7. If events and logs are inconclusive, compare crash patterns with resource usage metrics to identify gradual resource exhaustion or dependency failures.

**If no clear root cause is identified from pod events**: Review application logs for stack traces or error patterns, check if liveness probes are misconfigured (too aggressive timeouts), verify external dependencies (databases, APIs) are reachable, examine if startup time exceeds initialDelaySeconds, and check for configuration issues in environment variables or mounted volumes.
