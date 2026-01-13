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

1. Retrieve the PersistentVolumeClaim `<pvc-name>` in namespace `<namespace>` and inspect its status, phase, and conditions to verify Lost state and identify the cause.

2. Retrieve the PersistentVolume bound to the PVC and inspect its status, phase, and storage backend information to verify if the volume exists and is accessible.

3. List events in namespace `<namespace>` and filter for volume-related events, focusing on events with reasons such as `VolumeLost` or messages indicating storage backend unavailability.

4. Check the storage backend (e.g., cloud provider storage, NFS server) to verify if the underlying storage resource exists and is accessible.

5. Retrieve the StorageClass referenced by the PVC and verify if the storage provisioner is available and functioning.

6. Check pods using the PVC and inspect their status to verify if volume mount failures are occurring.

## Diagnosis

1. Compare the PVC Lost state timestamps with PersistentVolume deletion timestamps, and check whether volumes were deleted within 30 minutes before PVCs entered Lost state.

2. Compare the PVC Lost state timestamps with storage backend unavailability or deletion timestamps, and check whether storage resources were removed within 30 minutes before PVCs became Lost.

3. Compare the PVC Lost state timestamps with storage backend connectivity failure timestamps, and check whether storage provider connection issues occurred within 10 minutes before PVCs became Lost.

4. Compare the PVC Lost state timestamps with PersistentVolume status change timestamps, and check whether volumes transitioned to Failed or Released state within 30 minutes before PVCs became Lost.

5. Compare the PVC Lost state timestamps with storage provisioner pod restart or failure timestamps, and check whether provisioner issues occurred within 5 minutes before PVCs became Lost.

6. Compare the PVC Lost state timestamps with cluster storage plugin restart or failure timestamps, and check whether storage infrastructure issues occurred within 1 hour before PVCs became Lost.

**If no correlation is found within the specified time windows**: Extend the search window (10 minutes → 30 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review storage plugin logs for gradual volume connectivity issues, check for intermittent storage backend availability problems, examine if storage resources were gradually deleted or migrated, verify if storage provider connections degraded over time, and check for storage backend quota or capacity issues that may have caused resource removal. PVC Lost state may result from gradual storage infrastructure degradation rather than immediate deletions.

