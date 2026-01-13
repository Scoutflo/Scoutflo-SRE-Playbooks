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

1. Retrieve the PersistentVolumeClaim `<pvc-name>` in namespace `<namespace>` and inspect its status, conditions, and resize requests to verify if resize is pending or failed.

2. Retrieve the StorageClass referenced by the PVC and verify if volume expansion is enabled in the StorageClass configuration.

3. Retrieve the PersistentVolume bound to the PVC and inspect its status and capacity to verify current volume size.

4. List events in namespace `<namespace>` and filter for volume-related events, focusing on events with reasons such as `VolumeResizeFailed` or messages indicating resize failures.

5. Check the volume expansion controller pod status in the kube-system namespace to verify if the controller is running and processing resize requests.

6. Verify if the storage backend (e.g., cloud provider storage) supports volume expansion by checking storage provider documentation or capabilities.

## Diagnosis

1. Compare the volume resize failure timestamps with StorageClass modification timestamps, and check whether `allowVolumeExpansion` was set to false or removed within 30 minutes before resize failures.

2. Compare the volume resize failure timestamps with PVC resize request timestamps, and check whether resize requests were made but not processed within 30 minutes before failures.

3. Compare the volume resize failure timestamps with volume expansion controller restart or failure timestamps, and check whether controller issues occurred within 5 minutes before resize failures.

4. Compare the volume resize failure timestamps with storage backend unavailability or API error timestamps, and check whether storage provider issues occurred within 10 minutes before resize failures.

5. Compare the volume resize failure timestamps with PersistentVolume status change timestamps, and check whether volume state changes occurred within 30 minutes before resize failures.

6. Compare the volume resize failure timestamps with cluster upgrade or storage plugin update timestamps, and check whether infrastructure changes occurred within 1 hour before resize failures, affecting volume expansion capabilities.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review volume expansion controller logs for gradual processing issues, check for intermittent storage backend connectivity problems, examine if StorageClass configurations drifted over time, verify if storage provider capabilities changed gradually, and check for volume expansion quota or limit issues that may have accumulated. Volume resize failures may result from gradual storage infrastructure or configuration issues rather than immediate changes.

