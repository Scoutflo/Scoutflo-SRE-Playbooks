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

1. Retrieve the DaemonSet `<daemonset-name>` in namespace `<namespace>` and inspect its status to check number scheduled versus desired number scheduled and identify the mismatch.

2. Retrieve the Pod `<pod-name>` in namespace `<namespace>` belonging to the DaemonSet `<daemonset-name>` and check pod status to identify pods in Pending state.

3. Retrieve events for the Pod `<pod-name>` in namespace `<namespace>` and filter for scheduling error patterns including 'FailedScheduling', 'InsufficientCPU', 'InsufficientMemory', 'Unschedulable' to identify scheduling blockers.

4. Retrieve the DaemonSet `<daemonset-name>` in namespace `<namespace>` and check DaemonSet pod template parameters including resource requests, node selectors, tolerations, and affinity rules to verify configuration issues.

5. Retrieve the Node `<node-name>` resources and verify node availability and conditions for nodes where DaemonSet pods should be scheduled.

6. Retrieve the Node `<node-name>` resources and check node taints and verify compatibility with DaemonSet tolerations to identify taint/toleration mismatches.

## Diagnosis

Compare DaemonSet scheduling failure timestamps with node taint or label change timestamps within 10 minutes and verify whether scheduling failures began after node configuration changes, using node taint/label history and pod scheduling events as supporting evidence.

Correlate DaemonSet scheduling failures with DaemonSet configuration change timestamps within 30 minutes and verify whether scheduling failures began after DaemonSet template updates, using DaemonSet modification history and pod scheduling events as supporting evidence.

Analyze pod scheduling failure patterns over the last 15 minutes to determine if failures are due to resource constraints, node availability, or configuration mismatches, using pod events and node conditions as supporting evidence.

Compare DaemonSet pod resource requests with node available resources at scheduling failure times and verify whether resource constraints prevented scheduling, using node metrics and pod resource specifications as supporting evidence.

Correlate DaemonSet scheduling failures with node condition transitions within 5 minutes and verify whether node NotReady or resource pressure conditions prevented scheduling, using node conditions and pod scheduling events as supporting evidence.

Compare DaemonSet toleration configurations with node taint configurations and verify whether missing or incorrect tolerations prevented pods from scheduling on tainted nodes, using DaemonSet tolerations and node taints as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 1 hour for configuration changes, review DaemonSet selector and toleration configurations, check for persistent resource constraints, verify node feature discovery label changes, examine historical DaemonSet scheduling patterns. DaemonSet scheduling failures may result from configuration mismatches, persistent resource constraints, or node pool changes rather than immediate changes.
