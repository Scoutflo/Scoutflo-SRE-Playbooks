---
title: Pod Cannot Access PersistentVolume - Storage
weight: 260
categories:
  - kubernetes
  - storage
---

# PodCannotAccessPersistentVolume-storage

## Meaning

Pods cannot access PersistentVolumes (triggering KubePodPending or storage-related alerts) because PersistentVolumeClaims are not bound, volumes cannot be attached, volume mount failures occur, storage classes are misconfigured, or the storage backend is unavailable. Pods show Pending or ContainerCreating state, PersistentVolumeClaim resources show unbound status, and pod events show FailedMount or FailedAttachVolume errors. This affects the storage plane and prevents applications from accessing persistent storage, typically caused by PersistentVolumeClaim binding failures, storage class issues, or storage backend unavailability; PersistentVolumeClaim binding failures may block pod creation.

## Impact

Pods cannot start; persistent storage is unavailable; volume mount failures occur; pods remain in Pending or ContainerCreating state; KubePodPending alerts fire; PersistentVolumeClaims remain unbound; applications cannot access data; stateful workloads fail to start; database pods cannot mount data volumes. Pods show Pending or ContainerCreating state indefinitely; PersistentVolumeClaim resources show unbound status; PersistentVolumeClaim binding failures may prevent pod creation; applications cannot access data and may show errors.

## Playbook

1. Describe PersistentVolumeClaim <pvc-name> in namespace <namespace> to inspect the PVC status, phase, conditions, and verify if it is bound to a PersistentVolume.

2. Retrieve events for PersistentVolumeClaim <pvc-name> in namespace <namespace> sorted by timestamp to identify binding failures or provisioning issues.

3. Describe pod <pod-name> in namespace <namespace> to inspect pod volume configuration and identify which PersistentVolumeClaim is referenced.

4. Retrieve events for pod <pod-name> in namespace <namespace> sorted by timestamp to identify FailedMount, FailedAttachVolume, or volume attachment failures.

5. Describe PersistentVolume <pv-name> to inspect the bound volume status, phase, and access modes to verify volume availability.

6. Describe the StorageClass referenced by the PVC and verify it exists and the provisioner is available.

7. Describe the node where the pod is scheduled to check volume attachment status and verify if the volume can be attached to the node.

## Diagnosis

1. Analyze pod events from Playbook step 4 to identify the specific volume access failure type. The event reason indicates the failure point:
   - "FailedMount" - Volume exists but cannot be mounted (permission, filesystem, or node issue)
   - "FailedAttachVolume" - Volume cannot be attached to the node (CSI driver or backend issue)
   - "FailedScheduling" with volume-related message - No node can satisfy volume requirements

2. If events show FailedMount or FailedAttachVolume, check the PVC status from Playbook step 1. If PVC phase is not "Bound", the volume binding is the root cause:
   - If PVC is Pending, follow PVC Pending diagnosis (check StorageClass from step 6)
   - If PVC is Lost, the underlying PV is no longer available (check PV from step 5)

3. If PVC is Bound but pod still shows volume errors, examine PVC events from Playbook step 2. Events may show:
   - "WaitForFirstConsumer" - Normal for certain binding modes, pod scheduling will trigger binding
   - "ProvisioningFailed" - Storage backend cannot create the volume
   - Access mode conflicts - PV access mode does not match pod requirements

4. If PVC and PV appear healthy from steps 1-5, check the node status from Playbook step 7. If the node shows volume attachment limits reached or storage-related conditions, the pod cannot attach more volumes to that node.

5. If the StorageClass from step 6 is missing or misconfigured, correlate when the StorageClass was modified/deleted with when pods started failing to access volumes.

6. If all Kubernetes resources appear correct, the issue is at the storage backend level. Check if the PV's volumeHandle or storage path (from step 5) still exists and is accessible from the scheduled node.

**If no correlation is found within the specified time windows**: Extend the search window (10 minutes → 30 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review storage plugin logs for gradual volume provisioning issues, check for intermittent storage backend connectivity problems, examine if storage class configurations drifted over time, verify if volume attachment limits accumulated gradually, and check for storage provider quota or capacity issues that may have developed. Volume access failures may result from gradual storage infrastructure degradation rather than immediate changes.

