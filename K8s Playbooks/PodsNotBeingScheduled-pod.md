---
title: Pods Not Being Scheduled - Pod
weight: 233
categories:
  - kubernetes
  - pod
---

# PodsNotBeingScheduled-pod

## Meaning

Pods remain stuck in Pending state (triggering KubePodPending alerts) because the scheduler cannot find any suitable node due to resource constraints, node taints without matching tolerations, affinity/anti-affinity rules, or other placement restrictions. Pods show Pending state in kubectl, pod events show "0/X nodes are available" messages with InsufficientCPU, InsufficientMemory, or Unschedulable errors, and ResourceQuota resources may show exceeded limits. This affects the workload plane and prevents pod placement, typically caused by resource constraints, node taint/toleration mismatches, or ResourceQuota limits; applications cannot start.

## Impact

Pods cannot be scheduled; deployments fail to scale; applications remain unavailable; services cannot get new pods; pods remain in Pending state indefinitely; scheduler cannot place pods; replica counts mismatch desired state; KubePodPending alerts fire; pod events show "0/X nodes are available" messages with specific scheduling failure reasons. Pods show Pending state indefinitely; pod events show InsufficientCPU, InsufficientMemory, or Unschedulable errors; ResourceQuota limits may prevent pod creation; applications cannot start and may show errors.

## Playbook

1. Retrieve the pod `<pod-name>` in namespace `<namespace>` and inspect its status and associated events to see scheduler messages explaining why it remains Pending.

2. List all nodes and retrieve resource usage metrics to compare available CPU and memory on each node with the pod's requested resources.

3. Retrieve the Deployment `<deployment-name>` in namespace `<namespace>` and review container resource requests and limits to ensure they are reasonable relative to node capacity.

4. Inspect the pod `<pod-name>` spec for node selectors, affinity, or anti-affinity rules that may restrict which nodes it can schedule onto.

5. List all nodes and examine their taints, then compare with the pod's tolerations to determine whether taints are preventing scheduling.

6. Retrieve ResourceQuota objects in namespace `<namespace>` and compare current usage against limits to see whether quotas are blocking new pod creation.

## Diagnosis

1. Compare the pod Pending timestamps with node resource availability timestamps, and check whether nodes ran out of allocatable resources within 30 minutes before pods became Pending.

2. Compare the pod Pending timestamps with node taint modification timestamps, and check whether new taints were applied within 30 minutes before pods started failing to schedule.

3. Compare the pod Pending timestamps with deployment resource request modification timestamps, and check whether resource requests were increased within 30 minutes before scheduling failures.

4. Compare the pod Pending timestamps with node removal or cordoning timestamps, and check whether available nodes were removed or made unschedulable within 30 minutes before scheduling failures.

5. Compare the pod Pending timestamps with ResourceQuota creation or modification timestamps, and check whether quota constraints were introduced or tightened within 30 minutes before pods became Pending.

6. Compare the pod Pending timestamps with cluster scaling events, workload increases, or node capacity changes, and check whether resource competition increased within 1 hour before scheduling failures.

**If no correlation is found within the specified time windows**: Extend the search window (30 minutes → 1 hour, 1 hour → 2 hours), review scheduler logs for detailed scheduling failure reasons, check for gradual resource exhaustion patterns, examine node capacity changes over a longer period, verify if quota or scheduling constraints were recently tightened, and check for cumulative resource pressure from multiple workloads. Scheduling failures may result from cumulative resource pressure rather than immediate changes.

