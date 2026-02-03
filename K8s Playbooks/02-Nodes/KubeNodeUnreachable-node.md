---
title: Kube Node Unreachable
weight: 20
---

# KubeNodeUnreachable

## Meaning

Kubernetes node is unreachable and some workloads may be rescheduled (triggering alerts like KubeNodeUnreachable or KubeNodeNotReady) because the node has lost network connectivity, the kubelet cannot communicate with the control plane, or the node has failed completely. Nodes show Unknown or NotReady condition in cluster dashboards, node events show NodeUnreachable or NodeLost errors, and kubectl commands fail with connection timeout errors. This affects the data plane and indicates network partitioning, hardware failures, or node-level issues preventing communication, typically caused by network infrastructure problems, node hardware failures, or disruptive software upgrades; applications running on affected nodes may experience errors or become unreachable.

## Impact

KubeNodeUnreachable alerts fire; node becomes unreachable; pods on node may be rescheduled; workloads experience disruption; node condition transitions to Unknown or NotReady; pod status becomes Unknown; service endpoints may be removed; data plane capacity is reduced; applications may experience downtime. Nodes show Unknown or NotReady condition indefinitely; pods on affected nodes may be rescheduled or become unreachable; applications running on affected nodes may experience errors or performance degradation.

## Playbook

1. Describe node <node-name> to see:
   - Conditions section showing Ready status (expected to be Unknown or False)
   - Events section showing NodeUnreachable, NodeNotReady, or NodeLost events
   - Last heartbeat times and condition transitions

2. Retrieve events for node <node-name> sorted by timestamp to see the sequence of unreachability events including 'NodeUnreachable', 'NodeNotReady', 'NodeLost'.

3. Check node conditions for node <node-name> to verify if node is in Unknown state indicating unreachability.

4. Verify network connectivity between monitoring system and the Node <node-name> to confirm connectivity issues.

5. Check kubelet status on the Node <node-name> by accessing via Pod Exec tool or SSH if node access is available to verify kubelet operation.

6. Verify API server connectivity from the Node <node-name> perspective to identify control plane communication issues.

7. Check for recent node maintenance, upgrades, or infrastructure changes that may affect node reachability by reviewing node events and maintenance logs.

## Diagnosis

1. Analyze node events from Playbook steps 1-2 to identify the primary cause of unreachability. Events with reason "NodeUnreachable" or "NodeLost" indicate complete loss of communication. Events with reason "NodeNotReady" with Unknown status indicate heartbeat timeout. Note the event timestamps to establish when unreachability began.

2. If node events indicate kubelet communication failure (no recent heartbeats), verify network connectivity from Playbook step 4 to confirm whether the node is network-reachable from the monitoring system or other cluster nodes.

3. If node events indicate kubelet issues, check kubelet status from Playbook step 5 (if node is accessible). Kubelet service failure or crash will cause the node to appear unreachable even if network is functional.

4. If network connectivity tests fail, check API server connectivity from Playbook step 6. This distinguishes between node-side network issues and control plane accessibility problems.

5. If node events show unreachability affecting multiple nodes simultaneously, this indicates cluster-wide issues such as control plane problems, network infrastructure failures, or API server unavailability rather than individual node failures.

6. If node events show isolated unreachability for a single node, check for node-specific issues: hardware failures, operating system crashes, or local network problems.

7. If node events indicate planned maintenance, verify against maintenance logs from Playbook step 7 to confirm whether unreachability is expected behavior during maintenance windows.

**If no root cause is identified from events**: Review cloud provider infrastructure status for node or availability zone issues, check for network infrastructure problems affecting node connectivity, verify node hardware health through out-of-band management, and examine if node was terminated or stopped at the infrastructure level.
