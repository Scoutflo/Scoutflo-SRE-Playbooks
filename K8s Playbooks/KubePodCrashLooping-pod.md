---
title: Kube Pod Crash Looping
weight: 20
---

# KubePodCrashLooping

## Meaning

Pod is in CrashLoopBackOff state (triggering alerts like KubePodCrashLooping or KubePodNotReady) because the container application is crashing or exiting immediately after startup, causing Kubernetes to repeatedly restart it. Pods show continuous restart counts in kubectl, container exit codes indicate non-zero failures (typically 1, 137, or 143), and application logs show fatal errors, panic messages, or exceptions. This affects the workload plane and indicates application-level failures typically caused by configuration errors, resource constraints, missing dependencies, or application bugs; application crashes and exceptions may appear in application monitoring; missing ConfigMap, Secret, or PersistentVolumeClaim dependencies may block container initialization.

## Impact

KubePodCrashLooping alerts fire; pods cannot serve traffic; services become unavailable or degraded; applications fail to start; pods remain in CrashLoopBackOff state; restart counts increase continuously; container exit codes show non-zero values (typically 1, 137, or 143); application logs show fatal errors, panic messages, or exceptions; readiness probes never succeed; workloads cannot reach desired state. Rolling updates cannot complete; scheduled tasks fail; pod status shows CrashLoopBackOff indefinitely in kubectl; service endpoints are removed; deployments may show replica count mismatches. Application errors increase; application exceptions occur frequently; application performance degrades; missing ConfigMap, Secret, or PersistentVolumeClaim dependencies may cause initialization failures.

## Playbook

1. Retrieve the Pod `<pod-name>` in namespace `<namespace>` and inspect its status and restart count to confirm crash loop and identify restart causes.

2. Retrieve events for the Pod `<pod-name>` in namespace `<namespace>` and filter for error patterns including 'Failed', 'Error', 'CrashLoopBackOff', 'BackOff' to identify pod lifecycle issues.

3. Retrieve logs from the Pod `<pod-name>` in namespace `<namespace>` for container `<container-name>` and filter for error patterns including 'fatal', 'panic', 'exception', 'failed to start', 'connection refused', 'permission denied' to identify application errors.

4. Retrieve the Deployment or StatefulSet `<workload-name>` in namespace `<namespace>` and check pod template parameters including resource requests and limits, readiness and liveness probe configurations, security context settings, volume mounts, and environment variables to verify configuration issues.

5. Retrieve the Node `<node-name>` where pod `<pod-name>` is scheduled and verify node resource availability and conditions to identify resource constraints.

6. Retrieve ConfigMap, Secret, and PersistentVolumeClaim resources referenced by pod `<pod-name>` in namespace `<namespace>` and check for missing dependencies that block container initialization.

## Diagnosis

Compare pod restart timestamps with deployment or StatefulSet change timestamps within 30 minutes and verify whether crashes began shortly after a configuration change, using pod events and deployment rollout history as supporting evidence.

Correlate pod crash timestamps with node condition transition times within 5 minutes and verify whether crashes coincide with node resource pressure (MemoryPressure, DiskPressure, PIDPressure), using node conditions and pod scheduling events as supporting evidence.

Analyze restart frequency over the last 15 minutes to determine if restarts are constant (application crash on startup) or intermittent (resource constraints or dependency failures), using pod restart count and container exit codes as supporting evidence.

Compare container exit codes and log error patterns across multiple restart cycles and verify whether the same error pattern repeats consistently, using pod logs and container status as supporting evidence.

Correlate pod crash timestamps with ConfigMap or Secret update timestamps within 5 minutes and verify whether crashes began after configuration changes, using pod events and resource modification times as supporting evidence.

Compare pod resource requests with node available resources at crash times and verify whether resource constraints prevent successful startup, using node metrics and pod resource specifications as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 1 hour for deployment changes, review application logs for gradual degradation patterns, check for external dependency failures (databases, APIs), examine historical restart patterns, verify container image changes. Pod crashes may result from application bugs, image corruption, or runtime environment issues rather than immediate configuration changes.
