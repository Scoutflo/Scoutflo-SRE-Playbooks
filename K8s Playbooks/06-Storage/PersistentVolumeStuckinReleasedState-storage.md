---
title: PersistentVolume Stuck in Released State - Storage
weight: 285
categories:
  - kubernetes
  - storage
---

# PersistentVolumeStuckinReleasedState-storage

## Meaning

PersistentVolumes are stuck in Released state (triggering KubePersistentVolumeNotReady alerts) because the bound PersistentVolumeClaim was deleted but the volume's persistentVolumeReclaimPolicy is set to Retain preventing automatic deletion, or the storage backend (CSI driver, cloud provider) cannot release the volume due to backend issues. PersistentVolumes show Released phase in kubectl, persistent volume reclaim policy may show Retain, and storage backend may indicate unavailability. This affects the storage plane and blocks storage resources, typically caused by Retain reclaim policy or storage backend issues; PersistentVolumeClaim binding may fail if volumes are needed.

## Impact

PersistentVolumes remain in Released state indefinitely; storage resources are not released; volumes cannot be reused; new PVCs may fail to bind if volumes are needed; storage capacity is wasted; KubePersistentVolumeNotReady alerts fire when volumes are in Released state; volume cleanup is blocked; cluster storage management is impaired; volume status shows Released phase; storage backend resources remain allocated. PersistentVolumes show Released phase indefinitely; persistent volume reclaim policy may show Retain; PersistentVolumeClaim binding may fail if volumes are needed; storage capacity is wasted and cluster storage management is impaired.

## Playbook

1. Describe PersistentVolume <pv-name> to inspect the volume status, phase, reclaim policy, claim reference, and finalizers to understand why it is stuck in Released state.

2. Retrieve events for PersistentVolume <pv-name> sorted by timestamp to identify events related to volume release or deletion, including any errors preventing cleanup.

3. List all PersistentVolumes with status Released to identify all stuck volumes in the cluster.

4. Check if the PersistentVolumeClaim that was previously bound to the volume still exists or was deleted.

5. Verify the PersistentVolume reclaim policy to check if it is set to Retain, Delete, or Recycle.

6. Check the storage backend to verify if the underlying storage resource can be released or if backend issues are preventing cleanup.

7. Check for orphaned storage resources in the cloud provider that may need manual cleanup.

## Diagnosis

1. Analyze PV events from Playbook step 2 to identify why the volume is stuck in Released state. Events may show:
   - No cleanup events - Indicates Retain reclaim policy is working as designed (not an error)
   - "VolumeFailedDelete" - Storage backend cannot delete the underlying resource
   - Finalizer-related events - External controllers are blocking cleanup

2. Check the reclaim policy from Playbook step 5. If persistentVolumeReclaimPolicy is "Retain", the Released state is expected behavior after PVC deletion:
   - If Retain was intentional (for data protection), the volume requires manual cleanup or reconfiguration
   - If Retain was unintentional, the reclaim policy should be changed before PVC deletion in the future

3. If reclaim policy is "Delete" but the volume is stuck, examine PV events from step 2 for storage backend errors. The CSI driver or storage provisioner cannot delete the underlying storage resource. Check if:
   - The storage backend resource still exists (step 6)
   - The storage backend is accessible (step 6)
   - The CSI driver/provisioner has permissions to delete resources

4. If the PV description from Playbook step 1 shows finalizers, identify which controller owns the finalizer. A stuck finalizer prevents the volume from being cleaned up even with Delete policy.

5. If the previously bound PVC from Playbook step 4 still exists but is not bound to this PV, there may be a claimRef mismatch. The PV thinks the claim was deleted, but the PVC exists in a different state.

6. If cloud provider orphaned resources exist from step 7, the PV was partially cleaned up but the backend resource remains. This requires manual cleanup in the cloud provider console.

**If no correlation is found within the specified time windows**: Extend the search window (10 minutes → 30 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review storage plugin logs for gradual volume cleanup issues, check for intermittent storage backend connectivity problems, examine if reclaim policies were always set to Retain but only recently enforced, verify if storage provider capabilities changed gradually, and check for volume finalizer processing issues that may have accumulated. PersistentVolume Released state issues may result from gradual storage infrastructure or policy configuration rather than immediate changes.

