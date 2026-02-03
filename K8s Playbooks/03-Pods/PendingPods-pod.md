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

1. Describe pod <pod-name> in namespace <namespace> and look at the Events section - the scheduler will explain exactly why the pod cannot be scheduled (e.g., "0/5 nodes are available: 3 Insufficient cpu, 2 node(s) had taint that the pod didn't tolerate").

2. Retrieve events for pod <pod-name> in namespace <namespace> filtered by reason FailedScheduling to see the scheduling failure reason.

3. Retrieve the resource requests for pod <pod-name> in namespace <namespace> and compare with available node capacity using node resource metrics.

4. List all nodes with their taints and compare with the tolerations configured for pod <pod-name> in namespace <namespace>.

5. Retrieve the node selectors and affinity rules for pod <pod-name> in namespace <namespace> to identify placement constraints.

6. Describe ResourceQuota resources in namespace <namespace> to see if CPU/memory/pod count quotas are exhausted.

7. List PodDisruptionBudgets in namespace <namespace> to see if PDBs are blocking pod scheduling.

8. Check cluster autoscaler status (if enabled) by retrieving events in kube-system namespace filtered by reason ScaleUp to see if new nodes are being provisioned.

## Diagnosis

1. Analyze pod events from Playbook steps 1-2 to identify the scheduling failure reason. The scheduler provides detailed messages like "0/X nodes are available: ..." followed by why each node was rejected.

2. If events indicate resource issues (from Playbook step 2):
   - "Insufficient cpu": Pod CPU requests exceed available capacity
   - "Insufficient memory": Pod memory requests exceed available capacity
   - Compare pod requests (Playbook step 3) with node capacity and reduce requests or add nodes

3. If events indicate taint issues (from Playbook step 4):
   - "node(s) had taint {key=value:effect} that pod didn't tolerate"
   - Add tolerations to pod spec or remove taints from nodes
   - Check if nodes were recently tainted for maintenance

4. If events indicate affinity/selector issues (from Playbook step 5):
   - "node(s) didn't match Pod's node affinity/selector"
   - Verify nodes with required labels exist and are schedulable
   - Relax placement constraints if too restrictive

5. If ResourceQuota is exceeded (from Playbook step 6):
   - Namespace has reached CPU, memory, or pod count limits
   - Increase quota or reduce resource usage in namespace

6. If PodDisruptionBudget blocks scheduling (from Playbook step 7):
   - Too many pods already disrupted
   - Wait for existing disruptions to resolve

7. If cluster autoscaler is not scaling up (from Playbook step 8):
   - Check autoscaler logs for errors
   - Verify cloud provider quota allows new nodes
   - Check if node pool configuration matches pod requirements

**To resolve Pending pods**: Address the specific scheduling constraint identified in the scheduler message. Common solutions include adding nodes, adjusting resource requests, adding tolerations, or relaxing placement constraints.

