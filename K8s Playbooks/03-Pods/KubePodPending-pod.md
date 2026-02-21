---
title: Kube Pod Pending
weight: 27
categories: [kubernetes, pod]
---

# KubePodPending

## Meaning

Pod is stuck in Pending state (triggering KubePodPending alerts) because the Kubernetes scheduler cannot find a suitable node to place the pod due to resource constraints, node selectors, taints/tolerations, affinity rules, or insufficient cluster capacity. Pod status shows Pending with scheduling failure events, no node is assigned, and the pod cannot start. This affects the workload plane and indicates cluster capacity or scheduling configuration issues; deployments cannot complete; scaling operations fail; service capacity is limited.

## Impact

KubePodPending alerts fire; pod cannot start; deployment replicas are unavailable; scaling operations blocked; HPA cannot scale up effectively; jobs cannot execute; service capacity is reduced; batch processing is delayed; new application versions cannot deploy; critical workloads may be blocked; cluster utilization appears full while pods wait.

## Playbook

1. Retrieve the Pod `<pod-name>` in namespace `<namespace>` and confirm status is Pending with no node assigned.

2. Retrieve events for the Pod `<pod-name>` in namespace `<namespace>` and filter for scheduling events including 'FailedScheduling', 'Unschedulable', 'Insufficient' to identify specific scheduling failures.

3. Retrieve the pod resource requests (CPU, memory) and compare against available capacity on nodes to identify resource constraints.

4. Check node selectors in pod spec and verify matching labels exist on nodes in the cluster.

5. Retrieve node taints and verify pod has appropriate tolerations to schedule on tainted nodes.

6. Check pod affinity and anti-affinity rules to verify they don't create impossible scheduling constraints.

7. Retrieve all nodes and their allocatable resources, current usage, and conditions to identify if any node can accept the pod.

## Diagnosis

Compare pod resource requests with node available capacity and verify whether requests exceed what any single node can provide, using node allocatable resources and current pod allocations as supporting evidence.

Analyze FailedScheduling events for specific reasons (Insufficient cpu, Insufficient memory, node(s) didn't match node selector) and verify the blocking constraint, using scheduler events and pod spec as supporting evidence.

Correlate pending pods with cluster-wide resource utilization and verify whether cluster needs more nodes (capacity issue) versus pods are misconfigured (configuration issue), using cluster resource metrics and pending pod specs as supporting evidence.

Check if PriorityClass affects scheduling and verify whether lower priority pods are being preempted or if pending pod has too low priority, using pod priority and preemption events as supporting evidence.

Verify if PersistentVolumeClaims referenced by the pod are bound, as unbound PVCs block pod scheduling, using PVC status and storage class availability as supporting evidence.

If no correlation is found within the specified time windows: check for resource quota limits in namespace, verify LimitRange constraints, review scheduler logs for detailed decisions, check if cluster autoscaler can add nodes, verify node cordons or drains are not blocking scheduling.
