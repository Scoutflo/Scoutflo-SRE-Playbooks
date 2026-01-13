---
title: PVC Pending Due To StorageClass Issues - Storage
weight: 274
categories:
  - kubernetes
  - storage
---

# PVCPendingDueToStorageClassIssues-storage

## Meaning

A PersistentVolumeClaim remains in the Pending phase (potentially triggering KubePersistentVolumeFillingUp alerts if related to capacity) because its referenced StorageClass is missing, misconfigured, or its provisioner cannot create a backing volume for the requested capacity and parameters. PersistentVolumeClaim resources show Pending phase in kubectl, StorageClass may show missing or misconfigured status, and storage provisioner pods may show failures in kube-system namespace. This indicates storage provisioning failures, StorageClass configuration errors, or storage backend availability issues preventing PVC binding; PersistentVolumeClaim binding failures may block pod creation.

## Impact

PVCs cannot bind to volumes; pods requiring persistent storage cannot start; stateful workloads fail to deploy; databases and storage-dependent applications remain unavailable; KubePersistentVolumeFillingUp alerts may fire if capacity-related; PVCs remain in Pending state; volume provisioning fails; storage-dependent pods cannot start. PersistentVolumeClaim resources show Pending phase indefinitely; StorageClass may show missing or misconfigured status; PersistentVolumeClaim binding failures may prevent pod creation; applications cannot access data and may show errors.

## Playbook

1. Retrieve persistent volume claim `<pvc-name>` in namespace `<namespace>` and verify PVC and storage class.

2. List all storage classes to check available storage classes.

3. List events in namespace `<namespace>` and filter for PVC-related events to check PVC events for binding issues.

4. Retrieve storage class `<storage-class-name>` and verify storage class configuration.

5. List pods in namespace `kube-system` and filter for storage provisioner pods to check storage provisioner pod status.

## Diagnosis

1. Compare the timestamps when PVC entered Pending state with storage class change timestamps, and check whether Pending state begins within 1 hour of storage class modifications.

2. Compare the PVC pending timestamps with storage provisioner pod restart timestamps, and verify whether Pending state correlates with provisioner pod restarts within 5 minutes.

3. Compare the PVC pending timestamps with storage class deletion or modification timestamps, and check whether Pending state correlates with storage class removal or changes at the same time.

4. Compare the PVC pending timestamps with deployment or configuration change timestamps, and verify whether Pending state begins within 1 hour of deployment changes.

5. Compare the PVC pending timestamps with storage backend availability issue timestamps, and check whether Pending state correlates with storage backend problems.

6. Compare the PVC pending timestamps with node capacity or storage quota exhaustion timestamps, and verify whether Pending state correlates with storage capacity constraints at the same time.

**If no correlation is found within the specified time windows**: Extend the search window (1 hour → 2 hours, 5 minutes → 10 minutes), review storage provisioner logs for detailed error messages, check for storage backend quota limits, examine StorageClass parameters for misconfiguration, verify if storage provisioner has sufficient permissions, check for storage backend connectivity issues, and review storage capacity trends over time. PVC pending issues may result from storage backend limitations or provisioner configuration problems not immediately visible in Kubernetes events.
