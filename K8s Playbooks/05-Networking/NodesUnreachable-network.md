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

1. Describe the unreachable node `<node-name>` to retrieve detailed information including conditions, addresses, capacity, and events.

2. Retrieve events for the node `<node-name>` sorted by timestamp to identify recent issues affecting the node.

3. List all nodes and their status to identify nodes marked NotReady or unreachable and note their Ready condition transitions.

4. List pods in `kube-system` and filter for CNI plugin pods (for example, DaemonSet pods) to verify they are running and not restarting excessively on the affected nodes.

5. From a pod on a healthy node, execute ping or similar network tests to the unreachable node IPs to verify node-to-node connectivity.

6. List NetworkPolicy resources in `kube-system` and other relevant namespaces and review their rules to determine whether any policies could be blocking node or pod traffic between nodes.

## Diagnosis

1. Analyze node events from Playbook to identify when nodes transitioned to NotReady or Unknown state. If events show NodeNotReady with specific timestamps, note the transition time and any associated error messages.

2. If node events indicate unreachability, check node conditions from Playbook for Ready condition status and LastHeartbeatTime. If LastHeartbeatTime is stale, the kubelet is not communicating with the API server.

3. If kubelet communication is failing, check CNI plugin pod status on affected nodes from Playbook. If CNI pods are not running or show failures, network connectivity between the node and control plane is broken.

4. If CNI pods are healthy, verify network connectivity test results from Playbook (ping tests between nodes). If node-to-node connectivity fails, check for network infrastructure issues affecting node communication.

5. If node connectivity works, check NetworkPolicy resources from Playbook for policies that may block control plane traffic to kubelets (port 10250). If policies restrict kube-system or node communication, API server cannot reach kubelets.

6. If NetworkPolicy is not blocking, review node network interface and route configuration. If routes to the API server or cluster network are missing or incorrect, kubelet cannot report status.

**If no network configuration issue is found**: Check cloud provider networking (VPC, subnets, security groups), verify if nodes are in different availability zones with connectivity issues, review kubelet logs for authentication or certificate errors, and examine if recent infrastructure maintenance affected node networking.

