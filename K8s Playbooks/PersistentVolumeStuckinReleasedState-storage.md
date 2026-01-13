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

1. List PersistentVolumes and filter for volumes with status `Released` to identify all stuck volumes.

2. Retrieve the PersistentVolume `<pv-name>` and inspect its status, phase, reclaim policy, and claim reference to understand why it is stuck in Released state.

3. Check if the PersistentVolumeClaim that was previously bound to the volume still exists or was deleted.

4. Retrieve the PersistentVolume `<pv-name>` and inspect its persistent volume reclaim policy to verify if it is set to `Retain`, `Delete`, or `Recycle`.

5. List events related to the PersistentVolume and filter for volume release or deletion events to identify any errors preventing release.

6. Check the storage backend to verify if the underlying storage resource can be released or if backend issues are preventing cleanup.

## Diagnosis

1. Compare the PersistentVolume Released state timestamps with PersistentVolumeClaim deletion timestamps, and check whether PVCs were deleted within 30 minutes before volumes entered Released state.

2. Compare the PersistentVolume Released state timestamps with PersistentVolume reclaim policy modification timestamps, and check whether reclaim policy changes occurred within 30 minutes before volumes became stuck.

3. Compare the PersistentVolume Released state timestamps with storage backend unavailability or API error timestamps, and check whether storage provider issues occurred within 10 minutes before volumes became stuck.

4. Compare the PersistentVolume Released state timestamps with volume finalizer addition timestamps, and check whether finalizers were added within 30 minutes before volumes became stuck, preventing cleanup.

5. Compare the PersistentVolume Released state timestamps with cluster storage plugin restart or failure timestamps, and check whether storage infrastructure issues occurred within 1 hour before volumes became stuck.

6. Compare the PersistentVolume Released state timestamps with PersistentVolume deletion attempt failure timestamps, and check whether deletion attempts failed within 30 minutes before volumes became stuck.

**If no correlation is found within the specified time windows**: Extend the search window (10 minutes → 30 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review storage plugin logs for gradual volume cleanup issues, check for intermittent storage backend connectivity problems, examine if reclaim policies were always set to Retain but only recently enforced, verify if storage provider capabilities changed gradually, and check for volume finalizer processing issues that may have accumulated. PersistentVolume Released state issues may result from gradual storage infrastructure or policy configuration rather than immediate changes.

