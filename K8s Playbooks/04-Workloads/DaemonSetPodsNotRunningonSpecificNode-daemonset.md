---
title: DaemonSet Pods Not Running on Specific Node - DaemonSet
weight: 264
categories:
  - kubernetes
  - daemonset
---

# DaemonSetPodsNotRunningonSpecificNode-daemonset

## Meaning

DaemonSet pods are not running on a specific node (triggering DaemonSet-related alerts) because the node has taints without matching tolerations in the DaemonSet, the node selector does not match the node's labels, insufficient resources prevent pod creation, or the node is unschedulable. DaemonSets show number scheduled mismatch for the specific node, pods remain in Pending state, and pod events show FailedCreate or scheduling errors. This affects the workload plane and prevents DaemonSet pods from being created on the specific node, typically caused by node taint/toleration mismatches or resource constraints; node-level functionality is unavailable on that node.

## Impact

DaemonSet pod is missing on the specific node; node-level functionality is unavailable on that node; monitoring, logging, or networking components are missing; DaemonSet desired number of nodes does not match ready number; KubeDaemonSetNotReady alerts may fire; node-specific services are not running on the affected node; cluster functionality is inconsistent. DaemonSets show number scheduled mismatch for the specific node indefinitely; pods remain in Pending state; node-level functionality is unavailable on that node and may cause errors; cluster functionality is inconsistent.

## Playbook

1. Describe DaemonSet <daemonset-name> in namespace <namespace> to see:
   - Desired versus ready number of pods
   - Node selector, tolerations, and affinity rules configuration
   - Conditions showing why pods are not running on specific nodes
   - Events showing FailedCreate or scheduling errors

2. Retrieve events for DaemonSet <daemonset-name> in namespace <namespace> sorted by timestamp to see the sequence of deployment failures.

3. Verify that the DaemonSet controller is running by listing kube-controller-manager pods in kube-system namespace.

4. Describe node <node-name> and inspect its labels, taints, and scheduling status to verify if it matches DaemonSet requirements.

5. Retrieve resource usage metrics for node <node-name> to verify if insufficient CPU, memory, or other resources are preventing DaemonSet pod creation.

6. List PodDisruptionBudget resources in namespace <namespace> to check for conflicts that may prevent DaemonSet pod creation on the specific node.

## Diagnosis

1. Analyze DaemonSet and pod events from Playbook to identify why the pod is not running on the specific node. Events showing "FailedScheduling" with the node name indicate scheduling constraints specific to that node. Events showing "FailedCreate" indicate pod creation blockers.

2. If events indicate taint-related failures for the specific node, compare the node's taints with DaemonSet tolerations. The specific node may have taints that other nodes do not have, such as custom workload isolation taints or maintenance taints.

3. If events indicate resource constraints on the specific node (InsufficientCPU, InsufficientMemory), compare available resources on that node versus other nodes where DaemonSet pods are running. The specific node may have higher utilization from other workloads.

4. If the specific node's labels do not match DaemonSet nodeSelector, verify whether this node should have the required labels. The node may be missing labels that other nodes have, or may have been added to a different node pool.

5. If the node is cordoned or has spec.unschedulable=true, DaemonSet pods cannot be scheduled. Check node status from Playbook to identify if the node was intentionally marked unschedulable for maintenance.

6. If the node shows NotReady condition or has resource pressure conditions (MemoryPressure, DiskPressure, PIDPressure), the kubelet may not be accepting new pods. Verify node conditions and kubelet health on the specific node.

7. If no scheduling event exists and the pod simply does not exist on that node, verify that the node matches all DaemonSet scheduling requirements including nodeSelector, nodeAffinity, and tolerations. Also check if a PodDisruptionBudget is preventing pod creation by blocking necessary evictions.

