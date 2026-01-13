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

1. Retrieve the DaemonSet `<daemonset-name>` in namespace `<namespace>` and inspect its status to check rollout status, desired number scheduled, and number ready to verify rollout progress.

2. Retrieve the Pod `<pod-name>` in namespace `<namespace>` belonging to the DaemonSet `<daemonset-name>` and check pod status to identify pods in Pending or Terminating states.

3. Retrieve events for the DaemonSet `<daemonset-name>` in namespace `<namespace>` and filter for error patterns including 'FailedCreate', 'FailedScheduling', 'FailedDelete' to identify rollout blockers.

4. Retrieve the DaemonSet `<daemonset-name>` in namespace `<namespace>` and check pod template parameters including resource requests, node selectors, tolerations, affinity rules, and pod priority class to verify configuration issues.

5. Retrieve the Node `<node-name>` resources and verify node availability and conditions for nodes where DaemonSet pods should be scheduled.

6. Retrieve PodDisruptionBudget resources and check for pod disruption budget constraints that may prevent pod termination.

## Diagnosis

Compare DaemonSet update initiation timestamps with pod scheduling failure timestamps within 30 minutes and verify whether rollout became stuck immediately after update started, using DaemonSet events and pod scheduling events as supporting evidence.

Correlate stuck pod timestamps with node condition transitions within 5 minutes and verify whether pods cannot be scheduled due to node resource pressure or NotReady conditions, using node conditions and pod scheduling events as supporting evidence.

Analyze pod termination duration for old DaemonSet pods over the last 15 minutes to determine if termination grace period is too long or pods are stuck terminating, using pod status and termination timestamps as supporting evidence.

Compare new pod resource requests with node available resources at scheduling failure times and verify whether resource constraints prevent new pod scheduling, using node metrics and pod resource specifications as supporting evidence.

Correlate DaemonSet rollout stuck detection with node taint or label change timestamps within 10 minutes and verify whether node configuration changes prevented pod scheduling, using node taints, labels, and pod toleration/selector configurations as supporting evidence.

Compare DaemonSet pod priority with other pod priorities on affected nodes and verify whether higher priority pods preempted DaemonSet pods, using pod priority classes and node pod distributions as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 1 hour for infrastructure changes, review DaemonSet update strategy configuration, check for cluster autoscaler issues, verify pod disruption budget settings, examine historical DaemonSet rollout patterns. DaemonSet rollout may be stuck due to persistent resource constraints, misconfigured affinity rules, or cluster capacity limitations rather than immediate changes.
