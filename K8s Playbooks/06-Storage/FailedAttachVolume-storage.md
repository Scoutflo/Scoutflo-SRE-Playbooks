---
title: Failed Attach Volume - Storage
weight: 227
categories:
  - kubernetes
  - storage
---

# FailedAttachVolume-storage

## Meaning

Kubernetes is unable to attach or mount a PersistentVolume to a pod (potentially related to KubePersistentVolumeFillingUp alerts if storage is full), usually because of PVC/PV binding problems, CSI or storage driver failures, node-to-storage connectivity issues, or storage provisioner errors. Volume attachment failures prevent pods from accessing persistent storage.

## Impact

Pods cannot start; applications requiring persistent storage fail; stateful workloads cannot access data; databases and storage-dependent services become unavailable; pods remain in Pending state; volume mount errors occur; PVC binding fails; storage provisioner errors; CSI driver communication issues.

## Playbook

1. Describe PersistentVolumeClaim <pvc-name> in namespace <namespace> to inspect the PVC status, phase, bound volume, storage class, and any conditions or events indicating why the volume cannot attach.

2. Retrieve events for PersistentVolumeClaim <pvc-name> in namespace <namespace> sorted by timestamp to identify FailedAttachVolume, ProvisioningFailed, or FailedMount errors.

3. Describe pod <pod-name> in namespace <namespace> to inspect pod volume definitions, status fields, and events to see which volumes are failing to attach or mount.

4. Retrieve events for pod <pod-name> in namespace <namespace> sorted by timestamp to identify pod-specific volume attachment failures.

5. Describe the StorageClass used by the PVC and list the corresponding storage provisioner pods in kube-system to ensure the CSI or provisioner components are running and healthy.

6. Describe node <node-name> where the pod is scheduled and inspect its conditions and labels to verify it is Ready and allowed to access the storage backend.

7. List VolumeAttachment objects relevant to the PVC or pod and verify that the CSI driver is reporting volumes as attached or identify specific errors.

8. Describe node <node-name> capacity fields (such as attachable volume limits) to confirm it has not exceeded the maximum number of attachable volumes for the storage provider.

9. List all VolumeAttachments in the cluster to check for orphaned volume attachments that may be blocking new attachments and compare with running pods.

## Diagnosis

1. Analyze pod events from Playbook step 4 to identify the specific attachment failure reason. The event message contains critical diagnostic information:
   - "Multi-Attach error" - Volume is already attached to another node (common with ReadWriteOnce volumes)
   - "attachment timeout" - CSI driver or storage backend is slow/unreachable
   - "volume not found" - The underlying storage resource does not exist
   - "permission denied" - Node lacks credentials to attach the volume

2. If events show "Multi-Attach error", the volume is attached to another node. Check VolumeAttachment objects from Playbook step 7:
   - If the previous pod was terminated but VolumeAttachment remains, the detachment is stuck
   - If the previous pod is still running on another node, this is expected behavior for RWO volumes
   - Compare with orphaned VolumeAttachments from step 9 to identify stuck attachments

3. If events show attachment timeout or CSI errors, check the storage provisioner pods from Playbook step 5. If CSI driver pods are not Running or show restarts, correlate restart timestamps with when attachment failures began.

4. If PVC events from Playbook step 2 show the PVC is not Bound, the attachment failure is a symptom of PVC binding issues. Follow PVC Pending diagnosis instead.

5. If node description from Playbook step 6 shows volume attachment limits reached (step 8), the node cannot attach more volumes. This is common with cloud providers that limit volumes per node (e.g., AWS limits EBS volumes per instance type).

6. If all components appear healthy, check VolumeAttachment objects from step 7 for the specific attachment status. If attachmentMetadata shows errors or attached=false with an error message, the storage backend is rejecting the attachment request.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 1 hour → 2 hours), review storage provisioner logs for earlier errors or warnings, check for gradual volume limit exhaustion, examine CSI driver health over a longer period, verify if storage backend connectivity issues developed gradually, and check node volume attachment limits that may have been reached earlier. Volume attachment failures may result from cumulative issues or storage backend problems not immediately visible.

