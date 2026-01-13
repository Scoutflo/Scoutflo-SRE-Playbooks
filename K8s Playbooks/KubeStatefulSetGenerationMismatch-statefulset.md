---
title: Kube StatefulSet Generation Mismatch
weight: 20
---

# KubeStatefulSetGenerationMismatch

## Meaning

StatefulSet generation mismatch due to possible rollback or failed update (triggering alerts related to StatefulSet generation issues) because the observed generation does not match the desired generation, indicating that a StatefulSet update or rollback operation has not completed successfully. StatefulSets show generation mismatches in kubectl, StatefulSet events show Failed, ProgressDeadlineExceeded, or PodCreateError errors, and pods may show failed or error states. This affects the workload plane and indicates StatefulSet reconciliation failures or update problems, typically caused by persistent resource constraints, volume zone issues, or cluster capacity limitations; PersistentVolumeClaim binding failures may prevent generation updates.

## Impact

KubeStatefulSetGenerationMismatch alerts fire; service degradation or unavailability; StatefulSet cannot achieve desired state; generation mismatch prevents proper reconciliation; StatefulSet update or rollback is stuck; StatefulSet status shows generation mismatch; controllers cannot reconcile StatefulSet state; StatefulSet reconciliation operations fail. StatefulSets show generation mismatches indefinitely; StatefulSet events show Failed or ProgressDeadlineExceeded errors; PersistentVolumeClaim binding failures may prevent pod creation; applications run with outdated configurations and may experience errors or performance degradation.

## Playbook

1. Retrieve the StatefulSet `<statefulset-name>` in namespace `<namespace>` and inspect its status to check observed generation versus desired generation and identify the mismatch.

2. Retrieve rollout history for the StatefulSet `<statefulset-name>` in namespace `<namespace>` to identify recent updates or rollbacks that may have caused the mismatch.

3. Retrieve events for the StatefulSet `<statefulset-name>` in namespace `<namespace>` and filter for error patterns including 'Failed', 'ProgressDeadlineExceeded', 'PodCreateError' to identify StatefulSet issues.

4. Retrieve the Pod `<pod-name>` in namespace `<namespace>` belonging to the StatefulSet `<statefulset-name>` and check pod status to identify pods in failed or error states.

5. Retrieve PersistentVolumeClaim resources belonging to StatefulSet pods and check PersistentVolumeClaim status to verify volume binding and availability.

6. Retrieve the StatefulSet `<statefulset-name>` in namespace `<namespace>` and verify StatefulSet update strategy and check if rollout is paused to identify update blockers.

## Diagnosis

Compare StatefulSet generation mismatch detection timestamps with StatefulSet update or rollback initiation times within 30 minutes and verify whether generation mismatch began when update or rollback started, using StatefulSet events and rollout history as supporting evidence.

Correlate StatefulSet generation mismatch with pod creation failure timestamps within 30 minutes and verify whether pod creation failures prevented generation update, using pod events and StatefulSet status as supporting evidence.

Compare StatefulSet generation mismatch with PersistentVolume binding failure timestamps within 10 minutes and verify whether volume binding failures prevented StatefulSet from achieving desired generation, using PVC events and StatefulSet pod status as supporting evidence.

Analyze StatefulSet generation mismatch patterns over the last 1 hour to determine if mismatch is persistent (reconciliation failure) or transient (update in progress), using StatefulSet status history and pod status as supporting evidence.

Correlate StatefulSet generation mismatch with resource quota exhaustion timestamps within 30 minutes and verify whether quota limits prevented pod creation, using resource quota status and StatefulSet events as supporting evidence.

Compare StatefulSet generation mismatch with node capacity exhaustion timestamps within 30 minutes and verify whether insufficient cluster capacity prevented StatefulSet from achieving desired generation, using node metrics and StatefulSet scaling attempts as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 1 hour for StatefulSet operations, review StatefulSet update strategy configuration, check for persistent resource constraints, verify PersistentVolume availability and zone configurations, examine historical StatefulSet generation patterns. StatefulSet generation mismatch may result from persistent resource constraints, volume zone issues, or cluster capacity limitations rather than immediate changes.
