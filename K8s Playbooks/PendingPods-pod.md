---
title: Pending Pods - Pod
weight: 203
categories:
  - kubernetes
  - pod
---

# PendingPods-pod

## Meaning

Pods remain stuck in the Pending phase (triggering KubePodPending alerts) because the scheduler cannot find any node that satisfies their resource requirements, affinity rules, taints, node selectors, or other placement constraints. Pods show Pending state in kubectl, pod events show "0/X nodes are available" messages with InsufficientCPU, InsufficientMemory, or Unschedulable errors, and ResourceQuota resources may show exceeded limits. This affects the workload plane and prevents pod placement, typically caused by resource constraints, node taint/toleration mismatches, or ResourceQuota limits; applications cannot start.

## Impact

New workloads cannot start; deployments fail to scale; applications remain unavailable; services cannot get new pods; capacity constraints prevent workload deployment; KubePodPending alerts fire; pods remain in Pending state; scheduler cannot place pods; replica counts mismatch desired state. Pods show Pending state indefinitely; pod events show InsufficientCPU, InsufficientMemory, or Unschedulable errors; applications cannot start and may show errors; capacity constraints prevent workload deployment.

## Playbook

1. Retrieve the pod `<pod-name>` in namespace `<namespace>` and inspect its status and associated events to see scheduler messages explaining why it remains Pending.

2. List all nodes and retrieve resource usage metrics to compare available CPU and memory on each node with the pod’s requested resources.

3. Retrieve the Deployment `<deployment-name>` in namespace `<namespace>` and review container resource requests and limits to ensure they are reasonable relative to node capacity.

4. Inspect the pod `<pod-name>` spec for node selectors, affinity, or anti-affinity rules that may restrict which nodes it can schedule onto.

5. List all nodes and examine their taints, then compare with the pod’s tolerations to determine whether taints are preventing scheduling.

6. Retrieve ResourceQuota objects in namespace `<namespace>` and compare current usage against limits to see whether quotas are blocking new pod creation.

7. List PodDisruptionBudget objects in namespace `<namespace>` and review their specs to understand whether PDB constraints are limiting evictions or rescheduling needed to place the pod.

## Diagnosis

1. Compare the timestamps when pods entered Pending state with the timestamps when Deployment resource requests were modified, and check whether Pending pods appear within 30 minutes of increases in requested CPU or memory.

2. Compare the pod Pending timestamps with node capacity and usage metrics (CPU, memory) from node metrics, and check whether Pending pods correlate with nodes running out of allocatable resources at the same time.

3. Compare the pod Pending timestamps with node Ready condition transition times, and check whether Pending pods appear within 5 minutes of nodes becoming NotReady or leaving the cluster.

4. Compare the pod Pending timestamps with changes to affinity and anti-affinity rules in pod specifications and check whether new or stricter placement rules were introduced within 30 minutes before pods became Pending.

5. Compare the pod Pending timestamps with node taint modification times and check whether new taints were applied within 30 minutes before pods started failing to schedule.

6. Compare the pod Pending timestamps with cluster scaling events, node maintenance windows, namespace ResourceQuota creation or update times, and PodDisruptionBudget change times, and check whether scheduling issues began within 1 hour after any of these changes.

**If no correlation is found within the specified time windows**: Extend the search window (30 minutes → 1 hour, 1 hour → 2 hours), review scheduler logs for detailed scheduling failure reasons, check for gradual resource exhaustion patterns, examine node capacity changes over a longer period, and verify if quota or PDB constraints were recently tightened. Scheduling issues may result from cumulative resource pressure rather than immediate changes.

