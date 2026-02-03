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

1. Describe the kube-proxy pod `<kube-proxy-pod-name>` in namespace `kube-system` to retrieve detailed information including status, conditions, and failure reasons.

2. Retrieve events for the kube-proxy pod `<kube-proxy-pod-name>` in namespace `kube-system` sorted by timestamp to identify recent failures and issues.

3. List kube-proxy pods in the `kube-system` namespace and check their status to identify which pods are failing or crashing.

4. Retrieve logs from the kube-proxy pod in namespace `kube-system` and filter for errors, crashes, or startup failures that explain why kube-proxy is failing.

5. Describe the kube-proxy DaemonSet in namespace `kube-system` to verify if pods are being created and scheduled correctly.

6. Verify API server connectivity from kube-proxy pods by checking if kube-proxy can reach the API server endpoint.

7. Check node resource availability where kube-proxy pods are scheduled to verify if resource constraints are causing failures.

## Diagnosis

1. Analyze kube-proxy pod events from Playbook to identify failure reasons and error patterns. If events show CrashLoopBackOff, BackOff, or FailedScheduling, note the specific failure reason from event messages.

2. If events indicate pod crashes, check kube-proxy logs from Playbook for error patterns (panic, fatal, connection refused, timeout). If logs show API server connection errors, kube-proxy cannot sync service/endpoint information.

3. If API server connectivity fails, verify API server availability and kube-proxy service account permissions. If kube-proxy cannot authenticate or API server is unreachable, service routing rules cannot be updated.

4. If API server is accessible, check kube-proxy DaemonSet status from Playbook. If pods are not scheduled on all nodes, verify node selectors, tolerations, and resource availability on affected nodes.

5. If DaemonSet is correctly configured, review node resource conditions from Playbook. If nodes show MemoryPressure, DiskPressure, or PIDPressure, resource constraints may prevent kube-proxy from functioning correctly.

6. If resources are available, check kube-proxy configuration (ConfigMap) from Playbook for iptables/ipvs mode settings and verify network interface configuration matches cluster networking requirements.

**If no configuration issue is found**: Review iptables/ipvs rules on affected nodes for corruption, check if kernel modules required by kube-proxy are loaded, verify container runtime is functioning correctly, and examine if recent cluster upgrades introduced compatibility issues with kube-proxy version.

