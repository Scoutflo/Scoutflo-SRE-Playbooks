---
title: Volume Mount Permissions Denied - Storage
weight: 247
categories:
  - kubernetes
  - storage
---

# VolumeMountPermissionsDenied-storage

## Meaning

Containers cannot access mounted volumes due to permission issues (triggering KubePodCrashLooping or KubePodNotReady alerts) because the volume has incorrect file permissions on the storage backend, the container's security context runAsUser does not match volume ownership, or the filesystem group ID (fsGroup) in pod security context is not set correctly. Pods show permission denied errors in logs, pod events show FailedMount errors with permission issues, and PersistentVolumeClaim resources may show access problems. This affects the storage plane and prevents applications from accessing persistent data, typically caused by security context mismatches or volume permission issues; applications fail to access persistent data and may show errors.

## Impact

Containers cannot read or write to volumes; volume mount permissions are denied; applications fail to access persistent data; pods start but applications crash with permission denied errors; KubePodCrashLooping alerts fire when containers restart due to permission failures; KubePodNotReady alerts fire when pods cannot access required volumes; file permission errors occur in pod logs; database pods cannot access data directories; log collection fails; persistent storage is inaccessible; pod events show permission denied errors. Pods show permission denied errors in logs indefinitely; pod events show FailedMount errors; applications fail to access persistent data and may experience errors or performance degradation; persistent storage is inaccessible.

## Playbook

1. Retrieve the pod `<pod-name>` in namespace `<namespace>` and inspect pod security context and container security context to verify user ID (runAsUser) and group ID (fsGroup) settings.

2. Retrieve logs from the pod `<pod-name>` in namespace `<namespace>` and filter for permission denied errors, access denied messages, or filesystem permission failures.

3. List events in namespace `<namespace>` and filter for volume-related events, focusing on events with reasons such as `FailedMount` or messages indicating permission issues.

4. Check the PersistentVolumeClaim `<pvc-name>` and PersistentVolume to verify volume ownership and permissions on the storage backend.

5. From the pod `<pod-name>`, execute `ls -la` on the mounted volume path using Pod Exec tool to check file permissions and ownership.

6. Retrieve the Deployment `<deployment-name>` in namespace `<namespace>` and review security context configuration in the pod template to verify fsGroup and runAsUser settings.

## Diagnosis

1. Compare the volume permission denied error timestamps with pod security context modification timestamps in the deployment, and check whether security context changes occurred within 30 minutes before permission errors.

2. Compare the volume permission denied error timestamps with PersistentVolume creation or modification timestamps, and check whether volume ownership changes occurred within 30 minutes before permission errors.

3. Compare the volume permission denied error timestamps with deployment rollout or pod template update timestamps, and check whether security context changes occurred within 1 hour before permission errors.

4. Compare the volume permission denied error timestamps with storage class or provisioner modification timestamps, and check whether storage backend changes occurred within 30 minutes before permission errors.

5. Compare the volume permission denied error timestamps with pod user ID or group ID modification timestamps, and check whether runAsUser or fsGroup changes occurred within 30 minutes before permission errors.

6. Compare the volume permission denied error timestamps with cluster security policy or PodSecurityPolicy modification timestamps, and check whether security policy changes occurred within 1 hour before permission errors.

**If no correlation is found within the specified time windows**: Extend the search window (30 minutes → 1 hour, 1 hour → 2 hours), review pod logs for gradual permission issues, check for intermittent filesystem permission problems, examine if security context configurations drifted over time, verify if volume ownership changed gradually, and check for storage backend permission changes that may have accumulated. Volume permission issues may result from gradual security context or storage configuration drift rather than immediate changes.

