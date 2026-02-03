---
title: Pod IP Conflict - Network
weight: 251
categories:
  - kubernetes
  - network
---

# PodIPConflict-network

## Meaning

Multiple pods are assigned the same IP address (triggering KubeNetworkPluginError or KubePodNotReady alerts) because the CNI plugin (Calico, Flannel, Cilium) is misconfigured, pod CIDR ranges overlap between nodes, the network plugin pods are experiencing issues in kube-system namespace, or IP address allocation from the IP pool is failing. Pods show duplicate IP addresses, CNI plugin pods show IP allocation errors in kube-system namespace, and pod events show FailedCreatePodSandbox or IP allocation failures. This affects the network plane and causes network connectivity problems and routing failures, typically caused by CNI plugin misconfiguration or IP pool exhaustion; applications cannot communicate correctly.

## Impact

Pods have duplicate IP addresses; network routing fails; pods cannot communicate correctly; IP conflicts cause connectivity issues; CNI plugin allocation errors occur in pod events; KubeNetworkPluginError alerts fire when CNI plugin fails to allocate unique IPs; KubePodNotReady alerts fire when pods cannot establish network connectivity; pod networking is broken; service endpoints may point to wrong pods; cluster networking is unstable; pod-to-pod communication fails. Pods show duplicate IP addresses indefinitely; CNI plugin pods show IP allocation errors; applications cannot communicate correctly and may show errors; network routing fails and pod-to-pod communication fails.

## Playbook

1. Describe the pod `<pod-name>` in namespace `<namespace>` with IP conflict to retrieve detailed information including network configuration and IP assignment.

2. Retrieve events for the pod `<pod-name>` in namespace `<namespace>` sorted by timestamp to identify IP allocation failures and network-related issues.

3. List all pods across all namespaces and retrieve their IP addresses to identify pods with duplicate IP addresses.

4. List pods in the `kube-system` namespace and check CNI plugin pod status (e.g., Calico, Flannel, Cilium) to verify if the network plugin is running and functioning.

5. Retrieve logs from CNI plugin pods in the `kube-system` namespace and filter for IP allocation errors, conflicts, or CIDR issues.

6. Check cluster pod CIDR configuration to verify if CIDR ranges are correctly configured and do not overlap.

## Diagnosis

1. Analyze pod events from Playbook to identify FailedCreatePodSandbox or IP allocation failure errors. If events show IP allocation conflicts or IPAM errors, note the specific error message indicating the conflict source.

2. If events indicate IP conflicts, check the list of all pod IPs from Playbook to identify pods with duplicate IP addresses. If multiple pods share the same IP, identify which pods are affected and their respective nodes.

3. If duplicate IPs are confirmed, check CNI plugin pod status in kube-system from Playbook. If CNI pods show failures, restarts, or NotReady state, the network plugin IPAM is not functioning correctly.

4. If CNI pods are healthy, review CNI plugin logs from Playbook for IPAM errors, IP pool exhaustion, or CIDR overlap warnings. If logs show IP pool exhaustion, the allocated CIDR range has no available addresses.

5. If IPAM is functioning, check cluster pod CIDR configuration from Playbook. If CIDR ranges overlap between nodes or conflict with node CIDRs, IP allocation produces duplicates.

6. If CIDR configuration is correct, verify recent node additions from Playbook events. If new nodes were added without proper CIDR allocation, node CIDR ranges may overlap with existing nodes.

**If no IPAM configuration issue is found**: Review CNI plugin version compatibility, check if manual IP assignments conflict with IPAM allocations, verify if multiple CNI plugins are installed causing conflicts, and examine if CNI plugin database or state store is corrupted.

