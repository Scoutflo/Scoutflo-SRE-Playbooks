---
title: Nodes Unreachable - Network
weight: 270
categories:
  - kubernetes
  - network
---

# NodesUnreachable-network

## Meaning

One or more nodes are marked unreachable (triggering KubeNodeUnreachable alerts) because the control plane cannot reliably communicate with their kubelets over the cluster network. Node unreachability indicates network partition, kubelet failures, or connectivity issues preventing node-to-control-plane communication.

## Impact

Nodes cannot communicate with each other; pod-to-pod communication fails; services cannot reach pods on unreachable nodes; cluster networking is disrupted; applications experience connectivity issues; KubeNodeUnreachable alerts fire; node Ready condition becomes Unknown; kubelet communication failures; pod scheduling fails on unreachable nodes.

## Playbook

1. List all nodes and retrieve detailed information to identify nodes marked NotReady or unreachable and note their `status.conditions[type=Ready]` transitions.

2. For each unreachable node, inspect node conditions such as `NetworkUnavailable` and other status fields that may indicate connectivity problems.

3. List pods in `kube-system` and filter for CNI plugin pods (for example, DaemonSet pods) to verify they are running and not restarting excessively on the affected nodes.

4. From a pod on a healthy node, execute `ping <node-ip>` or similar network tests to the unreachable node IPs to verify node-to-node connectivity.

5. List NetworkPolicy resources in `kube-system` and other relevant namespaces and review their rules to determine whether any policies could be blocking node or pod traffic between nodes.

## Diagnosis

1. Compare the node unreachable timestamps from node status (when Ready condition transitions to False or Unknown) with CNI plugin pod restart timestamps in `kube-system`, and check whether CNI pods restart within 5 minutes of nodes becoming unreachable.

2. Compare the node unreachable timestamps with NetworkPolicy modification timestamps in `kube-system` and relevant namespaces, and check whether new or updated policies appear within 10 minutes before nodes become unreachable.

3. Compare the node unreachable timestamps with firewall or security group update timestamps from your infrastructure, and check whether rules affecting node IPs or cluster subnets changed within 10 minutes of the nodes becoming unreachable.

4. Compare the node unreachable timestamps with kubelet restart timestamps from affected nodes' logs, and check whether kubelet restarts occur within 5 minutes before nodes are marked unreachable.

5. Compare the node unreachable timestamps with network interface configuration change times (for example, changes to routes, NIC settings, or VLANs), and check whether such changes occurred within 10 minutes of the nodes becoming unreachable.

6. Compare the node unreachable timestamps with cluster upgrade or infrastructure maintenance window timestamps, and check whether unreachability starts within 1 hour of those activities.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 10 minutes → 30 minutes, 1 hour → 2 hours), review network connectivity tests from multiple time points, check for gradual network degradation patterns, examine CNI plugin logs for earlier errors, verify if network interface configuration changes occurred outside of recorded maintenance, and check cloud provider network logs for infrastructure-level issues. Node unreachability may result from network problems that developed gradually or infrastructure changes not immediately visible.

