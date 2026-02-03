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

1. Describe pod <pod-name> in namespace <namespace> to inspect its status and see scheduler messages explaining why it remains Pending.

2. Retrieve events in namespace <namespace> for pod <pod-name> sorted by timestamp to identify scheduler events and scheduling failure reasons.

3. List all nodes and retrieve resource usage metrics to compare available CPU and memory on each node with the pod's requested resources.

4. Retrieve the Deployment <deployment-name> in namespace <namespace> and review container resource requests and limits to ensure they are reasonable relative to node capacity.

5. Inspect the pod <pod-name> spec for node selectors, affinity, or anti-affinity rules that may restrict which nodes it can schedule onto.

6. List all nodes and examine their taints, then compare with the pod's tolerations to determine whether taints are preventing scheduling.

7. Retrieve ResourceQuota objects in namespace <namespace> and compare current usage against limits to see whether quotas are blocking new pod creation.

## Diagnosis

1. Analyze pod events from Playbook steps 1-2 to identify the scheduling failure reason. The scheduler provides detailed messages like "0/X nodes are available" followed by specific reasons for each node rejection.

2. If events indicate "Insufficient cpu" or "Insufficient memory" (from Playbook step 2), compare pod resource requests (Playbook step 4) with node available capacity (Playbook step 3). Either reduce resource requests or add more nodes to the cluster.

3. If events indicate "node(s) had taint that pod didn't tolerate" (from Playbook step 6), the pod needs tolerations for the node taints. Add appropriate tolerations to the pod spec or remove unnecessary taints from nodes.

4. If events indicate node selector or affinity mismatches (from Playbook step 5), verify that nodes with matching labels exist. Either update node labels or adjust pod placement constraints.

5. If ResourceQuota shows exceeded limits (from Playbook step 7), the namespace has reached its resource quota. Either increase the quota or reduce resource usage in the namespace.

6. If events indicate PodDisruptionBudget constraints, too many pods are already unavailable. Wait for existing disruptions to resolve or adjust PDB settings.

7. If events indicate inter-pod anti-affinity conflicts, there are not enough nodes to satisfy the spreading requirements. Add more nodes or relax anti-affinity rules.

8. If cluster autoscaler is enabled but not scaling up (from Playbook step 8), check autoscaler events for errors. Common issues include cloud provider API limits, insufficient quota, or autoscaler configuration problems.

**If scheduling failure persists**: Review the complete scheduler message which lists all nodes and why each was rejected. Address the most common rejection reason first. Consider using `kubectl describe nodes` to see current resource allocation on each node.

