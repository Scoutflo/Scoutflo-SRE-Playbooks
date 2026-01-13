---
title: Node Not Ready - Node
weight: 204
categories:
  - kubernetes
  - node
---

# NodeNotReady-node

## Meaning

A node has its Ready condition marked False or Unknown (triggering alerts like KubeNodeNotReady or KubeNodeUnreachable) because kubelet health checks are failing, the node is under resource pressure (MemoryPressure, DiskPressure, PIDPressure), or the kubelet cannot reliably communicate with the control plane. This indicates node-level failures affecting pod scheduling and availability.

## Impact

Node becomes unschedulable; pods on node may become unavailable or restart; workloads cannot be scheduled to node; services lose endpoints; applications experience reduced capacity; KubeNodeNotReady alerts fire; node condition transitions to NotReady state; kubelet communication failures occur.

## Playbook

1. List all nodes and check their status to identify nodes where the Ready condition is `False` or `Unknown`.

2. For each affected node, retrieve detailed node information to review labels, taints, conditions, and any recent changes.

3. Inspect node conditions such as `DiskPressure`, `MemoryPressure`, and `NetworkUnavailable` to see which underlying pressures are contributing to the NotReady state.

4. On affected nodes, check kubelet service logs (for example, last 100–500 lines) for errors about registration, health checks, resource pressure, or runtime issues.

5. From a pod on the affected node (or a test pod in the cluster), run network connectivity tests such as `ping` or `curl` to key cluster endpoints to verify that node networking is functioning.

6. Check the container runtime status on affected nodes using its health or info commands to confirm it is running correctly and able to start containers.

7. On affected nodes, check kubelet client certificate validity and expiration to ensure kubelet can authenticate to the API server.

## Diagnosis

1. Compare the timestamps when nodes transitioned to NotReady state with the timestamps when disk pressure conditions were reported on those nodes, and check whether disk pressure appears within 5 minutes of the NotReady transition.

2. Compare the node NotReady transition timestamps with the timestamps when memory pressure conditions were reported, and check whether memory pressure is reported within 5 minutes of the NotReady transition.

3. Compare the node NotReady transition timestamps with kubelet restart timestamps from the affected node's logs, and check whether kubelet restarts occur within 5 minutes before the node becomes NotReady.

4. Compare the node NotReady transition timestamps with the results and timestamps of network connectivity tests (for example, `ping` or `curl` from pods on the node or other nodes), and check whether network failures appear at the same time as the NotReady events.

5. Compare the node NotReady transition timestamps with node maintenance or configuration change timestamps from your infrastructure or change records, and check whether NotReady events start within 1 hour of those changes.

6. Compare the node NotReady transition timestamps with cluster upgrade windows, container runtime failure times, and kubelet certificate expiration timestamps, and check whether any of these events occur within 1 hour before or at the time of the NotReady transition.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 1 hour → 2 hours), check kubelet logs for earlier warning signs, review infrastructure change records for delayed effects, examine related nodes for similar patterns, and verify network connectivity tests from multiple time points. Node condition changes may be preceded by gradual degradation not immediately visible in status transitions.

