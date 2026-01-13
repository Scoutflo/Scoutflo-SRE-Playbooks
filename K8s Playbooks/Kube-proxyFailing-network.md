---
title: Kube-proxy Failing - Network
weight: 280
categories:
  - kubernetes
  - network
---

# Kube-proxyFailing-network

## Meaning

Kube-proxy pods are failing (triggering KubeProxyDown or KubeServiceNotReady alerts) because kube-proxy DaemonSet pods cannot start, are crashing in CrashLoopBackOff state, or cannot connect to the API server endpoint. Kube-proxy pods show CrashLoopBackOff or Failed state in kube-system namespace, kube-proxy logs show connection timeout errors or process failures, and service IP routing fails. This affects the network plane and prevents services from forwarding traffic to backend pods, typically caused by kube-proxy process crashes, API server connectivity issues, or resource constraints; applications cannot access services and may show errors.

## Impact

Services cannot forward traffic; service IP routing fails; load balancing does not work; pods cannot reach services by service name or ClusterIP; KubeProxyDown alerts fire when kube-proxy pods are not running; KubeServiceNotReady alerts fire when services cannot route traffic; kube-proxy pods crash or restart; service endpoints are not updated; cluster-internal service communication fails; applications cannot access services; service DNS resolution works but connections fail. Kube-proxy pods remain in CrashLoopBackOff or Failed state indefinitely; kube-proxy logs show connection timeout errors; applications cannot access services and may experience errors or performance degradation; cluster-internal service communication fails.

## Playbook

1. List kube-proxy pods in the kube-system namespace and check their status to identify which pods are failing or crashing.

2. Retrieve logs from the kube-proxy pod `<kube-proxy-pod-name>` in namespace kube-system and filter for errors, crashes, or startup failures that explain why kube-proxy is failing.

3. List events in namespace kube-system and filter for kube-proxy-related events, focusing on events with reasons such as `Failed`, `CrashLoopBackOff`, or messages indicating kube-proxy failures.

4. Check kube-proxy DaemonSet status and verify if pods are being created and scheduled correctly.

5. Verify API server connectivity from kube-proxy pods by checking if kube-proxy can reach the API server endpoint.

6. Check node resource availability where kube-proxy pods are scheduled to verify if resource constraints are causing failures.

## Diagnosis

1. Compare the kube-proxy failure timestamps with kube-proxy pod restart or crash timestamps, and check whether pod crashes occurred within 5 minutes before failures.

2. Compare the kube-proxy failure timestamps with API server unavailability or connectivity failure timestamps, and check whether API server issues occurred within 5 minutes before kube-proxy failures.

3. Compare the kube-proxy failure timestamps with kube-proxy DaemonSet configuration modification timestamps, and check whether configuration changes occurred within 30 minutes before failures.

4. Compare the kube-proxy failure timestamps with node resource pressure condition timestamps, and check whether resource constraints occurred within 5 minutes before kube-proxy failures.

5. Compare the kube-proxy failure timestamps with cluster network plugin restart or failure timestamps, and check whether network infrastructure issues occurred within 1 hour before kube-proxy failures.

6. Compare the kube-proxy failure timestamps with cluster upgrade or kube-proxy image update timestamps, and check whether infrastructure changes occurred within 1 hour before failures.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review kube-proxy logs for gradual performance degradation, check for intermittent API server connectivity issues, examine if kube-proxy configuration drifted over time, verify if node resource constraints developed gradually, and check for network plugin issues that may have accumulated. Kube-proxy failures may result from gradual infrastructure degradation rather than immediate changes.

