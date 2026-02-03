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

1. Describe the pod `<pod-name>` in namespace `<namespace>` to retrieve detailed information including IP address, network configuration, and conditions.

2. Retrieve events for the pod `<pod-name>` in namespace `<namespace>` sorted by timestamp to identify network-related issues and sandbox creation failures.

3. List pods in the `kube-system` namespace and check network plugin pod status (e.g., Calico, Flannel, Cilium) to verify if the network plugin is running and healthy.

4. From another pod, execute ping or curl to the pod `<pod-name>` IP address to test connectivity and verify if the pod IP is reachable.

5. Retrieve logs from network plugin pods in the `kube-system` namespace and filter for networking errors, route configuration issues, or connectivity problems.

6. Check node network interfaces and routes to verify if node networking is correctly configured for pod communication.

## Diagnosis

1. Analyze pod events from Playbook to identify FailedCreatePodSandbox or network configuration errors. If events show sandbox creation failures, the CNI plugin failed to configure networking for the pod.

2. If events indicate CNI failures, check network plugin pod status in kube-system from Playbook data. If CNI pods (Calico, Flannel, Cilium) show CrashLoopBackOff, NotReady, or recent restarts, the network plugin is not functioning correctly.

3. If CNI pods are healthy, verify pod IP assignment and Ready condition from Playbook data. If pod has IP but is not Ready, the issue may be application-level rather than network-level.

4. If pod is Ready with IP assigned, check NetworkPolicy rules from Playbook for policies blocking ingress traffic to the pod. If restrictive policies exist without proper allow rules, traffic is blocked at the policy level.

5. If NetworkPolicy is not blocking, review connectivity test results from Playbook. If ping fails but pod is running, check node routing tables and network interface configuration for route misconfiguration.

6. If routing appears correct, check CNI plugin logs from Playbook for IP allocation errors, IPAM failures, or route programming issues that may indicate underlying network infrastructure problems.

**If no network configuration issue is found**: Review node network interface status, check for MTU mismatches between nodes, verify if cloud provider networking (VPC routes, security groups) is correctly configured, and examine if recent cluster or node updates affected network configuration.

