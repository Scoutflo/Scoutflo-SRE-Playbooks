---
title: PersistentVolume Not Resizing - Storage
weight: 297
categories:
  - kubernetes
  - storage
---

# PersistentVolumeNotResizing-storage

## Meaning

PersistentVolumes are not resizing when PersistentVolumeClaims are expanded (triggering KubePersistentVolumeFillingUp or KubePersistentVolumeNotReady alerts) because the StorageClass does not have allowVolumeExpansion set to true, the storage backend (CSI driver, cloud provider) does not support resizing, the volume expansion controller pods are not functioning in kube-system namespace, or the PVC resize request is not being processed by the storage provisioner. PersistentVolumeClaim resources show resize pending or failed conditions, StorageClass may show allowVolumeExpansion set to false, and volume expansion controller pods may show failures. This affects the storage plane and limits application growth, typically caused by StorageClass configuration or storage backend limitations; applications may run out of disk space.

## Impact

Volume capacity cannot be increased; PVC resize requests are not applied; applications run out of disk space; persistent storage cannot grow; KubePersistentVolumeFillingUp alerts fire when volumes approach capacity limits; KubePersistentVolumeNotReady alerts fire when volume expansion fails; volume expansion fails with errors; storage capacity constraints limit application growth; database pods cannot expand data volumes; PVC status shows resize pending or failed conditions. PersistentVolumeClaim resources show resize pending or failed conditions indefinitely; StorageClass may show allowVolumeExpansion set to false; applications may run out of disk space and may show errors; persistent storage cannot grow.

## Playbook

1. Describe PersistentVolumeClaim <pvc-name> in namespace <namespace> to inspect the PVC status, conditions, resize requests, and verify if resize is pending or failed.

2. Retrieve events for PersistentVolumeClaim <pvc-name> in namespace <namespace> sorted by timestamp to identify VolumeResizeFailed or FileSystemResizePending events.

3. Describe PersistentVolume <pv-name> to inspect the bound volume status, capacity, and verify current volume size.

4. Retrieve events for PersistentVolume <pv-name> sorted by timestamp to identify resize status events.

5. Describe the StorageClass referenced by the PVC and verify if allowVolumeExpansion is set to true in the StorageClass configuration.

6. List pods in the kube-system namespace and check the volume expansion controller pod status to verify if the controller is running and processing resize requests.

7. Verify if the storage backend (e.g., cloud provider storage) supports volume expansion by checking storage provider documentation or capabilities.

## Diagnosis

1. Analyze PVC events from Playbook step 2 to identify the specific resize failure reason. Events will indicate the failure point:
   - "VolumeResizeFailed" - Storage backend cannot expand the volume
   - "FileSystemResizePending" - Volume expanded but filesystem resize requires pod restart
   - No resize events - Resize request was not processed by the controller

2. If events show "FileSystemResizePending", the volume backend expansion succeeded but the filesystem needs to be resized. This typically requires:
   - Restarting the pod using the volume (for online resize-capable storage)
   - Detaching and reattaching the volume (for offline resize)
   This is not a failure but a pending operation from Playbook step 1 conditions.

3. If events show "VolumeResizeFailed" or no resize events, check the StorageClass from Playbook step 5. If allowVolumeExpansion is false or not set, the StorageClass does not permit volume expansion. This is a configuration limitation, not a runtime error.

4. If StorageClass allows expansion but resize still fails, check the storage backend capability from Playbook step 7. Not all storage backends support online expansion, and some have minimum/maximum size constraints.

5. If StorageClass and backend support expansion, check the volume expansion controller pods from Playbook step 6. If controller pods are not Running or show errors, the resize request cannot be processed. Correlate controller pod restarts with when resize requests were submitted.

6. If PV events from Playbook step 4 show resize activity but PVC still shows pending, compare the PV capacity (step 3) with the PVC requested capacity (step 1). If PV shows the new size but PVC does not, there may be a controller synchronization issue.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review volume expansion controller logs for gradual processing issues, check for intermittent storage backend connectivity problems, examine if StorageClass configurations drifted over time, verify if storage provider capabilities changed gradually, and check for volume expansion quota or limit issues that may have accumulated. Volume resize failures may result from gradual storage infrastructure or configuration issues rather than immediate changes.

