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

1. Retrieve the pod `<pod-name>` in namespace `<namespace>` and inspect pod restart count and container termination reason to confirm liveness probe failures and restarts.

2. List events in namespace `<namespace>` and filter for liveness probe failure events associated with the pod, focusing on events with reasons such as `Unhealthy` and messages containing "liveness probe failed".

3. Retrieve the Deployment `<deployment-name>` in namespace `<namespace>` and review the liveness probe configuration including probe path, port, initial delay, period, timeout, and failure threshold settings to verify probe settings.

4. Retrieve logs from the pod `<pod-name>` in namespace `<namespace>` and filter for application crashes, hangs, errors, or health check endpoint problems that may cause liveness probe failures.

5. From the pod `<pod-name>`, execute the liveness probe command or HTTP request manually using Pod Exec tool to verify the endpoint responds correctly and test probe behavior.

6. Check the pod `<pod-name>` resource usage metrics and OOM kill events to verify if resource constraints or out-of-memory conditions are causing application failures.

## Diagnosis

1. Compare the liveness probe failure timestamps with container restart timestamps, and check whether probe failures consistently occur within the `failureThreshold` period before each restart.

2. Compare the liveness probe failure timestamps with application error or crash log timestamps from the pod, and check whether application failures coincide with probe failures within 5 minutes.

3. Compare the liveness probe failure timestamps with liveness probe configuration modification timestamps in the deployment, and check whether probe configuration changes occurred within 30 minutes before failures.

4. Compare the liveness probe failure timestamps with pod resource limit modification timestamps, and check whether resource constraints or OOM conditions were introduced within 30 minutes before probe failures and restarts.

5. Compare the liveness probe failure timestamps with network policy or security policy modification timestamps that may affect probe endpoint access, and check whether policy changes occurred within 10 minutes before probe failures.

6. Compare the liveness probe failure timestamps with deployment rollout or image update timestamps, and check whether application changes occurred within 1 hour before probe failures, indicating the new application version may have bugs or different behavior causing crashes.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review application logs for gradual memory leaks or performance degradation, check for intermittent network issues affecting probe execution, examine resource usage trends for gradual constraint development, verify if application dependencies became unavailable causing hangs, and check for external factors like database connection issues that may cause application unresponsiveness. Liveness probe failures may result from gradual application degradation or external dependency issues rather than immediate configuration changes.

