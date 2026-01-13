---
title: KubeProxy Down
weight: 20
---

# KubeProxyDown

## Meaning

Kubernetes Proxy (kube-proxy) instances are unreachable or non-responsive (triggering KubeProxyDown alerts) because all kube-proxy DaemonSet pods have failed, lost network connectivity, or cannot be reached by the monitoring system. Kube-proxy pods show CrashLoopBackOff or Failed state in kubectl, kube-proxy logs show fatal errors, panic messages, or connection timeout errors, and service endpoints fail to route traffic. This affects the network plane and prevents service networking, load balancing, and network rule management on affected nodes, typically caused by pod failures, node networking issues, iptables/ipvs problems, or container runtime issues; applications cannot access services and may show errors.

## Impact

KubeProxyDown alerts fire; network communication to pods fails; service endpoints may not work; load balancing fails; network rules are not maintained; pods cannot communicate via services; cluster networking is degraded; cross-pod communication may fail; service discovery is affected; service networking and load balancing operations fail. Kube-proxy pods remain in CrashLoopBackOff or Failed state; service endpoints return connection refused or timeout errors; applications cannot access services and may experience errors or performance degradation.

## Playbook

1. Retrieve the DaemonSet `<daemonset-name>` in namespace `kube-system` with label `k8s-app=kube-proxy` and inspect its status to verify kube-proxy DaemonSet status.

2. Retrieve the Pod `<pod-name>` in namespace `kube-system` with label `k8s-app=kube-proxy` and check pod status to identify pods in failed or error states.

3. Retrieve logs from the Pod `<pod-name>` in namespace `kube-system` and filter for error patterns including 'panic', 'fatal', 'connection refused', 'timeout', 'iptables', 'ipvs' to identify kube-proxy failures.

4. Retrieve events for the Pod `<pod-name>` in namespace `kube-system` and filter for error patterns including 'Failed', 'Error', 'CrashLoopBackOff' to identify pod lifecycle issues.

5. Verify network connectivity between monitoring system and kube-proxy pod endpoints to confirm connectivity issues.

6. Retrieve the Node `<node-name>` where kube-proxy pods should be running and check node status and conditions to identify node issues.

7. Retrieve the ConfigMap `<configmap-name>` in namespace `kube-system` for kube-proxy configuration and verify kube-proxy configuration ConfigMap for configuration issues.

## Diagnosis

Compare kube-proxy unavailability timestamps with kube-proxy pod restart or failure timestamps within 5 minutes and verify whether unavailability coincides with pod failures, using pod events and kube-proxy status as supporting evidence.

Correlate kube-proxy failures with node condition transitions within 5 minutes and verify whether kube-proxy failures align with node NotReady conditions or resource pressure, using node conditions and kube-proxy pod status as supporting evidence.

Compare kube-proxy log error timestamps with configuration change times within 10 minutes and verify whether kube-proxy failures began after configuration updates, using kube-proxy logs and ConfigMap modification times as supporting evidence.

Analyze kube-proxy error patterns over the last 15 minutes to determine if failures are sudden (crash) or gradual (resource exhaustion), using kube-proxy logs and pod resource usage metrics as supporting evidence.

Correlate kube-proxy unavailability with network policy or firewall rule change timestamps within 10 minutes and verify whether connectivity issues began after network configuration changes, using network policy events and kube-proxy connection logs as supporting evidence.

Compare kube-proxy pod resource usage metrics with resource limits at failure times and verify whether resource constraints caused kube-proxy failures, using pod metrics and resource specifications as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 1 hour for infrastructure changes, review kube-proxy configuration, check for iptables or ipvs issues, verify node networking configuration, examine historical kube-proxy stability patterns. Kube-proxy failures may result from node networking issues, iptables/ipvs problems, or container runtime issues rather than immediate configuration changes.
