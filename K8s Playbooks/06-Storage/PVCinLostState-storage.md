---
title: PVC in Lost State - Storage
weight: 217
categories:
  - kubernetes
  - storage
---

# PVCinLostState-storage

## Meaning

PersistentVolumeClaims are in Lost state (triggering KubePersistentVolumeNotReady alerts) because the underlying PersistentVolume or storage backend is unavailable, the volume was deleted from the storage provider, or the storage connection is broken. PersistentVolumeClaim resources show Lost phase in kubectl, PersistentVolume may show Failed or Released state, and pod events show VolumeLost or storage backend unavailability errors. This affects the storage plane and prevents pods from accessing persistent storage, typically caused by storage backend unavailability or volume deletion; PersistentVolumeClaim binding failures may block pod creation.

## Impact

PersistentVolumeClaims are in Lost state; pods cannot access persistent storage; volume mounts fail; applications cannot access data; KubePersistentVolumeNotReady alerts fire; stateful workloads fail; database pods cannot mount volumes; persistent data is inaccessible; storage-dependent services are unavailable. PersistentVolumeClaim resources show Lost phase indefinitely; PersistentVolume may show Failed or Released state; PersistentVolumeClaim binding failures may prevent pod creation; applications cannot access data and may show errors.

## Playbook

1. Describe PersistentVolumeClaim <pvc-name> in namespace <namespace> to inspect the PVC status, phase, conditions, and identify the cause of the Lost state.

2. Retrieve events for PersistentVolumeClaim <pvc-name> in namespace <namespace> sorted by timestamp to identify VolumeLost or storage backend unavailability errors.

3. Describe PersistentVolume <pv-name> to inspect the bound volume status, phase, and storage backend information to verify if the volume exists and is accessible.

4. Retrieve events for PersistentVolume <pv-name> sorted by timestamp to identify backend connectivity issues.

5. Check the storage backend (e.g., cloud provider storage, NFS server) to verify if the underlying storage resource exists and is accessible.

6. Describe the StorageClass referenced by the PVC and verify if the storage provisioner is available and functioning.

7. List pods using the PVC and inspect their status to verify if volume mount failures are occurring.

## Diagnosis

1. Analyze PVC events from Playbook step 2 to identify the specific reason for the Lost state. Events showing "VolumeLost" or "VolumeNotFound" indicate the underlying storage resource is no longer accessible. The event message typically contains the specific error from the storage backend.

2. If events indicate volume not found, examine the PersistentVolume status from Playbook step 3. If the PV shows Failed or Released state, or if the PV no longer exists, the underlying storage was deleted or became inaccessible:
   - If PV is in Released state with Retain policy, the previous PVC was deleted but the volume data still exists
   - If PV is in Failed state, the storage backend reported an error
   - If PV does not exist, it was deleted (manually or by Delete reclaim policy)

3. If PV events from Playbook step 4 show backend connectivity errors, the storage backend (NFS server, cloud storage, etc.) is unreachable. Check the storage backend status from step 5 to confirm availability.

4. If PV exists and appears healthy from steps 3-4, but PVC is still Lost, check the claimRef field in the PV. If claimRef points to a different or non-existent PVC, there is a binding mismatch.

5. If the StorageClass provisioner from Playbook step 6 shows issues, correlate provisioner problems with when the PVC entered Lost state. A failing provisioner cannot maintain volume bindings properly.

6. If pods using the PVC from Playbook step 7 show repeated mount failures before the Lost state, the issue may have started as intermittent connectivity that degraded to complete failure. Check if pod mount failure timestamps precede the PVC Lost state.

**If no correlation is found within the specified time windows**: Extend the search window (10 minutes → 30 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review storage plugin logs for gradual volume connectivity issues, check for intermittent storage backend availability problems, examine if storage resources were gradually deleted or migrated, verify if storage provider connections degraded over time, and check for storage backend quota or capacity issues that may have caused resource removal. PVC Lost state may result from gradual storage infrastructure degradation rather than immediate deletions.

