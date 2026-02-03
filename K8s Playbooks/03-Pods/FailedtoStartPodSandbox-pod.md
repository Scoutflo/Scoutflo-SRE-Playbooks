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

1. Describe pod <pod-name> in namespace <namespace> to inspect container waiting state reason and message fields to identify sandbox creation failures.

2. Retrieve events in namespace <namespace> for pod <pod-name> sorted by timestamp to identify pod-related events, focusing on events with reasons such as FailedCreatePodSandbox or messages indicating sandbox creation failures.

3. On the node where the pod is scheduled, check container runtime status (Docker, containerd) using Pod Exec tool or SSH if node access is available to verify if the runtime is functioning.

4. List pods in the kube-system namespace and check CNI plugin pod status (e.g., Calico, Flannel, Cilium) to verify if network plugins are running.

5. Retrieve kubelet logs from the node and filter for sandbox creation errors, container runtime failures, or CNI plugin errors.

6. Check node resource availability and verify if resource constraints are preventing sandbox creation.

## Diagnosis

1. Analyze pod events from Playbook steps 1-2 to identify the sandbox creation failure reason. Events showing "FailedCreatePodSandbox" include detailed error messages indicating the specific cause.

2. If events show CNI-related errors (e.g., "network plugin is not ready", "failed to set up pod network"), check CNI plugin status (Playbook step 4):
   - Verify CNI plugin pods (Calico, Flannel, Cilium, etc.) are running in kube-system namespace
   - Check CNI plugin pod logs for errors
   - Verify CNI configuration files exist in /etc/cni/net.d/ on the node
   - Check if CNI binaries exist in /opt/cni/bin/

3. If events show container runtime errors (from Playbook step 3), the runtime cannot create the pod sandbox:
   - Verify containerd or Docker service is running
   - Check runtime logs for specific errors
   - Verify runtime socket is accessible (/run/containerd/containerd.sock)

4. If kubelet logs show sandbox errors (from Playbook step 5), common causes include:
   - Runtime not responding to sandbox creation requests
   - Network namespace creation failures
   - IP address allocation failures (IPAM exhausted)
   - Cgroup creation failures

5. If node shows resource pressure (from Playbook step 6), sandbox creation may fail due to:
   - Insufficient disk space for container layers
   - Too many open files (PID or file descriptor limits)
   - Memory pressure preventing new cgroup creation

6. If the issue affects all pods on a specific node, the problem is node-specific (runtime, CNI, or resource). If it affects pods across multiple nodes, the issue is likely cluster-wide (CNI configuration, IPAM exhaustion).

**To resolve sandbox failures**: Restart the CNI plugin pods if they are unhealthy, restart the container runtime if it is unresponsive, verify network configuration is correct, and ensure node has sufficient resources. For persistent issues, check kubelet and runtime logs for detailed error information.

