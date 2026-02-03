---
title: Kube DaemonSet Rollout Stuck
weight: 20
---

# KubeDaemonSetRolloutStuck

## Meaning

DaemonSet update is stuck waiting for pod replacement (triggering alerts related to DaemonSet rollout issues) because new pods cannot be scheduled or old pods cannot be terminated during the rolling update process. DaemonSets show rollout status stuck, pods remain in Pending or Terminating state, and DaemonSet events show FailedCreate, FailedScheduling, or FailedDelete errors. This affects the workload plane and indicates scheduling constraints, resource availability issues, or pod termination problems preventing DaemonSet updates, typically caused by persistent resource constraints, misconfigured affinity rules, or cluster capacity limitations; PodDisruptionBudget constraints may prevent pod termination.

## Impact

DaemonSet rollout alerts fire; DaemonSet cannot complete rolling updates; old pods remain running with outdated configurations; new pods cannot be scheduled; service degradation or unavailability; DaemonSet desired state mismatch; pods stuck in Terminating state; update strategy cannot progress; system components may run with inconsistent versions. DaemonSets show rollout status stuck indefinitely; pods remain in Pending or Terminating state; DaemonSet events show FailedCreate, FailedScheduling, or FailedDelete errors; PodDisruptionBudget constraints may prevent pod termination; system components may run with inconsistent versions.

## Playbook

1. Describe DaemonSet <daemonset-name> in namespace <namespace> to see:
   - Rollout status, desired number scheduled, and number ready
   - Update strategy configuration
   - Conditions showing why rollout is stuck
   - Events showing FailedCreate, FailedScheduling, or FailedDelete errors

2. Retrieve events for DaemonSet <daemonset-name> in namespace <namespace> sorted by timestamp to see the sequence of rollout issues.

3. List pods belonging to DaemonSet in namespace <namespace> with label app=<daemonset-label> and describe pods to identify pods in Pending or Terminating states.

4. Check rollout status for DaemonSet <daemonset-name> in namespace <namespace> to see if rollout is progressing or stuck.

5. Describe node <node-name> to verify node availability and conditions for nodes where DaemonSet pods should be scheduled.

6. Describe PodDisruptionBudget resources in namespace <namespace> to check for constraints that may prevent pod termination.

## Diagnosis

1. Analyze DaemonSet events from Playbook to identify the rollout blocker. Events showing "FailedCreate" indicate pod creation issues. Events showing "FailedScheduling" indicate resource or placement constraints. Events showing "FailedDelete" indicate pods cannot be terminated to make room for new ones.

2. If events indicate pod creation failures on specific nodes, check those nodes' available resources and conditions. DaemonSets using RollingUpdate strategy must terminate old pods before creating new ones on the same node. If the new pod has higher resource requests, it may not fit alongside other workloads.

3. If events indicate scheduling failures (InsufficientCPU, InsufficientMemory), the new DaemonSet pod template requires more resources than available on target nodes. Compare new pod resource requests with node allocatable resources minus existing pod requests.

4. If events indicate pods stuck in Terminating state, check for finalizers on the old pods or PodDisruptionBudget constraints preventing eviction. DaemonSets with maxUnavailable=1 cannot proceed if even one pod termination is blocked.

5. If pods are created but not becoming Ready, analyze pod logs and container status from Playbook. The rollout waits for new pods to become Ready before terminating the next old pod. Readiness probe failures or application startup issues block the rollout.

6. If events show node-related issues (NodeNotReady, node taints), verify node conditions and taints match DaemonSet tolerations. New taints added during rollout may prevent new pods from scheduling even though old pods were running.

7. If no clear event pattern exists, check the DaemonSet's updateStrategy configuration. Verify maxUnavailable and maxSurge settings allow pods to be replaced. Also verify if any PodDisruptionBudget in the namespace is blocking pod evictions required for the update.
