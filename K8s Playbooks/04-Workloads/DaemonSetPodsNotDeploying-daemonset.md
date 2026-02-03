---
title: DaemonSet Pods Not Deploying - DaemonSet
weight: 239
categories:
  - kubernetes
  - daemonset
---

# DaemonSetPodsNotDeploying-daemonset

## Meaning

DaemonSet pods are not being deployed to nodes (triggering DaemonSet-related alerts) because node selectors do not match available nodes, tolerations do not match node taints, resource constraints prevent pod creation, or the DaemonSet controller is not functioning. DaemonSets show number scheduled mismatch in kubectl, pods remain in Pending state, and pod events show FailedCreate or scheduling errors. This affects the workload plane and prevents DaemonSet pods from being created, typically caused by node selector/toleration mismatches, resource constraints, or DaemonSet controller issues; node-level functionality is unavailable.

## Impact

DaemonSet pods are not created; node-level functionality is unavailable; monitoring, logging, or networking components are missing; DaemonSet desired number of nodes does not match ready number; KubeDaemonSetNotReady alerts may fire; cluster functionality is impaired; node-specific services are not running. DaemonSets show number scheduled mismatch indefinitely; pods remain in Pending state; node-level functionality is unavailable and may cause errors; cluster functionality is impaired.

## Playbook

1. Describe DaemonSet <daemonset-name> in namespace <namespace> to see:
   - Desired number of nodes versus current/ready number
   - Node selector, tolerations, and affinity rules configuration
   - Conditions showing why pods are not deploying
   - Events showing FailedCreate or scheduling errors

2. Retrieve events for DaemonSet <daemonset-name> in namespace <namespace> sorted by timestamp to see the sequence of deployment failures.

3. Verify that the DaemonSet controller is running by listing kube-controller-manager pods in kube-system namespace and retrieve controller logs.

4. List all nodes and check their labels, taints, and scheduling status by describing nodes to verify if any nodes match the DaemonSet's requirements.

5. Retrieve node resource usage metrics to verify if insufficient CPU, memory, or other resources are preventing DaemonSet pod creation.

6. List PodDisruptionBudget resources in namespace <namespace> to check for conflicts that may prevent DaemonSet pod creation.

## Diagnosis

1. Analyze DaemonSet events from Playbook to identify why pods are not deploying. Events showing "FailedCreate" indicate the controller cannot create pods. Events showing "FailedScheduling" on multiple nodes indicate cluster-wide scheduling constraints.

2. If events indicate controller issues (no events being generated, stale events only), verify kube-controller-manager status from Playbook. The DaemonSet controller runs within kube-controller-manager and must be healthy to create pods.

3. If events indicate node selector mismatches across all nodes, the DaemonSet's nodeSelector may specify labels that no nodes have. Verify that at least some nodes in the cluster have the required labels. This is common after DaemonSet configuration changes or node pool migrations.

4. If events indicate taint-related failures on all nodes, compare cluster-wide node taints with DaemonSet tolerations. All nodes may have taints that the DaemonSet does not tolerate, such as control-plane taints on single-node clusters.

5. If events indicate resource constraints cluster-wide (InsufficientCPU, InsufficientMemory on all nodes), the DaemonSet's resource requests exceed available capacity on all nodes. Verify pod resource requests against node allocatable resources.

6. If no pods exist and no scheduling events appear, verify the DaemonSet's desired number scheduled is greater than zero. Check if nodeSelector or nodeAffinity rules exclude all nodes in the cluster.

7. If the DaemonSet controller is running but pods are not being created, check for resource quota restrictions in the DaemonSet's namespace that may prevent pod creation. Also verify if the namespace has any LimitRange that conflicts with DaemonSet pod specs.

