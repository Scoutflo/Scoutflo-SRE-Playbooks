---
title: Kube StatefulSet Update Not RolledOut
weight: 20
---

# KubeStatefulSetUpdateNotRolledOut

## Meaning

StatefulSet update has not been rolled out (triggering alerts related to StatefulSet update issues) because the StatefulSet update process is stuck, paused, or cannot progress due to pod scheduling failures, resource constraints, or update strategy issues. StatefulSets show update status stuck, pods remain in Pending or Terminating state, and StatefulSet events show FailedCreate, FailedScheduling, or FailedAttachVolume errors. This affects the workload plane and indicates that StatefulSet updates are not completing, leaving pods running with outdated configurations, typically caused by persistent resource constraints, volume zone mismatches, or cluster capacity limitations; PersistentVolumeClaim binding failures may block update rollout.

## Impact

StatefulSet update alerts fire; service degradation or unavailability; StatefulSet update is stuck; old pods remain running with outdated configurations; new pods cannot be created or scheduled; StatefulSet desired state mismatch; update strategy cannot progress; system components may run with inconsistent versions. StatefulSets show update status stuck indefinitely; pods remain in Pending or Terminating state; PersistentVolumeClaim binding failures may prevent new pod creation; applications run with outdated configurations and may experience errors or performance degradation.

## Playbook

1. Retrieve the StatefulSet `<statefulset-name>` in namespace `<namespace>` and inspect its status to check update status, current revision, and update revision to verify update progress.

2. Retrieve the StatefulSet `<statefulset-name>` in namespace `<namespace>` and check if StatefulSet update was paused manually by examining StatefulSet status.

3. Retrieve the Pod `<pod-name>` in namespace `<namespace>` belonging to the StatefulSet `<statefulset-name>` and check pod status to identify pods in Pending or Terminating states.

4. Retrieve events for the StatefulSet `<statefulset-name>` in namespace `<namespace>` and filter for error patterns including 'FailedCreate', 'FailedScheduling', 'FailedAttachVolume' to identify update blockers.

5. Retrieve the StatefulSet `<statefulset-name>` in namespace `<namespace>` and check pod template parameters including resource requests, node selectors, tolerations, and affinity rules to verify configuration issues.

6. Retrieve PersistentVolumeClaim resources belonging to StatefulSet pods and verify PersistentVolumeClaim status to verify volume availability.

## Diagnosis

Compare StatefulSet update stuck detection timestamps with StatefulSet update initiation times within 30 minutes and verify whether update became stuck when update started, using StatefulSet events and update history as supporting evidence.

Correlate StatefulSet update stuck with pod scheduling failure timestamps within 30 minutes and verify whether pod scheduling failures prevented update rollout, using pod events and StatefulSet update status as supporting evidence.

Compare StatefulSet update stuck with PersistentVolume binding failure timestamps within 10 minutes and verify whether volume binding failures prevented new pod creation during update, using PVC events and StatefulSet pod status as supporting evidence.

Analyze StatefulSet update progress patterns over the last 1 hour to determine if update is completely stuck (resource issue) or progressing slowly (performance issue), using StatefulSet update status and pod creation events as supporting evidence.

Correlate StatefulSet update stuck with node capacity exhaustion timestamps within 30 minutes and verify whether insufficient cluster capacity prevented update rollout, using node metrics and StatefulSet scaling attempts as supporting evidence.

Compare StatefulSet update stuck with pod termination issues and verify whether old pods cannot terminate, blocking update progress, using pod termination events and StatefulSet update strategy as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 1 hour for StatefulSet operations, review StatefulSet update strategy configuration, check for persistent resource constraints, verify PersistentVolume availability, examine historical StatefulSet update patterns. StatefulSet update may be stuck due to persistent resource constraints, volume zone mismatches, or cluster capacity limitations rather than immediate changes.
