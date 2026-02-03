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

1. Describe StatefulSet <statefulset-name> in namespace <namespace> to see:
   - Update status, current revision, and update revision
   - Update strategy configuration
   - Conditions showing why update is not rolled out
   - Events showing FailedCreate, FailedScheduling, or FailedAttachVolume errors

2. Retrieve events for StatefulSet <statefulset-name> in namespace <namespace> sorted by timestamp to see the sequence of update rollout issues.

3. Check rollout status for StatefulSet <statefulset-name> in namespace <namespace> to see if update is progressing or stuck.

4. List pods belonging to StatefulSet in namespace <namespace> with label app=<statefulset-label> and describe pods to identify pods in Pending or Terminating states.

5. Retrieve StatefulSet <statefulset-name> configuration in namespace <namespace> and verify resource requests, node selectors, tolerations, and affinity rules.

6. List PersistentVolumeClaim resources in namespace <namespace> with label app=<statefulset-label> and describe PVCs to verify volume availability.

## Diagnosis

1. Analyze StatefulSet events from Playbook to identify the rollout blocker. Events showing "FailedCreate" indicate PVC provisioning or pod creation issues. Events showing "FailedScheduling" indicate node resource or affinity constraints. Events showing "FailedAttachVolume" indicate storage backend problems.

2. If events indicate PVC issues (FailedCreate with volume-related messages), verify PVC status for the pending pod ordinal. StatefulSets create PVCs sequentially and wait for each PVC to be bound before creating the corresponding pod. Check if the StorageClass can provision volumes in the required zone.

3. If events indicate scheduling failures (FailedScheduling, InsufficientCPU, InsufficientMemory), correlate with node capacity from Playbook. Verify whether pod resource requests exceed available node capacity or if node selectors/affinity rules exclude all available nodes.

4. If events indicate pod readiness issues (pod created but not becoming Ready), analyze the pod that is blocking the rollout. StatefulSets use OrderedReady update strategy by default, so a single unhealthy pod blocks the entire rollout. Check pod logs and readiness probe configuration.

5. If events indicate pod termination issues (pods stuck in Terminating state), check for finalizers preventing deletion or PodDisruptionBudget constraints blocking termination of the old pod revision.

6. If events indicate volume attachment failures (FailedAttachVolume, VolumeNotFound), verify that the PersistentVolume exists and is accessible from the node where the pod is scheduled. Check storage backend connectivity and volume zone alignment with node zones.

7. If no clear event pattern exists, compare the StatefulSet's current revision with update revision from Playbook. If revisions differ, the controller is attempting to update but pods are not transitioning. Check partition settings in the update strategy that may be intentionally holding back the rollout.
