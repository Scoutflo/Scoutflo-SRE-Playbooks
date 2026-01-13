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

1. List all pods and retrieve their IP addresses to identify pods with duplicate IP addresses.

2. Retrieve the pod `<pod-name>` in namespace `<namespace>` with IP conflict and inspect its network configuration and IP assignment.

3. List pods in the kube-system namespace and check CNI plugin pod status (e.g., Calico, Flannel, Cilium) to verify if the network plugin is running and functioning.

4. Retrieve logs from CNI plugin pods in the kube-system namespace and filter for IP allocation errors, conflicts, or CIDR issues.

5. Check cluster pod CIDR configuration and verify if CIDR ranges are correctly configured and do not overlap.

6. List events in namespace `<namespace>` and filter for network-related events, focusing on events with reasons such as `FailedCreatePodSandbox` or messages indicating IP allocation failures.

## Diagnosis

1. Compare the pod IP conflict timestamps with CNI plugin pod restart or failure timestamps, and check whether network plugin failures occurred within 5 minutes before IP conflicts.

2. Compare the pod IP conflict timestamps with pod CIDR configuration modification timestamps, and check whether CIDR range changes occurred within 30 minutes before IP conflicts.

3. Compare the pod IP conflict timestamps with cluster network plugin deployment update timestamps, and check whether network plugin updates occurred within 1 hour before IP conflicts.

4. Compare the pod IP conflict timestamps with node addition or removal timestamps, and check whether cluster scaling events occurred within 30 minutes before IP conflicts, potentially causing CIDR overlap.

5. Compare the pod IP conflict timestamps with CNI plugin configuration modification timestamps, and check whether network plugin settings were changed within 30 minutes before IP conflicts.

6. Compare the pod IP conflict timestamps with IP address pool exhaustion timestamps, and check whether IP pools ran out of available addresses within 30 minutes before IP conflicts.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review CNI plugin logs for gradual IP allocation issues, check for intermittent network plugin failures, examine if IP address pools gradually exhausted over time, verify if CIDR configurations drifted gradually, and check for network plugin resource constraints that may have accumulated. IP conflicts may result from gradual network plugin issues rather than immediate configuration changes.

