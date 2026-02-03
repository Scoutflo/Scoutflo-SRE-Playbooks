---
title: Kube Persistent Volume Errors
weight: 20
---

# KubePersistentVolumeErrors

## Meaning

PersistentVolume is experiencing provisioning or operational errors (triggering alerts related to PersistentVolume issues) because volume provisioning has failed, volume binding cannot complete, or the storage backend is experiencing problems. PersistentVolumes show Failed or Pending state in kubectl, volume events show FailedBinding, ProvisioningFailed, or VolumeFailed errors, and pods remain in Pending or ContainerCreating state waiting for volumes. This affects the storage plane and prevents pods from mounting required persistent storage, typically caused by storage backend failures, capacity exhaustion, or storage provider issues; PersistentVolumeClaim binding failures may block pod creation.

## Impact

PersistentVolume error alerts fire; volumes may be unavailable; pods cannot start due to missing volumes; data access failures occur; PersistentVolume errors appear in events; volume binding fails; PVC remains in Pending state; service degradation or unavailability; potential data loss or corruption if volume is corrupted; volume provisioning or binding operations fail completely. PersistentVolumes remain in Failed or Pending state indefinitely; PersistentVolumeClaim binding failures may prevent pod creation; applications cannot access data and may experience errors or performance degradation; volume provisioning or binding operations fail completely.

## Playbook

1. Describe PersistentVolume <pv-name> to inspect the volume status, phase, reclaim policy, storage class, claim reference, and any error messages indicating provisioning or operational errors.

2. Retrieve events for PersistentVolume <pv-name> sorted by timestamp to identify FailedBinding, ProvisioningFailed, VolumeFailed, and StorageClassNotFound errors.

3. Describe PersistentVolumeClaim <pvc-name> in namespace <namespace> to inspect the PVC status, phase, and binding status.

4. Retrieve events for PersistentVolumeClaim <pvc-name> in namespace <namespace> sorted by timestamp to identify binding or provisioning issues.

5. Describe StorageClass <storageclass-name> to verify if the storage class exists and is properly configured.

6. Retrieve storage provider logs for volume provisioning errors if storage provider logs are accessible to identify backend issues.

7. Check storage quotas in the cloud provider for namespace or cluster to verify if quotas are preventing volume creation.

8. List all PersistentVolumes not in Bound state to check for orphaned volumes in Released or Failed state that may indicate storage backend issues.

## Diagnosis

1. Analyze PV events from Playbook step 2 to identify the specific error type. The event reason indicates the failure category:
   - "FailedBinding" - No suitable PV available or PVC requirements cannot be satisfied
   - "ProvisioningFailed" - Storage backend cannot create the requested volume
   - "VolumeFailed" - Existing volume encountered an error
   - "StorageClassNotFound" - Referenced StorageClass does not exist

2. If events show "ProvisioningFailed", examine the error message for the specific backend failure:
   - Quota exceeded - Storage quota exhausted (check step 7)
   - Capacity unavailable - Storage backend has no capacity
   - Permission denied - Provisioner lacks credentials
   - Timeout - Storage backend is slow or unreachable

3. If events show "FailedBinding", check the PVC requirements from Playbook step 3-4 against available PVs from step 8:
   - Access mode mismatch (ReadWriteOnce vs ReadWriteMany)
   - Capacity mismatch (PVC requests more than available PVs offer)
   - StorageClass mismatch (PVC specifies a class with no matching PVs)
   - Node affinity conflicts (PV is restricted to nodes where pod cannot run)

4. If events show "StorageClassNotFound", verify the StorageClass exists from Playbook step 5. If the class was deleted or renamed, all PVCs referencing it will fail.

5. If error patterns from PV events are intermittent rather than consistent, the issue is likely storage backend instability rather than configuration. Check storage provider logs from step 6 for backend health issues.

6. If PVs in Released or Failed state exist from Playbook step 8, these orphaned volumes may indicate recurring provisioning/cleanup issues. Correlate the timestamps when these volumes entered error states with current PV error timestamps.

**If no correlation is found within the specified time windows**: Extend timeframes to 24 hours for storage system changes, review storage provider health status, check for storage backend capacity issues, verify storage class configurations, examine historical volume provisioning patterns. PersistentVolume errors may result from storage backend failures, capacity exhaustion, or storage provider issues rather than immediate configuration changes.
