---
title: Ingress Controller Pods CrashLooping - Ingress
weight: 256
categories:
  - kubernetes
  - ingress
---

# IngressControllerPodsCrashLooping-ingress

## Meaning

Ingress controller pods are repeatedly crashing and restarting (triggering KubePodCrashLooping alerts) because configuration errors prevent startup, invalid ingress resources cause controller failures, resource constraints cause crashes, or the controller cannot access required resources. Ingress controller pods show CrashLoopBackOff state in kubectl, ingress controller logs show startup failures or configuration errors, and pod restart counts increase continuously. This affects the network plane and prevents traffic routing through ingress resources, typically caused by configuration errors, invalid ingress resources, or resource constraints; applications become unavailable to users and may show errors.

## Impact

Ingress controller is unavailable; all ingress resources stop routing traffic; external traffic cannot reach applications; ingress endpoints return errors; applications become unreachable from outside the cluster; KubePodCrashLooping alerts fire; ingress controller logs show startup failures; cluster ingress functionality is completely broken. Ingress controller pods remain in CrashLoopBackOff state indefinitely; ingress controller logs show startup failures; applications become unavailable to users and may experience errors or performance degradation; cluster ingress functionality is completely broken.

## Playbook

1. Retrieve the ingress controller pod `<controller-pod-name>` in namespace `<namespace>` and inspect pod restart count and container termination reason to confirm crash loop and identify restart causes.

2. Retrieve logs from the ingress controller pod `<controller-pod-name>` in namespace `<namespace>` and filter for configuration errors, startup failures, or crash messages that explain why the controller cannot start.

3. List events in namespace `<namespace>` and filter for ingress controller-related events, focusing on events with reasons such as `Failed`, `CrashLoopBackOff`, or messages indicating configuration or startup errors.

4. Retrieve the ingress controller Deployment or DaemonSet in namespace `<namespace>` and review configuration, environment variables, and resource limits to verify if configuration issues are causing crashes.

5. List all Ingress resources in the cluster and check for invalid or misconfigured ingress resources that may be causing the controller to crash.

6. Check the ingress controller pod resource usage metrics to verify if resource constraints or OOM conditions are causing crashes.

## Diagnosis

1. Compare the ingress controller pod crash timestamps with ingress controller configuration modification timestamps, and check whether configuration changes occurred within 30 minutes before crashes began.

2. Compare the ingress controller pod crash timestamps with invalid Ingress resource creation or modification timestamps, and check whether problematic ingress resources were added within 30 minutes before controller crashes.

3. Compare the ingress controller pod crash timestamps with ingress controller resource limit modification timestamps, and check whether resource constraints were introduced within 30 minutes before crashes.

4. Compare the ingress controller pod crash timestamps with ingress controller image update or deployment rollout timestamps, and check whether controller updates occurred within 1 hour before crashes, indicating the new version may have bugs or different requirements.

5. Compare the ingress controller pod crash timestamps with required Secret or ConfigMap unavailability timestamps, and check whether dependencies became unavailable within 5 minutes before controller crashes.

6. Compare the ingress controller pod crash timestamps with node resource pressure or network policy modification timestamps, and check whether infrastructure changes occurred within 1 hour before controller crashes.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review ingress controller logs for gradual performance degradation, check for intermittent configuration validation failures, examine if ingress resources accumulated invalid configurations over time, verify if resource constraints developed gradually, and check for external dependency issues that may have caused controller failures. Ingress controller crashes may result from cumulative configuration or infrastructure issues rather than immediate changes.

