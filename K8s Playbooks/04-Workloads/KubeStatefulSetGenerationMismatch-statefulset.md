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

1. Describe StatefulSet <statefulset-name> in namespace <namespace> to see:
   - Observed generation versus desired generation
   - Replicas status (desired/current/ready)
   - Update strategy configuration
   - Conditions showing why generation mismatch exists
   - Events showing Failed, ProgressDeadlineExceeded, or PodCreateError errors

2. Retrieve events for StatefulSet <statefulset-name> in namespace <namespace> sorted by timestamp to see the sequence of generation mismatch issues.

3. Retrieve rollout history for StatefulSet <statefulset-name> in namespace <namespace> to identify recent updates or rollbacks that may have caused the mismatch.

4. List pods belonging to StatefulSet in namespace <namespace> with label app=<statefulset-label> and describe pods to identify pods in failed or error states.

5. List PersistentVolumeClaim resources in namespace <namespace> with label app=<statefulset-label> and describe PVCs to verify volume binding and availability.

6. Retrieve StatefulSet <statefulset-name> configuration in namespace <namespace> and check update strategy to identify update blockers.

## Diagnosis

1. Analyze StatefulSet events from Playbook to identify why the controller cannot reconcile to the desired generation. Events showing "FailedCreate" or "FailedScheduling" indicate the controller is attempting to update pods but encountering blockers. Events showing "ProgressDeadlineExceeded" indicate the update has stalled beyond acceptable time.

2. If events indicate pod creation failures (FailedCreate, PodCreateError), the controller cannot create new pods for the updated generation. Check PVC binding status and resource quota availability in the namespace. StatefulSets require successful PVC binding before pod creation.

3. If events indicate scheduling failures, the new pods cannot be placed on nodes. Compare resource requests in the updated pod template with available node capacity. Verify that node selectors and tolerations in the new spec match available nodes.

4. If rollout history from Playbook shows a recent update or rollback, verify whether the update strategy allows the rollout to proceed. Check the partition field in updateStrategy - a non-zero partition intentionally prevents some pods from updating, which may appear as a generation mismatch.

5. If pods exist but are not transitioning to the new revision, check if pods are stuck in termination or if the update strategy is waiting for pods to become Ready before proceeding. StatefulSets with OrderedReady strategy update pods one at a time, waiting for each to be Ready.

6. If events indicate resource quota exceeded (Forbidden, exceeded quota), the namespace quota prevents creating new pods. Check ResourceQuota status and current usage against limits.

7. If no clear event pattern exists, compare observed generation with metadata generation in the StatefulSet spec. A persistent mismatch indicates the StatefulSet controller is unable to process the spec change. Check kube-controller-manager logs for StatefulSet controller errors.
