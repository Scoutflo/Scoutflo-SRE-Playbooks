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

1. Retrieve the pod `<pod-name>` in namespace `<namespace>` and inspect its volume definitions and status fields to see which volumes are failing to attach or mount.

2. Retrieve the PersistentVolumeClaim `<pvc-name>` in namespace `<namespace>` and verify that its `status.phase` is `Bound` and that it is bound to the expected PersistentVolume.

3. List events in namespace `<namespace>` and filter for volume-related errors or warnings associated with the pod or PVC, including attach and mount failures.

4. Retrieve the StorageClass used by the PVC and list the corresponding storage provisioner pods in `kube-system` to ensure the CSI or provisioner components are running and healthy.

5. Retrieve the node `<node-name>` where the pod is scheduled and inspect its conditions and labels to verify it is Ready and allowed to access the storage backend.

6. List VolumeAttachment objects relevant to the PVC or pod and verify that the CSI driver is reporting volumes as attached or identify specific errors.

7. Retrieve the node `<node-name>` capacity fields (such as attachable volume limits) to confirm it has not exceeded the maximum number of attachable volumes for the storage provider.

## Diagnosis

1. Compare the volume attachment failure timestamps from pod status with PVC binding transition times, and check whether failures begin within 5 minutes of PVCs failing to bind or remaining Pending.

2. Compare the volume attachment failure timestamps with storage provisioner pod restart timestamps in `kube-system`, and check whether provisioner restarts occur within 5 minutes of attachment failures.

3. Compare the volume attachment failure timestamps with changes in pod node assignment, and check whether failures coincide with pods being scheduled to specific nodes or moved between nodes.

4. Compare the volume attachment failure timestamps with node Ready condition transition times for the target node, and check whether node readiness or storage-related conditions change around the time of failures.

5. Compare the volume attachment failure timestamps with Deployment or StatefulSet configuration change timestamps, and check whether new releases or configuration changes occurred within 1 hour before the failures began.

6. Compare the volume attachment failure timestamps with StorageClass modification timestamps and node volume limit information, and check whether recent StorageClass changes or exhausted node volume limits align within 1 hour of attachment failures.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 1 hour → 2 hours), review storage provisioner logs for earlier errors or warnings, check for gradual volume limit exhaustion, examine CSI driver health over a longer period, verify if storage backend connectivity issues developed gradually, and check node volume attachment limits that may have been reached earlier. Volume attachment failures may result from cumulative issues or storage backend problems not immediately visible.

