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

1. Describe node <node-name> to see:
   - Conditions section showing Ready status and other pressure conditions
   - Events section showing NodeNotReady, KubeletNotReady events with timestamps
   - Labels, taints, and allocated resources

2. Retrieve events for node <node-name> sorted by timestamp to see the sequence of node issues.

3. Check node conditions for node <node-name> to see Ready, MemoryPressure, DiskPressure, PIDPressure, NetworkUnavailable status and lastTransitionTime.

4. On affected nodes, check kubelet service logs (for example, last 100-500 lines) for errors about registration, health checks, resource pressure, or runtime issues.

5. From a pod on the affected node (or a test pod in the cluster), verify network connectivity to key cluster endpoints to confirm that node networking is functioning.

6. Check the container runtime status on affected nodes using its health or info commands to confirm it is running correctly and able to start containers.

7. On affected nodes, check kubelet client certificate validity and expiration to ensure kubelet can authenticate to the API server.

## Diagnosis

1. Analyze node events from Playbook steps 1-2 to identify the primary cause of NotReady. Events showing "NodeNotReady" with reason "KubeletNotReady" indicate kubelet issues. Events showing "NodeHasDiskPressure", "NodeHasMemoryPressure", or "NodeHasPIDPressure" indicate resource exhaustion issues. Events showing "NodeNotSchedulable" indicate manual cordoning.

2. If node events indicate kubelet issues (KubeletNotReady, KubeletStopped), verify kubelet service status from Playbook step 4 to confirm kubelet is not running or unhealthy. Check kubelet logs for crash reasons, OOM kills, or startup failures.

3. If node events indicate resource pressure (MemoryPressure, DiskPressure, PIDPressure), correlate with node conditions from Playbook step 3 to identify which resource is exhausted. Check the lastTransitionTime of pressure conditions against the NotReady transition time.

4. If node events show network-related errors or no recent heartbeat updates, verify network connectivity results from Playbook step 5 to identify network issues preventing node-to-API-server communication.

5. If node events show certificate-related errors or authentication failures, verify node certificate validity from Playbook step 7 and compare certificate expiration timestamps with the NotReady transition time.

6. If node events show container runtime errors (ContainerRuntimeDown, RuntimeUnhealthy), check container runtime status from Playbook step 6 to confirm runtime issues preventing kubelet from managing containers.

7. If node events are inconclusive, compare the node condition lastTransitionTime timestamps with kubelet log timestamps to identify whether kubelet crashes, resource exhaustion, or external factors triggered the NotReady state.

**If no root cause is identified from events**: Review kubelet logs for warnings preceding the NotReady transition, check for node-level system issues (kernel panics, hardware failures), verify if multiple nodes show similar patterns indicating cluster-wide issues, and examine infrastructure change records for recent modifications.

