---
title: DaemonSet Not Deploying Pods on All Nodes - DaemonSet
weight: 220
categories:
  - kubernetes
  - daemonset
---

# DaemonSetNotDeployingPodsonAllNodes-daemonset

## Meaning

DaemonSet pods are not being deployed on all nodes (triggering DaemonSet-related alerts) because node selectors or affinity rules restrict which nodes can run the pods, node taints prevent scheduling without matching tolerations, insufficient resources on nodes prevent pod creation, or nodes are unschedulable. DaemonSets show number scheduled mismatch in kubectl, pods remain in Pending state on some nodes, and pod events show FailedCreate or scheduling errors. This affects the workload plane and prevents DaemonSet pods from being created on all nodes, typically caused by node selector/toleration mismatches or resource constraints; node-level functionality is unavailable on affected nodes.

## Impact

DaemonSet pods are missing on some nodes; node-level functionality is unavailable on affected nodes; monitoring, logging, or networking components may be missing; DaemonSet desired number of nodes does not match ready number; KubeDaemonSetNotReady alerts may fire; node-specific services are not running; cluster functionality is inconsistent across nodes. DaemonSets show number scheduled mismatch indefinitely; pods remain in Pending state on some nodes; node-level functionality is unavailable on affected nodes and may cause errors; cluster functionality is inconsistent across nodes.

## Playbook

1. Describe DaemonSet <daemonset-name> in namespace <namespace> to see:
   - Desired number of nodes versus ready/available number
   - Node selector and tolerations configuration
   - Conditions showing why pods are not deploying
   - Events showing FailedCreate, FailedScheduling, or scheduling errors

2. Retrieve events for DaemonSet <daemonset-name> in namespace <namespace> sorted by timestamp to see the sequence of deployment failures.

3. List all nodes and compare with DaemonSet pod distribution by listing pods in namespace <namespace> with label app=<daemonset-label> to identify which nodes are missing DaemonSet pods.

4. Verify that the DaemonSet controller is running by listing kube-controller-manager pods in kube-system namespace.

5. For nodes missing DaemonSet pods, describe node <node-name> to check labels, taints, and scheduling status and verify if they match DaemonSet requirements.

6. Retrieve resource usage metrics for nodes missing DaemonSet pods to verify if insufficient resources are preventing pod creation.

7. List PodDisruptionBudget resources in namespace <namespace> to check for conflicts that may prevent DaemonSet pod creation on nodes.

## Diagnosis

1. Analyze DaemonSet events and pod distribution from Playbook to identify which nodes are missing DaemonSet pods. Compare nodes with pods running versus nodes without pods to identify the differentiating factor (labels, taints, resources, or conditions).

2. If events indicate scheduling failures on specific nodes, examine those nodes individually. Group nodes by failure reason - some may have taint issues while others have resource constraints. Different nodes may have different blockers.

3. If missing pods correlate with specific node pools or node groups, verify that those nodes have labels matching the DaemonSet's nodeSelector. Node pool configuration changes may add nodes without required labels.

4. If missing pods correlate with nodes having specific taints, verify DaemonSet tolerations cover all taint keys and effects. Common missing tolerations include NoSchedule taints for specialized workloads, GPU nodes, or spot/preemptible instances.

5. If some nodes have insufficient resources, compare DaemonSet pod resource requests with available allocatable resources on the affected nodes. Nodes with more existing workloads may not have capacity for DaemonSet pods.

6. If affected nodes are cordoned or unschedulable, DaemonSet pods cannot be created on those nodes. Check node descriptions from Playbook for spec.unschedulable or cordon status.

7. If affected nodes show NotReady condition or have kubelet issues, the node may not be accepting pod scheduling. Verify node conditions and check for MemoryPressure, DiskPressure, or PIDPressure conditions that prevent scheduling.

8. If no clear pattern emerges, compare the full scheduling requirements (nodeSelector, nodeAffinity, tolerations) against each affected node's configuration. The intersection of multiple constraints may exclude nodes that pass individual checks.

