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

1. Describe the kube-proxy pod `<pod-name>` in namespace `kube-system` to retrieve detailed information including status, conditions, and events.

2. Retrieve events for the kube-proxy pod `<pod-name>` in namespace `kube-system` sorted by timestamp to identify recent issues.

3. Retrieve the kube-proxy DaemonSet in namespace `kube-system` and inspect its status to verify kube-proxy DaemonSet status.

4. Retrieve logs from the kube-proxy pod in namespace `kube-system` and filter for error patterns including 'panic', 'fatal', 'connection refused', 'timeout', 'iptables', 'ipvs' to identify kube-proxy failures.

5. Verify network connectivity between monitoring system and kube-proxy pod endpoints to confirm connectivity issues.

6. Describe the Node `<node-name>` where kube-proxy pods should be running and check node status and conditions to identify node issues.

7. Retrieve the ConfigMap in namespace `kube-system` for kube-proxy configuration and verify kube-proxy configuration for issues.

## Diagnosis

1. Analyze kube-proxy pod events from Playbook to identify failure reasons. If events show CrashLoopBackOff, Failed, or BackOff states, note the specific error messages indicating why kube-proxy is failing.

2. If events indicate pod failures, check kube-proxy logs from Playbook for panic, fatal, or connection errors. If logs show API server connection timeout or refused errors, kube-proxy cannot communicate with the control plane.

3. If API server connectivity issues are present, verify API server endpoint reachability from affected nodes. If API server is unreachable, kube-proxy cannot sync endpoints and iptables/ipvs rules become stale.

4. If API server is reachable, check kube-proxy DaemonSet status from Playbook. If desired count does not match ready count, identify which nodes are missing kube-proxy pods and check node conditions.

5. If DaemonSet scheduling is correct, review node conditions from Playbook for NotReady state, MemoryPressure, DiskPressure, or PIDPressure. If nodes show resource pressure, kube-proxy may be evicted or unable to start.

6. If node resources are available, check kube-proxy ConfigMap from Playbook for configuration issues. If iptables/ipvs mode is misconfigured or clusterCIDR is incorrect, kube-proxy fails to program network rules.

**If no configuration issue is found**: Review iptables/ipvs kernel module availability, check container runtime status on affected nodes, verify network connectivity between kube-proxy and API server, and examine if security contexts or Pod Security Policies prevent kube-proxy from running with required privileges.
