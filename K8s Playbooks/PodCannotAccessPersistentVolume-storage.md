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

1. Retrieve the pod `<pod-name>` in namespace `<namespace>` and inspect pod volume configuration to identify which PersistentVolumeClaim is referenced.

2. Retrieve the PersistentVolumeClaim `<pvc-name>` in namespace `<namespace>` and inspect its status, phase, and conditions to verify if it is bound to a PersistentVolume.

3. Retrieve the PersistentVolume bound to the PVC and inspect its status, phase, and access modes to verify volume availability.

4. List events in namespace `<namespace>` and filter for volume-related events, focusing on events with reasons such as `FailedMount`, `FailedAttachVolume`, or messages indicating volume attachment failures.

5. Check the StorageClass referenced by the PVC and verify it exists and the provisioner is available.

6. Check the node where the pod is scheduled for volume attachment status and verify if the volume can be attached to the node.

## Diagnosis

1. Compare the pod volume access failure timestamps with PersistentVolumeClaim creation timestamps, and check whether PVCs were created but not bound within 30 minutes before pod access failures.

2. Compare the pod volume access failure timestamps with StorageClass modification or unavailability timestamps, and check whether storage class issues occurred within 30 minutes before volume access failures.

3. Compare the pod volume access failure timestamps with PersistentVolume deletion or release timestamps, and check whether volumes were released or deleted within 30 minutes before access failures.

4. Compare the pod volume access failure timestamps with storage backend unavailability timestamps, and check whether storage provider issues occurred within 10 minutes before volume access failures.

5. Compare the pod volume access failure timestamps with node volume attachment limit exhaustion timestamps, and check whether node attachment limits were reached within 30 minutes before access failures.

6. Compare the pod volume access failure timestamps with cluster storage plugin restart or failure timestamps, and check whether storage infrastructure issues occurred within 1 hour before volume access failures.

**If no correlation is found within the specified time windows**: Extend the search window (10 minutes → 30 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review storage plugin logs for gradual volume provisioning issues, check for intermittent storage backend connectivity problems, examine if storage class configurations drifted over time, verify if volume attachment limits accumulated gradually, and check for storage provider quota or capacity issues that may have developed. Volume access failures may result from gradual storage infrastructure degradation rather than immediate changes.

