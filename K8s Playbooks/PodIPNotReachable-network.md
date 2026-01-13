---
title: Pod IP Not Reachable - Network
weight: 224
categories:
  - kubernetes
  - network
---

# PodIPNotReachable-network

## Meaning

Pod IP addresses are not reachable (triggering KubeNetworkPluginError or KubePodNotReady alerts) because the network plugin (CNI) pods are not functioning in kube-system namespace, pod networking is misconfigured, routes are not properly configured on nodes, or nodes cannot communicate due to network infrastructure issues. Pods have IP addresses assigned but connectivity tests fail, CNI plugin pods show failures in kube-system namespace, and pod events show FailedCreatePodSandbox or network configuration errors. This affects the network plane and prevents pod-to-pod communication, typically caused by CNI plugin failures or network misconfiguration; applications cannot communicate across pods.

## Impact

Pods cannot communicate with each other; pod IP addresses are unreachable; network connectivity between pods fails; service endpoints may be unreachable; KubeNetworkPluginError alerts fire when network plugin fails to configure pod networking; KubePodNotReady alerts fire when pods cannot establish network connectivity; cluster networking is broken; pod-to-pod communication is blocked; applications cannot communicate across pods; service DNS resolves but connections fail. Pods have IP addresses assigned but connectivity tests fail indefinitely; CNI plugin pods show failures; applications cannot communicate across pods and may show errors; service endpoints may be unreachable.

## Playbook

1. Retrieve the pod `<pod-name>` in namespace `<namespace>` and inspect its IP address and network configuration to verify pod networking setup.

2. List pods in the kube-system namespace and check network plugin pod status (e.g., Calico, Flannel, Cilium) to verify if the network plugin is running and healthy.

3. From another pod, execute `ping` or `curl` to the pod `<pod-name>` IP address using Pod Exec tool to test connectivity and verify if the pod IP is reachable.

4. Retrieve logs from network plugin pods in the kube-system namespace and filter for networking errors, route configuration issues, or connectivity problems.

5. Check node network interfaces and routes to verify if node networking is correctly configured for pod communication.

6. List events in namespace `<namespace>` and filter for network-related events, focusing on events with reasons such as `FailedCreatePodSandbox` or messages indicating network configuration failures.

## Diagnosis

1. Compare the pod IP unreachable timestamps with network plugin pod restart or failure timestamps, and check whether network plugin failures occurred within 5 minutes before pod IP became unreachable.

2. Compare the pod IP unreachable timestamps with pod network configuration modification timestamps, and check whether pod networking changes occurred within 30 minutes before IP unreachability.

3. Compare the pod IP unreachable timestamps with cluster network plugin deployment update timestamps, and check whether network plugin updates occurred within 1 hour before pod IP unreachability.

4. Compare the pod IP unreachable timestamps with node network interface or route modification timestamps, and check whether node networking changes occurred within 10 minutes before pod IP became unreachable.

5. Compare the pod IP unreachable timestamps with NetworkPolicy creation or modification timestamps, and check whether network policies were added or modified within 10 minutes before pod IP unreachability.

6. Compare the pod IP unreachable timestamps with cluster network plugin configuration modification timestamps, and check whether network plugin settings were changed within 30 minutes before pod IP unreachability.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review network plugin logs for gradual performance degradation, check for intermittent network routing issues, examine if network configurations drifted over time, verify if node networking gradually degraded, and check for network plugin resource constraints that may have accumulated. Pod IP unreachability may result from gradual network infrastructure degradation rather than immediate changes.

