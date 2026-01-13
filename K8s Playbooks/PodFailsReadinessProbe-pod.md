---
title: Pod Fails Readiness Probe - Pod
weight: 212
categories:
  - kubernetes
  - pod
---

# PodFailsReadinessProbe-pod

## Meaning

Pods are failing readiness probe checks (triggering KubePodNotReady alerts) because the application is not responding on the probe endpoint, the probe configuration is incorrect, the application startup time exceeds probe delays, or network issues prevent probe execution. Pods show NotReady state in kubectl, pod events show Unhealthy events with "readiness probe failed" messages, and readiness probe checks fail repeatedly. This affects the workload plane and prevents pods from transitioning to Ready state, typically caused by application startup delays, probe configuration issues, or application errors; applications may show errors in application monitoring.

## Impact

Pods remain in NotReady state; services have no endpoints; traffic cannot reach application pods; load balancers exclude pods from rotation; applications appear unavailable even if running; rolling updates fail; deployments cannot achieve desired replica count; KubePodNotReady alerts fire; pod status shows readiness probe failures. Pods show NotReady state indefinitely; pod events show Unhealthy events with "readiness probe failed" messages; applications may show errors in application monitoring; services have no endpoints and applications appear unavailable.

## Playbook

1. Retrieve the pod `<pod-name>` in namespace `<namespace>` and inspect pod ready status and Ready condition to confirm readiness probe failures.

2. List events in namespace `<namespace>` and filter for readiness probe failure events associated with the pod, focusing on events with reasons such as `Unhealthy` and messages containing "readiness probe failed".

3. Retrieve the Deployment `<deployment-name>` in namespace `<namespace>` and review the readiness probe configuration including probe path, port, initial delay, period, and timeout settings to verify probe settings.

4. Retrieve logs from the pod `<pod-name>` in namespace `<namespace>` and filter for application errors, startup issues, or health check endpoint problems that may prevent readiness.

5. From the pod `<pod-name>`, execute the readiness probe command or HTTP request manually using Pod Exec tool to verify the endpoint responds correctly and test probe behavior.

6. Check the pod `<pod-name>` resource usage metrics to verify if resource constraints or throttling are affecting application startup or health check responsiveness.

## Diagnosis

1. Compare the readiness probe failure timestamps with pod startup timestamps, and check whether probe failures occur within the `initialDelaySeconds` window, indicating the application needs more startup time.

2. Compare the readiness probe failure timestamps with application error log timestamps from the pod, and check whether application errors coincide with probe failures within 5 minutes.

3. Compare the readiness probe failure timestamps with readiness probe configuration modification timestamps in the deployment, and check whether probe configuration changes occurred within 30 minutes before failures.

4. Compare the readiness probe failure timestamps with pod resource limit or request modification timestamps, and check whether resource constraints were introduced within 30 minutes before probe failures.

5. Compare the readiness probe failure timestamps with network policy or security policy modification timestamps that may affect probe endpoint access, and check whether policy changes occurred within 10 minutes before probe failures.

6. Compare the readiness probe failure timestamps with deployment rollout or image update timestamps, and check whether application changes occurred within 1 hour before probe failures, indicating the new application version may have different startup or health check behavior.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review application logs for gradual performance degradation, check for intermittent network issues affecting probe execution, examine resource usage trends for gradual constraint development, verify if application dependencies became unavailable over time, and check for DNS or service discovery issues that may affect probe endpoint resolution. Readiness probe failures may result from gradual application or infrastructure degradation rather than immediate configuration changes.

