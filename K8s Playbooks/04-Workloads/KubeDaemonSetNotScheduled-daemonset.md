---
title: Kube DaemonSet Not Scheduled
weight: 20
---

# KubeDaemonSetNotScheduled

## Meaning

DaemonSet pods are not scheduled on nodes where they should run (triggering alerts related to DaemonSet scheduling issues) because node selectors, tolerations, or affinity rules prevent scheduling, nodes lack required resources, or node taints are incompatible with DaemonSet tolerations. DaemonSets show number scheduled mismatch in kubectl, pods remain in Pending state, and pod events show FailedScheduling, InsufficientCPU, InsufficientMemory, or Unschedulable errors. This affects the workload plane and indicates scheduling constraints preventing DaemonSet from achieving desired state, typically caused by configuration mismatches, persistent resource constraints, or node pool changes; node taint/toleration mismatches may prevent scheduling.

## Impact

DaemonSet scheduling alerts fire; service degradation or unavailability; DaemonSet cannot achieve desired state; pods remain in Pending state; DaemonSet desired number scheduled mismatch; system components may be missing on required nodes; functionality dependent on DaemonSet pods fails; DaemonSet desired state cannot be achieved. DaemonSets show number scheduled mismatch indefinitely; pods remain in Pending state; pod events show FailedScheduling or Unschedulable errors; node taint/toleration mismatches may prevent scheduling; system components may be missing on required nodes.

## Playbook

1. Describe DaemonSet <daemonset-name> in namespace <namespace> to see:
   - Number scheduled versus desired number scheduled
   - Node selector, tolerations, and affinity rule configurations
   - Conditions showing why pods are not scheduled
   - Events showing FailedScheduling, InsufficientCPU, InsufficientMemory, or Unschedulable errors

2. Retrieve events for DaemonSet <daemonset-name> in namespace <namespace> sorted by timestamp to see the sequence of scheduling failures.

3. List pods belonging to DaemonSet in namespace <namespace> with label app=<daemonset-label> and describe pods to identify pods in Pending state and scheduling blockers.

4. Describe node <node-name> to verify node availability, conditions, taints, and compatibility with DaemonSet tolerations.

5. Retrieve node resource usage metrics to verify resource availability for nodes where DaemonSet pods should be scheduled.

## Diagnosis

1. Analyze DaemonSet and pod events from Playbook to identify the scheduling blocker. Events showing "FailedScheduling" with specific reasons (InsufficientCPU, InsufficientMemory, node(s) had taint) indicate the exact constraint preventing pod placement.

2. If events indicate taint-related failures (node(s) had taint that the pod didn't tolerate), compare node taints from Playbook with DaemonSet tolerations. DaemonSets require explicit tolerations for node taints. Common missing tolerations include node-role.kubernetes.io/master, node-role.kubernetes.io/control-plane, or custom taints.

3. If events indicate resource constraints (InsufficientCPU, InsufficientMemory), compare DaemonSet pod resource requests with node allocatable resources. DaemonSet pods compete with other pods for node resources. Verify if existing pods consume resources that DaemonSet pods need.

4. If events indicate node selector mismatches (node(s) didn't match Pod's node affinity/selector), verify that the DaemonSet's nodeSelector or nodeAffinity matches labels on target nodes. Check if expected node labels exist using node descriptions from Playbook.

5. If events indicate nodes are unschedulable (node(s) were unschedulable), check node conditions for cordoned nodes or nodes with scheduling disabled. Cordoned nodes prevent new pod scheduling including DaemonSet pods.

6. If pods are Pending but no clear scheduling failure event exists, check if the nodes are in NotReady state. DaemonSet pods are not scheduled to NotReady nodes by default. Verify node conditions from Playbook.

7. If DaemonSet uses nodeAffinity with requiredDuringSchedulingIgnoredDuringExecution, pods will not schedule if no nodes match the affinity rules. Verify that at least some nodes in the cluster match the specified node affinity expressions.
