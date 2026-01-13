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

1. Check the node `<node-name>` status and verify its Ready condition to confirm the node is NotReady due to kubelet issues.

2. On the node, check kubelet service status using Pod Exec tool or SSH if node access is available to verify if the service is running, stopped, or failed.

3. On the node, retrieve kubelet service logs (for example, using `journalctl -u kubelet` via Pod Exec tool or SSH) and filter for errors, crashes, or startup failures that explain why kubelet is not running.

4. List events on the node and filter for kubelet-related events, focusing on events with reasons such as `NodeNotReady` or messages indicating kubelet service failures.

5. Check the node for resource constraints (CPU, memory, disk) that may have caused kubelet to crash or be killed.

6. Verify container runtime status on the node since kubelet depends on the container runtime, and check if runtime issues are preventing kubelet from starting.

## Diagnosis

1. Compare the kubelet service not running timestamps with kubelet service restart or crash timestamps, and check whether kubelet crashes occurred within 5 minutes before the service stopped.

2. Compare the kubelet service not running timestamps with node resource pressure condition timestamps (MemoryPressure, DiskPressure), and check whether resource constraints occurred within 5 minutes before kubelet stopped.

3. Compare the kubelet service not running timestamps with container runtime failure timestamps, and check whether runtime issues occurred within 5 minutes before kubelet stopped.

4. Compare the kubelet service not running timestamps with kubelet configuration modification timestamps, and check whether configuration changes occurred within 30 minutes before kubelet stopped.

5. Compare the kubelet service not running timestamps with node maintenance or reboot timestamps, and check whether node operations occurred within 1 hour before kubelet stopped.

6. Compare the kubelet service not running timestamps with cluster upgrade or kubelet version update timestamps, and check whether infrastructure changes occurred within 1 hour before kubelet stopped.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review kubelet logs for gradual performance degradation, check for intermittent resource constraint issues, examine if kubelet configuration drifted over time, verify if container runtime issues developed gradually, and check for node-level system problems that may have accumulated. Kubelet service failures may result from gradual node infrastructure degradation rather than immediate changes.

