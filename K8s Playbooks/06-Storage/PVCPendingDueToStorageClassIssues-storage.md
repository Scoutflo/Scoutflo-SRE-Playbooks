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

1. Describe PersistentVolumeClaim <pvc-name> in namespace <namespace> to inspect the PVC status, phase, storage class reference, requested capacity, and any conditions indicating why it remains Pending.

2. Retrieve events for PersistentVolumeClaim <pvc-name> in namespace <namespace> sorted by timestamp to identify provisioning failures, storage class not found errors, or capacity issues.

3. Describe StorageClass <storage-class-name> to verify storage class configuration, provisioner, parameters, and allowVolumeExpansion settings.

4. List all StorageClasses in the cluster to check available storage classes and identify the default.

5. List pods in namespace kube-system and filter for storage provisioner pods to check storage provisioner pod status.

6. List all PersistentVolumes in the cluster and check for orphaned volumes that could be reused, verifying their reclaim policies.

## Diagnosis

1. Analyze PVC events from Playbook step 2 to identify the specific provisioning failure reason. Events showing "ProvisioningFailed" indicate the exact error from the storage provisioner. Common reasons include:
   - "storageclass.storage.k8s.io not found" - StorageClass is missing or misspelled
   - "waiting for first consumer" - WaitForFirstConsumer binding mode requires a pod to be scheduled first
   - "exceeded quota" - Storage quota exhausted
   - Provisioner-specific errors indicating backend issues

2. If events indicate StorageClass not found, verify the StorageClass exists from Playbook step 3-4. If the referenced StorageClass does not appear in the list, it was either deleted or never created. Check if a default StorageClass exists and whether the PVC should use it.

3. If events indicate provisioner errors, check the storage provisioner pod status from Playbook step 5. If provisioner pods are not Running or show restarts, the provisioner itself is unhealthy. Correlate provisioner pod restart timestamps with when the PVC entered Pending state.

4. If events show capacity or quota errors, examine the StorageClass parameters from step 3 and available PVs from step 6. If existing Released PVs match the PVC requirements, manual intervention to make them Available may resolve the issue.

5. If events indicate "waiting for first consumer" but pods using the PVC are also Pending, this is expected behavior for WaitForFirstConsumer binding mode. The root cause is likely why the pod cannot be scheduled (check pod events separately).

6. If events are inconclusive or show generic errors, the issue is likely at the storage backend level. Check if the provisioner in StorageClass (from step 3) matches the installed CSI driver, and verify storage backend connectivity.

**If no correlation is found within the specified time windows**: Extend the search window (1 hour → 2 hours, 5 minutes → 10 minutes), review storage provisioner logs for detailed error messages, check for storage backend quota limits, examine StorageClass parameters for misconfiguration, verify if storage provisioner has sufficient permissions, check for storage backend connectivity issues, and review storage capacity trends over time. PVC pending issues may result from storage backend limitations or provisioner configuration problems not immediately visible in Kubernetes events.
