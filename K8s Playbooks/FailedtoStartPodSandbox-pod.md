---
title: Failed to Start Pod Sandbox - Pod
weight: 243
categories:
  - kubernetes
  - pod
---

# FailedtoStartPodSandbox-pod

## Meaning

Pod sandbox creation is failing (triggering KubePodPending alerts) because the container runtime cannot create the pod sandbox, CNI plugins are not functioning, network configuration is incorrect, or resource constraints prevent sandbox creation. Pods show ContainerCreating state, pod events show FailedCreatePodSandbox errors, and container runtime or CNI plugin pods may show failures. This affects the workload plane and prevents pods from transitioning to Running state, typically caused by container runtime issues, CNI plugin failures, or resource constraints; applications cannot start.

## Impact

Pods cannot start; pod sandbox creation fails; pods remain in ContainerCreating state; KubePodPending alerts fire; container runtime errors occur; network setup fails; pods cannot be created; applications cannot deploy; services cannot get new pods. Pods show ContainerCreating state indefinitely; pod events show FailedCreatePodSandbox errors; container runtime or CNI plugin pods may show failures; applications cannot start and may show errors.

## Playbook

1. Retrieve the pod `<pod-name>` in namespace `<namespace>` and inspect container waiting state reason and message fields to identify sandbox creation failures.

2. List events in namespace `<namespace>` and filter for pod-related events, focusing on events with reasons such as `FailedCreatePodSandbox` or messages indicating sandbox creation failures.

3. On the node where the pod is scheduled, check container runtime status (Docker, containerd) using Pod Exec tool or SSH if node access is available to verify if the runtime is functioning.

4. List pods in the kube-system namespace and check CNI plugin pod status (e.g., Calico, Flannel, Cilium) to verify if network plugins are running.

5. Retrieve kubelet logs from the node and filter for sandbox creation errors, container runtime failures, or CNI plugin errors.

6. Check node resource availability and verify if resource constraints are preventing sandbox creation.

## Diagnosis

1. Compare the pod sandbox creation failure timestamps with container runtime restart or failure timestamps on the node, and check whether runtime issues occurred within 5 minutes before sandbox creation failures.

2. Compare the pod sandbox creation failure timestamps with CNI plugin pod restart or failure timestamps, and check whether network plugin issues occurred within 5 minutes before sandbox creation failures.

3. Compare the pod sandbox creation failure timestamps with node resource pressure condition timestamps, and check whether resource constraints occurred within 5 minutes before sandbox creation failures.

4. Compare the pod sandbox creation failure timestamps with cluster network plugin configuration modification timestamps, and check whether network configuration changes occurred within 30 minutes before sandbox creation failures.

5. Compare the pod sandbox creation failure timestamps with kubelet restart or configuration modification timestamps, and check whether kubelet changes occurred within 30 minutes before sandbox creation failures.

6. Compare the pod sandbox creation failure timestamps with cluster upgrade or container runtime update timestamps, and check whether infrastructure changes occurred within 1 hour before sandbox creation failures.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review kubelet logs for gradual sandbox creation issues, check for intermittent container runtime problems, examine if CNI plugin configurations drifted over time, verify if node resource constraints developed gradually, and check for network plugin issues that may have accumulated. Pod sandbox creation failures may result from gradual infrastructure degradation rather than immediate changes.

