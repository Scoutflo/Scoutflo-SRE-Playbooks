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

1. Retrieve the Node `<node-name>` and inspect its status to check Ready condition status and node reachability to verify unreachability.

2. Retrieve the Node `<node-name>` and check node conditions to verify if node is in Unknown state indicating unreachability.

3. Retrieve events for the Node `<node-name>` and filter for error patterns including 'NodeUnreachable', 'NodeNotReady', 'NodeLost' to identify unreachability causes.

4. Verify network connectivity between monitoring system and the Node `<node-name>` to confirm connectivity issues.

5. Check kubelet status on the Node `<node-name>` by accessing via Pod Exec tool or SSH if node access is available to verify kubelet operation.

6. Verify API server connectivity from the Node `<node-name>` perspective to identify control plane communication issues.

7. Check for recent node maintenance, upgrades, or infrastructure changes that may affect node reachability by reviewing node events and maintenance logs.

## Diagnosis

Compare node unreachability detection timestamps with network policy or firewall rule change timestamps within 10 minutes and verify whether unreachability began after network configuration changes, using network policy events and connectivity logs as supporting evidence.

Correlate node unreachability with control plane node failures or API server unavailability within 5 minutes and verify whether node lost connectivity due to control plane issues, using API server status and node connection attempts as supporting evidence.

Compare node unreachability timestamps with node maintenance or upgrade event times within 1 hour and verify whether unreachability coincides with planned maintenance, using maintenance logs and node status changes as supporting evidence.

Analyze node reachability patterns over the last 15 minutes to determine if unreachability is complete (node failure) or intermittent (network issues), using node condition history and connectivity metrics as supporting evidence.

Correlate node unreachability with storage area network or infrastructure change timestamps within 1 hour and verify whether infrastructure changes caused node suspension or failure, using infrastructure logs and node status as supporting evidence.

Compare node unreachability with other node failures within the same timeframe and verify whether multiple nodes are affected (cluster-wide issue) or isolated to single node, using node status across cluster and failure patterns as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 24 hours for infrastructure changes, review node hardware logs, check for storage area network issues, verify cloud provider infrastructure status, examine historical node failure patterns. Node unreachability may result from hardware failures, network infrastructure problems, or cloud provider issues rather than immediate configuration changes.
