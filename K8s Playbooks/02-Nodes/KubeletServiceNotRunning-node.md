---
title: Kubelet Service Not Running - Node
weight: 225
categories:
  - kubernetes
  - node
---

# KubeletServiceNotRunning-node

## Meaning

The kubelet service is not running on nodes (triggering KubeNodeNotReady or KubeletDown alerts) because the service stopped, crashed, failed to start, or was disabled. Nodes show NotReady condition in cluster dashboards, kubelet service status shows stopped or failed state, and kubelet service logs show error messages, crashes, or startup failures. This affects the data plane and prevents nodes from managing pods, reporting status, or responding to API server requests, typically caused by kubelet process crashes, resource constraints, container runtime issues, or configuration problems; applications running on affected nodes may experience errors or become unreachable.

## Impact

Nodes become NotReady; pods on the node cannot be managed; new pods cannot be scheduled to the node; pod status cannot be reported to control plane; KubeNodeNotReady alerts fire; KubeletDown alerts fire; node condition transitions to NotReady; cluster loses node capacity; applications on the node become unavailable. Nodes show NotReady condition indefinitely; kubelet service status shows stopped or failed state; pods on affected nodes may become unreachable or be evicted; applications running on affected nodes may experience errors or performance degradation.

## Playbook

1. Describe node <node-name> to see:
   - Conditions section showing Ready status (expected to be False or Unknown)
   - Events section showing NodeNotReady or kubelet service failure events
   - System Info and resource allocation details

2. Retrieve events for node <node-name> sorted by timestamp to see the sequence of kubelet-related events including 'NodeNotReady' or messages indicating kubelet service failures.

3. On the node, check kubelet service status using Pod Exec tool or SSH if node access is available to verify if the service is running, stopped, or failed.

4. On the node, retrieve kubelet service logs via Pod Exec tool or SSH and filter for errors, crashes, or startup failures that explain why kubelet is not running.

5. Check the node for resource constraints (CPU, memory, disk) that may have caused kubelet to crash or be killed.

6. Verify container runtime status on the node since kubelet depends on the container runtime, and check if runtime issues are preventing kubelet from starting.

## Diagnosis

1. Analyze node events from Playbook steps 1-2 to identify when kubelet service issues began. Events with reason "NodeNotReady" and message indicating "Kubelet stopped posting node status" show when kubelet became unresponsive. Note the event timestamps to establish the failure timeline.

2. If node events indicate kubelet stopped unexpectedly, check kubelet service status and logs from Playbook steps 3-4. Look for crash reasons, OOM kills, panic messages, or fatal errors that explain why kubelet stopped.

3. If kubelet logs show OOM kills or resource exhaustion, check node resource constraints from Playbook step 5. Memory pressure or disk exhaustion can cause kubelet to be killed by the OOM killer or fail to function.

4. If node events indicate container runtime issues, verify container runtime status from Playbook step 6. Kubelet depends on the container runtime (containerd/docker) and cannot start or function if the runtime is unavailable.

5. If kubelet logs show configuration errors or startup failures, check for recent kubelet configuration changes. Invalid configuration prevents kubelet from starting or causes immediate crashes.

6. If kubelet logs show certificate or authentication errors, verify kubelet certificates are valid and accessible. Certificate issues prevent kubelet from authenticating to the API server.

7. If kubelet service status shows the service is disabled or not enabled, verify systemd service configuration to ensure kubelet is configured to start automatically.

**If no root cause is identified from events**: Review system logs (journalctl, dmesg) for kernel-level issues or hardware failures, check for disk corruption affecting kubelet binaries or configuration, verify node operating system health, and examine if kubelet was manually stopped or disabled.

